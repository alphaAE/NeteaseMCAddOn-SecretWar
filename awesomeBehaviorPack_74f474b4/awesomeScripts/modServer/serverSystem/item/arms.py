import server.extraServerApi as serverApi

from awesomeScripts.modCommon import modConfig


class Arms(object):

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

    # 武器开始蓄力时触发
    def OnServerItemTryUseEvent(self, data):
        pass

    # 武器射出投掷物时触发
    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        pass

    # 武器击中实体时触发
    def OnProjectileHit(self, data):
        # 在子弹射中后发送广播并将体清除掉
        self.system.BroadcastToAllClient(modConfig.BulletHitEvent, data)
        self.system.DestroyEntity(data.get("id", "-1"))

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
    def setAttr(entityId, armsId, level):
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        comp.SetAttr(modConfig.ModName + modConfig.ProjectileAttr, {"armsId": armsId, "level": level})


# 燃烧连弩


class ArmsBowFlame(Arms):
    id = "secret_war:bow_flame"
    damage = 6.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        rotComp = self.system.GetComponent(playerId, modConfig.Minecraft, modConfig.RotComponent)
        rot = rotComp.GetRot()

        # 根据蓄力等级创建抛射物
        if level == Arms.Stage1:
            param = {
                'power': 2.0 * power,
                'damage': self.damage * 0.65
            }
            self.CreateProjectile(playerId, param, Arms.Stage1)
        elif level == Arms.Stage2:
            param = {
                'power': 2.6 * power,
                'damage': self.damage
            }
            param1 = {
                'power': 2.6 * power,
                'damage': self.damage * 0.45,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 8))
            }
            param2 = {
                'power': 2.6 * power,
                'damage': self.damage * 0.45,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 8))
            }
            self.CreateProjectile(playerId, param, Arms.Stage2)
            self.CreateProjectile(playerId, param1, Arms.Stage2)
            self.CreateProjectile(playerId, param2, Arms.Stage2)
        elif level == Arms.Stage3:
            param = {
                'power': 3.4 * power,
                'damage': self.damage
            }
            param1 = {
                'power': 3.4 * power,
                'damage': self.damage * 0.65,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 12))
            }
            param2 = {
                'power': 3.4 * power,
                'damage': self.damage * 0.65,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 12))
            }
            self.CreateProjectile(playerId, param, Arms.Stage3)
            self.CreateProjectile(playerId, param1, Arms.Stage3)
            self.CreateProjectile(playerId, param2, Arms.Stage3)

    def OnProjectileHit(self, data):
        entityId = data["id"]
        targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        if level == Arms.Stage1:
            comp = serverApi.CreateComponent(targetId, "Minecraft", "attr")
            comp.SetEntityOnFire(5)
        elif level == Arms.Stage2:
            comp = serverApi.CreateComponent(entityId, "Minecraft", "game")
            entityIdList = comp.GetEntitiesAround(entityId, 2, {})
            for id in entityIdList:
                tmpComp = serverApi.CreateComponent(id, "Minecraft", "attr")
                tmpComp.SetEntityOnFire(5)
        elif level >= Arms.Stage3:
            comp = serverApi.CreateComponent(targetId, "Minecraft", "attr")
            comp.SetEntityOnFire(5)
            comp = serverApi.CreateComponent(entityId, "Minecraft", "explosion")
            comp.CreateExplosion(pos, 3, False, False, entityId, srcId)
        super(ArmsBowFlame, self).OnProjectileHit(data)


# 强击连弩（击退有待研究）


class ArmsBowStrong(Arms):
    id = "secret_war:bow_strong"
    damage = 8.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")

        # 根据蓄力等级创建抛射物
        if level == Arms.Stage1:
            param = {
                'power': 2.0 * power,
                'damage': self.damage * 0.8
            }
            self.CreateProjectile(playerId, param, Arms.Stage1)
        elif level == Arms.Stage2:
            param = {
                'power': 2.6 * power,
                'damage': self.damage * 0.8
            }
            for i in range(0, 2):
                compGame.AddTimer(i / 10.0, self.CreateProjectile, playerId, param, Arms.Stage2)
        elif level == Arms.Stage3:
            param = {
                'power': 3.4 * power,
                'damage': self.damage
            }
            for i in range(0, 3):
                compGame.AddTimer(i / 10.0, self.CreateProjectile, playerId, param, Arms.Stage3)

    def OnProjectileHit(self, data):
        super(ArmsBowStrong, self).OnProjectileHit(data)


# 猎人之弩（效果需要在词缀模块制作后）


