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
        self.eventList = [
            # BulletFlyFrameEvent 用于通知客户端在设计时给子弹绑定特效
            [modConfig.BulletFlyFrameEvent]
        ]
        self.eventAndCallbackList = []
        self.userEventAndCallbackList = [
            # 客户端自定义的事件 ShootEvent
            [modConfig.ShootEvent, modConfig.ClientSystemName, self.OnShoot]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

        # 初始化定义的功能模块
        self.moduleList.append(BasicInitServerModule(self, namespace, systemName))
        self.moduleList.append(ArmsServerModule(self, namespace, systemName))
        self.moduleList.append(JobsServerModule(self, namespace, systemName))

    def Destroy(self):
        logger.info("===== Server Destroy =====")
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)
        # 销毁定义的功能模块
        for module in self.moduleList:
            module.Destroy()

    # 这个Update函数是基类的方法，同样会在引擎tick的时候被调用，1秒30帧（被调用30次）
    def Update(self):
        pass

    # 客户端ShootEvent的回调，在客户端射击的时候被调用 关于参数问题参考《MODSDK文档》
    def OnShoot(self, data):
        playerId = data.get("id", "-1")
        logger.info("OnShoot playerId: %s" % playerId)
        # 下面这些内容都可以在《MODSDK文档中找到》

        # 获取到玩家的位置pos和转向rot信息
        posComp = self.CreateComponent(playerId, modConfig.Minecraft, modConfig.PosComponent)
        rotComp = self.GetComponent(playerId, modConfig.Minecraft, modConfig.RotComponent)
        pos = posComp.GetPos()
        rot = rotComp.GetRot()
        direct = serverApi.GetDirFromRot(rot)
        power = modConfig.BulletPower
        gravity = modConfig.BulletGravity
        # 使用弓箭类型来创建抛射物子弹
        bulletId = self.CreateEngineBullet(playerId, serverApi.GetMinecraftEnum().EntityType.Arrow, pos, direct, power, gravity)

        # 创建事件数据 data 并赋值，注意事件数据不支持 tuple
        # 广播BulletFlyFrameEvent子弹飞行这个事件通知客户端让客户端给子弹绑上特效
        frameInfo = self.CreateEventData()
        frameInfo["bindId"] = bulletId
        self.BroadcastToAllClient(modConfig.BulletFlyFrameEvent, frameInfo)

        # 广播PlayShootAnimEvent事件，通知客户端播放发射的玩家骨骼动作大天狗风袭
        animInfo = self.CreateEventData()
        animInfo["entityId"] = playerId
        animInfo["anim"] = modConfig.DatiangouFengxiAnim
        animInfo["isLoop"] = False
        self.BroadcastToAllClient(modConfig.PlayShootAnimEvent, animInfo)
