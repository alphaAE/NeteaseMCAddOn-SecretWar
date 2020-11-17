# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class NPCServerModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== JobsServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = []
        self.eventAndCallbackList = []
        self.userEventAndCallbackList = [
            [modConfig.CreateNPCEvent, modConfig.ServerSystemName, self.OnCreateNPC],
            ["AddServerPlayerEvent", self.OnAddServerPlayerEvent]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # CallBack
    def OnCreateNPC(self, data):
        entityId1 = self.system.CreateEngineEntityByTypeStr("secret_war:npc_mage", (296.5, 5, 72.5), (0, 0))
        entityId2 = self.system.CreateEngineEntityByTypeStr("secret_war:npc_hunter", (288.5, 5, 72.5), (0, 0))

        compName = serverApi.CreateComponent(entityId1, "Minecraft", "name")
        compName.SetName("职业法师")
        compName = serverApi.CreateComponent(entityId2, "Minecraft", "name")
        compName.SetName("职业猎人")

    # 初始化角色物品、状态
    def OnAddServerPlayerEvent(self, data):
        playerId = data.get("id", "0")
        if playerId != "0":
            self.NotifyOneMessageToPlayer(playerId, "职业猎人：看呐，又一个被召唤过来的打手，你们是哪个时代过来的")
            self.NotifyOneMessageToPlayer(playerId, "职业法师：仪式，很成功")

    # 定义功能封装

    # 通知消息到玩家
    def NotifyOneMessageToPlayer(self, playerId, msg):
        compMsg = serverApi.CreateComponent(playerId, "Minecraft", "msg")
        compMsg.NotifyOneMessage(playerId, msg, "§c")