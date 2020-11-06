# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
from secretWarScripts.modCommon import modConfig

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil

# 用来打印规范的log
from secretWarScripts.modClient import logger


class JobsClientModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== JobsClientModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(clientApi, self.system, self)
        self.eventList = [
            [modConfig.JobsSelectEvent]
        ]
        self.eventAndCallbackList = [
            ["UiInitFinished", self.OnUiInitFinished]
        ]
        self.userEventAndCallbackList = []

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # 监听引擎初始化完成事件，在这个事件后创建我们的战斗UI
    def OnUiInitFinished(self, args):
        # 注册UI 创建UI
        # clientApi.SetResponse(False)
        clientApi.RegisterUI(
            modConfig.ModName,
            modConfig.JobsSelectUIName,
            modConfig.JobsSelectUIPyClsPath,
            modConfig.JobsSelectUIScreenDef
        )
        self.mFpsBattleUINode = clientApi.CreateUI(modConfig.ModName, modConfig.JobsSelectUIName, {"isHud": 1})
        # self.mFpsBattleUINode = clientApi.GetUI(modConfig.ModName, modConfig.FpsBattleUIName)
        if self.mFpsBattleUINode:
            self.mFpsBattleUINode.Init(self.system)
        else:
            logger.error("create ui %s failed!" % modConfig.FpsBattleUIScreenDef)
