# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()
CompFactory=serverApi.GetEngineCompFactory()

class the_harbinger(public):
    def __init__(self,args):
        super(the_harbinger,self).__init__(args)
        
    def use(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        if   pl>15:
            return
        data={
            "skill_use1":3,
            "skill_use2":3,
            "skill_use3":2,
            "skill_use4":2,
            "skill_use5":1,

        }
        skill_name=self.random_skill(data)
  
        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(self.entityId)
        self.jieduan=entitycomp.GetExtraData("stage")

        self.skill_jn(skill_name,[2,2,2,7.5,2],[0,0,0,0,1.4])

    def skill_5(self):
        '''凋灵巡回飞弹'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        for i in range(0,2):
            def f1(i):
                for i1 in range(3):
                    def f2(i):
                        if i==0:
                            x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+90))
                        else:
                            x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]-90))
                        if entId and entId!="-1":
                            pos=(entityFootPos[0]+x*1.8,entityFootPos[1]+4+random.uniform(0,1),entityFootPos[2]+z*1.8)
                            param = {
                            'position': pos,
                            "direction":(0,0,0),
                            'targetId': entId,
                            'power':1
                            }
                            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                            id=comp.CreateProjectileEntity(self.entityId, "zaibian:the_harbinger_psw2", param)
                    if self.stage==None:
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.1*i1,f2,1)
                        comp.AddTimer(0.1*i1,f2,0)
                    else:
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.1*i1,f2,i)
                    

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.4*i,f1,i)
        

    def skill_1(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        p=6
        if self.jieduan==2:
            p=8

        for i in range(p):
            def f1():
                pos=(entityFootPos[0],entityFootPos[1]+3,entityFootPos[2])
                comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)

                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesAroundByType(self.entityId, 12, serverApi.GetMinecraftEnum().EntityType.Mob)
                lists.remove(self.entityId)
                if lists:
                    id =random.choice(lists)
                    comp = serverApi.GetEngineCompFactory().CreatePos(id)
                    entityFootPos1 = comp.GetFootPos()
                    pos1=(entityFootPos1[0]-entityFootPos[0],entityFootPos1[1]-entityFootPos[1]-3,entityFootPos1[2]-entityFootPos[2])
                    param = {
                    'position': pos,
                    'direction': pos1,
                    }
                    comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                    id=comp.CreateProjectileEntity(self.entityId, "zaibian:the_harbinger_pswd", param)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.2*i,f1)


    def skill_2(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        for i in range(1,3):
            def f1():
                for i1 in range(4):
                    x=random.randint(-8,8)
                    z=random.randint(-8,8)
                    y=random.randint(2,3)

                    pos=(entityFootPos[0],entityFootPos[1]+y,entityFootPos[2])
                    comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
                    entityFootPos1=(entityFootPos[0]+x,entityFootPos[1]-2,entityFootPos[2]+z)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    pos1=(entityFootPos1[0]-entityFootPos[0],entityFootPos1[1]-entityFootPos[1]-4,entityFootPos1[2]-entityFootPos[2])
                    param = {
                    'position': pos,
                    'direction': pos1,
                    'power':1
                    }
                    comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                    id=comp.CreateProjectileEntity(self.entityId, "zaibian:the_harbinger_psw", param)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.9*i,f1)
    def GetBlockOfRange(self,pos, radius, dimensionId):
        '''返回区域内所有方块列表'''
        x, y, z = pos[0], pos[1], pos[2]
        rangeList = list()
        for i in range(radius + 1):
            if i not in rangeList:
                rangeList.append(i)
            if -i not in rangeList:
                rangeList.append(-i)
        blockList = list()
        for xx in rangeList:
            for yy in rangeList:
                for zz in rangeList:
                    x_new = x + xx
                    y_new = y + yy
                    z_new = z + zz
                    pos_new = (x_new, y_new, z_new)
                    blockDict = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId).GetBlockNew(pos_new, dimensionId)
                    if blockDict["name"]=="minecraft:air":continue
                    block = dict()
                    block["name"] = blockDict["name"]
                    block["aux"] = blockDict["aux"]
                    block["pos"] = pos_new
                    block["dim"] = dimensionId
                    if block not in blockList :
                        blockList.append(block)
        return blockList

    def skill_3(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()

        p=1
        if self.jieduan==2:
            p=random.randint(2,3)

        def io():
            self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'data':3,'key':'the_harbinger'})
            def f2():
                comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                entityFootPos = comp.GetFootPos()
                if not entityFootPos1:
                    return
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
                x,z=entityFootPos[0]-entityFootPos[0],entityFootPos[2]-entityFootPos1[2]
                if abs(x)<abs(z):
                    if z>1 or z<-1:
                        x/=abs(z)
                        z/=abs(z)
                else:
                    if x>1 or x<-1:
                        z/=abs(x)
                        x/=abs(x)

                motionComp.SetMotion((x*2, 1,z*2))
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.1,f2)

            def f1():
                comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                entityFootPos = comp.GetFootPos()
                if not entityFootPos1:
                    return

                x,y,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[1]+0.1-entityFootPos[1],entityFootPos1[2]-entityFootPos[2]
                if abs(x)<abs(z):
                    if z>1 or z<-1:
                        x/=abs(z)
                        z/=abs(z)
                else:
                    if x>1 or x<-1:
                        z/=abs(x)
                        x/=abs(x)
                for i in range(0,15):
                    self.time_J(0.1*i,f,(x,y,z))
            def f(a):
                def SetBlockNew():
                    """破坏经过的方块。"""
                    pos = compFactory.CreatePos(self.entityId).GetPos()
                    dim= compFactory.CreateDimension(self.entityId).GetEntityDimensionId()
                    blockList=self.GetBlockOfRange(pos,1,dim)
                    for block in blockList:
                        blockPos = block["pos"]
                        dim=block["dim"]
                        self.set_block(blockPos,dim)
                SetBlockNew()
                x,y,z=a
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
                motionComp.SetMotion((x/1.2, y,z/1.2))
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesAroundByType(self.entityId, 1, serverApi.GetMinecraftEnum().EntityType.Mob)
                lists.remove(self.entityId)
                for i in lists:
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(25, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    comp.SetMobKnockback(x, z, 15, 0, 0)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.4,f1)
        for i in range(p):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(2*i,io)
    
    def skill_4(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 5, 100, False)
        def f(w):
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            entId=comp.GetAttackTarget()
            entityFootPos1=None
            if entId!='-1':
                comp = serverApi.GetEngineCompFactory().CreatePos(entId)
                entityFootPos1 = comp.GetFootPos()
                id_p=entId

            else:
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesAroundByType(self.entityId, 15, serverApi.GetMinecraftEnum().EntityType.Mob)
                lists.remove(self.entityId)
                if lists:
                    comp = serverApi.GetEngineCompFactory().CreatePos(lists[0])
                    entityFootPos1 = comp.GetFootPos()
                    id_p=lists[0]

            if entityFootPos1:
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesAroundByType(self.entityId, 40, serverApi.GetMinecraftEnum().EntityType.Mob)
                lists.remove(self.entityId)
                for i in lists:
                    comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                    if comp.CanSee(self.entityId,i,40.0,True,120.0,120.0):
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(3, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                # comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
                # comp.SetEntityLookAtPos(entityFootPos1, 0.8, 1, True)


        # self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'data':4,'key':'the_harbinger'})
        for i in range(37):
            self.time_J(0.2*i,f,None)
        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
        
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        if entityFootPos1:
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
            x,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[2]-entityFootPos[2]
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.1,motionComp.SetMotion,(x/5, 0.7,z/5))
            

    def use_stage(self):
        # comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        # comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        # self.serverapi.BroadcastToAllClient("stage_lizi",{"entityId":self.entityId,"entityFootPos":entityFootPos})
        # comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        # comp.ImmuneDamage(True)
        # self.time_J(1,comp.ImmuneDamage,False)
        # comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        # self.time_J(1,comp1.SetBlockControlAi,True)
      

    def start_death(self):
        time=5+1
        self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'data':100,'key':'the_harbinger'})
        comp = serverApi.GetEngineCompFactory().CreateItem(self.entityId)
        comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, None, 0)
        def die():
            self.die_wp()
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 15, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i==self.entityId:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(int(25), serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)


        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 
    
        
    def stop(self):
        pass