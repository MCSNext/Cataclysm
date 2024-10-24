
from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class abyssal_fear(Public):

    def __init__(self,entityId):
        super(abyssal_fear, self).__init__(entityId)
        self.tick_=0

    def status_start(self,cs):
        super(abyssal_fear,self).status_start(cs)
        self.serverapi.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "HealthChangeBeforeServerEvent",self, self.HealthChangeBeforeServerEvent)
 
        
    def HealthChangeBeforeServerEvent(self,args):
        entityId=args["entityId"]
        from1=args["from"]
        to=args["to"]
        if self.entityId==entityId and from1-to<0:
            args["cancel"]=True




    def status_end(self):
        super(abyssal_fear,self).status_end()
        self.serverapi.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "HealthChangeBeforeServerEvent",self, self.HealthChangeBeforeServerEvent)

