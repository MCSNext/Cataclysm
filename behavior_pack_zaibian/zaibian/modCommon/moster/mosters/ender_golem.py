# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class ender_golem(public):
    def __init__(self,args):
        super(ender_golem,self).__init__(args)
        
    def use(self):
        data={
            "skill_use1":20,
            "skill_use2":12,

        }
        skill_name=self.random_skill(data)
        self.skill_jn(skill_name,[3,1.5],[1.1,1.2])

    def skill_1(self):
    
            
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        all_pos=[[0.0, 5.0], [0.78, 4.94], [1.55, 4.76], [2.27, 4.46], [2.94, 4.05], [3.54, 3.54], [4.05, 2.94], [4.46, 2.27], [4.76, 1.55], [4.94, 0.78], [5.0, 0.0], [4.94, -0.78], [4.76, -1.55], [4.46, -2.27], [4.05, -2.94], [3.54, -3.54], [2.94, -4.05], [2.27, -4.46], [1.55, -4.76], [0.78, -4.94], [0.0, -5.0], [-0.78, -4.94], [-1.55, -4.76], [-2.27, -4.46], [-2.94, -4.05], [-3.54, -3.54], [-4.05, -2.94], [-4.46, -2.27], [-4.76, -1.55], [-4.94, -0.78], [-5.0, -0.0], [-4.94, 0.78], [-4.76, 1.55], [-4.46, 2.27], [-4.05, 2.94], [-3.54, 3.54], [-2.94, 4.05], [-2.27, 4.46], [-1.55, 4.76], [-0.78, 4.94], [-0.0, 5.0]]
        blockPos=(entityFootPos[0],entityFootPos[1],entityFootPos[2])

        self.xlfangk(all_pos,blockPos)
        
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            if i==self.entityId:
                continue
            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
            comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
            comp = serverApi.GetEngineCompFactory().CreateAction(i)
            comp.SetMobKnockback(0, 0, 0, 0.7, 0.7)
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(random.randint(14,22), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateDimension(self.entityId)
        DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
        for i in range(-60,60,20):
            x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+i))
            for f in range(6):
                for f1 in range(4):
                    pos=(entityFootPos[0]+x*f,entityFootPos[1]+f1,entityFootPos[2]+z*f)
                    self.set_block(pos,DimensionId)


    def skill_2(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        def void_core_evocation(rot,pos,DimensionId):  #延迟放技能
            po=self.serverapi.CreateEngineEntityByTypeStr('zaibian:void_rune', pos, rot, DimensionId)
            comp = serverApi.GetEngineCompFactory().CreateModAttr(po)
            comp.SetAttr('zr', self.entityId)

        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
       
        comp = serverApi.GetEngineCompFactory().CreateDimension(self.entityId)
        DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
        for i1 in [-5,5]:
            for i in range(2,15):    #放置15个磨牙
                x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+i1))

                pos=(entityFootPos[0]+x*i,entityFootPos[1],entityFootPos[2]+z*i)
                comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                comp.AddTimer(0.1*i,void_core_evocation,rot,pos,DimensionId)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            if i==self.entityId:
                continue
            comp = serverApi.GetEngineCompFactory().CreateAction(i)
            comp.SetMobKnockback(0, 0, 0, 0.7, 0.7)
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(random.randint(20,40), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

    def start_death(self):
        time=1.5+1
        def die():
            self.die_wp()

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 

    def use_attack(self,args=None):
        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 7, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,6.5,True,60.0,240.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(8, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
                break
        self.ack_time(1.25,1.25*0.45,f)


    def stop(self):
        pass