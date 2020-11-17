# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import client.extraClientApi as clientApi
from secretWarScripts.modClient import logger
from secretWarScripts.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


# 所有的UI类需要继承自引擎的ScreenNode类
class StopGameScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()

        self.mainPanel = "/mainPanel"
        self.menuPanel = self.mainPanel + "/menuPanel"

        self.btnClose = self.menuPanel + "/btnClose"
        self.jobLabel = self.menuPanel + "/jobLabel"

        self.healthPanel = self.menuPanel + "/healthPanel"
        self.healthLable = self.healthPanel + "/healthLable"
        self.damagePanel = self.menuPanel + "/damagePanel"
        self.damageLabel = self.damagePanel + "/damageLabel"
        self.killMobNumPanel = self.menuPanel + "/killMobNumPanel"
        self.KillMobNumLabel = self.killMobNumPanel + "/KillMobNumLabel"

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.AddTouchEventHandler(self.btnClose, self.OnBtnClose, {"isSwallow": True})

    # 界面的一些初始化操作
    def Init(self, system, data):
        # print data
        self.system = system
        jobs = data.get("jobs", "无")
        playerKillMobNum = data.get("playerKillMobNum", "0")
        damage = data.get("damage", "0")
        health = data.get("health", "0")
        # 转化职业名称
        jobs = modConfig.JobsNameDict.get(jobs, "无")
        # 设置数值
        self.SetText(self.jobLabel, str(jobs))
        self.SetText(self.KillMobNumLabel, str(playerKillMobNum))
        self.SetText(self.damageLabel, str(damage))
        self.SetText(self.healthLable, str(health))

    # OnButton
    def OnBtnClose(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.SetRemove()

    # 定义功能封装
