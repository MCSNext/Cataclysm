# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class the_leviathan(public):
    def __init__(self,args):
        super(the_leviathan,self).__init__(args)
        
    def use(self):
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        if   pl<6:
            data={
            "skill_use3":2,  ##近
            "skill_use4":2,  ##近
            "skill_use11":2, ##近
            }
            
        else:
            data={
                "skill_use1":2,
                "skill_use2":2,
                "skill_use5":2,  ##远
                "skill_use6":2,  
                "skill_use7":2, 
                "skill_use8":2, 
                "skill_use9":2, 
                "skill_use10":2, 
            }
        if random.randint(0,100)<35 and pl<8:
            data={
            "skill_use12":2, ##近
            }
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        self.rot = rotComp.GetRot()
        skill_name=self.random_skill(data)
        # skill_name="skill_use12" #TODO
        self.skill_jn(skill_name,[5,1,1.5,1,1.25,4,6,7.25,7,9,5,5],[2,1,0,0.7,0.6,0.75,1,1.5,0,0,0.4,0])


    def skill_1(self):
        '''冲撞撕咬'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        lists=comp.GetEntitiesAroundByType(self.entityId, 10, serverApi.GetMinecraftEnum().EntityType.Mob)
        lists.remove(self.entityId)
        for i in lists:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if comp.CanSee(self.entityId,i,10.0,True,180.0,180.0):
                comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                res = comp.AddEffectToEntity("blindness", 3, 0, True)
                
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        x,y,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[1]-entityFootPos[1],entityFootPos1[2]-entityFootPos[2]
        comp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
        jl=float(self.calculate_distance(entityFootPos1,entityFootPos))

        kpos=entityFootPos1[0]+x*100,entityFootPos1[2]+y*100,entityFootPos1[1]+y*100
        comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        comp.SetEntityLookAtPos(kpos, 3.5, 3.5, True)

        rot=[x/jl,y/jl,z/jl]
        if rot[1]*15>3:
            rot[1]=3/15.0
        def f(args):
            comp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
            comp.SetMotion((rot[0]*1.5,rot[1]*1.5,rot[2]*1.5))
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(self.entityId, 3, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(self.entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if comp.CanSee(self.entityId,i,2.0,True,180.0,180.0):
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
        for i in range(15):
            self.time_J(0.2*i,f,None)

    def skill_2(self):
        '''瞬移'''
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        entityFootPos1 = comp.GetFootPos()
        if entityFootPos1:
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'data':2,'key':'the_leviathan','pos':entityFootPos})
            self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'data':2,'key':'the_leviathan','pos':entityFootPos1})

            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            comp.SetPos(entityFootPos1)
                        
    def skill_3(self):
        '''蛮横甩尾'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        def func(k):
            if k==0:
                self.block_del((entityFootPos[0]-5,entityFootPos[1]-2,entityFootPos[2]-5),(entityFootPos[0]+5,entityFootPos[1]+2,entityFootPos[2]+5),dimensionId,["zaibian:dungeon_block","minecraft:bedrock"],True)
            '''计算圆形伤害'''
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(self.entityId, 3, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(self.entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)

            xs=360/29
            d=xs*k
            self.rot=(0,d)
            x, y, z = serverApi.GetDirFromRot(self.rot)
            maxpos=x*8+entityFootPos[0]+3, y+entityFootPos[1]+2, z*8+entityFootPos[2]+3
            minpos=x*8+entityFootPos[0]-3, y+entityFootPos[1]-2, z*8+entityFootPos[2]-3

            self.block_del(minpos,maxpos,dimensionId,["zaibian:dungeon_block","minecraft:bedrock"],True)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesInSquareArea(None, minpos, maxpos, dimensionId)

            if self.entityId in lists:
                lists.remove(self.entityId)
            
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                res = comp.AddEffectToEntity("bone_fracture", 8, 0, False)


        for i in range(30):
            self.time_J(0.05*i,func,i)

    def skill_4(self):
        '''触手戳刺'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 9, serverApi.GetMinecraftEnum().EntityType.Mob)
        Entities.remove(self.entityId)
        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,8.0,True,90.0,180.0) :
                continue
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(17, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)

    def skill_5(self):
        '''触手牵引'''
        dr=[]
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 18, serverApi.GetMinecraftEnum().EntityType.Mob)
        Entities.remove(self.entityId)
        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,18.0,True,30.0,30.0) :
                continue
            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
            comp.Hurt(6, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
            dr.append(i)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()

        def xi():
            for i in dr:
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos1 = comp.GetFootPos()
                x,y,z=entityFootPos[0]-entityFootPos1[0],entityFootPos[1]-entityFootPos1[1],entityFootPos[2]-entityFootPos1[2]
                comp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
                jl=float(self.calculate_distance(entityFootPos1,entityFootPos))
                if abs(y)<2.5:
                    rot=(x/jl,0,z/jl)

                    if i not in serverApi.GetPlayerList():
                        comp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                        comp.SetMotion(rot)
                    else:
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                        motionComp.SetPlayerMotion(rot)

        for i in range(18):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(i*0.03,xi) 

    def skill_6(self):
        '''深渊水雷'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        dim= compFactory.CreateDimension(self.entityId).GetEntityDimensionId()
        def zhadan():
            x=random.randint(-10,10)
            y=random.randint(-10,10)
            z=random.randint(-10,10)
            pos=entityFootPos[0]+x,entityFootPos[1]+y,entityFootPos[2]+z
            entityId = self.serverapi.CreateEngineEntityByTypeStr('zaibian:abyss_mine', pos, (0, 0), dim)

        for i in range(29):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(i*0.1,zhadan) 

    def skill_7(self):
        '''深渊之吼'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 12, serverApi.GetMinecraftEnum().EntityType.Mob)
        Entities.remove(self.entityId)
        dim= compFactory.CreateDimension(self.entityId).GetEntityDimensionId()
        
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        pos = comp.GetFootPos()

        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,12.0,True,120.0,120.0) :
                continue
            comp = serverApi.GetEngineCompFactory().CreateEffect(i)
            res = comp.AddEffectToEntity("blindness", 3, 0, True)

        # def fangzhisyuan():
        #     comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        #     entId=comp.GetAttackTarget()
        #     comp = serverApi.GetEngineCompFactory().CreatePos(entId)
        #     entityFootPos = comp.GetFootPos()
        #     if entityFootPos:
        #         entityId = self.serverapi.CreateEngineEntityByTypeStr('zaibian:abyss_blast_portal', entityFootPos, (0, 0), dim)
        
        # for i in range(3):
        #     comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        #     comp.AddTimer(i*0.5,fangzhisyuan) 

        def chixifangzhi():
            pos1=self.calculate_random_pos_in_area(pos,10,False,dim)

            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew((pos1[0], pos1[1],  pos1[2]), dim)
            if blockDict["name"] in ["minecraft:air","minecraft:water","minecraft:flowing_water",]:
                y=-50
                step=-1
            else:
                y=50
                step=1

            for i in range(0,y,step):
                blockDict = comp.GetBlockNew((pos1[0], pos1[1]+i,  pos1[2]), dim)
                if y==-50 and   blockDict["name"]  not in ["minecraft:air","minecraft:water","minecraft:flowing_water",]:
                    pos1=(pos1[0], pos1[1]+i+1,  pos1[2])
                    break
                elif y==50 and  blockDict["name"]   in ["minecraft:air","minecraft:water","minecraft:flowing_water",]:
                    pos1=(pos1[0], pos1[1]+i,  pos1[2])
                    break
            

            entityId = self.serverapi.CreateEngineEntityByTypeStr('zaibian:abyss_blast_portal', pos1, (0, 0), dim)

        for i in range(15):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(2+i*0.3,chixifangzhi) 

    def skill_8(self):
        '''维度撕裂'''
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        pos = comp.GetFootPos()
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        self.rot = rotComp.GetRot()
        x, y, z = serverApi.GetDirFromRot((self.rot[0],self.rot[1]))
        pos=pos[0]+x*6,pos[1],pos[2]+z*6
        self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'data':8,'key':'the_leviathan','pos':pos})
        def xi():
            self.attract_skill(pos,12,10,2)
        for i in range(50):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(2+i*0.2,xi) 
    
    def skill_9(self):
        '''深渊冲击波'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 9, 100, False)
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        pos = comp.GetFootPos()
        def fase(p):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(self.entityId, 40, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(self.entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if comp.CanSee(self.entityId,i,40.0,True,80.0,80.0):
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("abyssal_burn", 5, 4, False)
            if  p<13 and self.stage==2:
                comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
                entId=comp.GetAttackTarget()
                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)

                x=random.randint(-5,5)
                y=random.randint(-5,5)
                z=random.randint(-5,5)
                pos1=pos[0]+x,pos[1]+y,pos[2]+z
                rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
                self.rot = rotComp.GetRot()
                x, y, z = serverApi.GetDirFromRot(self.rot )

                if entId != '-1':
                    param = {
                        'position': pos1,
                        'direction': (x, y, z),
                        "targetId":entId
                    }
                else:
                    param = {
                        'position': pos1,
                        'direction': (x, y, z)
                    }
                comp.CreateProjectileEntity(self.entityId, "zaibian:lingzhu", param)
        for i in range(35):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(3.25+i*0.1,fase,i) 

    def skill_10(self):
        '''三连式深渊冲击波'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        res = comp.AddEffectToEntity("slowness", 5, 100, False)
        sj=[3,5,7]
        def fase():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(self.entityId, 40, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(self.entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if comp.CanSee(self.entityId,i,40.0,True,60.0,60.0):
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(10, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("abyssal_burn", 5, 4, False)

        for i in range(3):
            for i1 in range(10):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(sj[i]+i1*0.1,fase) 


    def skill_11(self):
        '''抓取式深渊冲击波'''
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        Entities=comp.GetEntitiesAroundByType(self.entityId, 10, serverApi.GetMinecraftEnum().EntityType.Mob)
        jl=99
        stid=None
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        pos = comp.GetFootPos()
        for i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
            if i==self.entityId or not  comp.CanSee(self.entityId,i,10.0,True,60.0,180.0) :
                continue
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            pos1 = comp.GetFootPos()
            jl1=self.calculate_distance(pos1,pos)
            if jl>jl1:
                jl=jl1
                stid=i

        def fase():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(self.entityId, 40, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(self.entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if comp.CanSee(self.entityId,i,40.0,True,60.0,60.0):
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(18, serverApi.GetMinecraftEnum().ActorDamageCause.Contact, self.entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("abyssal_burn", 5, 4, False)

        if stid:
            # rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            # self.rot = rotComp.GetRot()
            x, y, z = serverApi.GetDirFromRot((self.rot[0],self.rot[1]))
            pos=pos[0]+x*6,pos[1],pos[2]+z*6
            comp = serverApi.GetEngineCompFactory().CreatePos(stid)
            comp.SetPos(pos)
            comp = serverApi.GetEngineCompFactory().CreateEffect(stid)
            res = comp.AddEffectToEntity("stun", 5, 0, False)      

            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            comp.SetAttackTarget(stid)

            comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
            res = comp.AddEffectToEntity("slowness", 5, 100, False)
            # def siyao():
            #     comp = serverApi.GetEngineCompFactory().CreateHurt(stid)
            #     comp.Hurt(23, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            # comp.AddTimer(1.41,siyao) 

            for i in range(8):
                comp.AddTimer(2.75+0.2*i,fase) 

        else:
            self.romve_skill("异常skill_11")

            
    def skill_12(self):
        '''逃跑机制'''
        def f(a):
            comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
            if comp.GetAttackTarget()=="-1":
                filters = {
                 "any_of": [
                            {
                                "subject": "other",
                                "test": "is_family",
                                "value": "squid"
                            },
                            {
                                "subject": "other",
                                "test": "is_family",
                                "value": "player"
                            }
                        ]
                }
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                list_1=comp.GetEntitiesAround(self.entityId, 60, filters)
                if list_1:
                    comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
                    comp.SetAttackTarget(list_1[0])
                    
       


        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        self.time_J(5.1,f,None)


    def use_attack(self,args=None):
        def f():
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or not  comp.CanSee(self.entityId,i,5.0,True,180.0,180.0) :
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(30, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, True)
        self.ack_time(1,0.4,f)

    def use_stage(self):
        self.use_stage_tz(3)

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        pos = comp.GetFootPos()
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        def f(a):
            comp = serverApi.GetEngineCompFactory().CreateAttr(self.entityId)
            health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,health_max*2)
            comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,health_max)
        def f1(a):
            comp1.SetBlockControlAi(True)
            comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
            comp.ImmuneDamage(False)

        self.time_J(1.5,f,None)
        self.time_J(3,f1,None)


        comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
        self.time_J(0,comp.SetCommand,"/playanimation @e[x={},y={},z={},r=0.1] bianshen".format(pos[0],pos[1],pos[2]))


        


        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()
        

        def fase():
            x=random.randint(-8,8)
            y=random.randint(-4,4)
            z=random.randint(-8,8)
            pos1=pos[0]+x,pos[1]+y,pos[2]+z
            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            self.rot = rotComp.GetRot()
            x, y, z = serverApi.GetDirFromRot(self.rot )
            if entId != '-1':
                param = {
                    'position': pos1,
                    'direction': (x, y, z),
                    "targetId":entId
                }
            else:
                param = {
                    'position': pos1,
                    'direction': (x, y, z)
                }
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            comp.CreateProjectileEntity(self.entityId, "zaibian:lingzhu", param)

        for i in range(24):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(1.1+i*0.1,fase) 



    def start_death(self):
        time=10+1.5
        comp = serverApi.GetEngineCompFactory().CreateItem(self.entityId)
        comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, None, 0)
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