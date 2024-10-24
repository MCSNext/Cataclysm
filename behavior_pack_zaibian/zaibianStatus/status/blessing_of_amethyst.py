
from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class blessing_of_amethyst(Public):

    def __init__(self,entityId):
        super(blessing_of_amethyst, self).__init__(entityId)
        self.tick_=0
        self.effctname=["abyssal_fear","abyssal_burn","blindness"]
    def status_start(self,cs):
        super(blessing_of_amethyst,self).status_start(cs)
        self.serverapi.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "WillAddEffectServerEvent",self, self.WillAddEffectServerEvent)

        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        for i in self.effctname:
            res = comp.RemoveEffectFromEntity(i)

                
    def WillAddEffectServerEvent(self,args):
        entityId=args["entityId"]
        effectName=args["effectName"]
        if self.entityId==entityId and effectName in self.effctname:
            args['cancel']=True


    def status_end(self):
        super(blessing_of_amethyst,self).status_end()
        self.serverapi.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "WillAddEffectServerEvent",self, self.WillAddEffectServerEvent)

