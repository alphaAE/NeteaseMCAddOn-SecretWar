# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class CurrencyServerModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== CurrencyServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = [
            [modConfig.ServerCallbackPlayerCurrencyEvent],
            [modConfig.OpenShopEvent]
        ]
        self.eventAndCallbackList = [
            ["AddServerPlayerEvent", self.OnAddServerPlayerEvent],
            ["ServerPlayerTryTouchEvent", self.OnServerPlayerTryTouchEvent],
            ["PlayerAttackEntityEvent", self.OnPlayerAttackEntityEvent]
        ]
        self.userEventAndCallbackList = [
            [modConfig.ClientGetPlayerCurrencyEvent, modConfig.ClientSystemName, self.OnClientGetPlayerCurrencyEvent],
            [modConfig.ClientSetPlayerCurrencyEvent, modConfig.ClientSystemName, self.OnClientSetPlayerCurrencyEvent],
            [modConfig.PlayerBuyEvent, modConfig.ClientSystemName, self.OnPlayerBuyEvent]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # CallBack
    def OnAddServerPlayerEvent(self, data):
        playerId = data.get("id", "0")
        if playerId != "0":
            # 给予初始金币
            modVarPool.PlayerCurrencyPool[playerId] = 20

    def OnClientGetPlayerCurrencyEvent(self, data):
        playerId = data.get("playerId", "0")
        if playerId != "0":
            self.NotifyToClientUpdateCurrency(playerId)

    def OnClientSetPlayerCurrencyEvent(self, data):
        playerId = data.get("playerId", "0")
        if playerId != "0":
            currency = data.get("currency", -3)
            self.SetPlayerCurrency(playerId, currency)

    # 捡起物品时回调 如果是金币则给玩家金币并销毁
    def OnServerPlayerTryTouchEvent(self, data):
        itemName = data.get("itemName", "")
        if itemName == "secret_war:coin":
            data["cancel"] = True
            # 获取掉落金币个数
            entityId = data.get("entityId", "")
            compTtem = serverApi.CreateComponent(serverApi.GetLevelId(), 'Minecraft', 'item')
            entityInfo = compTtem.GetDroppedItem(entityId)
            count = entityInfo.get("count", -1)
            # print entityInfo
            # 增加玩家金币
            playerId = data.get("playerId", "")
            currency = modVarPool.PlayerCurrencyPool[playerId]
            self.SetPlayerCurrency(data["playerId"], currency + count)
            # 删除掉落物
            self.system.DestroyEntity(entityId)

    # 攻击指定实体广播客户端打开上商店
    def OnPlayerAttackEntityEvent(self, data):
        playerId = data.get("playerId", "0")
        victimId = data.get("victimId", "0")
        if playerId == "0" or victimId == "0":
            return
        compEngineType = serverApi.CreateComponent(victimId, "Minecraft", "engineType")
        entityTypeStr = compEngineType.GetEngineTypeStr()
        if entityTypeStr == "secret_war:npc_mage":
            self.NotifyToClientOpenShop(playerId, modConfig.ShopMageUIName)
            data["cancel"] = True
        elif entityTypeStr == "secret_war:npc_hunter":
            self.NotifyToClientOpenShop(playerId, modConfig.ShopHunterUIName)
            data["cancel"] = True

    # 接收客户端购买物品广播
    def OnPlayerBuyEvent(self, data):
        playerId = data.get("playerId", "0")
        itemStr = data.get("item", "0")
        # 职业合法性检查
        playerJob = self.getJob(playerId)
        if playerJob == "NULL":
            self.NotifyOneMessageToPlay(playerId, "我没法帮助身份不明的人！")
            return
        if itemStr not in modConfig.jobsCanUseArms[playerJob]:
            self.NotifyOneMessageToPlay(playerId, "这玩意儿很明显不适合你，我是不会卖给你的！")
            return
        # 背包重复检查
        compItem = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        allItems = compItem.GetPlayerAllItems(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)
        for item in allItems:
            if item is None:
                continue
            if item.get("itemName", "") == itemStr:
                self.NotifyOneMessageToPlay(playerId, "你已经拥有这件商品了！")
                return
        # 金币额检查
        currency = self.GetPlayerCurrency(playerId)
        difference = int(currency) - int(modConfig.shopItem[itemStr])
        if difference >= 0:
            self.SetPlayerCurrency(playerId, difference)
            if itemStr == "secret_war:attack":
                compAttr = serverApi.CreateComponent(playerId, "Minecraft", "attr")
                maxDamage = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.DAMAGE)
                compAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.DAMAGE, maxDamage + 2)
                maxDamage = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.DAMAGE)
                self.NotifyOneMessageToPlay(playerId, "攻击力加强到了[{}]！".format(maxDamage))
                return
            elif itemStr == "secret_war:health":
                compAttr = serverApi.CreateComponent(playerId, "Minecraft", "attr")
                maxHealth = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                compAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, maxHealth + 5)
                maxHealth = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                # 回复至满
                compAttr.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, maxHealth)
                self.NotifyOneMessageToPlay(playerId, "已经为你提升生命上限到[{}]！".format(maxHealth))
                return
            else:
                self.GivePlayersItem(playerId, itemStr)
                self.NotifyOneMessageToPlay(playerId, "拿着，让怪物们尝尝这家伙！")
                return
        else:
            self.NotifyOneMessageToPlay(playerId, "你钱不够！")
        # print playerId, itemStr, modConfig.shopItem[itemStr]

    # 定义功能封装
    def GetPlayerCurrency(self, playerId):
        return modVarPool.PlayerCurrencyPool[playerId]

    def SetPlayerCurrency(self, playerId, currency):
        modVarPool.PlayerCurrencyPool[playerId] = currency
        self.NotifyToClientUpdateCurrency(playerId)

    def NotifyToClientUpdateCurrency(self, playerId):
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = playerId
        eventArgs["currency"] = modVarPool.PlayerCurrencyPool[playerId]
        self.system.NotifyToClient(playerId, modConfig.ServerCallbackPlayerCurrencyEvent, eventArgs)

    def NotifyToClientOpenShop(self, playerId, shopName):
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = playerId
        eventArgs["shopName"] = shopName
        self.system.NotifyToClient(playerId, modConfig.OpenShopEvent, eventArgs)

    def GivePlayersItem(self, playerId, itemStr):
        itemDict = {
            'itemName': itemStr,
            'count': 1
        }
        compItem = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        compItem.SpawnItemToPlayerInv(itemDict, playerId)

    def NotifyOneMessageToPlay(self, playerId, msg):
        compMsg = serverApi.CreateComponent(playerId, "Minecraft", "msg")
        compMsg.NotifyOneMessage(playerId, msg, "§6")

    def getJob(self, entityId):
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        try:
            return comp.GetAttr(modConfig.ModName + modConfig.JobsAttr).get("job", "NULL")
        except Exception:
            return "NULL"
