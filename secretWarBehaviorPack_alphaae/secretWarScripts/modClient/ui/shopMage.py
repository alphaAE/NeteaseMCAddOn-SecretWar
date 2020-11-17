# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import client.extraClientApi as clientApi
from secretWarScripts.modClient import logger
from secretWarScripts.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


# 所有的UI类需要继承自引擎的ScreenNode类
class ShopMageScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()

        self.mainPanel = "/mainPanel"
        self.menuPanel = self.mainPanel + "/menuPanel"

        self.itemHealth = self.menuPanel + "/itemHealth"
        self.itemEggMage = self.menuPanel + "/itemEggMage"
        self.itemStaffToxic = self.menuPanel + "/itemStaffToxic"
        self.itemStaffSlime = self.menuPanel + "/itemStaffSlime"
        self.itemStaffInvigorating = self.menuPanel + "/itemStaffInvigorating"
        self.itemBurstingBlast = self.menuPanel + "/itemBurstingBlast"

        self.btnClose = self.menuPanel + "/btnClose"
        self.btnHealth = self.itemHealth + "/btnHealth"
        self.btnEggMage = self.itemEggMage + "/btnEggMage"
        self.btnStaffToxic = self.itemStaffToxic + "/btnStaffToxic"
        self.btnStaffSlime = self.itemStaffSlime + "/btnStaffSlime"
        self.btnStaffInvigorating = self.itemStaffInvigorating + "/btnStaffInvigorating"
        self.btnBurstingBlast = self.itemBurstingBlast + "/btnBurstingBlast"

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.AddTouchEventHandler(self.btnClose, self.OnBtnClose, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnHealth, self.OnBtnHealth, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnEggMage, self.OnBtnEggMage, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnStaffToxic, self.OnBtnStaffToxic, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnStaffSlime, self.OnBtnStaffSlime, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnStaffInvigorating, self.OnBtnStaffInvigorating, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnBurstingBlast, self.OnBtnBurstingBlast, {"isSwallow": True})

    # 界面的一些初始化操作
    def Init(self, system):
        self.system = system

    # OnButton
    def OnBtnClose(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.SetRemove()

    def OnBtnHealth(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:health")

    def OnBtnEggMage(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war:egg_exclusive_precious_mage")

    def OnBtnStaffToxic(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war_staff_toxic:bow")

    def OnBtnStaffSlime(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war_staff_slime:bow")

    def OnBtnStaffInvigorating(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war_staff_invigorating:bow")

    def OnBtnBurstingBlast(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.NotifyToServerPlayerBuy("secret_war_staff_bursting_blast:bow")

    # 定义功能封装
    def NotifyToServerPlayerBuy(self, itemStr):
        eventArgs = self.system.CreateEventData()
        eventArgs["playerId"] = self.playerId
        eventArgs["item"] = itemStr
        self.system.NotifyToServer(modConfig.PlayerBuyEvent, eventArgs)
