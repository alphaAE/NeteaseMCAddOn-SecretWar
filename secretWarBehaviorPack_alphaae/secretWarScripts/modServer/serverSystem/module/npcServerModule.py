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
            [modConfig.CreateNPCEvent, modConfig.ServerSystemName, self.OnCreateNPC]
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

    # 定义功能封装
