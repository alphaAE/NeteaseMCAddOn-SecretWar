# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import client.extraClientApi as clientApi
from secretWarScripts.modClient import logger
from secretWarScripts.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


# 所有的UI类需要继承自引擎的ScreenNode类
class ShopHunterScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()

        self.mainPanel = "/mainPanel"
        self.menuPanel = self.mainPanel + "/menuPanel"

        self.itemAttack = self.menuPanel + "/itemAttack"
        self.itemEggExclusivePreciousHunter = self.menuPanel + "/itemEggExclusivePreciousHunter"
        self.itemBowFlame = self.menuPanel + "/itemBowFlame"
        self.itemBowStrong = self.menuPanel + "/itemBowStrong"
        self.itemBowHunter = self.menuPanel + "/itemBowHunter"
        self.itemBowAntimatterHaz41 = self.menuPanel + "/itemBowAntimatterHaz41"

        self.btnClose = self.menuPanel + "/btnClose"
        self.btnAttack = self.itemAttack + "/btnAttack"
        self.btnEggExclusivePreciousHunter = self.itemEggExclusivePreciousHunter + "/btnEggExclusivePreciousHunter"
        self.btnBowFlame = self.itemBowFlame + "/btnBowFlame"
        self.btnBowStrong = self.itemBowStrong + "/btnBowStrong"
        self.btnBowHunter = self.itemBowHunter + "/btnBowHunter"
        self.btnBowAntimatterHaz41 = self.itemBowAntimatterHaz41 + "/btnBowAntimatterHaz41"

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.AddTouchEventHandler(self.btnClose, self.OnBtnClose, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnAttack, self.OnBtnAttack, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnEggExclusivePreciousHunter, self.OnBtnEggExclusivePreciousHunter, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnBowFlame, self.OnBtnBowFlame, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnBowStrong, self.OnBtnBowStrong, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnBowHunter, self.OnBtnBowHunter, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnBowAntimatterHaz41, self.OnBtnBowAntimatterHaz41, {"isSwallow": True})

    # 界面的一些初始化操作
    def Init(self, system):
        self.system = system

    # OnButton
    def OnBtnClose(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.SetRemove()

    def OnBtnAttack(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:attack")

    def OnBtnEggExclusivePreciousHunter(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:egg_exclusive_precious_hunter")

    def OnBtnBowFlame(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:bow_flame")

    def OnBtnBowStrong(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:bow_strong")

    def OnBtnBowHunter(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:bow_hunter")

    def OnBtnBowAntimatterHaz41(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:bow_antimatter_haz41")

    # 定义功能封装
    def NotifyToServerPlayerBuy(self, itemStr):
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = self.playerId
        eventArgs["item"] = itemStr
        self.system.NotifyToServer(modConfig.PlayerBuyEvent, eventArgs)
