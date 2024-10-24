# -*- coding:utf-8 -*-
import mod.server.extraServerApi as serverApi
from mod_effect_eF9xM9.modServer.manager import get_singleton,engineAPI
import mod_effect_eF9xM9.modCommon.modConfig as modConfig
import random,copy

levelId = serverApi.GetLevelId()
class lbBottle0(object):
    def __init__(self,server):
        self.server = server
        self.ListenEvent()



    def ListenEvent(self):
        # self.server.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnCarriedNewItemChangedServerEvent", self, self.OnCarriedNewItemChangedServerEvent)


        pass








