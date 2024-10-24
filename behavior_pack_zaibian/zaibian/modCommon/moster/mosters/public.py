# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import zaibian.modCommon.storage as storage
import math
import random
from mod.common.utils.mcmath import Vector3

levelId=serverApi.GetLevelId()

leven=serverApi.GetLevelId()
CompFactory=serverApi.GetEngineCompFactory()
compFactory=serverApi.GetEngineCompFactory()

jntime={}

class public(object):
    def __init__(self,args):
        self.entityId=args["entityId"]

        if not  jntime.get(self.entityId):
            jntime[self.entityId]=[]
        self.EngineTypeStr=args["EngineTypeStr"]

        

        self.shid=args.get("shid")

        self.stage=None
        self.serverapi=storage.serverapi
        self.clientapi=storage.clientapi
        # self.entityId_die=None
        if self.serverapi.stage.get(self.entityId):
            self.stage=self.serverapi.stage.get(self.entityId)
        else:
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(self.entityId)
            self.serverapi.stage[self.entityId]=entitycomp.GetExtraData("stage")
            self.stage=self.serverapi.stage.get(self.entityId)
        self.jl_list=None



    def Get_Use_Skill_Name(self,jl,g):
        '''用距离获取对应合适的技能'''
        dict_={}
        for i,data in self.jl_list.items():
            min_,max_,h=data[0]
            if g<=h  and  min_<=jl<=max_:
                dict_[i]=data[1]
        return dict_

    def chongcientity(self,entId,sh,knocked=True,jl=4,stop_st=False,call=None,CanSee=False):
        '''冲刺到实体位置'''
        comp = serverApi.GetEngineCompFactory().CreateDimension(self.entityId)
        DimensionId=comp.GetEntityDimensionId() #获取实体所在维度

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos1 = comp.GetFootPos()
        if type(entId)==str:
            comp = serverApi.GetEngineCompFactory().CreatePos(entId)
            entityFootPos = comp.GetFootPos()
        elif type(entId)==int:
            rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            rot = rotComp.GetRot()
            x, y, z = serverApi.GetDirFromRot(rot)
            entityFootPos=tuple(Vector3(x,y,z)*entId+Vector3(entityFootPos1))
        elif type(entId)==tuple:
            comp = serverApi.GetEngineCompFactory().CreatePos(entId[0])
            entityFootPos = comp.GetFootPos()
            if entId[1]<self.calculate_distance(entityFootPos,entityFootPos1):
                a=Vector3(entityFootPos[0] - entityFootPos1[0],0,entityFootPos[2] - entityFootPos1[2])
                a.Normalize()
                entityFootPos=tuple(a*entId[1]+Vector3(entityFootPos1[0],entityFootPos1[1],entityFootPos1[2]))
        
        act={}

        def func(k):
            motionComp.SetMotion((x, -0.2,z))
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            pos=entityFootPos[0]+x,entityFootPos[1],entityFootPos[2]+z
            pos1=entityFootPos[0]+x,entityFootPos[1]+1,entityFootPos[2]+z
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, DimensionId)
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict1 = comp.GetBlockNew(pos1, DimensionId)
            rot = serverApi.GetRotFromDir((x, 0, z))
            comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
            comp.SetRot(rot)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesAroundByType(self.entityId, 3, serverApi.GetMinecraftEnum().EntityType.Mob)

            for i in Entities:
                comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                if i==self.entityId or (  CanSee and   not  comp.CanSee(self.entityId,i,5.0,True,60.0,240.0) ):
                    continue
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(sh, serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, self.entityId, None, knocked)
                act[i]=True
            if k*2>pl-jl or (stop_st and act):
                motionComp.ResetMotion()
                if call:
                    call( act if act  else False)
                return
            if blockDict["name"]   in ["minecraft:air","minecraft:water","minecraft:flowing_water"] and blockDict1["name"]   in ["minecraft:air","minecraft:water","minecraft:flowing_water"]:
                self.time_J(0.0,func,k+1)
        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(self.entityId)
        x,z=entityFootPos[0]-entityFootPos1[0],entityFootPos[2]-entityFootPos1[2]
        pl=self.calculate_distance(entityFootPos,entityFootPos1)
        x=x/pl*2
        z=z/pl*2
        func(0)


    def attract_skill(self, entityId,r,atk,sh_jl=False):
        '''#吸引技能'''
        if type(entityId)=='str':
            comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
            if comp.GetPos() == None:
                return
            x0, y0, z0 = comp.GetPos()
            filters = {
            "all_of": [
                    {
                    "subject" : "other",
                    "operator": "!=",
                    "test" :  "is_family",
                    "value" :  "ender_guardian"
                    }
                ]
                }
            comp = serverApi.GetEngineCompFactory().CreateGame(entityId)
            Entities=comp.GetEntitiesAround(entityId, r, filters)
        else:
            x0, y0, z0 =entityId
            comp = serverApi.GetEngineCompFactory().CreateDimension(self.entityId)
            DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
            comp = serverApi.GetEngineCompFactory().CreateGame(leven)
            Entities=comp.GetEntitiesInSquareArea(None, (x0-r, y0-r, z0-r), (x0+r, y0+r, z0+r), DimensionId)
            try:
                Entities.remove(self.entityId)
            except:
                pass
        y0 += 0
        
        playerIdlist = serverApi.GetPlayerList()
        for effect_i in Entities:
            comp = serverApi.GetEngineCompFactory().CreateAttr(effect_i)
            Family=comp.GetTypeFamily()
            comp = serverApi.GetEngineCompFactory().CreatePos(effect_i)
            if comp.GetPos() != None  and "daojv" not in Family:
                x, y, z = comp.GetPos()
                # x1, y1, z1 = x0-x, y0-y, z0-z
                x1, y1, z1 = self.get_unit_vector((x0-x, y0-y, z0-z))

                if atk!=0:
                    key=0

                    if sh_jl:
                        jl=self.calculate_distance((x, y, z),(x0, y0, z0))
                        if jl<sh_jl:
                            key=1
                    else:
                        key=1
                    if key:
                        comp = serverApi.GetEngineCompFactory().CreateHurt(effect_i)
                        comp.Hurt(atk, serverApi.GetMinecraftEnum().ActorDamageCause.Magic, self.entityId, None, False)
                if effect_i in playerIdlist:
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(effect_i)
                    motionComp.SetPlayerMotion((x1/10, y1/5, z1/10))
                else:
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(effect_i)
                    motionComp.SetMotion(
                        (x1/5, y1/5, z1/5))
                pass
    def get_unit_vector(self, args):
        if len(args) == 2:
            rx,rz = args
            if rz == 0:
                rz = 0.01
            if rx == 0:
                rx = 0.01
            Rz = ((rz**2)/(rx**2+rz**2))**0.5
            Rx = Rz*(rx/rz)

            if rz < 0 and Rz > 0:
                Rz = Rz*-1
            elif rz > 0 and Rz < 0:
                Rz = Rz*-1
            if rx < 0 and Rx > 0:
                Rx = Rx*-1
            elif rx > 0 and Rx < 0:
                Rx = Rx*-1
            return (Rx,Rz)
        
        elif len(args) == 3:
            rx,ry,rz = args
            if ry == 0:
                ry = 0.01
            Ry = ((ry**2)/(rx**2+ry**2+rz**2))**0.5
            Rx = (rx*Ry)/ry
            Rz = (rz*Ry)/ry

            if rz < 0 and Rz > 0:
                Rz = Rz*-1
            elif rz > 0 and Rz < 0:
                Rz = Rz*-1
            if rx < 0 and Rx > 0:
                Rx = Rx*-1
            elif rx > 0 and Rx < 0:
                Rx = Rx*-1
            if ry < 0 and Ry > 0:
                Ry = Ry*-1
            elif ry > 0 and Ry < 0:
                Ry = Ry*-1
            return (Rx, Ry, Rz)

    
    def random_skill(self,skill_dict):
        sum_=0
        for i in skill_dict.values():
            sum_+=i
        vars=random.randint(1,sum_)
        sum_1=0
        for i in  skill_dict.keys():
            sum_1+=skill_dict[i]
            if sum_1>=vars:
                return i
    
    def skill_1(self):
        pass
    def skill_2(self):
        pass
    def skill_3(self):
        pass
    def skill_4(self):
        pass
    def skill_5(self):
        pass
    def skill_6(self):
        pass
    def skill_7(self):
        pass
    def skill_8(self):
        pass
    def skill_9(self):
            pass
    def skill_10(self):
            pass
    def skill_11(self):
            pass
    def skill_12(self):
            pass
    def skill_13(self):
            pass
    def skill_14(self):
            pass
    def skill_15(self):
            pass
    def skill_16(self):
            pass
    def skill_17(self):
            pass
    def skill_18(self):
            pass
    def skill_19(self):
            pass
    def skill_20(self):
            pass

    def getArcBlocksAroundEntityWithRadius(self, entityId, radius, angle, limit_radius=0, samples=None):
        """
        获取以实体朝向指定半径指定圆弧角度范围内的方块
        :param entityId: 实体Id
        :param radius: 圆弧半径
        :param angle: 圆弧角度
        :param limit_radius: 起始半径
        :param samples: 取样数量
        :return: (x, z) 坐标列表
        :rtype: list
        """

        def correct_position(pos):
            """矫正坐标位置"""
            x11, y11, z11 = int(pos[0]), int(pos[1]), int(pos[2])
            z02, x02 = 0, 0
            if x11 < 0:
                x02 = -1
            if z11 < 0:
                z02 = -1
            return x11 + x02, y11, z11 + z02

        playerFootPos = compFactory.CreatePos(entityId).GetFootPos()
        x, y, z = playerFootPos
        b_x, b_y, b_z = correct_position((x, y - 1, z))
        playerRot = compFactory.CreateRot(entityId).GetRot()

        blocks = []
        for x_offset in range(-radius, radius + 1):
            for z_offset in range(-radius, radius + 1):
                blocks.append((b_x + x_offset, b_y, b_z + z_offset))

        valid_block_pos = []
        for blockPos in blocks:

            dis = self.calculate_distance((b_x, b_y, b_z), blockPos)
            if dis < limit_radius or dis > radius:
                continue
            res = self.test_pos_is_in_sector((b_x + 0.5, b_y + 0.5, b_z + 0.5), angle, playerRot[1], blockPos)
            if res:
                valid_block_pos.append((blockPos[0]-b_x, blockPos[2]-b_z))

        if samples is not None:
            if not isinstance(samples, (int, long)):
                raise TypeError("采样数必须为整数。")
            valid_block_pos = random.sample(valid_block_pos, min(len(valid_block_pos), samples))

        return valid_block_pos

    def calculate_vector_player_to_entity(self,playerPos, entityPos):
        """
        计算从玩家指向某一实体的单位向量。

        :param playerPos: 玩家坐标
        :param entityPos: 实体坐标
        :return: 向量元组
        """
        if not playerPos or not entityPos:
            return None
        if len(playerPos) == len(entityPos):
            vector = []
            for i in range(len(playerPos)):
                vector.append(entityPos[i] - playerPos[i])
            length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])
            if length:
                company = 1 / length
                newVector = (vector[0] * company, vector[1] * company, vector[2] * company)
                return newVector
            else:
                return 0, 0, 0

    def calculate_vector_rotation(self,vector, xAngle, yAngle, zAngle):
        """
        计算向量旋转。

        :param vector: 向量
        :param xAngle: 绕x轴的旋转角度
        :param yAngle: 绕y轴的旋转角度
        :param zAngle: 绕z轴的旋转角度
        :return: 旋转后的向量
        """
        x1 = vector[0]
        y1 = vector[1]
        z1 = vector[2]
        x3 = x1 * math.cos(zAngle) - y1 * math.sin(zAngle)
        y3 = x1 * math.sin(zAngle) + y1 * math.cos(zAngle)
        z3 = z1
        z4 = z3 * math.cos(yAngle) - x3 * math.sin(yAngle)
        x4 = z3 * math.sin(yAngle) + x3 * math.cos(yAngle)
        y4 = y3
        y2 = y4 * math.cos(xAngle) - z4 * math.sin(xAngle)
        z2 = y4 * math.sin(xAngle) + z4 * math.cos(xAngle)
        x2 = x4
        return x2, y2, z2


    def test_pos_is_in_sector(self, vertexPos, sectorAngle, sectorBisectorAngle, testPos):
        """
        判断给定坐标是否在扇形区域内。

        :param vertexPos: 扇形顶点坐标
        :param radius: 扇形半径
        :param sectorAngle: 扇形张开的角度(=180)
        :param sectorBisectorAngle: 扇形角平分线所在直线在直角坐标系中的角度
        :param testPos: 待测试的坐标
        :return: 在扇形区域内则返回True，否则返回False
        """
        if sectorAngle > 360:
            sectorAngle = 360
        elif sectorAngle < 0:
            sectorAngle = 0
        dx = testPos[0] - vertexPos[0]
        dz = testPos[2] - vertexPos[2]
        testPosAngle = -math.degrees(math.atan2(dx, dz))
        minAngle = sectorBisectorAngle - sectorAngle / 2
        maxAngle = sectorBisectorAngle + sectorAngle / 2
        rangeList = []
        if sectorBisectorAngle < 0:
            if minAngle < -180:
                rangeList.append((-360, maxAngle))
                rangeList.append((360 - abs(minAngle), 360))
            else:
                rangeList.append((minAngle, maxAngle))
        else:
            if maxAngle > 180:
                rangeList.append((minAngle, 360))
                rangeList.append((-360, -360 + maxAngle))
            else:
                rangeList.append((minAngle, maxAngle))
        for r in rangeList:
            if r[0] <= testPosAngle <= r[1]:
                return True
        return False

    
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
    
    def skill_jn(self,name,time,stort=None):  #怪物技能选择
        self.serverapi.entity_boss_jl[self.entityId]=True
        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(self.entityId)
        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        if  entitycomp.GetExtraData("die") or comp.GetAttr('skill'):
            return

        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        self.setskill(True)

        def skilluse(name):
            if self.entityId  in self.serverapi.die_list[0]:
                return
            if name=="skill_use1":
                self.skill_1()
            elif name=="skill_use2":
                self.skill_2()
            elif name=="skill_use3":
                self.skill_3()
            elif name=="skill_use4":
                self.skill_4()
            elif name=="skill_use5":
                self.skill_5()
            elif name=="skill_use6":
                self.skill_6()
            elif name=="skill_use7":
                self.skill_7()
            elif name=="skill_use8":
                self.skill_8()
            elif name=="skill_use9":
                self.skill_9()
            elif name=="skill_use10":
                self.skill_10()
            elif name=="skill_use11":
                self.skill_11()
            elif name=="skill_use12":
                self.skill_12()
            elif name=="skill_use13":
                self.skill_13()
            elif name=="skill_use14":
                self.skill_14()
            elif name=="skill_use15":
                self.skill_15()
            elif name=="skill_use16":
                self.skill_16()
            elif name=="skill_use17":
                self.skill_17()
            elif name=="skill_use18":
                self.skill_18()
            elif name=="skill_use19":
                self.skill_19()
            elif name=="skill_use20":
                self.skill_20()
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp =CompFactory.CreateEntityEvent(self.entityId)
        comp.TriggerCustomEvent(self.entityId,name)

        comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(self.entityId)
        result = comp.SetMarkVariant(int(name.replace("skill_use","")))

        
        if stort:
            if len(name)>10:
                t=stort[int(name[-2:])-1]
            else:
                t=stort[int(name[-1:])-1]
            comp = CompFactory.CreateGame(leven)
            jntime[self.entityId].append(comp.AddTimer(t,skilluse,name) )
        else:
            skilluse(name)

    
        comp = CompFactory.CreateGame(leven)
        if len(name)>10:
            s=time[int(name[-2:])-1]
        else:
            s=time[int(name[-1])-1]
        def w():
            if self.entityId  in self.serverapi.die_list[0]:
                return
            comp1.SetBlockControlAi(True, False)
        def w1():
            self.romve_skill(name)
        try:
            jntime[self.entityId].append(comp.AddTimer(s,w))
            jntime[self.entityId].append(comp.AddTimer(s,w1))
        except:
            jntime[self.entityId].append(comp.AddTimer(s,w))
            self.romve_skill(name)
    def use(self):
        pass

    def romve_skill(self,key='not'):
        if self.entityId  in self.serverapi.die_list[0]:
            return
        if "异常" in key  or "死亡" in key or "组合" in key:
            comp = CompFactory.CreateGame(leven)
            for i in jntime[self.entityId]:
                comp.CancelTimer(i)
            jntime[self.entityId]=[]
            
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(True, False)
        self.serverapi.entity_boss_jl[self.entityId]=False
        if "组合"   not in key:
            comp = CompFactory.CreateEntityEvent(self.entityId)
            comp.TriggerCustomEvent(self.entityId,"romve_skill")
            comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(self.entityId)
            result = comp.SetMarkVariant(0)

        comp1 = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        if key=='ack':
            def f():
                self.setskill(False,'ack')
                if random.randint(1,3)!=1:
                    self.use()
            jntime[self.entityId].append(comp1.AddTimer(0.5,f))
        elif "异常"   in key:
            jntime[self.entityId].append(comp1.AddTimer(0.8,self.setskill,False,'异常')  )
        elif "死亡"   in key:
            self.setskill(False,'死亡',key)
        elif "组合"   in key:
            print "skill_use"+key.split(":")[-1]
            self.setskill(False,'组合')
            if key.split(":")[-1]!='None':
                sk="skill_use"+key.split(":")[-1]
                self.skill_jn_use(sk)
            
        else:
            jntime[self.entityId].append(comp1.AddTimer(0.0,self.setskill,False,'死亡',key)  )
     
    def skill_jn_use(self,k):
        pass

    def setskill(self,key,name='',l=""):
        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(self.entityId)
        if  entitycomp.GetExtraData("die") and key==False:
            return
        
        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        comp.SetAttr('skill',key)

        # print comp.GetAttr('skill'),574567456,key


    def start_die(self):
        '''开始死亡'''
        pass
        
    def use_stage_tz(self,time):
        '''阶段状态'''
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,self.romve_skill,"死亡") 
        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        self.setskill(True)

        comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(self.entityId)
        comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp1.AddTimer(0.0,comp.SetMarkVariant,1000)
        

        


    def die_wp(self):
        '''死亡逻辑'''
        self.serverapi.die_list[1].append(self.entityId)

        comp = serverApi.GetEngineCompFactory().CreateEffect(self.entityId)
        comp.AddEffectToEntity("invisibility", 3, 0, False )
        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(False)
        
        def f():
            comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
            comp.Hurt(10000, serverApi.GetMinecraftEnum().ActorDamageCause.NONE, self.shid, None, False)
            self.serverapi.die_list[0].remove(self.entityId)
        comp1 = serverApi.GetEngineCompFactory().CreateGame(leven)
        comp1.AddTimer(0.0,f)


    def ack_time(self,endtime,acktime,call):
        '''攻击开始及及结束'''

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(self.entityId)
        result = comp.SetMarkVariant(200)
        comp = serverApi.GetEngineCompFactory().CreateModAttr(self.entityId)
        self.setskill(True)

        comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
        jntime[self.entityId].append(comp1.AddTimer(endtime,self.romve_skill,'ack') )
        jntime[self.entityId].append(comp1.AddTimer(acktime,call) )

    

    def calculate_rot_player_to_entity(self,playerPos, entityPos):
        """
        计算从玩家指向某一实体的向量角度。

        :param playerPos: 玩家坐标
        :param entityPos: 实体坐标
        :return: 水平角度，垂直角度
        """
        if not playerPos or not entityPos:
            return None
        x = entityPos[0] - playerPos[0]
        if not x:
            x = 0.000000001
        y = entityPos[1] - playerPos[1]
        z = entityPos[2] - playerPos[2]
        horiDis = self.calculate_distance((entityPos[0], entityPos[2]), (playerPos[0], playerPos[2]))
        horiDis = horiDis if horiDis else 0.000000001
        horizontalRot = (math.atan(z / x) / math.pi) * 180
        verticalRot = (math.atan(y / horiDis) / math.pi) * 180 * (-1 if x < 0 else 1)
        return horizontalRot, verticalRot    

    def calculate_random_pos_in_area(self,centerPos, grid, useTopBlockHeight=False, dimension=0):
        """
        在指定区域内随机获取一点坐标。

        :param centerPos: 区域中心点坐标
        :param grid: 区域半径（格数）
        :param useTopBlockHeight: 是否以最高的非空气方块的高度作为返回坐标的Y值
        :param dimension: 维度
        :return: 坐标元组
        """
        ranX = random.randint(-grid, grid)
        ranZ = random.randint(-grid, grid)
        x = centerPos[0] + ranX
        z = centerPos[2] + ranZ
        if useTopBlockHeight:
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
            y = comp.GetTopBlockHeight((x, z), dimension)
            if y:
                return x, y, z
            else:
                return None
        else:
            ranY = random.randint(-grid, grid)
            y = centerPos[1] + ranY
            return x, y, z

    def time_J(self,time,func,*args):
        comp = CompFactory.CreateGame(leven)
        comp.AddTimer(time,func,*args) 
    
    def set_block(self,pos, dimensionId):
        '''设置方块为空气'''
        if self.serverapi.set_data.get("0"):
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimensionId)
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict1 = comp.GetBlockBasicInfo(blockDict['name'])
            if blockDict1["destroyTime"]>12 or blockDict1["destroyTime"]==-1:
                return
            blockDict = {
                'name': "minecraft:air",
                'aux': 0
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict, 0, dimensionId)

    def xlfangk(self,all_pos,entityFootPos):
        '''虚拟方块'''
        def func1(pos_):
            if random.randint(0,15)==1 and self.EngineTypeStr=="zaibian:ignis" and self.serverapi.set_data.get("1"):
                self.set_block(pos_,dimensionId)
        def func(entityId1):
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId1)
            motionComp.SetMotion((0 ,-0.5,0 ))

        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        blockPos=(entityFootPos[0],entityFootPos[1],entityFootPos[2])
        p=-1
        for x_,y_ in all_pos:
            if self.serverapi.set_data.get("5") <=random.randint(0,100):
                continue

            p+=1            
            def oi(x_,y_):
                x1, y1, z1 = blockPos[0]+int(x_),blockPos[1]-1,blockPos[2]+int(y_)
                x2, y2, z2 = blockPos[0]+int(x_),blockPos[1]-1,blockPos[2]+int(y_)
                func1((x1, y1, z1 ))
                blockComp = compFactory.CreateBlock(self.entityId)
                palette = blockComp.GetBlockPaletteBetweenPos(dimensionId, (x1, y1, z1), (x2, y2, z2))
                if palette is not None:
                    eventData ={}
                    # 创建一个实体，直到实体真正生成为止
                    entityId = self.serverapi.CreateEngineEntityByTypeStr('withered:withered_block', (x1, y1, z1), (0, 0), dimensionId)
                    if entityId:
                        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(leven)
                        # 将区域置为空气
                        eventData['entityId'] = entityId
                        eventData['pos'] = blockPos
                        # 序列化方块调色板数据
                        eventData['palette'] = palette.SerializeBlockPalette()
                        self.serverapi.BroadcastToAllClient( "block_entity", eventData)
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
                        motionComp.SetMotion((0 ,0.3+random.uniform(-0.05,0.05),0 ))
                        comp = serverApi.GetEngineCompFactory().CreateGame(leven)
                        comp.AddTimer(0.6,func,entityId)
                        comp = serverApi.GetEngineCompFactory().CreateGame(leven)
                        comp.AddTimer(1.05,self.serverapi.DestroyEntity,entityId)
            if p*0.01<1:
                comp = serverApi.GetEngineCompFactory().CreateGame(leven)
                comp.AddTimer(p*0.01,oi,x_,y_)
        
    def calculate_circle_points(self,radius):
        import math
        points = []
        
        for angle in range(0, 361, 20): # 每隔5度取一个点作为示例
            radian = math.radians(angle) # 将角度转换成弧度
            
            x = radius * math.cos(radian) # 根据三角函数计算x坐标
            y = radius * math.sin(radian) # 根据三角函数计算y坐标
            
            point = (round(x), round(y)) # 四舍五入并保存结果
            points.append(point)
        
        return points
    

    def block_del(self,minpos,maxpos,dim,not_del_block=[],liquid=False):
        """破坏方块"""
        for x in xrange(int(minpos[0]),int(maxpos[0])):
            for y in xrange(int(minpos[1]),int(maxpos[1])):
                for z in xrange(int(minpos[2]),int(maxpos[2])):
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(leven)
                    blockDict = comp.GetBlockNew((x, y, z), dim)
                    key=False
                    if liquid:
                        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(leven)
                        liquidBlockDict = comp.GetLiquidBlock((x, y, z), dim)
                        if liquidBlockDict:
                            key=True
                    if not blockDict["name"] in not_del_block and blockDict["name"] !="minecraft:air" and not  key:
                        self.set_block((x, y, z),dim)