
from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

class blazing_brand(Public):

    def __init__(self,entityId):
        super(blazing_brand, self).__init__(entityId)
        self.tick_=0

    def status_start(self,cs):
        super(blazing_brand,self).status_start(cs)
        self.serverapi.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ActuallyHurtServerEvent",self, self.ActuallyHurtServerEvent)
 
        
    def ActuallyHurtServerEvent(self,args):
        entityId=args["entityId"]
        if self.entityId==entityId and args["cause"]=="entity_attack":
            args["damage"]=int(args["damage"]*(1+self.effectAmplifier/10+0.1))




    def status_end(self):
        super(blazing_brand,self).status_end()
        self.serverapi.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ActuallyHurtServerEvent",self, self.ActuallyHurtServerEvent)

