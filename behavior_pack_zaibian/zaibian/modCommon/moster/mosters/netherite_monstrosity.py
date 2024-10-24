# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random,math
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class netherite_monstrosity(public):
    def __init__(self,args):
        super(netherite_monstrosity,self).__init__(args)
        self.key=args.get("key")
        
    def use(self):
   
        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        jl=comp.GetAttr('skill_1')
        if self.key=='k1' :
            if  jl>=3:
                self.skill_2()
            return

        data={
            "skill_use1":1,
            "skill_use2":0,
            "skill_use3":0,


        }
        skill_name=self.random_skill(data)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        if not entityFootPos1  or   pl<10:
            return
        self.skill_jn(skill_name,[2,25,0],[0,0,0])


    def skill_1(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        jl=comp.GetAttr('skill_1')
        if entId and  jl<3:
            power=1+(pl-10)*0.05
            if power<0.9:
                power=0.9
            elif power>2:
                power=2
            def f(jl):
                for i in range(3):
                    dir1= (entityFootPos1[0]-(entityFootPos[0])+random.uniform(-1,1),entityFootPos1[1]-(entityFootPos[1]+i+4.5)+random.uniform(6,7),entityFootPos1[2]-(entityFootPos[2])+random.uniform(-1,1))
                    param = {
                    'direction':dir1,
                    'position': (entityFootPos[0]+random.uniform(-1.3,1.3),entityFootPos[1]+4.5+random.uniform(-0.3,0.6),entityFootPos[2]+random.uniform(-1.3,1.3)),
                    "power":power
                    }
                    comp1 = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(0 +i*0.05,comp1.CreateProjectileEntity,self.entityId, "zaibian:netherite_monstrosity_zd", param)

                comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
                if jl:
                    jl+=1
                    comp.SetAttr('skill_1',jl)
                else:
                    comp.SetAttr('skill_1',1)

            self.time_J(1,f,jl)

        else:
            self.romve_skill("异常skill_1")
            if jl>=3:
                self.skill_2()
    

    def skill_2(self):
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        comp.ResetAttackTarget()
        self.time_J(0.1,self.search_molten,None)

    def calculate_distance(self,firstPoint, secondPoint):
        """
        计算两个坐标间的距离。

        :param firstPoint: 第一个坐标元组
        :param secondPoint: 第二个坐标元组
        :return: 两个坐标间的距离
        """
        if not firstPoint or not secondPoint:
            return -1
        if len(firstPoint) == len(secondPoint):
            powPos = 0
            for i in range(len(firstPoint)):
                powPos += math.pow(firstPoint[i] - secondPoint[i], 2)
            return math.sqrt(powPos)
        
        return -1

    def xzhaofk(self,fk=[],k=200,dimensionId=0,l=[]):
        if k<=0:
            return l
        if fk:
            pos=fk.pop(0)
            for i1 in [[0,0,1],[1,0,0],[-1,0,0],[0,0,-1],[0,1,0],[0,-1,0]]:
                p=pos[0]+i1[0],pos[1]+i1[1],pos[2]+i1[2]
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                if p not in  l :
                    blockDict = comp.GetBlockNew(p, dimensionId)
                    if blockDict and "lava" in blockDict['name']:
                        l.append(p)
                        fk.append(p)
                        k-=1
                        if k<=0:
                            return l

            self.xzhaofk(fk,k,dimensionId,l)
        return l
        



    def search_molten(self,args):
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        w={}
        o=5
        
        for x in  range(-o,o):
            for z in  range(-o,o):
                for y in  range(-3,3):
                    pos=(entityFootPos[0]+x,entityFootPos[1]+y,entityFootPos[2]+z)
                    w[pos]=self.calculate_distance(entityFootPos,pos)
  

        for x in  sorted(w.items() ,key=lambda w:w[1]):
            x_,y_,z_=x[0]
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew((x_,y_,z_), dimensionId)
            if blockDict and "lava" in blockDict['name']:
                def myCallback(entityId, result):
               
                    pos=( x_,y_,z_)
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    blockDict = comp.GetBlockNew(pos, dimensionId)
                    if blockDict and "lava" in blockDict['name']:
                        all_=  self.xzhaofk([pos],100,dimensionId,[])
                        def xi(pos):
                            blockDict = {
                                'name': 'minecraft:air',
                                'aux': 0
                            }
                            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                            comp.SetBlockNew(pos, blockDict, 0, dimensionId)
                        if all_:
                            comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
                            comp.SetAttr('skill_1',0)
                            comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
                            comp1.SetBlockControlAi(False, False)

                            comp =serverApi.GetEngineCompFactory().CreateEntityEvent(self.entityId)
                            comp.TriggerCustomEvent(self.entityId,"skill_use4")
                            for index,i in enumerate(all_):
                                self.time_J(0.5+0.02*index,xi,i)
                            def lo():
                                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                                comp.AddTimer(1,self.romve_skill,"异常skill_1") 

                                comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
                                health=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                                comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, health+random.randint(75,75))

                            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                            comp.AddTimer(0.5+(len(all_))*0.02,lo) 
                                        
                        return
                    self.romve_skill("异常skill_1")
   
                comp = serverApi.GetEngineCompFactory().CreateMoveTo(self.entityId)
                comp.SetMoveSetting(( x_,y_,z_),1.2,200,myCallback)
                return
        self.romve_skill("异常skill_1")


            

    def use_attack(self,args=None):


        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            if self.stage==2:
                r=8
            else:
                r=7
            Entities=comp.GetEntitiesAroundByType(self.entityId, r, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i==self.entityId :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/camerashake add @s 0.2 1 rotational",i)
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(random.randint(20,20), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, False)
                if self.stage:
                    comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                    comp.SetEntityOnFire(3, 1)
        self.ack_time(2.18,2.18*0.75,f)
            


    def use_stage(self):
        self.use_stage_tz(4)

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)
        self.time_J(4,comp.ImmuneDamage,False)
        def start(args):
            comp1.SetBlockControlAi(True,False)
            self.romve_skill("异常skill_1")
        self.time_J(4,start,None)
        
        def chuidi(args):
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            if not entityFootPos:
                return
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 8, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                if i==self.entityId:
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(int(25), serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                comp.SetEntityOnFire(4, 1)
                comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateAction(i)
                comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1, 0.2, 0.2)

        self.time_J(1.25,chuidi,False)
 

    def start_death(self):
        time=2.1+2
        def die():
            self.die_wp()

        

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(2.1,  self.serverapi.BroadcastToAllClient,'zhaohuan',{'id':self.entityId,'data':2,'key':'netherite_monstrosity'})

    def stop(self):
        pass