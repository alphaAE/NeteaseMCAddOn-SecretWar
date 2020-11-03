# -*- coding: utf-8 -*-

# 获取客户端Component的基类
import client.extraClientApi as clientApi
ComponentCls = clientApi.GetComponentCls()

# Component要继承于基类才能生效
class ShootComponentClient(ComponentCls):
    def __init__(self, entityId):
        ComponentCls.__init__(self, entityId)
        # 这里设置了一个开关来开关更新射击
        self.mShoot = False

    def GetShoot(self):
        return self.mShoot

    def SetShoot(self, val):
        self.mShoot = bool(val)
