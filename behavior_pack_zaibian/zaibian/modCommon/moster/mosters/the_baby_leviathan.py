# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class the_baby_leviathan(public):
    def __init__(self,args):
        super(the_baby_leviathan,self).__init__(args)
        
    def use(self):
        data={
            "skill_use1":20,
        }
        skill_name=self.random_skill(data)
        self.skill_jn(skill_name,[4.5],[3])

    def skill_1(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        def f(args):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(self.entityId, 20, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(self.entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if comp.CanSee(self.entityId,i,20.0,True,90.0,90.0):
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(3, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
        for i in range(15):
            self.time_J(0.1*i,f,None)

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

    def use_attack(self,args=None):
        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 4, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,3.0,True,180.0,180.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(4, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
        self.ack_time(1,0.4,f)


    def stop(self):
        pass