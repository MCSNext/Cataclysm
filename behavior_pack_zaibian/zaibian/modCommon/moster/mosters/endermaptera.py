from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class endermaptera(public):
    def __init__(self,args):
        super(endermaptera,self).__init__(args)

    
    def start_death(self):
        time=0.5
        def die():
            self.die_wp()
       

            

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 