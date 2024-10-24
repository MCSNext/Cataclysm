# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class deepling_priest(public):
    def __init__(self,args):
        super(deepling_priest,self).__init__(args)
        
    def use(self):
        data={
            "skill_use1":20,
        }
        skill_name=self.random_skill(data)
        self.skill_jn(skill_name,[3],[0])

    def skill_1(self):

        
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        def die():
            self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'key':'deepling_priest'})

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(self.entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                Family=comp.GetTypeFamily()
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)

                if Family and "coralssus" not in Family and "deepling" not in Family :
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(8, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("blindness", 3, 0, True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(0.5,die) 
    def start_death(self):
        time=0.1
        def die():
            self.serverapi.die_list[1].append(self.entityId)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.KillEntity(self.entityId)
            self.serverapi.die_list[1].remove(self.entityId)
            self.serverapi.die_list[0].remove(self.entityId)
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 

    def stop(self):
        pass