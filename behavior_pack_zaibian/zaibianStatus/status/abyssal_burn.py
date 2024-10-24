# -*- coding: utf-8 -*-

from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class abyssal_burn(Public):

    def __init__(self,entityId):
        super(abyssal_burn, self).__init__(entityId)
        self.tick_=0
  

    def status_start(self,cs):
        super(abyssal_burn,self).status_start(cs)
        self.tick_=0

    
    def kouxue(self):
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.Hurt(1, serverApi.GetMinecraftEnum().ActorDamageCause.Magic, None, None, False)
        
    def tick(self,sc=False):
        super(abyssal_burn,self).tick(sc)
        self.tick_+=1
        io=2-self.effectAmplifier*0.3
        if io<0.5:
            io=0.5
        if self.tick_>=io*30:
            self.tick_=0
            self.kouxue()
    def status_end(self):
        super(abyssal_burn,self).status_end()
