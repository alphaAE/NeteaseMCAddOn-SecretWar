# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class AffixServerModule:

    affix = {
        "id": {
            "name": "",
            "fun": ""
        }
    }

    def __init__(self, system, namespace, systemName):
        logger.info("===== AffixServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = []
        self.eventAndCallbackList = [
            ["PlayerAttackEntityEvent", self.OnPlayerAttackEntityEvent]
        ]
        self.userEventAndCallbackList = []

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # CallBack
    def OnPlayerAttackEntityEvent(self, data):
        playerId = data.get("playerId", "")
        comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if item is None:
            return
        itemName = item.get("itemName", "")
        if itemName == "secret_war:test":
            victimId = data.get("victimId", "")
            # 测试给予词缀
            print victimId
            # 设置名牌
            compName = serverApi.CreateComponent(victimId, "Minecraft", "name")
            compName.SetName("new Name")
            # 增大模型
            compScale = serverApi.CreateComponent(victimId, "Minecraft", "scale")
            scale = compScale.GetEntityScale()
            compScale.SetEntityScale(victimId, scale + 0.5)
            # 增大碰撞箱
            compCollisionBox = serverApi.CreateComponent(victimId, "Minecraft", "collisionBox")
            size = compCollisionBox.GetSize()
            compCollisionBox.SetSize((size[0] + 0.2, size[1] + 0.2))

            data["cancel"] = True
    # 定义功能封装


    