# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil
from secretWarScripts.modServer.serverSystem.item.arms import ArmsBowFlame, ArmsBowStrong, ArmsBowHunter, ArmsBowAntimatterHaz41
from secretWarScripts.modServer.serverSystem.item.arms import ArmsStaffToxic, ArmsStaffSlime, ArmsStaffInvigorating
from secretWarScripts.modServer.serverSystem.item.arms import ArmsStaffBurstingBlast

# 用来打印规范格式的log
from secretWarScripts.modServer import logger


class ArmsServerModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== ArmsServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = [
            [modConfig.BulletHitEvent]
        ]
        self.eventAndCallbackList = [
            ["ServerItemTryUseEvent", self.OnServerItemTryUseEvent],
            ["ItemReleaseUsingServerEvent", self.OnRangedWeaponReleaseUsingServerEvent],
            ["ProjectileDoHitEffectEvent", self.OnProjectileHit],
            ["DamageEvent", self.OnDamageEvent]
        ]
        self.userEventAndCallbackList = []

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

        # 初始化定义武器列表
        modVarPool.ArmsList = [
            ArmsBowFlame(self.system),
            ArmsBowStrong(self.system),
            ArmsBowHunter(self.system),
            ArmsBowAntimatterHaz41(self.system),
            ArmsStaffToxic(self.system),
            ArmsStaffSlime(self.system),
            ArmsStaffInvigorating(self.system),
            ArmsStaffBurstingBlast(self.system)
        ]

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # ServerItemTryUseEvent回调，尝试使用物品时服务端
    def OnServerItemTryUseEvent(self, data):
        # 判断并执行对应回调
        for arms in modVarPool.ArmsList:
            if data["itemName"] == arms.id:
                arms.OnServerItemTryUseEvent(data)
                break

    # ItemReleaseUsingServerEvent回调，释放正在使用的物品时
    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        # 执行对应武器的释放回调
        for arms in modVarPool.ArmsList:
            if data["itemName"] == arms.id:
                arms.OnRangedWeaponReleaseUsingServerEvent(data)
                break

    # ProjectileDoHitEffectEvent回调，在抛射物击中的时
    def OnProjectileHit(self, data):
        projectileId = data["id"]
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(projectileId, "Minecraft", "modAttr")
        attr = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)
        if attr is not None:
            armsId = attr["armsId"]
            # 判断并执行对应回调
            for arms in modVarPool.ArmsList:
                if armsId == arms.id:
                    arms.OnProjectileHit(data)
                    break

    # 屏蔽所有投掷物伤害 并清除实体
    def OnDamageEvent(self, data):
        cause = data.get("cause", "")
        projectileId = data.get("projectileId", "")
        if cause == "projectile":
            comp = serverApi.CreateComponent(projectileId, "Minecraft", "modAttr")
            attr = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)
            if attr is None:
                return
            level = attr.get("level", "-1")
            if level != "0":
                data["damage"] = 0
                self.system.BroadcastToAllClient(modConfig.BulletHitEvent, data)
                self.system.DestroyEntity(projectileId)
