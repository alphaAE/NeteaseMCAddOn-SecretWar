# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
from awesomeScripts.modCommon import modConfig

from awesomeScripts.modCommon import modConfig
from awesomeScripts.modCommon.listenEventUtil import ListenEventUtil

# 用来打印规范的log
from awesomeScripts.modClient import logger


class ArmsClientModule:

    def __init__(self, system, namespace, systemName):
        print "===== ArmsClientModule init ====="
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(clientApi, self.system, self)
        self.eventList = []
        self.eventAndCallbackList = []
        self.userEventAndCallbackList = [
            # 客户端自定义的事件 ShootEvent
            [modConfig.BulletHitEvent, self.OnBulletHit]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

# 当子弹射中后，服务端回调并返回数据
    def OnBulletHit(self, data):
        # logger.info("OnBulletHit %s", data)
        x = data.get("x", 0.0)
        y = data.get("y", 0.0)
        z = data.get("z", 0.0)
        pos = tuple((x, y, z))
        # 添加播放声音的Component
        audioComp = self.system.CreateComponent(clientApi.GetLocalPlayerId(), modConfig.Minecraft, modConfig.AudioComponent)
        audioComp.Play(modConfig.BulletHitSound, pos, 1.0, 1.0)
        # 添加击中后在原地产生的爆炸粒子特效
        particleEntityId = self.system.CreateEngineParticle(modConfig.BulletHitEffect, pos)
        ctrlComp = self.system.CreateComponent(particleEntityId, modConfig.Minecraft, modConfig.ParticleControlComponent)
        ctrlComp.Play()
        # 爆炸的粒子特效延迟销毁
        gameComp = clientApi.CreateComponent(clientApi.GetLevelId(), "Minecraft", "game")
        # 在延后modConfig.ParticleControlFrames这么多帧后开始执行销毁
        gameComp.AddTimer(modConfig.ParticleControlFrames / 30.0, lambda: ctrlComp.Stop())
        # # 在每次射中后删除绑定在子弹上的特效
        # destroyList = self.mHitDestroyIdList.get(bulletId, None)
        # if destroyList:
        #     for entityId in destroyList:
        #         self.DestroyEntity(entityId)
