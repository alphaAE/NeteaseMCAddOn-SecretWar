import server.extraServerApi as serverApi

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool

import random


class Arms(object):

    filters = {
        "any_of": [
            {
                "subject": "other",
                "test": "is_family",
                "operator": "not",
                "value": "player"
            }
        ]
    }

    Stage1 = 0
    Stage2 = 1
    Stage3 = 2

    id = ""
    damage = 0.0

    def __init__(self, system):
        self.system = system

    # 创建抛射物
    def CreateProjectile(self, playerId, param, identifier):
        comp = self.system.CreateComponent(serverApi.GetLevelId(), "Minecraft", "projectile")
        projectileId = comp.CreateProjectileEntity(playerId, "minecraft:arrow", param)
        # 为投掷物设置标识符
        Arms.setAttr(projectileId, self.id, identifier)

    # 创建抛射物
    def CreateStaffProjectile(self, playerId, param, identifier):
        comp = self.system.CreateComponent(serverApi.GetLevelId(), "Minecraft", "projectile")
        projectileId = comp.CreateProjectileEntity(playerId, "minecraft:snowball", param)
        # 为投掷物设置标识符
        Arms.setAttr(projectileId, self.id, identifier)
        return projectileId

    # 创建抛射物
    def CreateMyProjectile(self, playerId, projectile, param, identifier):
        comp = self.system.CreateComponent(serverApi.GetLevelId(), "Minecraft", "projectile")
        projectileId = comp.CreateProjectileEntity(playerId, projectile, param)
        # 为投掷物设置标识符
        Arms.setAttr(projectileId, self.id, identifier)

    # 武器开始蓄力时触发
    def OnServerItemTryUseEvent(self, data):
        pass

    # 武器射出投掷物时触发
    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        pass

    # 武器击中实体时触发
    def OnProjectileHit(self, data):
        # 在子弹射中后方块发送广播并将体清除掉
        hitTargetType = data.get("hitTargetType", "-1")
        if hitTargetType == 'BLOCK':
            self.system.BroadcastToAllClient(modConfig.BulletHitEvent, data)
            self.system.DestroyEntity(data.get("id", "-1"))

    @staticmethod
    def damageMob(playerId, targetId, damage):
        # 屏蔽阵亡玩家伤害
        if playerId in modVarPool.PlayerDie:
            return
        compAttr = serverApi.CreateComponent(playerId, "Minecraft", "attr")
        payerDamage = compAttr.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.DAMAGE)
        compAttr = serverApi.CreateComponent(targetId, "Minecraft", "attr")
        health = compAttr.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        if health is None:
            return
        damageNow = health - payerDamage - damage
        compAttr.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, damageNow)

    # 播放原生粒子
    @staticmethod
    def playParticles(entityId, pos, particles):
        compCommand = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "command")
        compCommand.SetCommand("/particle {} {} {} {}".format(particles, pos[0], pos[1], pos[2]), entityId)

    @staticmethod
    def getLaunchPower(durationLeft, maxUseDuration):
        timeHeld = maxUseDuration - durationLeft
        pow = timeHeld / 20.0
        pow = ((pow * pow) + pow * 2) / 3
        return min(pow, 1.0)

    @staticmethod
    def getLaunchLevel(durationLeft, maxUseDuration):
        timeHeld = maxUseDuration - durationLeft
        print "蓄力时间：" + str(timeHeld)
        if timeHeld < 8:
            return Arms.Stage1
        elif timeHeld < 13:
            return Arms.Stage1
        elif timeHeld < 18:
            return Arms.Stage2
        elif timeHeld > 18:
            return Arms.Stage3
        return 0

    @staticmethod
    def getDuration(durationLeft, maxUseDuration):
        return maxUseDuration - durationLeft

    @staticmethod
    def explosion(srcId, pos, entityIdList, damage):
        Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter")
        for entityId in entityIdList:
            Arms.damageMob(srcId, entityId, damage)

    @staticmethod
    def setAttr(entityId, armsId, level):
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        comp.SetAttr(modConfig.ModName + modConfig.ProjectileAttr, {"armsId": armsId, "level": level})


