# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
from secretWarScripts.modCommon import modConfig

from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil
# 模块
from secretWarScripts.modClient.clientSystem.module.armsClientModule import ArmsClientModule

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
        self.eventList = [
            [modConfig.ShootEvent]
        ]
        self.eventAndCallbackList = [
            # [modConfig.UiInitFinishedEvent, self.OnUIInitFinished]
        ]
        self.userEventAndCallbackList = [
            [modConfig.BulletFlyFrameEvent, self.OnBulletFlyFrame]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

        # 初始化定义的功能模块
        self.moduleList.append(ArmsClientModule(self, namespace, systemName))

        # 保存ui界面节点
        self.mFpsBattleUINode = None
        # 拼接ShootComponent的Key
        self.mShootKey = modConfig.ModName + ":" + modConfig.ClientShootComponent
        # 获取客户端本地玩家的playerId
        self.mPlayerId = clientApi.GetLocalPlayerId()
        # 用于保存在击中后需要释放的实体
        self.mHitDestroyIdList = {}
        # 用于保存shoot组件
        self.mShootComp = None

    # 在清楚该system的时候调用取消监听事件
    def Destroy(self):
        logger.info("===== Client Destroy =====")
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)
        # 销毁定义的功能模块
        for module in self.moduleList:
            module.Destroy()

    # 监听引擎初始化完成事件，在这个事件后创建我们的战斗UI
    def OnUIInitFinished(self, args):
        logger.info("OnUIInitFinished : %s", args)
        # 注册UI 详细解释参照《UI API》
        clientApi.RegisterUI(
            modConfig.ModName,
            modConfig.FpsBattleUIName,
            modConfig.FpsBattleUIPyClsPath,
            modConfig.FpsBattleUIScreenDef
        )
        # 创建UI 详细解释参照《UI API》，下面是两种获得 uiNode 的方式
        self.mFpsBattleUINode = clientApi.CreateUI(modConfig.ModName, modConfig.FpsBattleUIName, {"isHud": 1})
        self.mFpsBattleUINode = clientApi.GetUI(modConfig.ModName, modConfig.FpsBattleUIName)
        if self.mFpsBattleUINode:
            self.mFpsBattleUINode.Init()
        else:
            logger.error("create ui %s failed!" % modConfig.FpsBattleUIScreenDef)
        logger.info("change model datiangou")

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
        self.UpdateShoot()

    # 更新自定义的ClientShootComponent，提交ClientShootComponent更新操作的是fpsBattle.py UI类中
    # Component需要经过System更新后才能生效，自定义的Component需要自己写相应的更新函数
    # 引擎的Component则在NeedsUpdate之后，由引擎来更新
    def UpdateShoot(self):
        if not self.mShootComp:
            self.mShootComp = self.CreateComponent(self.mPlayerId, modConfig.ModName, modConfig.ClientShootComponent)

        if self.mShootComp and self.mShootComp.GetShoot():
            shootData = self.CreateEventData()
            shootData["id"] = self.mPlayerId
            # 向服务端发送事件，玩家为playerId的人发送了射击事件
            self.NotifyToServer(modConfig.ShootEvent, shootData)
            # 发送后将Component置为不需要更新
            self.mShootComp.SetShoot(False)
