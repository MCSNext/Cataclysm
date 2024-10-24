# -*- coding: utf-8 -*-

from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class stun(Public):

    def __init__(self,entityId):
        super(stun, self).__init__(entityId)
        self.tick_=0


    def status_start(self,cs):
        super(stun,self).status_start(cs)
        self.xianyun()
        comp = serverApi.GetEngineCompFactory().CreateCommand(serverApi.GetLevelId())
        comp.SetCommand("/camerashake add @s 0.1 {} rotational".format(self.effectDuration),self.entityId)
    
    def xianyun(self):
        if self.entityId not in serverApi.GetPlayerList():
            comp = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
            comp.SetBlockControlAi(False, True)
        if  clientApi.GetLocalPlayerId() ==self.entityId:
            comp = clientApi.GetEngineCompFactory().CreateOperation(clientApi.GetLevelId())
            comp.SetCanAttack(False)
            comp.SetCanInair(False)
            comp.SetCanJump(False)
            comp.SetCanMove(False)
    def status_end(self):
        super(stun,self).status_end()
        if self.entityId not  in serverApi.GetPlayerList():
            comp = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
            comp.SetBlockControlAi(True, True)

        if  clientApi.GetLocalPlayerId() ==self.entityId:
            comp = clientApi.GetEngineCompFactory().CreateOperation(clientApi.GetLevelId())
            comp.SetCanAttack(True)
            comp.SetCanInair(True)
            comp.SetCanJump(True)
            comp.SetCanMove(True)