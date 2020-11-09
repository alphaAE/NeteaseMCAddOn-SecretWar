# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi
import random as random

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class MobsSpawnServerModule:

    SpawnPointList = [
        (346, 5, 26),
        (238, 5, 26),
        (292, 5, -22)
    ]

    MobsSpawnList = [
        #第一波 级别1种选任意2组 级别2种任意1组
        {1: 2, 2: 1},
        {1: 1, 2: 3},
        {3: 3},
        {4: 2}
    ]

    MobsSpawnWeightsDict = {
        # 级别1 两种组合
        1: [
            {"minecraft:zombie": 1, "minecraft:creeper": 4},
            {"minecraft:zombie": 1, "minecraft:creeper": 1}
        ],
        # 级别2
        2: [
            {"minecraft:zombie": 2, "minecraft:creeper": 4},
            {"minecraft:zombie": 2, "minecraft:creeper": 1}
        ],
        # 级别3
        3: [
            {"minecraft:zombie": 3, "minecraft:creeper": 4},
            {"minecraft:zombie": 3, "minecraft:creeper": 1}
        ],
        # 级别4
        4: [
            {"minecraft:zombie": 4, "minecraft:creeper": 4},
            {"minecraft:zombie": 4, "minecraft:creeper": 1}
        ]
    }

    # 间隔时间 (>10)
    intervals = 15

    timer = 0
    timerBroadcast = 0

    playerId = 0

    def __init__(self, system, namespace, systemName):
        logger.info("===== MobsSpawnServerModule Init =====")
        self.system = system

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
        self.MobsSpawn(0)

    # 定义功能封装
    def MobsSpawn(self, waveNum):
        # 显示用波数
        showWaveNum = waveNum
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        self.NotifyOneMessageToAllPlay("第{}波来袭！".format(waveNum + 1))
        # 扫描列表 按规则检索出怪物
        for pos in self.SpawnPointList:
            if waveNum >= len(self.MobsSpawnList):
                waveNum = len(self.MobsSpawnList) - 1
                logger.info("超出列表，按最后一波规则生成")
            for mobLevel, count in self.MobsSpawnList[waveNum].items():
                for i in range(count):
                    self.MobsSpawnFromDict(
                        pos,
                        self.MobsSpawnWeightsDict[mobLevel][random.randint(0, len(self.MobsSpawnWeightsDict[mobLevel]) - 1)]
                    )
        # 添加下次计时器
        self.timer = compGame.AddTimer(self.intervals, self.MobsSpawn, showWaveNum + 1)
        self.timerBroadcast = compGame.AddTimer(self.intervals - 10, self.NotifyOneMessageToAllPlay, "下一波即将在10s后来临")

    # 通过字典生成实体
    def MobsSpawnFromDict(self, pos, mobDict):
        for mobName, count in mobDict.items():
            for i in range(count):
                # pass 概率获取词缀
                entityId = self.system.CreateEngineEntityByTypeStr(mobName, pos, (0, 0))
                # 为怪物进行合法性调整 锁定距离 寻路南门 不燃烧 可攻击对象
                if entityId is not None:
                    self.MobValidityModify(entityId)
        # print pos, mobDict

    # 通知消息到每一个玩家
    def NotifyOneMessageToAllPlay(self, msg):
        for i in serverApi.GetPlayerList():
            compMsg = serverApi.CreateComponent(i, "Minecraft", "msg")
            compMsg.NotifyOneMessage(i, msg, "§c")

    # 修改实体使其适合该游戏
    def MobValidityModify(self, entityId):
        # 因无法实现而搁置
        # comp = serverApi.GetComponent(entityId, "Minecraft", "health")
        # print comp
        pass