# 燃烧连弩
class ArmsBowFlame(Arms):
    id = "secret_war_bow_flame:bow"
    damage = 6.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        rotComp = self.system.GetComponent(playerId, modConfig.Minecraft, modConfig.RotComponent)
        rot = rotComp.GetRot()
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 3.0 * power
            }
            self.CreateProjectile(playerId, param, Arms.Stage2)
        else:
            param = {
                'power': 3.8 * power
            }
            param1 = {
                'power': 3.8 * power,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 12))
            }
            param2 = {
                'power': 3.8 * power,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 12))
            }
            self.CreateProjectile(playerId, param, Arms.Stage3)
            self.CreateProjectile(playerId, param1, Arms.Stage3)
            self.CreateProjectile(playerId, param2, Arms.Stage3)

    def OnProjectileHit(self, data):
        srcId = data["srcId"]
        entityId = data["id"]
        targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
        # 获取抛射物实体中的定义属性
        compGame = serverApi.CreateComponent(entityId, "Minecraft", "game")
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        if level < Arms.Stage3:
            entityIdList = compGame.GetEntitiesAround(entityId, 3, self.filters)
            Arms.damageMob(srcId, targetId, self.damage * 0.45)
            for tmpId in entityIdList:
                compAttr = serverApi.CreateComponent(tmpId, "Minecraft", "attr")
                compAttr.SetEntityOnFire(5)
        else:
            entityIdList = compGame.GetEntitiesAround(entityId, 3, self.filters)
            Arms.explosion(srcId, pos, entityIdList, self.damage * 0.60)
            for tmpId in entityIdList:
                comp = serverApi.CreateComponent(tmpId, "Minecraft", "attr")
                comp.SetEntityOnFire(5)
        super(ArmsBowFlame, self).OnProjectileHit(data)


# 强击连弩
class ArmsBowStrong(Arms):
    id = "secret_war_bow_strong:bow"
    damage = 8.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 3.0 * power
            }
            for i in range(0, 2):
                compGame.AddTimer(i / 10.0, self.CreateProjectile, playerId, param, Arms.Stage2)
        else:
            param = {
                'power': 3.8 * power
            }
            for i in range(0, 3):
                compGame.AddTimer(i / 10.0, self.CreateProjectile, playerId, param, Arms.Stage3)

    def OnProjectileHit(self, data):
        srcId = data["srcId"]
        entityId = data["id"]
        targetId = data["targetId"]
        srcId = data["srcId"]
        # pos = (data["x"], data["y"], data["z"])
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        if level < Arms.Stage3:
            Arms.damageMob(srcId, targetId, self.damage * 0.80)
        else:
            Arms.damageMob(srcId, targetId, self.damage * 0.75)
        super(ArmsBowStrong, self).OnProjectileHit(data)


# 猎人之弩（效果需要在词缀模块制作后）
class ArmsBowHunter(Arms):
    id = "secret_war_bow_hunter:bow"
    damage = 8.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        rotComp = self.system.GetComponent(playerId, modConfig.Minecraft, modConfig.RotComponent)
        rot = rotComp.GetRot()
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 3.0 * power
            }
            param1 = {
                'power': 3.0 * power,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 12))
            }
            param2 = {
                'power': 3.0 * power,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 12))
            }
            self.CreateProjectile(playerId, param, Arms.Stage2)
            self.CreateProjectile(playerId, param1, Arms.Stage2)
            self.CreateProjectile(playerId, param2, Arms.Stage2)
        else:
            param = {
                'power': 3.8 * power
            }
            for i in range(0, 5):
                compGame.AddTimer(i / 10.0, self.CreateProjectile, playerId, param, Arms.Stage3)

    def OnProjectileHit(self, data):
        srcId = data["srcId"]
        entityId = data["id"]
        targetId = data["targetId"]
        srcId = data["srcId"]
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        # pos = (data["x"], data["y"], data["z"])
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        if level < Arms.Stage3:
            Arms.damageMob(srcId, targetId, self.damage * 0.60)
            # 同化 6% (暂写为暴毙)
            num = random.randint(0, 100)
            if num < 6:
                compGame.KillEntity(targetId)
        else:
            Arms.damageMob(srcId, targetId, self.damage * 0.50)
            # 同化 10% (暂写为暴毙)
            num = random.randint(0, 100)
            if num < 10:
                compGame.KillEntity(targetId)
        super(ArmsBowHunter, self).OnProjectileHit(data)


