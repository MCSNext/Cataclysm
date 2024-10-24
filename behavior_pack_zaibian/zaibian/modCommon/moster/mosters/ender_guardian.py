# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class ender_guardian(public):
    def __init__(self,args):
        super(ender_guardian,self).__init__(args)
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
        if   pl>20:
            return
        if not self.stage:
            self.jl_list={"skill_use1":[[0,7,5],2],"skill_use2":[[0,8,4],1],"skill_use3":[[0,10,4],3],
             "skill_use5":[[6,15,4],1],   "skill_use6":[[0,9,5],3],"skill_use7":[[0,12,5],3],"skill_use8":[[3,15,5],2],
                          "skill_use9":[[0,7,5],2],
                          "skill_use10":[[3,10,4],2],

        }
        else:
            self.jl_list={"skill_use1":[[0,7,5],8],"skill_use2":[[0,8,4],4],"skill_use3":[[0,10,4],15],"skill_use4":[[6,20,8],8],
                          "skill_use5":[[6,15,4],8],   "skill_use6":[[0,9,5],8],"skill_use7":[[0,12,5],8],"skill_use8":[[3,15,5],8],

                          "skill_use9":[[0,7,5],8],
                          "skill_use10":[[3,10,4],8],
            
            }
        data=self.Get_Use_Skill_Name(pl,g)
        if data:
            skill_name=self.random_skill(data)
            # skill_name="skill_use5" #TODO
            self.skill_jn(skill_name,[2,2.0 ,2.5,4,5,3,4,2,3.5,3],[1.2,0,1.3,2.2,1.5,1.5,1.25,1.5,0,0.8])

    def skill_10(self):
        '''冲刺攻击'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        if entId:
            self.chongcientity(entId,0,False,0)
            def f():
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
                for i in Entities:
                    if i !=self.entityId:
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(20, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
            self.time_J(1.75-0.8,f)
        else:
            self.romve_skill("异常skill_10")

    def skill_9(self):
        '''捶地加横扫'''
        def f1():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,6.5,True,180.0,240.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

        self.time_J(2.6,f)
        self.time_J(1.13,f1)

        
    def skill_8(self):
        '''召唤虚空符文'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        def void_core_evocation(rot,pos,DimensionId):  #延迟放技能
            po=self.serverapi.CreateEngineEntityByTypeStr('zaibian:void_rune', pos, rot, DimensionId)
            comp = serverApi.GetEngineCompFactory().CreateModAttr(po)
            comp.SetAttr('zr', self.entityId)
        def use(args):
            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            rot = rotComp.GetRot()
            comp = serverApi.GetEngineCompFactory().CreateDimension(self.entityId)
            DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
            val=random.randint(1,3)
            if self.stage:
                val=5
            if val==1:
                al=[0]
            elif val==2:
                al=[-10,10]
            elif val==3:
                al=[-10,0,10]
            else:
                al=[-30,-20,-10,0,10,20,30]
            k=0
            for i1 in al:
                k+=1
                for i in range(4,24,3):    #放置15个磨牙
                    x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+i1))
                    pos=(entityFootPos[0]+x*i,entityFootPos[1],entityFootPos[2]+z*i)
                    comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                    comp.AddTimer(0.1*i,void_core_evocation,rot,pos,DimensionId)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i==self.entityId:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(0, 0, 0, 0.2, 0.2)
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(25,25), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
        use(None)
   

    def skill_7(self):
        '''上勾拳'''
   
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)

        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        x, y, z = serverApi.GetDirFromRot(rot)
        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
        motionComp.SetMotion((x * 2, 0, z * 2))

        def f():
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            entId=comp.GetAttackTarget()
            if entId:
                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                for i in range(6):
                    param = {
                    'direction': (i,1,i),
                    'position': (entityFootPos[0],entityFootPos[1]+i+2,entityFootPos[2]),
                    "targetId":entId
                    }
                    comp1 = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(0.1*i ,comp1.CreateProjectileEntity,self.entityId, "zaibian:qianbei", param)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 7, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,7,True,140.0,240.0) :
                    continue
                
                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                entityFootPos = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1, 0.6, 0.6)
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(16, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)
                
                def f1(i):
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("stun", 3, 0, False)

                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0.1,f1,i)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(0.1,f)

        
    def skill_6(self):
        '''爆裂冲击'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 8, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,8,True,180.0,240.0) :
                continue
            
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreatePos(i)
            entityFootPos1 = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateAction(i)
            comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 3, 0.3, 0.3)
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(16, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)
    
    

    def skill_5(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        if entId:
            comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
            res = comp.AddEffectToEntity("slowness", 2, 100, False)

            comp = serverApi.GetEngineCompFactory().CreatePos(entId)
            entityFootPos = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos1 = comp.GetFootPos()
            for i  in range(100):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(1+0.1*i ,self.attract_skill,entityFootPos,6,0)

            comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            comp.SetEntityLookAtPos(entityFootPos, 2, 2, True)
            self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'data':0,'key':'ender_guardian','pos':(entityFootPos[0],entityFootPos[1]+0.2,entityFootPos[2])})
            def f1():
                if self.st:
                    def fi(a):
                        self.romve_skill("异常skill_5")

                    self.chongcientity(entId,20,call=fi)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(1.75 ,f1)
        else:
            self.romve_skill("异常skill_5")
            


    def skill_1(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        all_pos=[[0.0, 5.0], [0.78, 4.94], [1.55, 4.76], [2.27, 4.46], [2.94, 4.05], [3.54, 3.54], [4.05, 2.94], [4.46, 2.27], [4.76, 1.55], [4.94, 0.78], [5.0, 0.0], [4.94, -0.78], [4.76, -1.55], [4.46, -2.27], [4.05, -2.94], [3.54, -3.54], [2.94, -4.05], [2.27, -4.46], [1.55, -4.76], [0.78, -4.94], [0.0, -5.0], [-0.78, -4.94], [-1.55, -4.76], [-2.27, -4.46], [-2.94, -4.05], [-3.54, -3.54], [-4.05, -2.94], [-4.46, -2.27], [-4.76, -1.55], [-4.94, -0.78], [-5.0, -0.0], [-4.94, 0.78], [-4.76, 1.55], [-4.46, 2.27], [-4.05, 2.94], [-3.54, 3.54], [-2.94, 4.05], [-2.27, 4.46], [-1.55, 4.76], [-0.78, 4.94], [-0.0, 5.0]]
        blockPos=(entityFootPos[0],entityFootPos[1],entityFootPos[2])
        self.xlfangk(all_pos,blockPos)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 7, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in Entities:
            if i==self.entityId:
                continue
            comp = serverApi.GetEngineCompFactory().CreatePos(i)
            entityFootPos1 = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateAction(i)
            comp.SetMobKnockback(entityFootPos[0]-entityFootPos1[0], entityFootPos[2]-entityFootPos1[2], 0.5, 0.7, 0.7)
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(random.randint(25,28), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

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
                    comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1, 0.7, 0.7)

                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(random.randint(24,24), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("stun", 1, 0, False)
    def skill_2(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        def stop(args):
            self.serverapi.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnMobHitMobServerEvent",self, self.OnMobHitMobServerEvent)

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()

        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        if entityFootPos1:

            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
            x,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[2]-entityFootPos[2]
            if abs(x)<abs(z):
                if z>1 or z<-1:
                    x/=abs(z)
                    z/=abs(z)
            else:
                if x>1 or x<-1:
                    z/=abs(x)
                    x/=abs(x)
            for i in range(15):
                self.time_J(0.1*i,motionComp.SetMotion,(x/2, 0,z/2))

            self.serverapi.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnMobHitMobServerEvent",self, self.OnMobHitMobServerEvent)
      

            self.time_J(2.2,stop,None)
        else:
            self.romve_skill("异常skill_2")
            
    def skill_3(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        def void_core_evocation(rot,pos,DimensionId):  #延迟放技能
            po=self.serverapi.CreateEngineEntityByTypeStr('zaibian:void_rune', pos, rot, DimensionId)
            comp = serverApi.GetEngineCompFactory().CreateModAttr(po)
            comp.SetAttr('zr', self.entityId)
        
        
        def use(args):

            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            rot = rotComp.GetRot()
        
            comp = serverApi.GetEngineCompFactory().CreateDimension(self.entityId)
            DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
         
            al=[-20,-10,0,10,20]
            for i1 in al:
                for i in range(2,20,3):    #放置15个磨牙
                    x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+i1))
                    pos=(entityFootPos[0]+x*i,entityFootPos[1],entityFootPos[2]+z*i)
                    comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                    comp.AddTimer(0.05*i,void_core_evocation,rot,pos,DimensionId)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i==self.entityId:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(0, 0, 0, 0.2, 0.2)
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(25,25), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

            if   self.stage:
                for i1 in [5,8]:
                    for i in range(0,18,2):
                        x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+i*20))
                        pos=(entityFootPos[0]+x*i1,entityFootPos[1],entityFootPos[2]+z*i1)
                        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                        comp.AddTimer(0,void_core_evocation,rot,pos,DimensionId)

  
        use(None)

    def skill_4(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        if entId:
            comp = serverApi.GetEngineCompFactory().CreatePos(entId)
            entityFootPos = comp.GetFootPos()
            def f1(args):
                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                comp.SetFootPos((entityFootPos[0], entityFootPos[1]+4, entityFootPos[2]))
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
                motionComp.SetMotion((0, -1, 0))
                def f(a):
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    Entities=comp.GetEntitiesAroundByType(self.entityId, 2, serverApi.GetMinecraftEnum().EntityType.Mob)
                    for i in Entities:
                        if i==self.entityId :
                            continue
                        comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                        comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(random.randint(12,14), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
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
                    for i1 in range(-80,81,30):
                        for i in range(10,25,5):    #放置15个磨牙
                            x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+i1))
                            pos=(entityFootPos[0]+x*i,entityFootPos[1],entityFootPos[2]+z*i)
                            comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                            comp.AddTimer(0.05*i,void_core_evocation,rot,pos,DimensionId)

                comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
                comp.SetEntityLookAtPos(entityFootPos, 0.8, 1, True)
                self.time_J(0.6,f,False)
            self.time_J(0.25,f1,False)

        
            
    def use_attack(self,args=None):
        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 5, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
        self.ack_time(2,2*0.68,f)
        print '攻击'



    def use_stage(self):
        self.use_stage_tz(2.5)
        def baozha(args):
            comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
            comp.CreateExplosion(entityFootPos,5,False,False,None,serverApi.GetPlayerList()[0])
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            dimensionComp = compFactory.CreateDimension(self.entityId)
            dimensionId = dimensionComp.GetEntityDimensionId()
            for x in range(-18,18):
                for z in range(-18,18):
                    for y in range(-3,0):
                        entityFootPos1=entityFootPos[0]+x,entityFootPos[1]+y,entityFootPos[2]+z
                        self.set_block(entityFootPos1,dimensionId)

            for i in Entities:
                if i==self.entityId:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(0, 0, 0, 0.5, 0.5)
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(20,25), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        self.time_J(0.6,baozha,False)

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        self.time_J(2.5,comp.ImmuneDamage,False)
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        self.time_J(2.5,comp1.SetBlockControlAi,True)

        


        comp1 = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        pos1=comp1.GetPos()
        comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
        comp.SetCommand("/playanimation @e[x={},y={},z={},r=0.1] attack3".format(pos1[0],pos1[1],pos1[2],))#传送指令

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

