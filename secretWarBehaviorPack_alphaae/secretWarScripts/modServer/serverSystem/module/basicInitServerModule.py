# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class BasicInitServerModule:

    init = 0

    def __init__(self, system, namespace, systemName):
        logger.info("===== BasicInitServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = [
            [modConfig.StartMobsSpawn],
            [modConfig.CreateNPCEvent]
        ]
        self.eventAndCallbackList = [
            ["AddServerPlayerEvent", self.OnAddServerPlayerEvent],
            ["ClientLoadAddonsFinishServerEvent", self.OnClientLoadAddonsFinishServerEvent],
            ["CommandEvent", self.OnCommandEvent]
        ]
        self.userEventAndCallbackList = [
            [modConfig.StartGame, modConfig.ServerSystemName, self.OnStartGame]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # CallBack
    # 客户端加载Addon完成时回调
    def OnClientLoadAddonsFinishServerEvent(self, data):
        levelId = serverApi.GetLevelId()
        # 游戏字典
        gameRuleDict = {
            'option_info': {
                'pvp': False,                       # 玩家伤害
                'show_coordinates': True,           # 显示坐标
                'fire_spreads': False,              # 火焰蔓延
                'tnt_explodes': False,              # tnt爆炸
                'mob_loot': False,                  # 生物战利品
                'natural_regeneration': True,       # 自然生命恢复
                'tile_drops': False,                # 方块掉落
                'immediate_respawn': True           # 作弊开启
            },
            'cheat_info': {
                'enable': True,                     # 是否开启作弊
                'always_day': True,                 # 终为白日
                'mob_griefing': False,              # 生物破坏
                'keep_inventory': True,             # 保留物品栏
                'weather_cycle': True,              # 天气更替
                'mob_spawn': False,                 # 生物生成
                'entities_drop_loot': False,        # 实体掉落
                'daylight_cycle': False,            # 开启昼夜交替
                'command_blocks_enabled': False     # 启用方块命令
            }
        }
        comp = serverApi.CreateComponent(levelId, "Minecraft", "game")
        comp.SetGameRulesInfoServer(gameRuleDict)
        logger.info("存档保护规则字典启用")

    # 初始化角色物品、状态
    def OnAddServerPlayerEvent(self, data):
        playerId = data.get("id", "0")
        if playerId != "0":
            # 初始化攻击 生命 速度
            compAttr = serverApi.CreateComponent(playerId, "Minecraft", "attr")
            compAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.DAMAGE, 1)
            compAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 40)
            compAttr.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 40)
            compAttr.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.SPEED, 0.15)
            # 首次进入重置
            if self.init == 0:
                self.init = 1
                self.KillAllEntity(playerId)

    def OnCommandEvent(self, data):
        entityId = data.get("entityId", "")
        command = data.get("command", "")
        if command == "/sw s":
            self.start(entityId)
        elif command == "/sw npc":
            self.BroadcastSpawnNPC(entityId)
        elif command == "/sw k":
            self.KillAllEntity(entityId)

    def OnStartGame(self, data):
        entityId = data.get("entityId", "")
        self.start(entityId)
    # 定义功能封装

    def start(self, entityId):
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        self.KillAllEntity(entityId)
        # 通知MobsSpawnServerModule开始刷新怪物
        compGame.AddTimer(4.0, self.BroadcastStartMobsSpawn, entityId)
        compGame.AddTimer(4.0, self.BroadcastSpawnNPC, entityId)
        modVarPool.MobPool.clear()

    # 杀死所有附近非玩家实体
    def killAllOtherEntity(self, entityId):
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
        comp = serverApi.CreateComponent(entityId, "Minecraft", "game")
        for i in range(5):
            entityIdList = comp.GetEntitiesAround(entityId, 80, filters)
            for entityId in entityIdList:
                compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
                compGame.KillEntity(entityId)

    # 通知MobsSpawnServerModule开始刷新怪物
    def BroadcastStartMobsSpawn(self, entityId):
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = entityId
        self.system.BroadcastEvent(modConfig.StartMobsSpawn, eventArgs)

    # 通知生成NPC
    def BroadcastSpawnNPC(self, entityId):
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = entityId
        self.system.BroadcastEvent(modConfig.CreateNPCEvent, eventArgs)

    def KillAllEntity(self, entityId):
        # 多次杀死所有附近非玩家实体 (防止史莱姆)
        compGame = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
        compGame.AddTimer(0.0, self.killAllOtherEntity, entityId)
        compGame.AddTimer(1.5, self.killAllOtherEntity, entityId)
        compGame.AddTimer(3.0, self.killAllOtherEntity, entityId)