# HAZ-41型反物质发射器
class ArmsBowAntimatterHaz41(Arms):
    id = "secret_war_bow_antimatter_haz41:bow"
    damage = 10.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        rotComp = self.system.GetComponent(playerId, modConfig.Minecraft, modConfig.RotComponent)
        rot = rotComp.GetRot()
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 3.0 * power
            }
            self.CreateProjectile(playerId, param, Arms.Stage2)
        else:
            param = {
                'power': 3.8 * power
            }
            param1 = {
                'power': 3.8 * power,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 12))
            }
            param2 = {
                'power': 3.8 * power,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 12))
            }
            self.CreateProjectile(playerId, param, Arms.Stage3)
            self.CreateProjectile(playerId, param1, Arms.Stage3)
            self.CreateProjectile(playerId, param2, Arms.Stage3)

    def OnProjectileHit(self, data):
        srcId = data["srcId"]
        entityId = data["id"]
        # targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        if level < Arms.Stage3:
            entityIdList = compGame.GetEntitiesAround(entityId, 4, self.filters)
            Arms.explosion(srcId, pos, entityIdList, self.damage * 0.65)
        else:
            # 获取范围内怪物并吸引 再延迟爆炸
            entityIdList = compGame.GetEntitiesAround(entityId, 6, self.filters)
            for entityId in entityIdList:
                self.AttractEntities(entityId, pos, 0.4)
            compGame.AddTimer(0.4, Arms.explosion, srcId, pos, entityIdList, self.damage * 0.8)
        super(ArmsBowAntimatterHaz41, self).OnProjectileHit(data)

    # 吸引怪物到指定位置
    def AttractEntities(self, entityId, posStop, time):
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        count = 10
        compPos = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        posStart = compPos.GetFootPos()

        try:
            step0 = (max(posStart[0], posStop[0]) - min(posStart[0], posStop[0])) / count
            step1 = (max(posStart[1], posStop[1]) - min(posStart[1], posStop[1])) / count
            step2 = (max(posStart[2], posStop[2]) - min(posStart[2], posStop[2])) / count
        except TypeError:
            return

        for i in range(0, count):
            if posStart[0] > posStop[0]:
                tmpPos0 = posStart[0] - step0
            else:
                tmpPos0 = posStart[0] + step0
            if posStart[1] > posStop[1]:
                tmpPos1 = posStart[1] - step1
            else:
                tmpPos1 = posStart[1] + step1
            if posStart[2] > posStop[2]:
                tmpPos2 = posStart[2] - step2
            else:
                tmpPos2 = posStart[2] + step2
            posStart = (tmpPos0, tmpPos1, tmpPos2)
            compGame.AddTimer(i / float(count) * float(time), self.SetAttractEntitiesPos, entityId, posStart)

    def SetAttractEntitiesPos(self, entityId, pos):
        comp = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        comp.SetFootPos(pos)


# 剧毒法杖
class ArmsStaffToxic(Arms):
    id = "secret_war_staff_toxic:bow"
    damage = 6.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        # power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 1.5
            }
            self.CreateStaffProjectile(playerId, param, Arms.Stage2)
        else:
            param = {
                'power': 1.5
            }
            self.CreateStaffProjectile(playerId, param, Arms.Stage3)

    def OnProjectileHit(self, data):
        srcId = data["srcId"]
        entityId = data["id"]
        targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        if level < Arms.Stage3:
            Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff2")
            Arms.damageMob(srcId, targetId, self.damage * 0.40)
            # 致命毒素
            compEffect = serverApi.CreateComponent(targetId, "Minecraft", "effect")
            compEffect.AddEffectToEntity("fatal_poison", 5, 1, True)
        else:
            entityIdList = compGame.GetEntitiesAround(entityId, 3, self.filters)
            Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff")
            for entityId in entityIdList:
                Arms.damageMob(srcId, entityId, self.damage * 0.60)
                # 致命毒素
                compEffect = serverApi.CreateComponent(entityId, "Minecraft", "effect")
                compEffect.AddEffectToEntity("fatal_poison", 5, 1, True)
        super(ArmsStaffToxic, self).OnProjectileHit(data)


