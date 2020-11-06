# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
from secretWarScripts.modCommon import modConfig

from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil
# 模块
from secretWarScripts.modClient.clientSystem.module.armsClientModule import ArmsClientModule
from secretWarScripts.modClient.clientSystem.module.jobsClientModule import JobsClientModule

# 用来打印规范的log
from secretWarScripts.modClient import logger

ClientSystem = clientApi.GetClientSystemCls()


class MainClientSystem(ClientSystem):

    moduleList = []

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        logger.info("===== Client Listen =====")

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(clientApi, self, self)
        self.eventList = []
        self.eventAndCallbackList = []
        self.userEventAndCallbackList = [
            [modConfig.BulletFlyFrameEvent, modConfig.ServerSystemName, self.OnBulletFlyFrame]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

        # 初始化定义的功能模块
        self.moduleList.append(JobsClientModule(self, namespace, systemName))
        self.moduleList.append(ArmsClientModule(self, namespace, systemName))

        # 用于保存在击中后需要释放的实体
        self.mHitDestroyIdList = {}

    # 在清楚该system的时候调用取消监听事件
    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)
        # 销毁定义的功能模块
        for module in self.moduleList:
            module.Destroy()

    # 在子弹开始飞的时候，给子弹绑定上特效
    def OnBulletFlyFrame(self, data):
        logger.info("OnBulletFlyFrame: %s", data)
        bindId = data.get("bindId", "-1")
        # 同服务端的解释，tempEntity保存来自各个Component的数据

        # 创建真正的特效SFX实体绑定在子弹上
        frameEntityId = self.CreateEngineSfx(modConfig.BulletFlyFrameSfx)
        entityBindComp = self.CreateComponent(frameEntityId, modConfig.Minecraft, modConfig.FrameAniBindComponent)
        entityBindComp.Bind(bindId, (0, 0, 0), (0, 0, 0))
        frameAniTransComp = self.CreateComponent(frameEntityId, modConfig.Minecraft, modConfig.FrameAniTransComponent)
        playerPosComp = self.GetComponent(self.mPlayerId, modConfig.Minecraft, modConfig.PosComponent)
        frameAniTransComp.SetPos(playerPosComp.GetPos())
        frameAniTransComp.SetRot((0, 0, 0))
        frameAniTransComp.SetScale((1, 1, 1))
        frameAniControlComp = self.CreateComponent(frameEntityId, modConfig.Minecraft, modConfig.FrameAniCtrlComponent)
        frameAniControlComp.SetLoop(True)
        frameAniControlComp.SetFaceCamera(True)
        frameAniControlComp.Play()

        # 将特效实体Id保存在self.mHitDestroyIdList中，后续更新中会清除
        bindList = self.mHitDestroyIdList.setdefault(bindId, [])
        bindList.append(frameEntityId)

    # 被引擎直接执行的父类的重写函数，引擎会执行该Update回调，1秒钟30帧
    def Update(self):
        # self.UpdateShoot()
        pass
