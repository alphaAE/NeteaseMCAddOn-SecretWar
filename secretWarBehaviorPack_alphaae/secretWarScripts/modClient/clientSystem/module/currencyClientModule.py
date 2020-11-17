# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
from secretWarScripts.modCommon import modConfig

from secretWarScripts.modCommon import modConfig
from secretWarScripts.modCommon.listenEventUtil import ListenEventUtil

# 用来打印规范的log
from secretWarScripts.modClient import logger


class CurrencyClientModule:

    def __init__(self, system, namespace, systemName):
        logger.info("===== CurrencyClientModule Init =====")
        self.system = system

        # 监听事件列表
        self.listenEventUtil = ListenEventUtil(clientApi, self.system, self)
        self.eventList = [
            [modConfig.ClientGetPlayerCurrencyEvent],
            [modConfig.ClientSetPlayerCurrencyEvent],
            [modConfig.ClientGetPlayerLifeEvent]
        ]
        self.eventAndCallbackList = [
            ["UiInitFinished", self.OnUiInitFinished]
        ]
        self.userEventAndCallbackList = [
            [modConfig.ServerCallbackPlayerCurrencyEvent, modConfig.ServerSystemName, self.OnServerCallbackPlayerCurrencyEvent],
            [modConfig.OpenShopEvent, modConfig.ServerSystemName, self.OnOpenShopEvent],
            [modConfig.ServerCallbackPlayerLifeEvent, modConfig.ServerSystemName, self.OnServerCallbackPlayerLifeEvent]
        ]

        # ListenEvent
        self.listenEventUtil.InitAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    def Destroy(self):
        # UnListenEvent
        self.listenEventUtil.DestroyAll(self.eventList, self.eventAndCallbackList, self.userEventAndCallbackList)

    # 监听引擎初始化完成事件创建UI
    def OnUiInitFinished(self, args):
        # 注册UI 创建UI
        clientApi.RegisterUI(
            modConfig.ModName,
            modConfig.CurrencyUIName,
            modConfig.CurrencyUIPyClsPath,
            modConfig.CurrencyUIScreenDef
        )
        self.currencyUINode = clientApi.CreateUI(modConfig.ModName, modConfig.CurrencyUIName, {"isHud": 1})
        # self.mFpsBattleUINode = clientApi.GetUI(modConfig.ModName, modConfig.FpsBattleUIName)
        if self.currencyUINode:
            self.currencyUINode.Init(self.system)
            # 向服务器icon请求数据
            eventArgs = self.system.CreateEventData()
            eventArgs["playerId"] = clientApi.GetLocalPlayerId()
            self.system.NotifyToServer(modConfig.ClientGetPlayerCurrencyEvent, eventArgs)
            # 请求Life数据
            eventArgs = self.system.CreateEventData()
            eventArgs["playerId"] = clientApi.GetLocalPlayerId()
            self.system.NotifyToServer(modConfig.ClientGetPlayerLifeEvent, eventArgs)
        else:
            logger.error("create ui %s failed!" % modConfig.FpsBattleUIScreenDef)

    # 收到服务端通知更改ICON显示
    def OnServerCallbackPlayerCurrencyEvent(self, args):
        if self.currencyUINode:
            self.currencyUINode.SetCurrency(args.get("currency", "-2"))

    # 收到服务端通知更改生命显示
    def OnServerCallbackPlayerLifeEvent(self, args):
        print args
        if self.currencyUINode:
            self.currencyUINode.SetLife(args.get("life", "-2"))

    # 收到服务端通知打开商店
    def OnOpenShopEvent(self, data):
        shopName = data.get("shopName", "")
        if shopName == modConfig.ShopMageUIName:
            clientApi.RegisterUI(
                modConfig.ModName,
                modConfig.ShopMageUIName,
                modConfig.ShopMageUIPyClsPath,
                modConfig.ShopMageUIScreenDef
            )
            self.shopMageUI = clientApi.CreateUI(modConfig.ModName, modConfig.ShopMageUIName, {"isHud": 0})
            if self.shopMageUI:
                self.shopMageUI.Init(self.system)
            else:
                logger.error("create ui %s failed!" % modConfig.FpsBattleUIScreenDef)
        elif shopName == modConfig.ShopHunterUIName:
            clientApi.RegisterUI(
                modConfig.ModName,
                modConfig.ShopHunterUIName,
                modConfig.ShopHunterUIPyClsPath,
                modConfig.ShopHunterUIScreenDef
            )
            self.shopHunterUI = clientApi.CreateUI(modConfig.ModName, modConfig.ShopHunterUIName, {"isHud": 0})
            if self.shopHunterUI:
                self.shopHunterUI.Init(self.system)
            else:
                logger.error("create ui %s failed!" % modConfig.FpsBattleUIScreenDef)
