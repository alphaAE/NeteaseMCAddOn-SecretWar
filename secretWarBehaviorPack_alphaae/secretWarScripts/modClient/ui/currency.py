# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import client.extraClientApi as clientApi
from secretWarScripts.modClient import logger
from secretWarScripts.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


# 所有的UI类需要继承自引擎的ScreenNode类
class CurrencyScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()

        self.mainPanel = "/mainPanel"
        self.currencyPanel = self.mainPanel + "/currencyPanel"
        self.currencyImage = self.currencyPanel + "/currencyImage"
        self.currencyNumLabel = self.currencyPanel + "/currencyNumLabel"

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        # 配置初始金币数量
        text = str(-1)
        self.SetText(self.currencyNumLabel, text)
        # 配置金币图标
        imagePath = "textures/items/coin"
        self.SetSprite(self.currencyImage, imagePath)

    # 界面的一些初始化操作
    def Init(self, system):
        self.system = system

    def SetCurrency(self, Count):
        text = str(Count)
        self.SetText(self.currencyNumLabel, text)