class ArmsBowHunter(Arms):
    id = "secret_war:bow_hunter"
    damage = 8.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        rotComp = self.system.GetComponent(playerId, modConfig.Minecraft, modConfig.RotComponent)
        rot = rotComp.GetRot()
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")

        # 根据蓄力等级创建抛射物
        if level == Arms.Stage1:
            param = {
                'power': 2.0 * power,
                'damage': self.damage * 0.5
            }
            self.CreateProjectile(playerId, param, Arms.Stage1)
        elif level == Arms.Stage2:
            param = {
                'power': 2.8 * power,
                'damage': self.damage
            }
            param1 = {
                'power': 2.8 * power,
                'damage': self.damage * 0.2,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 12))
            }
            param2 = {
                'power': 2.8 * power,
                'damage': self.damage * 0.2,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 12))
            }
            self.CreateProjectile(playerId, param, Arms.Stage2)
            self.CreateProjectile(playerId, param1, Arms.Stage2)
            self.CreateProjectile(playerId, param2, Arms.Stage2)
        elif level == Arms.Stage3:
            param = {
                'power': 3.3 * power,
                'damage': self.damage
            }
            for i in range(0, 5):
                compGame.AddTimer(i / 10.0, self.CreateProjectile, playerId, param, Arms.Stage3)

    def OnProjectileHit(self, data):
        super(ArmsBowHunter, self).OnProjectileHit(data)


# HAZ-41型反物质发射器


class ArmsBowAntimatterHaz41(Arms):
    id = "secret_war:bow_antimatter_haz41"
    damage = 10.0

    def OnRangedWeaponReleaseUsingServerEvent(self, data):
        power = Arms.getLaunchPower(data['durationLeft'], data['maxUseDuration'])
        level = Arms.getLaunchLevel(data['durationLeft'], data['maxUseDuration'])
        playerId = data["playerId"]
        rotComp = self.system.GetComponent(playerId, modConfig.Minecraft, modConfig.RotComponent)
        rot = rotComp.GetRot()

        # 根据蓄力等级创建抛射物
        if level == Arms.Stage1:
            param = {
                'power': 2.0 * power,
                'damage': self.damage * 0.0
            }
            self.CreateProjectile(playerId, param, Arms.Stage1)
        elif level == Arms.Stage2:
            param = {
                'power': 2.6 * power,
                'damage': self.damage
            }
            param1 = {
                'power': 2.6 * power,
                'damage': self.damage * 0.45,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 12))
            }
            param2 = {
                'power': 2.6 * power,
                'damage': self.damage * 0.45,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 12))
            }
            self.CreateProjectile(playerId, param, Arms.Stage2)
            self.CreateProjectile(playerId, param1, Arms.Stage2)
            self.CreateProjectile(playerId, param2, Arms.Stage2)
        elif level == Arms.Stage3:
            param = {
                'power': 3.4 * power,
                'damage': self.damage
            }
            param1 = {
                'power': 3.4 * power,
                'damage': self.damage * 0.65,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] + 13))
            }
            param2 = {
                'power': 3.4 * power,
                'damage': self.damage * 0.65,
                'direction': serverApi.GetDirFromRot((rot[0], rot[1] - 13))
            }
            self.CreateProjectile(playerId, param, Arms.Stage3)
            self.CreateProjectile(playerId, param1, Arms.Stage3)
            self.CreateProjectile(playerId, param2, Arms.Stage3)

    def OnProjectileHit(self, data):
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        entityId = data["id"]
        # targetId = data["targetId"]
        srcId = data["srcId"]
        pos = (data["x"], data["y"], data["z"])
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
        # 获取抛射物实体中的定义属性
        comp = serverApi.CreateComponent(entityId, "Minecraft", "modAttr")
        level = comp.GetAttr(modConfig.ModName + modConfig.ProjectileAttr)["level"]
        if level == Arms.Stage1:
            comp = serverApi.CreateComponent(entityId, "Minecraft", "explosion")
            comp.CreateExplosion(pos, 2, False, False, entityId, srcId)
        elif level == Arms.Stage2:
            # 获取范围内怪物并吸引 再延迟爆炸
            comp = serverApi.CreateComponent(entityId, "Minecraft", "game")
            entityIdList = comp.GetEntitiesAround(entityId, 6, filters)
            for entityId in entityIdList:
                self.AttractEntities(entityId, pos, 0.4)
            comp = serverApi.CreateComponent(entityId, "Minecraft", "explosion")
            compGame.AddTimer(0.4, lambda: comp.CreateExplosion(pos, 3, False, False, entityId, srcId))
        elif level == Arms.Stage3:
            comp = serverApi.CreateComponent(entityId, "Minecraft", "explosion")
            comp.CreateExplosion(pos, 6, False, False, entityId, srcId)
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
