# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class coralssus(public):
    def __init__(self,args):
        super(coralssus,self).__init__(args)
        
    def use(self):
        data={
            "skill_use1":20,
        }
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        if entId!='-1':
            skill_name=self.random_skill(data)
            self.skill_jn(skill_name,[2],[0])
    def skill_1(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        if entId!='-1':
            def f1():
                comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                entityFootPos1 = comp.GetFootPos()
                x,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[2]-entityFootPos[2]
                comp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
                jl=self.calculate_distance(entityFootPos1,entityFootPos)
                if jl<8:
                    g=0.4
                else:
                    g=0.4+jl*0.5/20
                if jl<10:
                    jl=jl/2
                else:
                    xs=(18-jl) *0.5/8
                    xs=2+xs
                    jl=jl/xs
                comp.SetMotion((x/jl, g,z/jl))
                def f():
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
                    comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                    entityFootPos = comp.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateRide(self.entityId)
                    riders = comp.GetRiders()
                    for i in Entities:
                        if i==self.entityId or (riders and  i in riders[0]["entityId"]):
                            continue
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(random.randint(10,14), serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)
                        comp = serverApi.GetEngineCompFactory().CreatePos(i)
                        entityFootPos1 = comp.GetFootPos()
                        x,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[2]-entityFootPos[2]
                        comp = serverApi.GetEngineCompFactory().CreateAction(i)
                        comp.SetMobKnockback(x, z, 2, 0.7, 0.6)

                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(1.5,f) 
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.5,f1) 
        else:
            self.romve_skill("异常skill_1")
        pass
    def use_attack(self,args=None):
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 3, serverApi.GetMinecraftEnum().EntityType.Mob)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateRide(self.entityId)
        riders = comp.GetRiders()
        for i in Entities:
            if i==self.entityId or (riders and  i in riders[0]["entityId"]):
                continue


            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(random.randint(10,14), serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)

            comp = serverApi.GetEngineCompFactory().CreatePos(i)
            entityFootPos1 = comp.GetFootPos()
            x,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[2]-entityFootPos[2]
            comp = serverApi.GetEngineCompFactory().CreateAction(i)
            comp.SetMobKnockback(x, z, 1.8, 0.60, 0.6)


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