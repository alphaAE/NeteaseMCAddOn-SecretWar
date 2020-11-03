# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
# ClientSystem = clientApi.GetClientSystemCls()
from secretWarScripts.modCommon import modConfig
# 用来打印规范的log
from secretWarScripts.modClient import logger


class EntityAnimClientSystem:

    def __init__(self, system, namespace, systemName):
        print "===== EntityAnimClientSystem init ====="
        self.system = system
        self.ListenEvent()
        # 获取客户端本地玩家的playerId
        self.mPlayerId = clientApi.GetLocalPlayerId()

    def Destroy(self):
        print "===== EntityAnimClientSystem Destroy ====="
        self.UnListenEvent()

    def ListenEvent(self):
        self.system.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), modConfig.UiInitFinishedEvent, self, self.OnUIInitFinished)
        self.system.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, modConfig.PlayShootAnimEvent, self, self.OnPlayShootAnim)

    def UnListenEvent(self):
        self.system.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), modConfig.UiInitFinishedEvent, self, self.OnUIInitFinished)
        self.system.UnListenForEvent(modConfig.ModName, modConfig.ServerSystemName, modConfig.PlayShootAnimEvent, self, self.OnPlayShootAnim)

    # 监听引擎初始化完成事件
    def OnUIInitFinished(self, args):
        # 客户端换上模型大天狗并循环播放动作大天狗跑步
        modelComp = self.system.CreateComponent(self.mPlayerId, modConfig.Minecraft, modConfig.ModelCompClient)
        modelComp.SetModel(modConfig.DatiangouModel)
        modelComp.PlayAnim(modConfig.DatiangouRunAnim, True)

    # 监听来自服务端的事件，客户端在这里开始播放服务端通知的相应的射击动作
    def OnPlayShootAnim(self, data):
        entityId = data.get("entityId", "-1")
        anim = data.get("anim", "")
        isLoop = data.get("isLoop", False)
        modelComp = self.system.GetComponent(entityId, modConfig.Minecraft, modConfig.ModelCompClient)
        if not modelComp:
            logger.warning("do not have model comp!")
            return
        modelComp.PlayAnim(anim, isLoop)
        # 延迟恢复播放大天狗跑步
        gameComp = clientApi.CreateComponent(clientApi.GetLevelId(), "Minecraft", "game")
        gameComp.AddTimer(modConfig.DatiangouFengxiAnimFrames / 30.0, self.DelayPlayAnimRun)

    # 在播放完大天狗风袭动作之后，播放大天狗跑步动作，延迟的帧数是风袭动作的播放帧数
    def DelayPlayAnimRun(self):
        logger.info("Delay play run anim")
        modelComp = self.system.GetComponent(self.mPlayerId, modConfig.Minecraft, modConfig.ModelCompClient)
        modelComp.PlayAnim(modConfig.DatiangouRunAnim, True)