# 黏液法杖
class ArmsStaffSlime(Arms):
    id = "secret_war_staff_slime:bow"
    damage = 7.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        # power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 1.5
            }
            self.CreateStaffProjectile(playerId, param, Arms.Stage2)
        else:
            param = {
                'power': 1.5
            }
            self.CreateStaffProjectile(playerId, param, Arms.Stage3)

    def OnProjectileHit(self, data):
        srcId = data["srcId"]
        entityId = data["id"]
        targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff2")
        if level < Arms.Stage3:
            Arms.damageMob(srcId, targetId, self.damage * 0.50)
            # 减速
            compEffect = serverApi.CreateComponent(targetId, "Minecraft", "effect")
            compEffect.AddEffectToEntity("slowness", 5, 3, True)
        else:
            entityIdList = compGame.GetEntitiesAround(entityId, 3, self.filters)
            Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff")
            for entityId in entityIdList:
                Arms.damageMob(srcId, entityId, self.damage * 0.60)
                # 减速
                compEffect = serverApi.CreateComponent(entityId, "Minecraft", "effect")
                compEffect.AddEffectToEntity("slowness", 5, 4, True)
        super(ArmsStaffSlime, self).OnProjectileHit(data)


# 振奋法杖
class ArmsStaffInvigorating(Arms):
    id = "secret_war_staff_invigorating:bow"
    damage = 7.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        # power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 1.5
            }
            self.CreateMyProjectile(playerId, "minecraft:snowball", param, Arms.Stage2)
        else:
            param = {
                'power': 1.5
            }
            self.CreateStaffProjectile(playerId, param, Arms.Stage3)

    def OnProjectileHit(self, data):
        filters = {
            "any_of": [
                {
                    "subject": "other",
                    "test": "is_family",
                    "value": "player"
                }
            ]
        }
        srcId = data["srcId"]
        entityId = data["id"]
        # targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        Arms.playParticles(srcId, pos, "minecraft:totem_particle")
        if level < Arms.Stage3:
            entityIdList = compGame.GetEntitiesAround(entityId, 2, filters)
            for entityId in entityIdList:
                # 治疗
                compEffect = serverApi.CreateComponent(entityId, "Minecraft", "effect")
                compEffect.AddEffectToEntity("instant_health", 1, 2, True)
        else:
            entityIdList = compGame.GetEntitiesAround(entityId, 3, self.filters)
            Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff")
            # 治疗自身
            compEffect = serverApi.CreateComponent(srcId, "Minecraft", "effect")
            compEffect.AddEffectToEntity("instant_health", 1, 1, True)
            for entityId in entityIdList:
                Arms.damageMob(srcId, entityId, self.damage * 0.60)
        super(ArmsStaffInvigorating, self).OnProjectileHit(data)


# 破灭的爆裂疾风杖
class ArmsStaffBurstingBlast(Arms):
    id = "secret_war_staff_bursting_blast:bow"
    damage = 8.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        # power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        # 根据蓄力等级创建抛射物
        if level < Arms.Stage3:
            param = {
                'power': 1.5
            }
            self.CreateStaffProjectile(playerId, param, Arms.Stage2)
        else:
            param = {
                'power': 1.5
            }
            projectileId = self.CreateStaffProjectile(playerId, param, Arms.Stage3)
            comp = serverApi.CreateComponent(projectileId, "Minecraft", "modAttr")
            comp.SetAttr(modConfig.ModName + "ArmsStaffBurstingBlast", data['maxUseDuration'] - data['durationLeft'])

    def OnProjectileHit(self, data):
        srcId = data["srcId"]
        entityId = data["id"]
        # targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff2")
        if level < Arms.Stage3:
            entityIdList = compGame.GetEntitiesAround(entityId, 3, self.filters)
            Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff")
            for entityId in entityIdList:
                Arms.damageMob(srcId, entityId, self.damage * 1.0)
        else:
            time = int(comp.GetAttr(modConfig.ModName + "ArmsStaffBurstingBlast")) / 20
            print time
            entityIdList = compGame.GetEntitiesAround(entityId, 2 + time, self.filters)
            Arms.playParticles(srcId, pos, "minecraft:huge_explosion_emitter_staff")
            for entityId in entityIdList:
                Arms.damageMob(srcId, entityId, self.damage + time)
        super(ArmsStaffBurstingBlast, self).OnProjectileHit(data)