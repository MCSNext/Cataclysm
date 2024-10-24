# -*- coding: utf-8 -*-

from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class bone_fracture(Public):

    def __init__(self,entityId):
        super(bone_fracture, self).__init__(entityId)
        self.tick_=0
        self.xg=0.02

        self.dq=0


    def status_start(self,cs):
        super(bone_fracture,self).status_start(cs)
        self.tick_=0
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", self.effectDuration, self.effectAmplifier, False)

    def status_end(self):
        super(bone_fracture,self).status_end()
        