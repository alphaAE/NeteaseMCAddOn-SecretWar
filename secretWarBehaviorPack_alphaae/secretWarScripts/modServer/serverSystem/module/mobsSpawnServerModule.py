# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi
import random as random

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class MobsSpawnServerModule:

    SecretWarEntitysList = {}

    BossSpawnPointList = [
        (292, 20, 26)
    ]

    SpawnPointList = [
        (327, 6, 26),
        (257, 6, 26),
        (292, 6, -3)
    ]

    MobsSpawnList = [
        {1: 2},
        {1: 2, 2: 1},
        {1: 1, 2: 2},
        {1: 1, 2: 1, 3: 1},
        {0: 1},

        {1: 3, 2: 1, 3: 1},
        {1: 2, 2: 2, 3: 2},
        {1: 3, 2: 2, 3: 2},
        {1: 3, 2: 2, 3: 2},
        {0: 1},

        {1: 2, 2: 1, 3: 2, 4: 1},
        {1: 2, 2: 1, 3: 2, 4: 1},
        {1: 2, 2: 1, 3: 2, 4: 2},
        {6: 1},
        {0: 1},

        {1: 1, 2: 2, 3: 2, 4: 2},
        {1: 1, 2: 2, 3: 2, 4: 3},
        {1: 1, 2: 3, 3: 3, 4: 3},
        {8: 1},
        {0: 1},

        {6: 1},
        {1: 1, 2: 3, 3: 1, 4: 3},
        {1: 1, 2: 2, 3: 2, 4: 2},
        {1: 1, 2: 1, 3: 3, 4: 4},
        {0: 1},

        {1: 1, 2: 3, 3: 3, 4: 4},
        {1: 1, 2: 2, 3: 2, 4: 4},
        {1: 1, 2: 3, 3: 2, 4: 5},
        {1: 1, 2: 3, 3: 2, 4: 5},
        {0: 1},

        {1: 1, 2: 3, 3: 3, 4: 5},
        {1: 1, 2: 2, 3: 4, 4: 5},
        {1: 1, 2: 2, 3: 4, 4: 5},
        {6: 1},
        {0: 1},

        {1: 2, 3: 1, 4: 2, 5: 1},
        {1: 2, 3: 2, 4: 2, 5: 1},
        {1: 2, 3: 2, 4: 2, 5: 2},
        {8: 1},
        {0: 1},

        {1: 6, 3: 2, 4: 2, 5: 2},
        {6: 1},
        {7: 1}
    ]

    MobsSpawnWeightsDict = {
        0: [
            {"secret_war:empty": 1}
        ],
        # 级别1
        1: [
            {"minecraft:zombie": 1},
            {"minecraft:creeper": 1},
            {"minecraft:skeleton": 1},
            {"minecraft:spider": 1},
            {"minecraft:slime": 1},
            {"minecraft:magma_cube": 1}
        ],
        # 级别2
        2: [
            {"minecraft:zombie": 1, "secret_war:chicken_jockey": 1},
            {"minecraft:skeleton": 1, "secret_war:spider_jockey": 1},
            {"minecraft:zombie_villager_v2": 1, "minecraft:zombie_pigman": 1},
            {"minecraft:spider": 1, "minecraft:wolf": 1},
            {"minecraft:stray": 1, "minecraft:zombie": 1}
        ],
        # 级别3
        3: [
            {"minecraft:ghast": 2},
            {"minecraft:enderman": 1},
            {"minecraft:wither_skeleton": 1, "minecraft:zombie_pigman": 1},
            {"minecraft:blaze": 1, "minecraft:snow_golem": 1},
            {"minecraft:vex": 2},
        ],
        # 级别4
        4: [
            {"minecraft:vindicator": 1},
            {"minecraft:witch": 1},
            {"minecraft:pillager": 1},
            {"minecraft:evocation_illager": 1}
        ],
        # 级别5
        5: [
            {"minecraft:zombie_pigman": 2, "minecraft:evocation_illager": 1},
            {"minecraft:zombie_pigman": 2, "minecraft:stray": 2}
        ],
        # 级别6
        6: [
            {"secret_war:zombie_big": 1, "secret_war:zombie_baby": 10},
            {"minecraft:zombie": 5, "minecraft:zombie_villager_v2": 5, "minecraft:drowned": 5, "minecraft:husk": 5,
                "minecraft:ghast": 2},
            {"minecraft:magma_cube": 5, "minecraft:blaze": 2},
            {"minecraft:evocation_illager": 2, "minecraft:pillager": 4, "minecraft:vindicator": 4, "minecraft:witch": 3},
            {"minecraft:enderman": 1, "minecraft:endermite": 10},
            {"secret_war:spider_jockey": 3, "secret_war:chicken_jockey": 5, "secret_war:skeleton_jockey": 3}
        ],
        # 级别7
        7: [
            {"minecraft:iron_golem": 2, "minecraft:zombie_villager_v2": 15, "minecraft:witch": 2},
            {"minecraft:ravager": 2, "minecraft:evocation_illager": 5, "minecraft:vindicator": 10, "minecraft:stray": 5},
            {"minecraft:iron_golem": 2, "minecraft:snow_golem": 10}
        ],
        # 级别8
        8: [
            {"secret_war:ender_dragon": 1}
        ]
    }

    # 间隔时间 (>10) 40
    intervals = 35
    timer = 0
    timerBroadcast = 0

    # 最大容纳怪物数
    maxMobCount = 100

    playerId = 0

    def __init__(self, system, namespace, systemName):
        logger.info("===== MobsSpawnServerModule Init =====")
        self.system = system

        self.SecretWarEntitysList = {
            "secret_war:empty": self.entitysEmpty,
            "secret_war:ender_dragon": self.entityEnderDragon,
            "secret_war:chicken_jockey": self.entitysChickenJockey,
            "secret_war:spider_jockey": self.entitySpiderJockey,
            "secret_war:zombie_big": self.entityZombieBig,
            "secret_war:zombie_baby": self.entityZombiebaby,
            "secret_war:skeleton_jockey": self.entitySkeletonJockey
        }

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = []
        self.eventAndCallbackList = [
            ["ServerPlayerTryDestroyBlockEvent", self.OnServerPlayerTryDestroyBlockEvent],
            ["MobDieEvent", self.OnMobDieEvent]
        ]
        self.userEventAndCallbackList = [
            [modConfig.StartMobsSpawn, modConfig.ServerSystemName, self.OnStartMobsSpawn]
            [modConfig.StopMobsSpawn, modConfig.ServerSystemName, self.OnStopMobsSpawn]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # CallBack
    def OnServerPlayerTryDestroyBlockEvent(self, data):
        # 使用test物品增加生成点
        playerId = data.get("playerId", "")
        comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        itemName = item.get("itemName", "")
        if itemName == "secret_war:test":
            self.SpawnPointList.append((data["x"], data["y"] + 1, data["z"]))
            self.NotifyOneMessageToAllPlay("添加点{}".format((data["x"], data["y"] + 1, data["z"])))
            data["cancel"] = True

    # 生物死亡时如果在怪物池中则 触发掉落 删除
    def OnMobDieEvent(self, data):
        entityId = data.get("id", "-1")
        if entityId in modVarPool.MobPool:
            self.SpawnLoot(entityId)
            del modVarPool.MobPool[entityId]
            modVarPool.PlayerKillMobNum += 1

    def OnStartMobsSpawn(self, data):
        self.playerId = data.get("playerId", "")
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        self.timer = compGame.AddTimer(30, self.StartMobsSpawn)
        self.TitleAllPlay("游戏30后开始，请做好准备！")

    def OnStopMobsSpawn(self, data):
        comp = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        if self.timer != 0:
            comp.CancelTimer(self.timer)
        if self.timerBroadcast != 0:
            comp.CancelTimer(self.timerBroadcast)

    # 定义功能封装
    def StartMobsSpawn(self):
        self.OnStopMobsSpawn("")
        self.MobsSpawn(0)

    def MobsSpawn(self, waveNum):
        # 全局变量波数，用于计算掉落概率等
        modVarPool.GameWaveNum = waveNum
        # 显示用波数
        showWaveNum = waveNum
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        logger.info("第{}波 怪物共计：{}/{}".format(showWaveNum + 1, len(modVarPool.MobPool), self.maxMobCount))
        self.TitleAllPlay("第{}波来袭！".format(showWaveNum + 1))

        # 扫描列表 按规则检索出怪物
        if waveNum >= len(self.MobsSpawnList):
            waveNum = len(self.MobsSpawnList) - random.randint(1, 3)
            logger.info("超出列表，按最后两波规则生成")
            self.NotifyOneMessageToAllPlay("你们已经赢了，但游戏仍会继续")
        for mobLevel, count in self.MobsSpawnList[waveNum].items():
            for i in range(count):
                self.MobsSpawnFromDict(
                    random.choice(self.SpawnPointList),
                    self.MobsSpawnWeightsDict[mobLevel][random.randint(0, len(self.MobsSpawnWeightsDict[mobLevel]) - 1)]
                )
        # 添加下次计时器
        self.timer = compGame.AddTimer(self.intervals, self.MobsSpawn, showWaveNum + 1)
        if self.intervals > 10:
            self.timerBroadcast = compGame.AddTimer(self.intervals - 10, self.NotifyOneMessageToAllPlay, "下一波即将在10s后来临")

    # 通过字典生成实体
    def MobsSpawnFromDict(self, pos, mobDict):
        for mobName, count in mobDict.items():
            for i in range(count):
                if mobName in self.SecretWarEntitysList:
                    self.CreateDefinitionMob(pos, mobName)
                else:
                    self.CreateMob(pos, modConfig.MobTypeOrdinary, mobName)

    # 通知消息到每一个玩家
    def NotifyOneMessageToAllPlay(self, msg):
        for p in serverApi.GetPlayerList():
            compMsg = serverApi.CreateComponent(p, "Minecraft", "msg")
            compMsg.NotifyOneMessage(p, msg, "§c")

    def TitleAllPlay(self, msg):
        compCommand = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "command")
        if serverApi.GetPlayerList()[0] is not None:
            compCommand.SetCommand("/title @a title §c{}".format(msg), serverApi.GetPlayerList()[0])

    # 定义的实体生成方法，用于校验怪物数量
    def CreateMob(self, pos, mobType, mobName, rot=(0, 0)):
        if len(modVarPool.MobPool) < self.maxMobCount:
            entityId = self.system.CreateEngineEntityByTypeStr(mobName, pos, rot)
            modVarPool.MobPool[entityId] = mobType
            # logger.info("{} 生成 {}".format(pos, mobName))
            return entityId
        return None

    # 按类型与波束计算并生成掉落
    def SpawnLoot(self, entityId):
        comp = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        pos = comp.GetPos()
        waveNum = modVarPool.GameWaveNum
        mobType = modVarPool.MobPool[entityId]
        rNum = random.randint(0, 100)
        if rNum <= (80 + waveNum * 0.4):
            self.CreateItem(pos, "secret_war:coin", modConfig.MobLootCount[mobType])
        rNum = random.randint(0, 100)
        if rNum <= (30 + waveNum * 0.4):
            itemDict = {
                'itemName': "minecraft:baked_potato",
                'count': 1
            }
            self.system.CreateEngineItemEntity(itemDict, 0, pos)

    def CreateItem(self, pos, itemName, count, dimensionId=0):
        itemDict = {
            'itemName': itemName,
            'count': count
        }
        itemEntityId = self.system.CreateEngineItemEntity(itemDict, dimensionId, pos)
        # logger.info("{} 掉落 {}".format(pos, itemName))
        return itemEntityId

    # 杀死所有附近怪物
    def killAllOtherMob(self, pos):
        entityId = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:zombie")
        filters = {
            "any_of": [
                {
                    "subject": "other",
                    "test": "is_family",
                    "value": "swmob"
                }
            ]
        }
        comp = serverApi.CreateComponent(entityId, "Minecraft", "game")
        for i in range(5):
            entityIdList = comp.GetEntitiesAround(entityId, 90, filters)
            for entityId in entityIdList:
                if entityId in modVarPool.MobPool:
                    del modVarPool.MobPool[entityId]
                compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
                compGame.KillEntity(entityId)

    # 生成代码定义的实体
    def CreateDefinitionMob(self, pos, mobName):
        self.SecretWarEntitysList[mobName](pos)

    # # 代码定义实体
    def entitysEmpty(self, pos):
        self.TitleAllPlay("本回合休整")
        self.killAllOtherMob(pos)

    def entityEnderDragon(self, pos):
        self.NotifyOneMessageToAllPlay("凋零已诞生")
        pos = self.BossSpawnPointList[0]
        compCommand = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "command")
        if serverApi.GetPlayerList()[0] is not None:
            compCommand.SetCommand(
                "/summon minecraft:wither {} {} {}".format(pos[0], pos[1], pos[2]),
                serverApi.GetPlayerList()[0]
            )

    def entitysChickenJockey(self, pos):
        entityId1 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:zombie")
        entityId2 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:chicken")
        # 合法性验证
        if entityId1 is None or entityId2 is None:
            return
        # 触发僵尸as_baby事件
        comp = serverApi.CreateComponent(entityId1, 'Minecraft', 'entityEvent')
        comp.TriggerCustomEvent(entityId1, "minecraft:as_baby")
        # 设置乘骑关系
        comtServer = serverApi.CreateComponent(entityId1, "Minecraft", "ride")
        comtServer.SetEntityRide(entityId1, entityId2)
        comtServer.SetRiderRideEntity(entityId1, entityId2)

    def entitySpiderJockey(self, pos):
        entityId1 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:skeleton")
        entityId2 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:spider")
        # 合法性验证
        if entityId1 is None or entityId2 is None:
            return
        # 设置乘骑关系
        comtServer = serverApi.CreateComponent(entityId1, "Minecraft", "ride")
        comtServer.SetEntityRide(entityId1, entityId2)
        comtServer.SetRiderRideEntity(entityId1, entityId2)

    def entityZombieBig(self, pos):
        self.NotifyOneMessageToAllPlay("生成ZombieBig")
        entityId1 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:zombie")
        # 合法性验证
        if entityId1 is None:
            return
        # 设置名牌
        compName = serverApi.CreateComponent(entityId1, "Minecraft", "name")
        compName.SetName("ZombieKing")
        # 增大模型 碰撞箱 生命 攻击力
        comp = serverApi.CreateComponent(entityId1, 'Minecraft', 'entityEvent')
        comp.TriggerCustomEvent(entityId1, "secret_war:as_big")

    def entityZombiebaby(self, pos):
        entityId1 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:zombie")
        # 合法性验证
        if entityId1 is None:
            return
        # 触发僵尸as_baby事件
        comp = serverApi.CreateComponent(entityId1, 'Minecraft', 'entityEvent')
        comp.TriggerCustomEvent(entityId1, "minecraft:as_baby")

    def entitySkeletonJockey(self, pos):
        entityId1 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:skeleton")
        entityId2 = self.CreateMob(pos, modConfig.MobTypeOrdinary, "minecraft:skeleton_horse")
        # 合法性验证
        if entityId1 is None or entityId2 is None:
            return
        # 设置乘骑关系
        comtServer = serverApi.CreateComponent(entityId1, "Minecraft", "ride")
        comtServer.SetEntityRide(entityId1, entityId2)
        comtServer.SetRiderRideEntity(entityId1, entityId2)
