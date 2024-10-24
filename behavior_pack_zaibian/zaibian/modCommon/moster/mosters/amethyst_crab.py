# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class amethyst_crab(public):
    def __init__(self,args):
        super(amethyst_crab,self).__init__(args)
        
    def use(self):
   
        # comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        # entityFootPos = comp.GetFootPos()
        # comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        # entId=comp.GetAttackTarget()
        # comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        # entityFootPos1 = comp.GetFootPos()
        # pl=self.calculate_distance(entityFootPos,entityFootPos1)
     
            
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        if   pl<6.5:
            data={

            "skill_use1":3, #3
            "skill_use2":3,  #3
            "skill_use3":2,  ##2
            "skill_use4":2,   #2
            }
            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            self.rot = rotComp.GetRot()
            skill_name=self.random_skill(data)
            # skill_name="skill_use4" #todo
            
            self.skill_jn(skill_name,[2,1.5,4,3],[1.1,0.9,1.1,0])
   
    def skill_1(self):
        '''巨钳横扫 crab_bite'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 4, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,5.0,True,140.0,240.0) :
                continue
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(random.randint(15,15), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
    
    def skill_2(self):
        '''巨钳猛击 monstrosityland'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        for i in Entities:
            if i==self.entityId  :
                continue
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(random.randint(16,16), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)
            comp = serverApi.GetEngineCompFactory().CreatePos(i)
            entityFootPos1 = comp.GetFootPos()
            
            comp = serverApi.GetEngineCompFactory().CreateAction(i)
            comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1.5, 0.4, 0.4)

    def skill_3(self):
        '''巨钳冲击波 monstrosityland'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)

            for i in Entities:
                if i==self.entityId  :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(16,16), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1.5, 0.4, 0.4)

        for i in range(3):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(1*i,f) 


    def skill_4(self):
        '''防御'''
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        def f():
            comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
            comp.ImmuneDamage(False)
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            rot = rotComp.GetRot()
            for i1 in range(0,361,15):
                x,y,z= serverApi.GetDirFromRot((rot[0],rot[1]+i1))
                pos=(entityFootPos[0]+x*2,entityFootPos[1]+0.5,entityFootPos[2]+z*2)
                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                param = {
                    'position': pos,
                    'direction': (x,0.23,z),
                }
                comp.CreateProjectileEntity(self.entityId, "zaibian:bloom_stone_pauldron_psw", param)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(2.3,f) 

    def start_death(self):
        time=3+1.5
        def die():
            self.die_wp()
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 
    def stop(self):
        pass

  