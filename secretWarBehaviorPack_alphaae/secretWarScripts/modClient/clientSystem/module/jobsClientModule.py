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
            [modConfig.JobsSelectEvent],
            [modConfig.PlayerStartButton]
        ]
        self.eventAndCallbackList = [
            ["UiInitFinished", self.OnUiInitFinished]
        ]
        self.userEventAndCallbackList = [
            [modConfig.JobsSelectFinished, modConfig.ServerSystemName, self.OnJobsSelectFinished],
            [modConfig.PlayerStartButton, modConfig.ClientSystemName, self.OnPlayerStartButton],
            [modConfig.StopMobsSpawn, modConfig.ServerSystemName, self.OnStopMobsSpawn]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # 监听引擎初始化完成事件创建UI
    def OnUiInitFinished(self, args):
        # 注册UI 创建UI
        clientApi.RegisterUI(
            modConfig.ModName,
            modConfig.StartGameUIName,
            modConfig.StartGameUIPyClsPath,
            modConfig.StartGameUIScreenDef
        )
        self.mStartGameUINode = clientApi.CreateUI(modConfig.ModName, modConfig.StartGameUIName, {"isHud": 1})
        if self.mStartGameUINode:
            self.mStartGameUINode.Init(self.system)
        else:
            logger.error("create ui %s failed!" % modConfig.JobsSelectUIScreenDef)

    def OnPlayerStartButton(self, args):
        self.CreateUIJobsSelect()

    # 收到服务职业设置完成广播 设置皮肤
    def OnJobsSelectFinished(self, args):
        comp = clientApi.CreateComponent(args["playerId"], "Minecraft", "model")
        comp.SetSkin("secretWar/" + args["jobs"])
        if self.mStartGameUINode:
            self.mStartGameUINode.SetRemove()

    # 游戏终止广播
    def OnStopMobsSpawn(self, args):
        print args
        # 展示结算Ui
        clientApi.RegisterUI(
            modConfig.ModName,
            modConfig.StopGameUIName,
            modConfig.StopGameUIPyClsPath,
            modConfig.StopGameUIScreenDef
        )
        self.mStopGameUINode = clientApi.CreateUI(modConfig.ModName, modConfig.JobsSelectUIName, {"isHud": 1})
        if self.mStopGameUINode:
            self.mStopGameUINode.Init(self.system, args)
        else:
            logger.error("create ui %s failed!" % modConfig.JobsSelectUIScreenDef)

    # 定义功能封装
    def CreateUIJobsSelect(self):
        clientApi.RegisterUI(
            modConfig.ModName,
            modConfig.JobsSelectUIName,
            modConfig.JobsSelectUIPyClsPath,
            modConfig.JobsSelectUIScreenDef
        )
        self.mJobsSelectUINode = clientApi.CreateUI(modConfig.ModName, modConfig.JobsSelectUIName, {"isHud": 0})
        if self.mJobsSelectUINode:
            self.mJobsSelectUINode.Init(self.system)
        else:
            logger.error("create ui %s failed!" % modConfig.JobsSelectUIScreenDef)
