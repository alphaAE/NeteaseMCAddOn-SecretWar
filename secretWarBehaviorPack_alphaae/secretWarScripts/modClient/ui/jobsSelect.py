# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import client.extraClientApi as clientApi
from secretWarScripts.modClient import logger
from secretWarScripts.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


# 所有的UI类需要继承自引擎的ScreenNode类
class JobsSelectScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()

        self.panelSelect = "/panelSelect"
        self.panelHunter = self.panelSelect + "/panelHunter"
        self.btnSelectHunter = self.panelHunter + "/btnSelectHunter"
        self.panelMage = self.panelSelect + "/panelMage"
        self.btnSelectMage = self.panelMage + "/btnSelectMage"

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.AddTouchEventHandler(self.btnSelectHunter, self.OnBtnSelectHunter, {"isSwallow": True})
        self.AddTouchEventHandler(self.btnSelectMage, self.OnBtnSelectMage, {"isSwallow": True})
        pass

    # 界面的一些初始化操作
    def Init(self, system):
        self.system = system

    def OnBtnSelectHunter(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            # 监听到选择猎人并发送广播
            eventArgs = self.system.CreateEventData()
            eventArgs["playerId"] = self.playerId
            eventArgs["jobs"] = modConfig.JobsHunter
            self.system.NotifyToServer(modConfig.JobsSelectEvent, eventArgs)
            self.CloneScreen()

    def OnBtnSelectMage(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            # 监听到选择猎人并发送广播
            eventArgs = self.system.CreateEventData()
            eventArgs["playerId"] = self.playerId
            eventArgs["jobs"] = modConfig.JobsMage
            self.system.NotifyToServer(modConfig.JobsSelectEvent, eventArgs)
            # self.CloneScreen()

    def CloneScreen(self):
        self.SetVisible("/", False)
