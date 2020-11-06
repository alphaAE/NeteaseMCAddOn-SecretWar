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
            [modConfig.JobsSelectFinished]
        ]
        self.eventAndCallbackList = [
            ["ServerPlayerTryTouchEvent", self.OnServerPlayerTryTouchEvent]
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
        # 测试获取
        print data["playerId"], "选择了:", self.getJob(data["playerId"])

    # 捡起物品时回调 判断是否是合格物品
    def OnServerPlayerTryTouchEvent(self, data):
        itemName = data.get("itemName", "")
        playerJob = self.getJob(data.get("playerId", ""))
        if playerJob != "NULL":
            if itemName in modConfig.jobsCanUseArms[playerJob]:
                return
            if itemName in modConfig.canUse:
                return
            data["cancel"] = True

    # 定义功能封装
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
        return comp.GetAttr(modConfig.ModName + modConfig.JobsAttr).get("job", "NULL")
