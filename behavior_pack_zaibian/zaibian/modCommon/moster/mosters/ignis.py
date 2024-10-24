# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random,math
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()
from mod.common.utils.mcmath import Vector3

class ignis(public):
    def __init__(self,args):
        super(ignis,self).__init__(args)
        self.skill_2_jn=False
    
    def act_pa(self):
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 7, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,6.5,True,180.0,240.0) :
                continue
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            if self.stage==3:
                comp.Hurt(random.randint(18,18), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
            else:
                comp.Hurt(random.randint(14,14), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
        



    def use(self):

        self.skill_2_jn=False
        
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        g=entityFootPos1[1]-entityFootPos[1]
        if   pl>24:
            return
        if  self.stage==3:
            self.jl_list={"skill_use2":[[0,7,4],3],"skill_use3":[[8,18,4],4],
            "skill_use4":[[6,20,24],1],   "skill_use12":[[6,20,24],1],
         "skill_use5":[[0,13,12],2],"skill_use6":[[4,9,4],5],"skill_use7":[[0,11,4],1],"skill_use8":[[3,11,4],3],
         "skill_use10":[[0,7,4],3],"skill_use11":[[0,8,4],2],"skill_use13":[[0,6,4],1],"skill_use14":[[0,7,4],4],"skill_use15":[[0,7,4],4],"skill_use16":[[6,15,8],3]
        }
        elif  self.stage==2:
            self.jl_list={"skill_use1":[[0,7,4],4],"skill_use2":[[0,7,4],3],"skill_use3":[[8,18,4],4],"skill_use4":[[6,20,24],2],
            "skill_use6":[[4,9,4],5],"skill_use7":[[0,11,4],1],"skill_use8":[[3,11,4],3], "skill_use12":[[6,20,24],1],
            "skill_use9":[[0,6,4],4],"skill_use11":[[0,8,4],2],"skill_use13":[[0,6,4],1],"skill_use14":[[0,7,4],4],"skill_use15":[[0,7,4],4],"skill_use16":[[6,15,4],3]
            }

        else:
            self.jl_list={"skill_use1":[[0,7,4],4],"skill_use2":[[0,7,4],3],"skill_use3":[[8,18,4],4],"skill_use4":[[6,20,24],2],
            "skill_use6":[[4,9,4],5],"skill_use7":[[0,11,4],1],"skill_use8":[[3,11,4],3], "skill_use12":[[6,20,24],1],"skill_use14":[[0,7,4],4],
            "skill_use9":[[0,6,4],4],"skill_use11":[[0,8,4],2],"skill_use13":[[0,6,4],1],"skill_use15":[[0,7,4],2],"skill_use16":[[6,15,8],3]
            }
        data=self.Get_Use_Skill_Name(pl,g)
        if data:
            skill_name=self.random_skill(data)
            # skill_name="skill_use1" #todo
            # print '技能',skill_name
            self.skill_jn_use(skill_name)

            
    
    def skill_jn_use(self,skill_name):
        self.skill_jn(skill_name,[3.9,
                                      2.25,
                                      3.5,
                                      3.33,
                                      4,
                                      4,
                                      5.5
                                      ,2.25
                                      ,4,
                                      11,
                                      2.5,
                                      3,
                                      2,
                                      2.5,4,12],[2,1,1,0.5,0,0,0,1,1.1,0,0,0.5,1,1.5,0,1.5])

    def OnGroundServerEvent(self,args):
        id=args["id"]
        if id == self.entityId:
         
            comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
            comp1.SetBlockControlAi(False, False)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId   :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(20,20), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
    
            
            self.serverapi.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnGroundServerEvent", self,self.OnGroundServerEvent)
            self.time_J(3.98,self.romve_skill,"异常skill_16")
            dimensionComp = compFactory.CreateDimension(self.entityId)
            dimensionId = dimensionComp.GetEntityDimensionId()
      
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            def f2(st):
                def fo(l):
                    all_pos=[]
                    for i in range(15):
                        if random.randint(0,1)==1:
                            x=random.uniform(st[l][0],st[l][1])
                        else:
                            x=random.uniform(-st[l][1],st[l][0])
                        if random.randint(0,1)==1:
                            z=random.uniform(st[l][0],st[l][1])
                        else:
                            z=random.uniform(-st[l][1],st[l][0])
                        all_pos.append([x,z])
                    self.xlfangk(all_pos,entityFootPos)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-st[l][1],entityFootPos[1]-2,entityFootPos[2]-st[l][1]), (entityFootPos[0]+st[l][1],entityFootPos[1]+2,entityFootPos[2]+st[l][1]), dimensionId)
                    for i in Entities:
                        
                        if i==self.entityId:
                            continue
                        comp = serverApi.GetEngineCompFactory().CreatePos(i)
                        entityFootPos1 = comp.GetFootPos()
                        pl=self.calculate_distance(entityFootPos,entityFootPos1)
                        if st[l][0]<pl <st[l][1]:
                            pass
                        else:
                            continue
                        comp = serverApi.GetEngineCompFactory().CreateAction(i)
                        x,z=entityFootPos[0]-entityFootPos1[0], entityFootPos[2]-entityFootPos1[2]
                        if abs(x)>abs(z):
                            sh=15*((10-abs(x))/10)
                        else:
                            sh=15*((10-abs(z))/10)
                        comp.SetMobKnockback(0,0, 0, 0.2, 0.2)
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        # comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                        comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                        comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
                    

                for i in range(5):
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(i*0.2,fo,i) 
                
                    

            k=0
            for i in [0,2.5]:
                k+=1
                if k==2:
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(i,f2,[[13,16],[10,12.5],[7,9.5],[4,6.5],[0,3.5]][::-1]  )
                elif  k==1:
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(i,f2,[[13,16],[10,12.5],[7,9.5],[4,6.5],[0,3.5]]  )


            def fun():
                a=[]
                rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
                rot = rotComp.GetRot()
                entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(self.entityId)
                bianti=entitycomp.GetExtraData("stage")
                for i in range(3):
                    ai=[90,0,-90]
                    bi=[2,0,2]
                    gi=[4.5,5,4.5]
                    rot1=(rot[0],rot[1]+ai[i])
                    x, y, z = serverApi.GetDirFromRot(rot1)
                    param = {
                        'position': (entityFootPos[0],entityFootPos[1],entityFootPos[2]),
                        'direction': (0,0,0),
                        'power': 0,
                        'gravity':0
                        }
                    comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                    id=comp.CreateProjectileEntity(self.entityId, "zaibian:ignis_psw", param)
                    if i==2:
                        comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                        comp.TriggerCustomEvent(id, "minecraft:mark_v")
                        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(id)
                        entitycomp.SetExtraData("teshu", True) 
                    elif bianti !=None:
                        comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                        comp.TriggerCustomEvent(id, "minecraft:mark_v1")
                    comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
                    target = (entityFootPos[0]+x*bi[i],entityFootPos[1]+gi[i],entityFootPos[2]+z*bi[i])
                    mID = motionComp.AddEntityTrackMotion(target, 0.7, startPos=None, isLoop=False, useVelocityDir=True, ease = serverApi.GetMinecraftEnum().TimeEaseType.linear)
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
                    motionComp.StartEntityMotion(mID)
                    a.append(id)
                
                def f1(i):
                    comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
                    entId=comp.GetAttackTarget()
                    if entId:
                        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                        entityFootPos1 = comp.GetFootPos()
                        if entityFootPos1 and entityFootPos:
                            entityFootPos1 = entityFootPos1[0],entityFootPos1[1]+0.7,entityFootPos1[2]
                            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(i)
                            teshu=entitycomp.GetExtraData("teshu") 
                            if teshu:
                                sj=0.7
                            else:
                                sj=0.69
                            if sj==0.7:
                                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                                entityFootPos2 = comp.GetFootPos()
                                self.serverapi.DestroyEntity(i)
                                param = {
                                    'position': entityFootPos2,
                                    'direction': (0,0,0),
                                    'power': 0,
                                    'gravity':0
                                    }
                                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                                id=comp.CreateProjectileEntity(self.entityId, "zaibian:ignis_psw1", param)
                                comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                                comp.TriggerCustomEvent(id, "minecraft:mark_v")
                                entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(id)
                                entitycomp.SetExtraData("teshu", True) 
                                i=id          
                            comp = serverApi.GetEngineCompFactory().CreatePos(i)
                            entityFootPos2 = comp.GetFootPos()
                            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                            from mod.common.utils.mcmath import Vector3
                            a=Vector3(entityFootPos1[0]-entityFootPos2[0],entityFootPos1[1]+1.4-entityFootPos2[1], entityFootPos1[2]-entityFootPos2[2])
                            a.Normalize()
                            motionComp.SetMotion(tuple(a*1.8))
                        else:
                            self.serverapi.DestroyEntity(i)
                    else:
                        self.serverapi.DestroyEntity(i)
                def f2():
                    for i1 in range(0,3):
                        self.time_J(0.6*i1,f1,a[i1])
                self.time_J(1.2,f2)
            self.time_J(2,fun)


    def xiaoweiyi(self):
        '''小位移'''
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos1 = comp.GetFootPos()
        if entityFootPos:
            a=Vector3(entityFootPos[0]-entityFootPos1[0],0,entityFootPos[2]-entityFootPos1[2])
            a.Normalize()
            x, y, z =tuple(a)
        else:
            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            rot = rotComp.GetRot()
            x, y, z = serverApi.GetDirFromRot(rot)
        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
        motionComp.SetMotion((x * 2, 0 * 2, z * 2))

    def skill_16(self):
        '''璀璨火球加璀璨星波'''

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        a=[]
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()

        
        

        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(self.entityId)
        bianti=entitycomp.GetExtraData("stage")
        rot1=(rot[0],rot[1])
        x_, y_, z_ = serverApi.GetDirFromRot(rot1)
        for i in range(3):
            ai=[90,0,-90]
            bi=[0.8,0,0.8]
            gi=[5,3.5,2]
            rot1=(rot[0],rot[1]+ai[i])
            x, y, z = serverApi.GetDirFromRot(rot1)
            param = {
                'position': (entityFootPos[0]+x*bi[i]+x_*3,entityFootPos[1]+gi[i],entityFootPos[2]+z*bi[i]+z_*3),
                'direction': (0,0,0),
                'power': 0,
                'gravity':0
                }
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            id=comp.CreateProjectileEntity(self.entityId, "zaibian:ignis_psw", param)
            if bianti !=None:
                comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                comp.TriggerCustomEvent(id, "minecraft:mark_v1")
            comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
            a.append(id)

        def f1(i):
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            entId=comp.GetAttackTarget()
            if entId:
                comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                entityFootPos1 = comp.GetFootPos()
                if entityFootPos1 and entityFootPos:
                    entityFootPos1 = entityFootPos1[0],entityFootPos1[1]+0.7,entityFootPos1[2]
                    entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(i)
                    teshu=entitycomp.GetExtraData("teshu") 
                    if teshu:
                        sj=0.7
                    else:
                        sj=0.69
                    if sj==0.7:
                        comp = serverApi.GetEngineCompFactory().CreatePos(i)
                        entityFootPos2 = comp.GetFootPos()
                        self.serverapi.DestroyEntity(i)
                        param = {
                            'position': entityFootPos2,
                            'direction': (0,0,0),
                            'power': 0,
                            'gravity':0
                            }
                        comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                        id=comp.CreateProjectileEntity(self.entityId, "zaibian:ignis_psw1", param)
                        comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                        comp.TriggerCustomEvent(id, "minecraft:mark_v")
                        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(id)
                        entitycomp.SetExtraData("teshu", True) 
                        i=id          
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos2 = comp.GetFootPos()
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                    from mod.common.utils.mcmath import Vector3
                    a=Vector3(entityFootPos1[0]-entityFootPos2[0],entityFootPos1[1]+1.4-entityFootPos2[1], entityFootPos1[2]-entityFootPos2[2])
                    a.Normalize()
                    motionComp.SetMotion(tuple(a*1.8))
                else:
                    self.serverapi.DestroyEntity(i)
            else:
                self.serverapi.DestroyEntity(i)

        def f2():
            for i1 in range(0,3):
                self.time_J(0.0*i1,f1,a[i1])

        self.time_J(2.5,f2)
        def f3():
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            entId=comp.GetAttackTarget()
            comp = serverApi.GetEngineCompFactory().CreatePos(entId)
            entityFootPos_1 = comp.GetFootPos()
            if entityFootPos_1:
                comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
                comp1.SetBlockControlAi(True, False)
                s=self.tiaoyue(self.entityId,entityFootPos_1)
                self.serverapi.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnGroundServerEvent", self,self.OnGroundServerEvent)
            else:
                self.romve_skill("异常skill_16")

        self.time_J(3.5,f3)
        def f4():
            self.serverapi.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnGroundServerEvent", self,self.OnGroundServerEvent)
        self.time_J(10.5,f4)


        

    



    def skill_15(self):
        """烈焰斩击＋裂地击"""

        self.time_J(1.5,self.act_pa)


        def f():
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            def fo(l):
                r=[4,8,11,15,20,0][l]
                dr=[4,8,11,15,20,0][l-1]
                all_pos=self.getArcBlocksAroundEntityWithRadius(self.entityId,r,180,dr,15)
                self.xlfangk(all_pos,entityFootPos)
                dimensionComp = compFactory.CreateDimension(self.entityId)
                dimensionId = dimensionComp.GetEntityDimensionId()
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-r,entityFootPos[1]-2,entityFootPos[2]-r), (entityFootPos[0]+r,entityFootPos[1]+2,entityFootPos[2]+r), dimensionId)
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                    if i==self.entityId or not  comp.CanSee(self.entityId,i,r,True,180.0,180.0) :
                        continue
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    pl=self.calculate_distance(entityFootPos,entityFootPos1)
                    if dr<pl <r:
                        pass
                    else:
                        continue
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    pl=self.calculate_distance(entityFootPos,entityFootPos1)
                    if 10-pl<4:
                        sh=13
                    else:
                        sh=25*((10-pl)/10)
                    comp.SetMobKnockback(0,0, 0, 0.2, 0.2)
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            rot = rotComp.GetRot()
            for i in range(5):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(i*0.2,fo,i) 
        self.time_J(2.75,f)

    def skill_14(self):
        """烈焰斩击"""
        self.act_pa()
        if random.randint(1,2)==1:
            '''烈焰斩击+火焰上勾拳'''
            self.time_J(0.1,self.romve_skill,"组合:13")
            

    
    
    def skill_13(self):
        '''火焰上勾拳'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        x, y, z = serverApi.GetDirFromRot(rot)
        # motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
        # motionComp.SetMotion((x * 2, 0 * 2, z * 2))
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        self.chongcientity((entId,8),14,jl=0,stop_st=True)

        # def f(a):
        #     comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        #     entityFootPos = comp.GetFootPos()
        #     comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        #     Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
        #     for i in Entities:
        #         comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
        #         if i==self.entityId or not  comp.CanSee(self.entityId,i,6.5,True,180.0,240.0) :
        #             continue
        #         comp = serverApi.GetEngineCompFactory().CreateHurt(i)
        #         comp.Hurt(random.randint(14,14), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)
        #         comp = serverApi.GetEngineCompFactory().CreatePos(i)
        #         entityFootPos1 = comp.GetFootPos()
        #         comp = serverApi.GetEngineCompFactory().CreateAction(i)
        #         comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1.5, 0.8, 0.8)
        # self.time_J(0.2,f,None)
      



    def skill_12(self):
        '''烈焰火球'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        a=[]
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()

        for i in range(3):
            ai=[90,0,-90]
            bi=[1,0,1]
            gi=[4.8,5,4.8]
            rot1=(rot[0],rot[1]+ai[i])
            x, y, z = serverApi.GetDirFromRot(rot1)
            param = {
                'position': (entityFootPos[0]+x*bi[i],entityFootPos[1]+gi[i],entityFootPos[2]+z*bi[i]),
                'direction': (0,0,0),
                'power': 0,
                'gravity':0

                }
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            id=comp.CreateProjectileEntity(self.entityId, "zaibian:ignis_psw", param)
            # comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
            # comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
            # comp.TriggerCustomEvent(id, "minecraft:mark_v1")
            a.append(id)

        def f2(args):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,5.0,True,140.0,240.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(18,18), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
            def f1(i):
                comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
                entId=comp.GetAttackTarget()
                if entId:
                    comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                    entityFootPos1 = comp.GetFootPos()
                    if entityFootPos1 and entityFootPos:
                        entityFootPos1 = entityFootPos1[0],entityFootPos1[1]+0.7,entityFootPos1[2]
                        sj=0.4
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                        mID = motionComp.AddEntityTrackMotion(entityFootPos1,sj, startPos=None, relativeCoord=False, isLoop=False, useVelocityDir=True)
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                        motionComp.StartEntityMotion(mID)
                        def fi(id):
                            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(id)
                            teshu=entitycomp.GetExtraData("teshu") 
                            comp = serverApi.GetEngineCompFactory().CreatePos(id)
                            entityFootPos = comp.GetFootPos()
                            entityFootPos=entityFootPos1
                            if entityFootPos:
                                comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
                                if not teshu :
                                    comp.CreateExplosion(entityFootPos,1,None,None,None,serverApi.GetPlayerList()[0])
                                else:
                                    def f3(a):
                                        self.serverapi.DestroyEntity(id)
                                    self.time_J(0.4,f3,None)
                                    return
                                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                                Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-5,entityFootPos[1]-5,entityFootPos[2]-5), (entityFootPos[0]+5,entityFootPos[1]+5,entityFootPos[2]+5), dimensionId)
                                self.serverapi.DestroyEntity(id)
                                if self.entityId in Entities :
                                    Entities.remove(self.entityId )
                                for i in Entities:
                                    if i!=self.entityId:
                                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                                        comp.Hurt(random.randint(15,16), serverApi.GetMinecraftEnum().ActorDamageCause.Projectile, self.entityId, None, True)
                        self.time_J(sj+0.1,fi,i)
                    else:
                        self.serverapi.DestroyEntity(i)
                else:
                    self.serverapi.DestroyEntity(i)
            for i1 in range(0,3):
                self.time_J(0.1*i1,f1,a[i1])
        self.time_J(0.7,f2,None)


    def skill_11(self):
        '''反击'''
        comp1 = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        def f():
            comp1.SetAttr("skill_11",True)
        def f1():
            comp1.SetAttr("skill_11",False)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(0.6,f) 
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(2.5,f1) 



    def skill_10(self):
        '''怒焰八连击'''

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 11, 1000, False)
        def gji(k,gj=18):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if k==10.4:
                    self.skill_8()
                if k not in [10.1,10.4]:
                    if i==self.entityId or not  comp.CanSee(self.entityId,i,6.0,True,180.0,240.0) :
                        continue
                else:
                    if i==self.entityId :
                        continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(gj,gj), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
                self.addeffect(i)
            
        time_lsit=[1.1,2.37,3.41,4.4 ,6.1,8.1,9.1,10.1,10.4]
        for i in time_lsit:
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
       
            comp.AddTimer(i,gji,i) 
        
        def wyi(k):
            if k==4:
                self.skill_13()
            else:
                self.xiaoweiyi()

        time_lsit=[1,2.33,3.33,4.25 ,6,8,9]
        for index,i in enumerate(time_lsit):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(i,wyi,index) 
            

    def skill_9(self):
        '''烈焰连斩'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 2, 100, False)
        def gji(k=0,gj=16):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            k+=1
            key=False
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,6.0,True,140.0,240.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(gj,gj), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
                self.addeffect(i)
                key=True
            self.xiaoweiyi()
            if ( k!=1 and  random.randint(0,1)==1) or k==3  :
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0.25,self.romve_skill,"异常skill_9") 
                return
            if k==2:
                gj=17
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.8,gji,k,gj) 
            comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
            res = comp.AddEffectToEntity("regeneration", 1, 2, False)
        gji()




    def skill_8(self):
        '''横扫'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 2, 100, False)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        def fo(l):
            r=[4,8,11,15,20,0][l]
            dr=[4,8,11,15,20,0][l-1]
            all_pos=self.getArcBlocksAroundEntityWithRadius(self.entityId,r,180,dr,15)
            self.xlfangk(all_pos,entityFootPos)
            dimensionComp = compFactory.CreateDimension(self.entityId)
            dimensionId = dimensionComp.GetEntityDimensionId()
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-r,entityFootPos[1]-2,entityFootPos[2]-r), (entityFootPos[0]+r,entityFootPos[1]+2,entityFootPos[2]+r), dimensionId)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,r,True,180.0,180.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                pl=self.calculate_distance(entityFootPos,entityFootPos1)
                if dr<pl <r:
                    pass
                else:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                pl=self.calculate_distance(entityFootPos,entityFootPos1)
                if 10-pl<4:
                    sh=13
                else:
                    sh=25*((10-pl)/10)
                comp.SetMobKnockback(0,0, 0, 0.2, 0.2)
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        for i in range(5):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(i*0.3,fo,i) 
            

    def skill_7(self):
        '''巨剑震地'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        def f1():
            def fo(l):
                st=[[0,3],[3,6],[7,10]]    
                all_pos=[]
                for i in range(15):
                    if random.randint(0,1)==1:
                        x=random.uniform(st[l][0],st[l][1])
                    else:
                        x=random.uniform(-st[l][1],st[l][0])
                    if random.randint(0,1)==1:
                        z=random.uniform(st[l][0],st[l][1])
                    else:
                        z=random.uniform(-st[l][1],st[l][0])
                    all_pos.append([x,z])
                self.xlfangk(all_pos,entityFootPos)
                
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-st[l][1],entityFootPos[1]-2,entityFootPos[2]-st[l][1]), (entityFootPos[0]+st[l][1],entityFootPos[1]+2,entityFootPos[2]+st[l][1]), dimensionId)
                for i in Entities:
                    if i==self.entityId:
                        continue
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    x,z=entityFootPos[0]-entityFootPos1[0], entityFootPos[2]-entityFootPos1[2]
                    if abs(x)>abs(z):
                        sh=15*((10-abs(x))/10)
                    else:
                        sh=15*((10-abs(z))/10)
                    comp.SetMobKnockback(0,0, 0, 0.2, 0.2)
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
            for i in range(2):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(i*0.3,fo,i) 
            
        def f2(st):
            def fo(l):
                all_pos=[]
                for i in range(15):
                    if random.randint(0,1)==1:
                        x=random.uniform(st[l][0],st[l][1])
                    else:
                        x=random.uniform(-st[l][1],st[l][0])
                    if random.randint(0,1)==1:
                        z=random.uniform(st[l][0],st[l][1])
                    else:
                        z=random.uniform(-st[l][1],st[l][0])
                    all_pos.append([x,z])
                self.xlfangk(all_pos,entityFootPos)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-st[l][1],entityFootPos[1]-2,entityFootPos[2]-st[l][1]), (entityFootPos[0]+st[l][1],entityFootPos[1]+2,entityFootPos[2]+st[l][1]), dimensionId)
                for i in Entities:
                    
                    if i==self.entityId:
                        continue
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    pl=self.calculate_distance(entityFootPos,entityFootPos1)
                    if st[l][0]<pl <st[l][1]:
                        pass
                    else:
                        continue
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    x,z=entityFootPos[0]-entityFootPos1[0], entityFootPos[2]-entityFootPos1[2]
                    if abs(x)>abs(z):
                        sh=15*((10-abs(x))/10)
                    else:
                        sh=15*((10-abs(z))/10)
                    comp.SetMobKnockback(0,0, 0, 0.2, 0.2)
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
                

            for i in range(5):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(i*0.2,fo,i) 

            
        k=0
        for i in [1.25,3,4.75]:
            k+=1
            if k==1:
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(i,f1) 
            elif k==2:
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(i,f2 ,[[13,16],[10,12.5],[7,9.5],[4,6.5],[0,3.5]]    )
            elif  k==3:
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(i,f2,[[13,16],[10,12.5],[7,9.5],[4,6.5],[0,3.5]][::-1]  )




    def skill_6(self):
        '''挑剑吸血'''
        
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 4, 100, False)
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        time=[]
        act_={}

        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        if entId:
            def st():
                comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
                comp1.SetBlockControlAi(True, False)
                def f2(act):
                    if not act:
                        for i in time:
                            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                            comp.CancelTimer(i)
                        self.romve_skill("异常skill_6")
                    else:
                        comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
                        dq_HEALTH=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                        comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,dq_HEALTH+2)
                        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
                        comp1.SetBlockControlAi(False, False)
                        act_.update(act)

                   
                if self.stage==3:
                    ak=17
                else:
                    ak=14
                self.chongcientity((entId,8),ak,jl=0,stop_st=True,call=f2,CanSee=True)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(1,st) 
            def f():
                comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
                comp1.SetBlockControlAi(False, False)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                entis=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                mbids=[]
                for i in entis:
                    if i==self.entityId or not  comp.CanSee(self.entityId,i,5.0,True,60.0,240.0) :
                        continue
                    mbids.append(i)

                mbids+=act_.keys()
                if mbids:
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
                    motionComp.ResetMotion()
                    x, y, z = serverApi.GetDirFromRot((0,rot[1]) )
                    comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                    entIdPos = comp.GetFootPos()
                    po=entIdPos[0]+x*5,entIdPos[1]+0,entIdPos[2]+z*5
            
                    for i in mbids:
                        comp = serverApi.GetEngineCompFactory().CreatePos(i)
                        comp.SetFootPos(po)
                        comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                        res = comp.AddEffectToEntity("stun", 2, 0, False)    
                    
                    
                    if not self.serverapi.data_init.get("cz_list"):
                        self.serverapi.data_init["cz_list"]=[]
                    self.serverapi.data_init["cz_list"].append(self.entityId)

                    def f2():
                        if  self.entityId in self.serverapi.data_init["cz_list"]:
                            self.serverapi.data_init["cz_list"].remove(self.entityId)
                        for mbid in mbids:
                            target = (0, 4, 0)
                            rot1 = (0, 0)
                            rot2 = (0, 360)
                            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(mbid)
                            if mbid in serverApi.GetPlayerList():
                                motions = motionComp.GetPlayerMotions()
                                for i in motions:
                                    motionComp.RemovePlayerMotion(i)
                                comp = serverApi.GetEngineCompFactory().CreateRide(mbid)
                                success = comp.StopEntityRiding()
                                mID = motionComp.AddPlayerTrackMotion(target, 0.9, startPos=None, relativeCoord=True, isLoop=False, targetRot=rot1, startRot=rot2, useVelocityDir=True)
                                motionComp.StartPlayerMotion(mID)
                                def f4():
                                    motions = motionComp.GetPlayerMotions()
                                    for i in motions:
                                        motionComp.RemovePlayerMotion(i)
                                    target = (0, 0, 0)
                                    mID = motionComp.AddPlayerTrackMotion(target, 1.0, startPos=None, relativeCoord=True, isLoop=False, targetRot=rot1, startRot=rot2, useVelocityDir=True)
                                    motionComp.StartPlayerMotion(mID)
                                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                                comp.AddTimer(1,f4) 

                            else:
                                motions = motionComp.GetEntityMotions()
                                for i in motions:
                                    motionComp.RemoveEntityMotion(i)
                                comp = serverApi.GetEngineCompFactory().CreateRide(mbid)
                                success = comp.StopEntityRiding()
                                mID = motionComp.AddEntityTrackMotion(target, 0.9, startPos=None, relativeCoord=True, isLoop=False, targetRot=rot1, startRot=rot2, useVelocityDir=True)
                                motionComp.StartEntityMotion(mID)

                                                
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(0.1,f2) 

            

                    def f3():
                        for mbid in mbids:
                            comp = serverApi.GetEngineCompFactory().CreateHurt(mbid)
                            comp.Hurt(random.randint(20,25), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                        comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
                        dq_HEALTH=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                        comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,dq_HEALTH+2)
                    

                    for i in range(5):
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.4*i,f3) 
            
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            time.append(comp.AddTimer(1.5,f) )
        else:
            self.romve_skill("异常skill_6")



    def skill_5(self):
        '''魂焰斩'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 4, 100, False)

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        self.serverapi.BroadcastToAllClient('zhaohuan',{'pos':(entityFootPos[0],entityFootPos[1]+0.2,entityFootPos[2]),'key':'ignis',"data":"skill5_0"})
        
                
        def f():
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            entId=comp.GetAttackTarget()

            if entId:
            
                comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                entIdPos = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                entityFootPos1 = comp.GetFootPos()
                x,y,z=entIdPos[0]-entityFootPos1[0],entityFootPos1[2],entIdPos[2]-entityFootPos1[2]
                dimensionComp = compFactory.CreateDimension(self.entityId)
                dimensionId = dimensionComp.GetEntityDimensionId()
                x,y,z=self.calculate_vector_player_to_entity(entityFootPos1,entIdPos)
                qx,qy,qz=x,y,z
                x,y,z=x*10,y,z*10
                p=[]
                for i1 in range(0,40,3):
                    x2,z2=qx*i1,qz*i1
                    x1,y1,z1=self.calculate_vector_rotation((qx,0,qz),90,0,0)
                    if -0.1<x1<0.1:
                        x1=0.5
                    elif -0.1<z1<0.1:
                        z1=0.5
                    for i2 in range(-13,13,2):
                        x3,z3=x1*i2,z1*i2
                        p.append([x2+x3,z2+z3])
                p = random.sample(p, min(len(p), 70))
                self.xlfangk(p,entityFootPos1)
                sh_pos=[]
                for i in range(1,5):
                    pos1=x*i*1+entityFootPos1[0],entityFootPos1[1]+0.1,z*i*1+entityFootPos1[2]
                    sh_pos.append(pos1)

                self.serverapi.BroadcastToAllClient('zhaohuan',{'pos':(x, y, z),
                                                                "entityFootPos1":sh_pos,
                                                                "entityFootPos":(entityFootPos[0],entityFootPos[1]+0.2,entityFootPos[2]),
                                                                'key':'ignis',"data":"skill5_1"})

                def f1(pos1,k):
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    lists=comp.GetEntitiesInSquareArea(None, (pos1[0]-3,pos1[1]-2,pos1[2]-3), (pos1[0]+3,pos1[1]+12,pos1[2]+3), dimensionId)
                    for i in lists:
                        if k in [1,2]:
                            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                            comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
                        if i != self.entityId:
                            comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                            MaxValue=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                            if MaxValue:
                                sh=MaxValue*0.03
                                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                                comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    if k==7:
                        comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
                        comp.CreateExplosion(pos1,1,False,False,None,serverApi.GetPlayerList()[0])

                sh_pos.append(entityFootPos1)
                for poi in sh_pos:
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    lists=comp.GetEntitiesInSquareArea(None, (poi[0]-8,poi[1]-2,poi[2]-8), (poi[0]+8,poi[1]+12,poi[2]+8), dimensionId)
                    for i in lists:
                        if i != self.entityId:
                            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                            comp.Hurt(30, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)

                    for i in range(8):
                        comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp1.AddTimer(0.5*i,f1,poi,i)
            else:
                self.romve_skill('异常skill_5')


        def f1():
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            entId=comp.GetAttackTarget()
            comp = serverApi.GetEngineCompFactory().CreatePos(entId)
            entityFootPos = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            # 设置该实体看向(0,78,0)这个位置，该凝视行为最少持续2秒，最多持续3秒，凝视过程中禁止触发其他行为
            comp.SetEntityLookAtPos(entityFootPos, 1, 1, True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(2.5,f)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(2.3,f1)

    def skill_4(self):
        '''烈焰火球'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        a=[]
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()

        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(self.entityId)
        bianti=entitycomp.GetExtraData("stage")
        for i in range(5):
            ai=[90,90,0,-90,-90]
            bi=[2,1,0,1,2]
            gi=[4.5,4.8,5,4.8,4.5]

            rot1=(rot[0],rot[1]+ai[i])
            x, y, z = serverApi.GetDirFromRot(rot1)
            param = {
                'position': (entityFootPos[0],entityFootPos[1],entityFootPos[2]),
                'direction': (0,0,0),
                'power': 0,
                'gravity':0
                }
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            id=comp.CreateProjectileEntity(self.entityId, "zaibian:ignis_psw", param)
            comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
       
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
            target = (entityFootPos[0]+x*bi[i],entityFootPos[1]+gi[i],entityFootPos[2]+z*bi[i])
            mID = motionComp.AddEntityTrackMotion(target, 0.7, startPos=None, isLoop=False, useVelocityDir=True, ease = serverApi.GetMinecraftEnum().TimeEaseType.linear)
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
            motionComp.StartEntityMotion(mID)
                                    
            if i==4:
                comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                comp.TriggerCustomEvent(id, "minecraft:mark_v")
                entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(id)
                entitycomp.SetExtraData("teshu", True) 
            elif bianti !=None:
                
                comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                comp.TriggerCustomEvent(id, "minecraft:mark_v1")

            a.append(id)

        def f2(args):
            def f1(i):
                comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
                entId=comp.GetAttackTarget()
                if entId:
                    comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                    entityFootPos1 = comp.GetFootPos()
                    if entityFootPos1 and entityFootPos:
                        entityFootPos1 = entityFootPos1[0],entityFootPos1[1]+0.7,entityFootPos1[2]

                        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(i)
                        teshu=entitycomp.GetExtraData("teshu") 
                        if teshu:
                            sj=0.7
                        else:
                            sj=0.69
                        if sj==0.7:
                            comp = serverApi.GetEngineCompFactory().CreatePos(i)
                            entityFootPos2 = comp.GetFootPos()
                            self.serverapi.DestroyEntity(i)
                            param = {
                                'position': entityFootPos2,
                                'direction': (0,0,0),
                                'power': 0,
                                'gravity':0
                                }
                            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                            id=comp.CreateProjectileEntity(self.entityId, "zaibian:ignis_psw1", param)
                            comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                            comp.TriggerCustomEvent(id, "minecraft:mark_v")
                            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(id)
                            entitycomp.SetExtraData("teshu", True) 
                            i=id          
                        comp = serverApi.GetEngineCompFactory().CreatePos(i)
                        entityFootPos2 = comp.GetFootPos()
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                        from mod.common.utils.mcmath import Vector3
                        a=Vector3(entityFootPos1[0]-entityFootPos2[0],entityFootPos1[1]+1.4-entityFootPos2[1], entityFootPos1[2]-entityFootPos2[2])
                        a.Normalize()
                        motionComp.SetMotion(tuple(a*1.5))
           
                    else:
                        self.serverapi.DestroyEntity(i)
                else:
                    self.serverapi.DestroyEntity(i)

            for i1 in range(0,5):
                self.time_J(0.6*i1,f1,a[i1])
        
        self.time_J(1.75,f2,None)




    def tiaoyue(self,id,entityFootPos1):
        comp = serverApi.GetEngineCompFactory().CreatePos(id)
        entityFootPos = comp.GetFootPos()
        x,y,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[1]-entityFootPos[1],entityFootPos1[2]-entityFootPos[2]
        pl=float(self.calculate_distance(entityFootPos,entityFootPos1))
        if pl<10:
            pl=12.0
        sx,sy,sz=x/pl,12/pl,z/pl

        def f():
            comp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
            comp.SetMotion((sx, sy,sz))
        for i in range(int(pl)):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.05*i,f)
        return pl*0.05

    def skill_3(self):
        '''飞跃猛击'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        if entId:
            comp = serverApi.GetEngineCompFactory().CreatePos(entId)
            entityFootPos1 = comp.GetFootPos()
            s=self.tiaoyue(self.entityId,entityFootPos1)
            def stop(args):
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
                motionComp.SetMotion((0,-5,0 ))
            self.time_J(s+0.2,stop,None)
            def fo(l):   
                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                entityFootPos = comp.GetFootPos()
                st=[[0,4],[4,7],[7,10]]             
                all_pos=[]
                l1=35+l*12
                for i in range(l1):
                    if random.randint(0,1)==1:
                        x=random.uniform(st[l][0],st[l][1])
                    else:
                        x=random.uniform(-st[l][1],st[l][0])
                    if random.randint(0,1)==1:
                        z=random.uniform(st[l][0],st[l][1])
                    else:
                        z=random.uniform(-st[l][1],st[l][0])
                    all_pos.append([x,z])

                self.xlfangk(all_pos,entityFootPos)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-st[l][1],entityFootPos[1]-2,entityFootPos[2]-st[l][1]), (entityFootPos[0]+st[l][1],entityFootPos[1]+2,entityFootPos[2]+st[l][1]), dimensionId)
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                    if i==self.entityId  :
                        continue
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    x,z=entityFootPos[0]-entityFootPos1[0], entityFootPos[2]-entityFootPos1[2]
                    if abs(x)>abs(z):
                        sh=15*((10-abs(x))/10)
                    else:
                        sh=15*((10-abs(z))/10)
                    
                    comp.SetMobKnockback(0,0, 0, 0.2, 0.2)
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
            for i in range(2):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(s+0.4+0.3*i,fo,i)



            # self.time_J(s+0.4,stop1,None)





    def skill_1(self):

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        if self.stage:
            zw=3
        else:
            zw=2
        def fo(l):   
            st=[[0,4],[4,7],[7,10]]             
            all_pos=[]
            l1=35+l*12

            for i in range(l1):
                if random.randint(0,1)==1:
                    x=random.uniform(st[l][0],st[l][1])
                else:
                    x=random.uniform(-st[l][1],st[l][0])
                if random.randint(0,1)==1:
                    z=random.uniform(st[l][0],st[l][1])
                else:
                    z=random.uniform(-st[l][1],st[l][0])
                all_pos.append([x,z])

            self.xlfangk(all_pos,entityFootPos)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-st[l][1],entityFootPos[1]-2,entityFootPos[2]-st[l][1]), (entityFootPos[0]+st[l][1],entityFootPos[1]+2,entityFootPos[2]+st[l][1]), dimensionId)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,10.5,True,180.0,240.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                x,z=entityFootPos[0]-entityFootPos1[0], entityFootPos[2]-entityFootPos1[2]
                if abs(x)>abs(z):
                    sh=15*((10-abs(x))/10)
                else:
                    sh=15*((10-abs(z))/10)
                
                comp.SetMobKnockback(0,0, 0, 0.2, 0.2)
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(int(sh), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
        for i in range(zw):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.3*i,fo,i)

        

    def addeffect(self,entityId):
        if self.stage:
            val=2
        else:
            val=1
        comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
        res = comp.AddEffectToEntity("blazing_brand", 15, val, True)

    def OnMobHitMobServerEvent(self,args):
        mobId=args["mobId"]
        hittedMobList=args["hittedMobList"]
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        if mobId==self.entityId:
            for i in hittedMobList:
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                if entityFootPos1 and entityFootPos:
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1, 0.1, 0.1)
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(random.randint(15,18), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    self.addeffect(i)
                    comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                    comp.SetEntityOnFire(3, 1)
                    self.skill_2_jn=True

    def skill_2(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        if self.stage==3:
            ak=17
        else:
            ak=14
        
        def stop(args):
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            for i in args:
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                self.addeffect(i)
                comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                comp.SetEntityOnFire(3, 1)
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1, 0.1, 0.1)
                comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
            if args:
                health=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, health+random.randint(5,5))
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        self.chongcientity((entId,8),ak,jl=0,stop_st=True,call=stop)
        

   
    def use_stage(self):
        print 'use_stage'

        self.use_stage_tz(3.5)

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        self.serverapi.BroadcastToAllClient("stage_lizi",{"entityId":self.entityId,"entityFootPos":entityFootPos,'key':'q'})
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        self.time_J(3.5,comp.ImmuneDamage,False)
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        self.time_J(3.5,comp1.SetBlockControlAi,True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            if i==self.entityId:
                continue
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(int(25), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)

    def use_stage1(self):
        print 'use_stage1'

        self.use_stage_tz(5)

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        self.time_J(5.0,comp.ImmuneDamage,False)
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        self.time_J(5.0,comp1.SetBlockControlAi,True)
        
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)

        self.serverapi.BroadcastToAllClient("stage_lizi",{"entityId":self.entityId,"entityFootPos":entityFootPos,'key':'1'})

        def func1(args):
            comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
            comp.CreateExplosion(entityFootPos,3,False,False,None,serverApi.GetPlayerList()[0])
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i==self.entityId:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(int(22), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
        def func2(args):
            self.skill_8()
        self.time_J(2,func1,None)
        self.time_J(3.75,func2,None)
      


    def start_death(self):
        time=2+2
        def die():
            self.die_wp()


        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 
        

    def use_attack(self,args=None):
        if random.randint(0,4)==0:
            def f():
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesAroundByType(self.entityId, 7, serverApi.GetMinecraftEnum().EntityType.Mob)
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                    if i==self.entityId or not  comp.CanSee(self.entityId,i,6.5,True,180.0,240.0) :
                        continue
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    if self.stage==3:
                        comp.Hurt(random.randint(18,18), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
                    else:
                        comp.Hurt(random.randint(14,14), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
            self.ack_time(3,1.5,f)
            print '攻击'
        else:
            self.use()
            print 'jn'



 
    def stop(self):
        pass