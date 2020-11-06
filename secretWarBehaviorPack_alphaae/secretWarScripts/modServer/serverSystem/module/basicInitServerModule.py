# -*- coding: utf-8 -*-

import server.extraServerApi as serverApi

# 用来打印规范格式的log
from secretWarScripts.modServer import logger

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon import modVarPool
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil


class BasicInitServerModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== BasicInitServerModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(serverApi, self.system, self)
        self.eventList = []
        self.eventAndCallbackList = [
            ["ClientLoadAddonsFinishServerEvent", self.OnClientLoadAddonsFinishServerEvent]
        ]
        self.userEventAndCallbackList = []

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
                'pvp': True,                        # 玩家伤害
                'show_coordinates': True,           # 显示坐标
                'fire_spreads': False,              # 火焰蔓延
                'tnt_explodes': False,              # tnt爆炸
                'mob_loot': False,                  # 生物战利品
                'natural_regeneration': False,      # 自然生命恢复
                'tile_drops': False,                # 方块掉落
                'immediate_respawn': True           # 作弊开启
            },
            'cheat_info': {
                'enable': True,                     # 是否开启作弊
                'always_day': True,                 # 终为白日
                'mob_griefing': False,              # 生物破坏
                'keep_inventory': True,             # 保留物品栏
                'weather_cycle': True,              # 天气更替
                'mob_spawn': True,                  # 生物生成
                'entities_drop_loot': False,        # 实体掉落
                'daylight_cycle': False,            # 开启昼夜交替
                'command_blocks_enabled': False     # 启用方块命令
            }
        }
        comp = serverApi.CreateComponent(levelId, "Minecraft", "game")
        comp.SetGameRulesInfoServer(gameRuleDict)
        logger.info("存档保护规则字典启用")

        # 初始化角色物品、货币、状态
        pass
