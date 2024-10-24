# -*- coding: utf-8 -*-

from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class monstrous(Public):
    def __init__(self,entityId):
        super(monstrous, self).__init__(entityId)
        self.tick_=0

    def status_start(self,cs):
        super(monstrous,self).status_start(cs)
        self.tick_=0
    
    def huifu(self):
        comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
        # 如果设置的值超过属性当前的最大值，需要先扩充该属性的最大值，否则不生效。
        health=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, health+self.effectAmplifier)
        
    def tick(self,sc=False):
        super(monstrous,self).tick(sc)
        self.tick_+=1
        if self.tick_>=40:
            self.tick_=0
            self.huifu()



    def status_end(self):
        super(monstrous,self).status_end()
