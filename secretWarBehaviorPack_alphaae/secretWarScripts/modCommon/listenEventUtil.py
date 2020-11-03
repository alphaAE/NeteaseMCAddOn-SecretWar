# -*- coding: utf-8 -*-
# 监听与注销事件工具
from secretWarScripts.modCommon import modConfig


class ListenEventUtil:

    def __init__(self, api, system, mSelf):
        self.api = api
        self.system = system
        self.mSelf = mSelf

    # 事件监听
    # 简单化注册事件监听
    def LiteListenForEvent(self, eventName, callback):
        self.system.ListenForEvent(
            self.api.GetEngineNamespace(),
            self.api.GetEngineSystemName(),
            eventName,
            self.mSelf,
            callback
        )

    # 简单化列表注册事件监听
    def ListListenForEvent(self, eventAndCallbackList):
        if len(eventAndCallbackList):
            for item in eventAndCallbackList:
                self.LiteListenForEvent(item[0], item[1])

    # 简单化销毁事件监听
    def LiteUnListenForEvent(self, eventName, callback):
        self.system.UnListenForEvent(
            self.api.GetEngineNamespace(),
            self.api.GetEngineSystemName(),
            eventName,
            self.mSelf,
            callback
        )

    # 简单化列表销毁事件监听
    def ListUnListenForEvent(self, eventAndCallbackList):
        if len(eventAndCallbackList):
            for item in eventAndCallbackList:
                self.LiteUnListenForEvent(item[0], item[1])

    # 事件自定义监听
    # 简单化注册事件监听
    def LiteListenForUserEvent(self, eventName, callback):
        self.system.ListenForEvent(
            modConfig.ModName,
            modConfig.ServerSystemName,
            eventName,
            self.mSelf,
            callback
        )

    # 简单化列表注册事件监听
    def ListListenForUserEvent(self, eventAndCallbackList):
        if len(eventAndCallbackList):
            for item in eventAndCallbackList:
                self.LiteListenForUserEvent(item[0], item[1])

    # 简单化销毁事件监听
    def LiteUnListenForUserEvent(self, eventName, callback):
        self.system.UnListenForEvent(
            modConfig.ModName,
            modConfig.ServerSystemName,
            eventName,
            self.mSelf,
            callback
        )

    # 简单化列表销毁事件监听
    def ListUnListenForUserEvent(self, eventAndCallbackList):
        if len(eventAndCallbackList):
            for item in eventAndCallbackList:
                self.LiteUnListenForUserEvent(item[0], item[1])

    # 自定义事件
    # 列表定义自定义事件
    def ListDefineEvent(self, eventList):
        if len(eventList):
            for item in eventList:
                self.system.DefineEvent(item[0])

    # 列表销毁自定义事件
    def ListUnDefineEvent(self, eventList):
        if len(eventList):
            for item in eventList:
                self.system.UnDefineEvent(item[0])

    # 汇总
    def InitAll(self, eventList, eventAndCallbackList, userEventAndCallbackList):
        self.ListDefineEvent(eventList)
        self.ListListenForEvent(eventAndCallbackList)
        self.ListListenForUserEvent(userEventAndCallbackList)

    def DestroyAll(self, eventList, eventAndCallbackList, userEventAndCallbackList):
        self.ListUnDefineEvent(eventList)
        self.ListUnListenForEvent(eventAndCallbackList)
        self.ListUnListenForUserEvent(userEventAndCallbackList)
