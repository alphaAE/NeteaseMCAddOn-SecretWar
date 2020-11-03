# -*- coding: utf-8 -*-

# 代码提示
import mod.server.extraServerApi as serverApi
import mod.server.serverEvent as serverEvent

import server.extraServerApi as serverApi
# ServerSystem = serverApi.GetServerSystemCls()
from secretWarScripts.modCommon import modConfig
# 用来打印规范格式的log
from secretWarScripts.modServer import logger


class EntityAnimServerSystem:

    def __init__(self, system, namespace, systemName):
        print "===== EntityAnimClientSystem init ====="
        self.system = system
        self.ListenEvent()

    def Destroy(self):
        print "===== EntityAnimClientSystem Destroy ====="
        self.UnListenEvent()

    def ListenEvent(self):
        # PlayShootAnimEvent 用于通知客户端在射击时播放玩家的骨骼动画
        self.system.DefineEvent(modConfig.PlayShootAnimEvent)

        self.system.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), modConfig.AddServerPlayerEvent, self, self.OnPlayerAdd)

    def UnListenEvent(self):
        self.system.UnDefineEvent(modConfig.PlayShootAnimEvent)

        self.system.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), modConfig.AddServerPlayerEvent, self, self.OnPlayerAdd)

    # AddServerPlayerEvent的回调函数，在服务器端加入玩家的时候被调用
    def OnPlayerAdd(self, data):
        logger.info("OnPlayerAdd : %s", data)
        playerId = data.get("id", "-1")
        if playerId == "-1":
            return
        # 将加入进服务器的玩家的模型换成大天狗
        modelComp = self.system.CreateComponent(playerId, modConfig.Minecraft, modConfig.ModelCompServer)
        modelComp.SetModel(modConfig.DatiangouModel)
        logger.info("TEST === enter set model ===")
  
        



