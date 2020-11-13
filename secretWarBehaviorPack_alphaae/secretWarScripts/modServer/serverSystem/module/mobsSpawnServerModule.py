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

    SpawnPointList = [
        (327, 6, 26),
        (257, 6, 26),
        (292, 6, -3)
    ]

    MobsSpawnList = [
        {1: 2},
        {1: 2, 2: 1},
        {1: 4, 2: 2},
        {1: 5, 2: 1, 3: 1},
        {1: 6, 2: 2, 3: 1},
        {1: 7, 2: 3, 3: 2},
        {1: 8, 2: 4, 3: 2},
        {1: 9, 2: 5, 3: 2},
        {1: 10, 2: 5, 3: 2, 4: 1},
        {6: 1},
        {1: 12, 2: 6, 3: 2, 4: 1},
        {1: 13, 2: 6, 3: 2, 4: 2},
        {1: 14, 2: 4, 3: 2, 4: 3},
        {1: 14, 2: 4, 3: 3, 4: 4},
        {1: 15, 2: 5, 3: 3, 4: 5},
        {1: 15, 2: 5, 3: 3, 4: 6},
        {1: 15, 2: 5, 3: 3, 4: 7},
        {8: 1},
        {0: 1},
        {6: 1},
        {1: 13, 2: 5, 3: 3, 4: 10},
        {1: 13, 2: 5, 3: 3, 4: 11},
        {1: 12, 2: 5, 3: 3, 4: 12},
        {1: 12, 2: 5, 3: 3, 4: 13},
        {1: 11, 2: 4, 3: 4, 4: 13},
        {1: 11, 2: 4, 3: 4, 4: 13},
        {1: 10, 2: 3, 3: 5, 4: 14},
        {1: 10, 2: 3, 3: 5, 4: 14},
        {1: 9, 2: 2, 3: 6, 4: 15},
        {6: 1},
        {1: 9, 2: 2, 3: 6, 4: 15},
        {1: 8, 2: 2, 3: 7, 4: 16},
        {1: 8, 2: 2, 3: 7, 4: 16},
        {1: 7, 3: 8, 4: 17, 5: 1},
        {1: 6, 3: 8, 4: 18, 5: 1},
        {1: 6, 3: 7, 4: 18, 5: 2},
        {8: 1},
        {0: 1},
        {7: 1}
    ]

    MobsSpawnWeightsDict = {
        0: [
            {"secret_war:empty": 0}
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
            {"minecraft:spider": 2, "minecraft:wolf": 1},
            {"minecraft:stray": 1, "minecraft:zombie": 1}
        ],
        # 级别3
        3: [
            {"minecraft:ghast": 2},
            {"minecraft:enderman": 2},
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
            {"minecraft:zombie_pigman": 3},
            {"minecraft:zombie_pigman": 2, "minecraft:evocation_illager": 1},
            {"minecraft:zombie_pigman": 2, "minecraft:stray": 2}
        ],
        # 级别6
        6: [
            {"secret_war:zombie_big": 1, "secret_war:zombie_baby": 30},
            {"minecraft:zombie": 5, "minecraft:zombie_villager_v2": 5, "minecraft:drowned": 5, "minecraft:husk": 5,
                "minecraft:skeleton": 5, "minecraft:phantom": 5, "minecraft:ghast": 2},
            {"minecraft:magma_cube": 20, "minecraft:blaze": 2},
            {"minecraft:evocation_illager": 4, "minecraft:pillager": 10, "minecraft:vindicator": 10, "minecraft:witch": 3},
            {"minecraft:enderman": 20, "minecraft:endermite": 10},
            {"secret_war:spider_jockey": 5, "secret_war:chicken_jockey": 10, "secret_war:skeleton_jockey": 5}
        ],
        # 级别7
        7: [
            {"minecraft:iron_golem": 2, "minecraft:zombie_villager_v2": 20, "minecraft:witch": 2},
            {"minecraft:ravager": 2, "minecraft:evocation_illager": 5, "minecraft:vindicator": 10, "minecraft:stray": 5},
            {"minecraft:iron_golem": 5, "minecraft:snow_golem": 20}
        ],
        # 级别8
        8: [
            {"secret_war:ender_dragon": 1}
        ]
    }

    # 间隔时间 (>10)
    intervals = 40

    timer = 0
    timerBroadcast = 0

    playerId = 0

    def __init__(self, system, namespace, systemName):
        logger.info("===== MobsSpawnServerModule Init =====")
        self.system = system

        self.SecretWarEntitysList = {
            "secret_war:empty": self.entitysEmpty,
            "secret_war:ender_dragon": self.entityEnderDragon,
            "secret_war:chicken_jockey": self.entitysChickenJockey,
            # "secret_war:spider_jockey": self.secretWarEntitys,
            # "secret_war:zombie_big": self.secretWarEntitys,
            # "secret_war:zombie_baby": self.secretWarEntitys,
            # "secret_war:skeleton_jockey": self.secretWarEntitys
        }

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = []
        self.eventAndCallbackList = [
            ["ServerPlayerTryDestroyBlockEvent", self.OnServerPlayerTryDestroyBlockEvent]
        ]
        self.userEventAndCallbackList = [
            [modConfig.StartMobsSpawn, modConfig.ServerSystemName, self.OnStartMobsSpawn]
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

    def OnStartMobsSpawn(self, data):
        self.playerId = data.get("playerId", "")
        self.OnStopMobsSpawn("")
        self.MobsSpawn(0)

    def OnStopMobsSpawn(self, data):
        comp = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        if self.timer != 0:
            comp.CancelTimer(self.timer)
        if self.timerBroadcast != 0:
            comp.CancelTimer(self.timerBroadcast)

    # 定义功能封装
    def MobsSpawn(self, waveNum):
        # 显示用波数
        showWaveNum = waveNum
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        self.TitleAllPlay("第{}波来袭！".format(waveNum + 1))
        # 扫描列表 按规则检索出怪物
        if waveNum >= len(self.MobsSpawnList):
            waveNum = len(self.MobsSpawnList) - 1
            logger.info("超出列表，按最后一波规则生成")
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
                logger.info("{} 生成 {}".format(pos, mobName))
                # 限制刷怪器

                if mobName in self.SecretWarEntitysList:
                    self.CreateEntityByTypeStr(pos, mobName)
                else:
                    entityId = self.system.CreateEngineEntityByTypeStr(mobName, pos, (0, 0))
                    # print(entityId)

    # 通知消息到每一个玩家
    def NotifyOneMessageToAllPlay(self, msg):
        for p in serverApi.GetPlayerList():
            compMsg = serverApi.CreateComponent(p, "Minecraft", "msg")
            compMsg.NotifyOneMessage(p, msg, "§c")

    def TitleAllPlay(self, msg):
        compCommand = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "command")
        if serverApi.GetPlayerList()[0] is not None:
            compCommand.SetCommand("/title @a title §c{}".format(msg), serverApi.GetPlayerList()[0])

    # 生成代码定义的实体
    def CreateEntityByTypeStr(self, pos, mobName):
        self.SecretWarEntitysList[mobName](pos)

    # # 代码定义实体
    def entitysEmpty(self, pos):
        self.TitleAllPlay("本回合休整")

    def entityEnderDragon(self, pos):
        self.NotifyOneMessageToAllPlay("boss暂时空缺")
        # compCommand = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "command")
        # if serverApi.GetPlayerList()[0] is not None:
        #     compCommand.SetCommand("/summon ender_drago {} {} {}".format(pos[0], pos[1], pos[2]), serverApi.GetPlayerList()[0])

    def entitysChickenJockey(self, pos):
        entityId = self.system.CreateEngineEntityByTypeStr("", pos, (0, 0))
        entityId2 = self.system.CreateEngineEntityByTypeStr("", pos, (0, 0))