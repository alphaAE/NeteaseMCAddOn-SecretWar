# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class JobsServerModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== JobsServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = [
            [modConfig.JobsSelectFinished],
            [modConfig.StartGame],
            [modConfig.StopMobsSpawn]
        ]
        self.eventAndCallbackList = [
            ["ServerPlayerTryTouchEvent", self.OnServerPlayerTryTouchEvent],
            ["PlayerAttackEntityEvent", self.OnPlayerAttackEntityEvent],
            ["AddServerPlayerEvent", self.OnAddServerPlayerEvent],
            ["PlayerDieEvent", self.OnPlayerDieEvent]
        ]
        self.userEventAndCallbackList = [
            [modConfig.JobsSelectEvent, modConfig.ClientSystemName, self.OnJobsSelectEvent]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # CallBack
    # 客户端加载Addon完成时回调
    def OnJobsSelectEvent(self, data):
        self.setJob(data["playerId"], data["jobs"])
        compName = serverApi.CreateComponent(data["playerId"], "Minecraft", "name")
        name = compName.GetName()
        self.NotifyOneMessageToAllPlay("{} 选择了职业 {}".format(name, self.getJob(data["playerId"])))
        # 给予初始装备
        if data["jobs"] == modConfig.JobsHunter:
            self.GivePlayersItem(data["playerId"], "secret_war:bow_flame")
        elif data["jobs"] == modConfig.JobsMage:
            self.GivePlayersItem(data["playerId"], "secret_war:staff_toxic")
        # 检测所有玩家选择职业结束
        for player in serverApi.GetPlayerList():
            if self.getJob(player) == "NULL":
                return
        # 广播开始游戏
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = data["playerId"]
        self.system.BroadcastEvent(modConfig.StartGame, eventArgs)
        print "广播开始游戏"

    # 捡起物品时回调 判断是否是合格物品
    def OnServerPlayerTryTouchEvent(self, data):
        # Test 测试掉落物字典
        comp = serverApi.CreateComponent(serverApi.GetLevelId(), 'Minecraft', 'item')
        print comp.GetDroppedItem(data["entityId"])

        playerJob = self.getJob(data.get("playerId", ""))
        if playerJob != "NULL":
            itemName = data.get("itemName", "")
            if itemName in modConfig.jobsCanUseArms[playerJob]:
                return
            if itemName in modConfig.canUse:
                return
            data["cancel"] = True

    # 修改攻击方式 附加上角色伤害AttrMax值
    def OnPlayerAttackEntityEvent(self, data):
        playerId = data.get("playerId", "0")
        victimId = data.get("victimId", "0")
        if playerId != "0" and victimId != "0":
            compAttr = serverApi.CreateComponent(playerId, "Minecraft", "attr")
            playerMaxDamage = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.DAMAGE)
            data["damage"] = int(playerMaxDamage)
            data["isValid"] = 1

    # 玩家加入时为其设置生命数3
    def OnAddServerPlayerEvent(self, data):
        playerId = data.get("id", "0")
        if playerId != "0":
            # 设置生命数
            modVarPool.PlayerLifePool[playerId] = 3

    # 玩家死亡触发
    def OnPlayerDieEvent(self, data):
        playerId = data.get("id", "0")
        self.playerDide(playerId)

    # # 定义功能封装
    def setJob(self, entityId, job):
        # 在实体上标注职业
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        comp.SetAttr(modConfig.ModName + modConfig.JobsAttr, {"job": job})
        # 发送广播的通知客户端 替换皮肤
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = entityId
        eventArgs["jobs"] = job
        self.system.BroadcastToAllClient(modConfig.JobsSelectFinished, eventArgs)
        # 播放原生粒子
        compCommand = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "command")
        # (knockback_roar_particle)
        compCommand.SetCommand("/particle minecraft:egg_destroy_emitter ~ ~1 ~", entityId)

    def getJob(self, entityId):
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        try:
            return comp.GetAttr(modConfig.ModName + modConfig.JobsAttr).get("job", "NULL")
        except Exception:
            return "NULL"

    # 通知消息到每一个玩家
    def NotifyOneMessageToAllPlay(self, msg):
        for p in serverApi.GetPlayerList():
            compMsg = serverApi.CreateComponent(p, "Minecraft", "msg")
            compMsg.NotifyOneMessage(p, msg, "§c")

    def GivePlayersItem(self, playerId, itemStr):
        itemDict = {
            'itemName': itemStr,
            'count': 1
        }
        compItem = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        compItem.SpawnItemToPlayerInv(itemDict, playerId)

    def playerDide(self, playerId):
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        compPlayer = serverApi.CreateComponent(playerId, "Minecraft", "player")
        life = modVarPool.PlayerLifePool[playerId]
        modVarPool.PlayerLifePool[playerId] = life - 1
        if life < 0:
            # 切换观察者模式
            compPlayer.SetPlayerGameType(3)
        # 检测所有玩家游戏模式判断 是否结束
        for p in serverApi.GetPlayerList():
            gameType = compGame.GetPlayerGameType(playerId)     
            if gameType != 3:
                return
        # 结束游戏
        self.StopGame(playerId)
        
    # 多次杀死所有附近非玩家实体 (防止史莱姆)
    def KillAllEntity(self, entityId):
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        compGame.AddTimer(0.0, self.killAllOtherEntity, entityId)
        compGame.AddTimer(1.5, self.killAllOtherEntity, entityId)
        compGame.AddTimer(3.0, self.killAllOtherEntity, entityId)

    def StopGame(self, playerId):
        compAttr = serverApi.CreateComponent(playerId, "Minecraft", "attr")
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = playerId
        self.system.BroadcastEvent(modConfig.StopMobsSpawn, eventArgs)
        # 杀死所有实体
        self.KillAllEntity(playerId)
        # 广播结算UI 及其数据给所有玩家
        for p in serverApi.GetPlayerList():
            eventArgs = self.system.CreateEventData()
            eventArgs["playerId"] = playerId
            eventArgs["playerKillMobNum"] = modVarPool.PlayerKillMobNum
            eventArgs["damage"] = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.DAMAGE)
            eventArgs["health"] = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            self.system.NotifyToClient(playerId, modConfig.StopMobsSpawn, eventArgs)
