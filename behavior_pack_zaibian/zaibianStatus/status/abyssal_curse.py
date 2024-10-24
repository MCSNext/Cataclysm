# -*- coding: utf-8 -*-

from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class abyssal_curse(Public):

    def __init__(self,entityId):
        super(abyssal_curse, self).__init__(entityId)
        self.tick_=0
        self.tick_tiem={0:3*30,1:1*30,2:0.7*30}

    def status_start(self,cs):
        super(abyssal_curse,self).status_start(cs)
        self.tick_=0

    
    def kouxue(self):
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.Hurt(1, serverApi.GetMinecraftEnum().ActorDamageCause.Magic, None, None, False)
    def tick(self,sc=False):
        super(abyssal_curse,self).tick(sc)
        self.tick_+=1
        if self.tick_>=self.tick_tiem.get(self.effectAmplifier,0.7*30):
            self.tick_=0
            self.kouxue()
    def status_end(self):
        super(abyssal_curse,self).status_end()
