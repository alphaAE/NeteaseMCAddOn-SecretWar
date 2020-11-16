# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class EggServerModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== BasicInitServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = []
        self.eventAndCallbackList = [
            # ["PlayerAttackEntityEvent", self.OnPlayerAttackEntityEvent]
        ]
        self.userEventAndCallbackList = []

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # CallBack
    # 客户端加载Addon完成时回调
    def OnPlayerAttackEntityEvent(self, data):
        playerId = data.get("playerId", "")
        comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if item is None:
            return
        itemName = item.get("itemName", "")
        if itemName == "secret_war:egg_exclusive_precious_hunter":
            pass
            data["cancel"] = True
