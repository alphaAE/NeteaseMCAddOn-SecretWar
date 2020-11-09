# -*- coding: utf-8 -*-

# 代码提示
import mod.server.extraServerApi as serverApi
import mod.server.serverEvent as serverEvent

import server.extraServerApi as serverApi
from secretWarScripts.modCommon import modConfig

from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil

from secretWarScripts.modServer.serverSystem.module.armsServerModule import ArmsServerModule
from secretWarScripts.modServer.serverSystem.module.basicInitServerModule import BasicInitServerModule
from secretWarScripts.modServer.serverSystem.module.jobsServerModule import JobsServerModule
from secretWarScripts.modServer.serverSystem.module.affixServerModule import AffixServerModule
from secretWarScripts.modServer.serverSystem.module.mobsSpawnServerModule import MobsSpawnServerModule
from secretWarScripts.modServer.serverSystem.module.npcServerModule import NPCServerModule

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

ServerSystem = serverApi.GetServerSystemCls()


class MainServerSystem(ServerSystem):

    moduleList = []

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        logger.info("===== Server Init =====")

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self, self)
        self.eventList = []
        self.eventAndCallbackList = []
        self.userEventAndCallbackList = []

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

        # 初始化定义的功能模块
        self.moduleList.append(BasicInitServerModule(self, namespace, systemName))
        self.moduleList.append(ArmsServerModule(self, namespace, systemName))
        self.moduleList.append(JobsServerModule(self, namespace, systemName))
        self.moduleList.append(AffixServerModule(self, namespace, systemName))
        self.moduleList.append(MobsSpawnServerModule(self, namespace, systemName))
        self.moduleList.append(NPCServerModule(self, namespace, systemName))

    def Destroy(self):
        logger.info("===== Server Destroy =====")
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)
        # 销毁定义的功能模块
        for module in self.moduleList:
            module.Destroy()

    # 基类的方法，同样会在引擎tick的时候被调用，1秒30帧
    def Update(self):
        pass
