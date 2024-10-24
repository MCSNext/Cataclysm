# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()
from mod.common.utils.mcmath import Vector3
class ancient_remnant(public):
    def __init__(self,args):
        super(ancient_remnant,self).__init__(args)
        self.st=True
    def use(self):
 
        
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        g=entityFootPos1[1]-entityFootPos[1]
        if   pl>25:
            return
        if not self.stage:
            self.jl_list={"skill_use1":[[0,10,5],3],"skill_use2":[[0,10,5],3],"skill_use3":[[0,10,5],1],
        "skill_use4":[[0,18,5],3],"skill_use5":[[12,25,5],3],"skill_use6":[[0,10,5],3]
        }
        else:
            self.jl_list={"skill_use7":[[0,10,5],3],"skill_use2":[[0,10,5],3],"skill_use3":[[0,10,5],1],
        "skill_use4":[[0,18,3],2],"skill_use5":[[12,25,5],3],"skill_use6":[[0,10,5],3]
            }
        data=self.Get_Use_Skill_Name(pl,g)
        if data:
            skill_name=self.random_skill(data)
            # skill_name="skill_use4" #TODO
            self.skill_jn(skill_name,[2,4.75 ,3.5,4,8,2.5,3],[0,0,2.5,1.5,3,0.92,0])
    def skill_6(self):
        '''甩尾横扫'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 8, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,8,True,180.0,240.0) :
                continue
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(27, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

    def skill_5(self):
        '''冲撞'''
        print '冲撞'
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)

        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()

        if entityFootPos1:
            def func(k):
                if k>=30:
                    return
                
                motionComp.SetMotion((x, -0.2,z))

                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                entityFootPos = comp.GetFootPos()
                pos=entityFootPos[0]+x,entityFootPos[1],entityFootPos[2]+z
                pos1=entityFootPos[0]+x,entityFootPos[1]+1,entityFootPos[2]+z

                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                blockDict = comp.GetBlockNew(pos, dimensionId)
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                blockDict1 = comp.GetBlockNew(pos1, dimensionId)
                if blockDict["name"]   in ["minecraft:air","minecraft:water","minecraft:flowing_water"] and blockDict1["name"]   in ["minecraft:air","minecraft:water","minecraft:flowing_water"]:
                    self.time_J(0.1,func,k+1)
                else:
                    self.romve_skill("异常skill_5")

                rot = serverApi.GetRotFromDir((x, 0, z))
                comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
                comp.SetRot(rot)
              
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                Entities=comp.GetEntitiesAround(self.entityId, 3,   { "test": "is_family", "subject": "other", "operator":"!=", "value": "desert" })
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)


            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
            x,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[2]-entityFootPos[2]
            pl=self.calculate_distance(entityFootPos,entityFootPos1)
            x=x/pl
            z=z/pl

            
            func(0)
                
     
        if entityFootPos and entityFootPos1:
            pass
        else:
            self.romve_skill("异常skill_5")

    def skill_4(self):
        '''方块砸地'''
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()


        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        x, y, z = serverApi.GetDirFromRot(rot)

        for i in range(0,25,2):
            pos=entityFootPos[0]+x*i, entityFootPos[1]+4, entityFootPos[2]+z*i
            blockDict = {
                'name': 'zaibian:ancient_desert_stele1',
                'aux': 0
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict, 2, dimensionId)

        
        for i in [5,9,13]:
            result = self.calculate_circle_points(i)
            for x,z  in result:
                pos=entityFootPos[0]+x, entityFootPos[1]+4, entityFootPos[2]+z
                blockDict = {
                'name': 'zaibian:ancient_desert_stele1',
                'aux': 0
                }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 2, dimensionId)

            
 
    

        

    def skill_7(self):
        '''击飞方块2'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        playerRot = compFactory.CreateRot(self.entityId).GetRot()
        def gongji():
            def gongji1(k,list_):
                
                self.xlfangk(list_,entityFootPos)
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                Entities=comp.GetEntitiesAround(self.entityId, (k+1)*3,  { "test": "is_family", "subject": "other", "operator":"!=", "value": "desert" })
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    
                    pl=self.calculate_distance(entityFootPos,entityFootPos1)
                    if self.test_pos_is_in_sector(entityFootPos,60,playerRot[1],entityFootPos1) and (k)*3<=pl<=(k+1)*3:
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(26, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

            for i in range(6):
                list_=self.getArcBlocksAroundEntityWithRadius(self.entityId,(i+1)*3,50,i*3,1000)
                self.time_J(0.4*i,gongji1,i,list_)
        self.time_J(0.75,gongji)
        self.time_J(2.25,gongji)




    def skill_1(self):
        '''击飞方块'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        playerRot = compFactory.CreateRot(self.entityId).GetRot()
        def gongji():
            def gongji1(k,list_):
                
                self.xlfangk(list_,entityFootPos)
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                Entities=comp.GetEntitiesAround(self.entityId, (k+1)*3,  { "test": "is_family", "subject": "other", "operator":"!=", "value": "desert" })
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    
                    pl=self.calculate_distance(entityFootPos,entityFootPos1)
                    if self.test_pos_is_in_sector(entityFootPos,60,playerRot[1],entityFootPos1) and (k)*3<=pl<=(k+1)*3:
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(26, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

            for i in range(6):
                list_=self.getArcBlocksAroundEntityWithRadius(self.entityId,(i+1)*3,50,i*3,1000)
                self.time_J(0.4*i,gongji1,i,list_)
        self.time_J(0.75,gongji)


    def skill_3(self):
        '''龙卷风'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        oi=[]
        oi.append(self.serverapi.CreateEngineEntityByTypeStr('zaibian:sandstorm', (entityFootPos[0]+5,entityFootPos[1],entityFootPos[2]+5), (0, 0), dimensionId))
        oi.append(self.serverapi.CreateEngineEntityByTypeStr('zaibian:sandstorm', (entityFootPos[0]-5,entityFootPos[1],entityFootPos[2]-5), (0, 0), dimensionId))
        oi.append(self.serverapi.CreateEngineEntityByTypeStr('zaibian:sandstorm', (entityFootPos[0]+5,entityFootPos[1],entityFootPos[2]-5), (0, 0), dimensionId))
        oi.append(self.serverapi.CreateEngineEntityByTypeStr('zaibian:sandstorm', (entityFootPos[0]-5,entityFootPos[1],entityFootPos[2]+5), (0, 0), dimensionId))

        for i in oi:
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
            axis=(0, 1, 0)
            mID = motionComp.AddEntityAroundEntityMotion(self.entityId, 1.0, axis, lockDir=False, stopRad=0, radius=10.0)
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
            motionComp.StartEntityMotion(mID)
    def skill_2(self):
        '''尾巴打地'''
        time=[1.88,2.63,3.38]
        def gongji():
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            Entities=comp.GetEntitiesAround(self.entityId, 8,   { "test": "is_family", "subject": "other", "operator":"!=", "value": "desert" })
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,9,True,180.0,240.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(27, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

        for i in time:
            self.time_J(i,gongji)
                        
                        
        
    def use_attack(self,args=None):

        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i !=self.entityId:
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(27, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
        self.ack_time(2,1,f)
        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)

        print '攻击'

    def use_stage(self):
        self.use_stage_tz(3)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        self.time_J(3,comp.ImmuneDamage,False)
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        self.time_J(3,comp1.SetBlockControlAi,True)


        
        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 12, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i==self.entityId :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/camerashake add @s 0.2 2 rotational",i)

            comp = serverApi.GetEngineCompFactory().CreateEntityEvent(self.entityId)

            comp.TriggerCustomEvent(self.entityId,"star_use")

        self.time_J(1.8,f)
        comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(self.entityId)

        self.time_J(0,comp.SetMarkVariant,1000)


        


    def start_death(self):
        self.start_die()
        time=7
        def die():
            self.die_wp()
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 
        
    def stop(self):
        pass# -*- coding: utf-8 -*-

