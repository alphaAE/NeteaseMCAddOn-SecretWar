# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import client.extraClientApi as clientApi
from secretWarScripts.modClient import logger
from secretWarScripts.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


# 所有的UI类需要继承自引擎的ScreenNode类
class StartGameScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()

        self.mainPanel = "/mainPanel"
        self.btnStart = self.mainPanel + "/btnStart"

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.AddTouchEventHandler(self.btnStart, self.OnBtnStart, {"isSwallow": True})

    # 界面的一些初始化操作
    def Init(self, system):
        self.system = system

    # OnButton
    def OnBtnStart(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            eventArgs = self.system.CreateEventData()
            self.system.BroadcastEvent(modConfig.PlayerStartButton, eventArgs)
