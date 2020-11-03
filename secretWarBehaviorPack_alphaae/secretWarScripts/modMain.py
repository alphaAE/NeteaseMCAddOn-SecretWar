# -*- coding: utf-8 -*-

from common.mod import Mod
import client.extraClientApi as clientApi
import server.extraServerApi as serverApi

from secretWarScripts.modCommon import modConfig
from secretWarScripts import logger


@Mod.Binding(name=modConfig.ModName, version=modConfig.ModVersion)
class HugoFpsMod(object):

    def __init__(self):
        logger.info("===== init mod =====")

    @Mod.InitServer()
    def HugoFpsServerInit(self):
        # logger.info("===== init server =====")
        serverApi.RegisterSystem(
            modConfig.ModName,
            modConfig.ServerSystemName,
            modConfig.ServerSystemClsPath
        )

    @Mod.DestroyServer()
    def HugoFpsServerDestroy(self):
        # logger.info("===== destroy server =====")
        pass

    @Mod.InitClient()
    def HugoFpsClientInit(self):
        # logger.info("===== init client =====")
        # 注册一个自定义的客户端Component
        clientApi.RegisterComponent(
            modConfig.ModName,
            modConfig.ClientShootComponent,
            modConfig.ClientShootCompClsPath
        )
        clientApi.RegisterSystem(
            modConfig.ModName,
            modConfig.ClientSystemName,
            modConfig.ClientSystemClsPath
        )

    @Mod.DestroyClient()
    def HugoFpsClientDestroy(self):
        # logger.info("===== destroy client =====")
        pass
