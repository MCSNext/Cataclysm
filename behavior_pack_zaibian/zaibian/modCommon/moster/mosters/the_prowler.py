# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
from common.utils.mcmath import Vector3


compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class the_prowler(public):
    def __init__(self,args):
        super(the_prowler,self).__init__(args)
        
    def use(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)

        if   pl<4:
            data={
            "skill_use1":20,
            }
        elif pl>4:
            data={
                "skill_use2":20,
            }

        skill_name=self.random_skill(data)
        self.skill_jn(skill_name,[3.6,2.5],[0.9,1.5])

    def skill_1(self):
        pass
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        def qf():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 3, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,4,True,240.0,240.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(4,4), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)

                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 0.1, 0.1, 0.1)

      
        for i in range(15):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(i*0.15,qf) 

        

    def skill_2(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]))
        vq2 = Vector3(x,0,z).Normalized()*0.5
        vq1 = Vector3(z,0,-x).Normalized()*1.2
        vq3 = Vector3(entityFootPos[0],entityFootPos[1]+2,entityFootPos[2])

        o=tuple(vq2+vq1+vq3)
        g=[0.4,0,-0.4]
        def f(k):
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            entId=comp.GetAttackTarget()
            if entId and entId!="-1":
                pos=(o[0],o[1]+g[k],+o[2])
                param = {
                'position': pos,
                "direction":(0,0,0),
                'targetId': entId,
                'power':1
                }
                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                id=comp.CreateProjectileEntity(self.entityId, "zaibian:the_harbinger_psw2", param)
        for i in range(3):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.33*i,f,i) 

            

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
            Entities=comp.GetEntitiesAroundByType(self.entityId, 3, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(16, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)

                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 0.2, 0.165, 0.165)

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        if   pl<3.2:
            self.ack_time(1.5,0.5,f)
        else:
            self.skill_jn("skill_use2",[5,2.5],[0.9,1.5])



    def stop(self):
        pass