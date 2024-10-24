# -*- coding: utf-8 -*-
#
import mod.server.extraServerApi as serverApi
import zaibian.modCommon.modConfig as modConfig
import zaibian.modCommon.storage as storage

from zaibian.modCommon.moster.moster_G import moster
import zaibian.modCommon.moster.moster_G as moster1
import random,math,copy

from mod.common.utils.mcmath import Vector3

minecraftEnum = serverApi.GetMinecraftEnum()
zb_zuantai={#名字 时间  强度(装备)  #当准备加成
    "zaibian:ignitium_elytra_chestplate":[["y_elytra",16,1]],
}

# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
levelId=serverApi.GetLevelId()
# 在modMain中注册的Server System类
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()
CF = serverApi.GetEngineCompFactory()


class ServerSystem(serverApi.GetServerSystemCls()):
    def __init__(self, namespace, name):
        super(ServerSystem, self).__init__(namespace, name)
        # 初始时调用监听函数监听事件
        self.ListenEvent()
        self.baozhajl={}
        storage.set_serverapi(self) 
        self.stage={}  

        self.die_list=[[],[]]#0 即将死亡  1 可以死亡


        self.set_data=None#设置信息

        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(levelId)
        stucture_data=entitycomp.GetExtraData("stucture_bc")
        if stucture_data:
            self.stucture=stucture_data
        else:
            self.stucture={} #x y
        self.bolck_time={}
        self.tick=0
        self.block_data={}

        self.item_tiem={}

        self.seep_wq={
            "zaibian:the_incinerator":0.8,
            "zaibian:void_forge":0.8,
            "zaibian:coral_bardiche":0.8,
            "zaibian:infernal_forge":1.2,
            "zaibian:coral_spear":1.1,
            "zaibian:zweiender":1.6,
            "zaibian:gauntlet_of_guard":1.3,
            "zaibian:gauntlet_of_bulwark":1.3,
            "zaibian:athame":2

        }


        self.ip={'zaibian:monstrous_eye':['xiajie_features5',1,'zaibian:xiajie_5'],
                 'zaibian:void_eye':['modi_features33',2,'zaibian:modi_1'],
                 'zaibian:mech_eye':['diaoling_features25',0,'zaibian:diaoling_1'],
                 'zaibian:abyss_eye':['sunken_features1',0,'zaibian:sunken_1'],

                 'zaibian:desert_eye':['cursed_pyramid_features1',0,'zaibian:cursed_pyramid_1'],


                 'zaibian:flame_eye':['xiajie1_features12',1,'zaibian:xiajie1_1'],
                 }
        comp = serverApi.GetEngineCompFactory().CreateFeature(levelId)
        for i in self.ip:
            w=self.ip[i][2]
            comp.AddNeteaseFeatureWhiteList(w)

        self.fangbao=set()

        serverApi.AddEntityTickEventWhiteList('zaibian:soulian')
        serverApi.AddEntityTickEventWhiteList('zaibian:abyss_mark')

        serverApi.AddEntityTickEventWhiteList('zaibian:item')

        serverApi.AddEntityTickEventWhiteList('zaibian:abyss_blast_portal')


    
        
        for i in moster1.boss:
            serverApi.AddEntityTickEventWhiteList(i)

        
        
        self.data_init={}
        self.st_tick={}
        self.entity_boss_atk={} #boss最后一下
        self.entity_boss_jl={} #实体记录
        
        self.tick_block_data={}
        self.block_data_sx={}  #展示台是否显示

        self.liweitan_wd={}  #利维坦无敌

        self.damagelist1 = {}
        self.zb_xq={} #玩家装备情况


        self.playerid_sneaking={} #记录玩家潜行状态  [是否潜行，冷却时间，上次状态]

        self.sheji={}  #射击


        self.zidan={}  #存储子弹


        



    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):        
        #描述触发时机：玩家使用盾牌抵挡伤害之后触发
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlaceNeteaseStructureFeatureEvent", self, self.PlaceNeteaseStructureFeatureEvent) #首次生成地形时，结构特征即将生成时服务端抛出该事件。
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "BlockStrengthChangedServerEvent", self, self.BlockStrengthChangedServerEvent) #首次生成地形时，结构特征即将生成时服务端抛出该事件。
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnNewArmorExchangeServerEvent", self, self.OnNewArmorExchangeServerEvent) #
        
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "RemoveEffectServerEvent", self, self.RemoveEffectServerEvent) #
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "BlockRemoveServerEvent", self, self.BlockRemoveServerEvents)

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityStopRidingEvent", self, self.EntityStopRidingEvent) #
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ActuallyHurtServerEvent", self, self.ActuallyHurtServerEvent) #

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "StartRidingServerEvent", self, self.StartRidingServerEvent) #
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnMobHitBlockServerEvent", self, self.OnMobHitBlockServerEvent) #

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerBlockUseEvent", self, self.ServerBlockUseEvent) #
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnCarriedNewItemChangedServerEvent", self, self.OnCarriedNewItemChangedServerEvent) #
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "FallingBlockReturnHeavyBlockServerEvent", self, self.FallingBlockReturnHeavyBlockServerEvent) #

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DestroyBlockEvent",
                                   self, self.DestroyBlockEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityPlaceBlockAfterServerEvent",
                                   self, self.EntityPlaceBlockAfterServerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PistonActionServerEvent",
                                   self, self.PistonActionServerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ExplosionServerEvent",
                                   self, self.ExplosionServerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnGroundServerEvent",
                                   self, self.OnGroundServerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "WillTeleportToServerEvent", self, self.WillTeleportToServerEvents)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerEntityTryPlaceBlockEvent", self, self.ServerEntityTryPlaceBlockEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.ServerChatEvent)

        # #客户端通信事件
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "void_core_jn", self, self.void_core_jn)  #虚空核心
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "gauntlet_of_guardJn", self, self.gauntlet_of_guardJn)  #守卫者护手
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "use_animation", self, self.use_animation)  #播放动画

        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "tb_animation", self, self.tb_animation)  #同步物品动画
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "boss_artk", self, self.boss_artk)  #boss范围攻击

        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "data_event", self, self.data_event)  #数据传输

        self.ListenForEvent("setmod_yf", "setmod_yftem", "change_data_yf", self, self.change_data_yf)


    def ServerChatEvent(self,args):
        playerId=args["playerId"]
        message=args["message"]
        if "mcs " in message:
            self.NotifyToClient(playerId,'ServerChatEvent',message[4:])
        comp = serverApi.GetEngineCompFactory().CreateScale(playerId)
        result = comp.SetEntityScale(playerId, int(message))
                
    def OnMobHitBlockServerEvent(self,args):
        entityId=args["entityId"]

        comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        TypeStr=comp.GetEngineTypeStr()
        comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
        if comp.GetAttr('sun'):
            comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
            res = comp.AddEffectToEntity("stun", 2, 0, True)



                        
    def ServerEntityTryPlaceBlockEvent(self,data):
        fullName = data.get("fullName")
        entityId = data['entityId']
        if fullName =="zaibian:stone_pillar":
            face = data['face']
            if face in [0, 1]:
                pass
            else:
                aux = {3: 2, 5: 3, 2: 0, 4: 1}[face]
                newName = fullName + '1'
                data['cancel'] = True
                blockPos = (data.get("x"), data.get("y"), data.get("z"))
                dimensionId = data.get("dimensionId")
                blockInfoComp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                blockInfoComp.SetBlockNew(blockPos, {'name': newName, 'aux': aux}, 0, dimensionId)
                self.deleteCarriedItems(data['entityId'])

    def deleteCarriedItems(self, playerId, count=1):
        gameType_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        gameType = gameType_comp.GetPlayerGameType(playerId)
        if gameType==1:
            return
        
        itemComp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        slotItem = itemComp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, True)
        if slotItem is not None:
            if slotItem['count'] > count:
                slotItem['count'] = slotItem['count'] - count
                itemComp.SpawnItemToPlayerCarried(slotItem, playerId)
            else:
                itemComp.SpawnItemToPlayerCarried({'newItemName': 'minecraft:air', 'newAuxValue': 0, 'count': 0},
                                                  playerId)

    def FallingBlockReturnHeavyBlockServerEvent(self,args):
        pos=args["blockX"],args["blockY"],args["blockZ"]
        dimensionId=args["dimensionId"]
        if args["heavyBlockName"]=='zaibian:sandstone_falling_trap1':
            blockDict = {
                'name': 'zaibian:sandstone_falling_trap',
                'aux': 0
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict, 0, dimensionId)
        elif args["heavyBlockName"]=='zaibian:ancient_desert_stele':
            blockDict = {
                'name': 'minecraft:air',
                'aux': 0
            }
            
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict, random.randint(0,1), dimensionId)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)

       
            list_=comp.GetEntitiesInSquareArea(None, (pos[0]-1,pos[1]-1,pos[2]-1), (pos[0]+1,pos[1]+1,pos[2]+1), dimensionId)
            for i in list_:
                comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                Family=comp.GetTypeFamily()
                if Family and "desert" not in Family:
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(13, serverApi.GetMinecraftEnum().ActorDamageCause.FallingBlock, None, None, False)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("curse_of_desert", 5, 0, False)

    def change_data_yf(self,args):
        if args["mod_id"]=="zaibian_yf":
            if args["data"].get("3")!=None:
                comp = serverApi.GetEngineCompFactory().CreateExtraData(levelId)
                comp.SetExtraData("zaibian_yf_3",args["data"]["3"])
            self.set_data=args["data"]
            self.BroadcastToAllClient("tb_data",args["data"])


 

    def BlockRemoveServerEvents(self, args):
        #  方块被破坏时掉落物品展示台里面的物品
        fullName = args['fullName']
        x,y,z = args['x'],args['y'],args['z']
        dimensionId = args['dimension']
        if fullName in "zaibian:miss":
            entityid = CF.CreateGame(levelId).GetEntitiesInSquareArea(None, (x, y, z), (x + 1, y + 1, z + 1), dimensionId)
            if entityid:
                self.DestroyEntity(entityid[0])
            compentityblock = CF.CreateBlockEntityData(levelId)
            blockdata = compentityblock.GetBlockEntityData(dimensionId, (x, y, z))
            if blockdata["item"]:
                self.CreateEngineItemEntity(blockdata["item"], dimensionId, (x+0.5, y+1.2, z+0.5))


    def data_event(self,args):
        key=args["key"]
        if key=="amethyst_crab_meat":
            pos=args["pos"]
            itemDict=args["item"]
            blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
            blockEntityData = blockEntitycomp.GetBlockEntityData(pos[1], pos[0])
            self.BroadcastToAllClient('zhaohuan',{'data':"jian","dim":pos[1],"itemDict":itemDict,'pos':pos[0],'key':'altar_of_amethyst'})
            self.BroadcastToAllClient('zhaohuan',{'data':"add","dim":pos[1],"itemDict":itemDict,'pos':pos[0],'key':'altar_of_amethyst'})
            blockEntityData["data"]=itemDict
    

  
        
        
    def OnGroundServerEvent(self,args):
        id=args['id']
        comp = serverApi.GetEngineCompFactory().CreateEngineType(id)
        EngineType=comp.GetEngineTypeStr()
        if EngineType=="zaibian:ignis":
            comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
            if comp.GetAttr("skill_2"):
                comp.SetAttr("skill_2",False)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesAroundByType(id, 9, serverApi.GetMinecraftEnum().EntityType.Mob)
                if id in Entities :
                    Entities.remove(id )
                comp = serverApi.GetEngineCompFactory().CreatePos(id)
                entityFootPos = comp.GetFootPos()
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(random.randint(15,20), serverApi.GetMinecraftEnum().ActorDamageCause.Contact,id, None, True)
                self.BroadcastToAllClient('zhaohuan',{'pos':entityFootPos,'key':'ignis',"data":"skill3"})

                def func(entityId1):
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId1)
                    motionComp.SetMotion((0 ,-0.5,0 ))
            
                comp = serverApi.GetEngineCompFactory().CreatePos(id)
                entityFootPos = comp.GetFootPos()
                dimensionComp = compFactory.CreateDimension(id)
                dimensionId = dimensionComp.GetEntityDimensionId()
                
                def fo(l):   
                    st=[[0,3],[3,6],[6,9]]             
                    all_pos=[]

                    for i in range(40):
                        if random.randint(0,1)==1:
                            x=random.uniform(st[l][0],st[l][1])
                        else:
                            x=random.uniform(-st[l][1],st[l][0])
                        if random.randint(0,1)==1:
                            z=random.uniform(st[l][0],st[l][1])
                        else:
                            z=random.uniform(-st[l][1],st[l][0])
                        all_pos.append([x,z])

                    blockPos=(entityFootPos[0],entityFootPos[1],entityFootPos[2])
                    for x_,y_ in all_pos:
                        x1, y1, z1 = blockPos[0]+int(x_),blockPos[1]-1,blockPos[2]+int(y_)
                        x2, y2, z2 = blockPos[0]+int(x_),blockPos[1]-1,blockPos[2]+int(y_)
                        blockComp = compFactory.CreateBlock(id)
                        palette = blockComp.GetBlockPaletteBetweenPos(dimensionId, (x1, y1, z1), (x2, y2, z2))
                        if palette is not None:
                            eventData ={}
                            # 创建一个实体，直到实体真正生成为止
                            entityId = self.CreateEngineEntityByTypeStr('withered:withered_block', (x1, y1, z1), (0, 0), dimensionId)
                            if entityId:
                                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                                # 将区域置为空气
                                eventData['entityId'] = entityId
                                eventData['pos'] = blockPos
                                # 序列化方块调色板数据
                                eventData['palette'] = palette.SerializeBlockPalette()
                                self.BroadcastToAllClient( "block_entity", eventData)
                                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
                                motionComp.SetMotion((0 ,0.3,0 ))
                                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                                comp.AddTimer(0.6,func,entityId)
                                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                                comp.AddTimer(1.05,self.DestroyEntity,entityId)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    Entities=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-10,entityFootPos[1]-2,entityFootPos[2]-10), (entityFootPos[0]+10,entityFootPos[1]+2,entityFootPos[2]+10), dimensionId)
                    for i in Entities:
                        if i==id:
                            continue
                        comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                        comp.SetCommand("/camerashake add @s 0.2 1 rotational ",i)
                for i in range(3):
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(0.3*i,fo,i)

        elif EngineType=="minecraft:item" :
            comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
            id1=comp.GetAttr('id')
            if id1:
                comp = serverApi.GetEngineCompFactory().CreatePos(id1)
                entityFootPos = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreatePos(id)
                comp.SetFootPos(entityFootPos)



    def OnCarriedNewItemChangedServerEvent(self,args):
        newItemDict=args['newItemDict']
        playerId=args['playerId']
        comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
        if newItemDict :
            if self.seep_wq.get(newItemDict["newItemName"]):
                comp.SetPlayerAttackSpeedAmplifier(self.seep_wq.get(newItemDict["newItemName"]))
            else:
                comp.SetPlayerAttackSpeedAmplifier(1)
        comp.SetPlayerAttackSpeedAmplifier(1)


        





    def StartRidingServerEvent(self,args):
        victimId=args["victimId"]
        comp = serverApi.GetEngineCompFactory().CreateEngineType(victimId)
        EngineTypeStr=comp.GetEngineTypeStr()

        if self.data_init.get("cz_list"):
           if victimId in self.data_init["cz_list"]:
               self.data_init["cz_list"].remove(victimId)
               return
        if EngineTypeStr=="zaibian:ignis":
            args["cancel"]=True


    
                                

    def EntityStopRidingEvent(self,args):
        '''触发时机：当实体停止骑乘时'''
        id=args["id"]
        comp = serverApi.GetEngineCompFactory().CreateEngineType(id)
        EngineTypeStr=comp.GetEngineTypeStr()
        if EngineTypeStr=="zaibian:ignited_revenant1":
            self.DestroyEntity(id)
        
    def RemoveEffectServerEvent(self,args):
        entityId=args["entityId"]
        effectName=args["effectName"]
        comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        EngineTypeStr=comp.GetEngineTypeStr()
        if  effectName=="invisibility" and EngineTypeStr in  moster1.mosters.keys():
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if entitycomp.GetExtraData("die"):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.KillEntity(entityId)

    def boss_artk(self,args):
        name=args["name"]
        pos=args["pos"]
        playerId=args["playerId"]
        dimId=args["dimId"]
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        entis=comp.GetEntitiesInSquareArea(None, (pos[0]-2,pos[1]-3,pos[2]-2), (pos[0]+2,pos[1]+3,pos[2]+2), dimId)
        for i in entis:
            comp = serverApi.GetEngineCompFactory().CreateEngineType(i)
            TypeStr=comp.GetEngineTypeStr()
            if TypeStr =="zaibian:deepling_angler":
                entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(i)
                k=entitycomp.GetExtraData("skill")
                if k==None:
                    k=0
                if k==3:
                    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(i)
                    comp.TriggerCustomEvent(i,"skill_use4")
                    k+=1
                elif k>=4:
                    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(i)
                    comp.TriggerCustomEvent(i,"skill_use0")
                    k=1
                else:
                    k+=1
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0,entitycomp.SetExtraData,"skill",k)

            elif TypeStr==name:
                args["entityId"]=i
                args["EngineTypeStr"]=name
                moster.use_attack(args)
                break
                
            
                


    def OnNewArmorExchangeServerEvent(self,args):
        oldArmorDict=args["oldArmorDict"]
        newArmorDict=args["newArmorDict"]
        playerId=args["playerId"]
        slot=args["slot"]
        comp = serverApi.GetEngineCompFactory().CreateAttr(playerId)
        if newArmorDict and newArmorDict["newItemName"]== "zaibian:ignitium_boots":
            # 如果设置的值超过属性当前的最大值，需要先扩充该属性的最大值，否则不生效。
            o=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.LAVA_SPEED)
            comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.LAVA_SPEED, 0.1)
            comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.LAVA_SPEED,0.1)
        elif oldArmorDict and oldArmorDict["newItemName"]== "zaibian:ignitium_boots":
            o=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.LAVA_SPEED)
            comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.LAVA_SPEED, o-0.08)
            comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.LAVA_SPEED, o-0.08)

        if not self.zb_xq.get(playerId):
            self.zb_xq[playerId]={}
        zb=None
        if newArmorDict:
            zb=newArmorDict["newItemName"]
        self.zb_xq[playerId][slot]=zb
        

        if self.damagelist1.get(playerId):
            self.damagelist1[playerId].update({args["slot"]:newArmorDict})
        else:
            self.damagelist1[playerId]={args["slot"]:newArmorDict}

        if  oldArmorDict and  oldArmorDict["newItemName"] in zb_zuantai.keys():
            comp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
            zt=comp.GetAllEffects()
            p={}
            for i in zt:
                p[i["effectName"]]=i["duration"]
            for i in zb_zuantai[oldArmorDict["newItemName"]]:
                name=i[0]
                if p[name]<17:
                    res = comp.RemoveEffectFromEntity(name)
            

   

        

    

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




                                
  

    


    def WillTeleportToServerEvents(self, args):
        # 阻止物品实体被传送走。
        entityId = args['entityId']
        entityStr = CF.CreateEngineType(entityId).GetEngineTypeStr()
        if entityStr == 'zaibian:emiss':
            args['cancel'] = True    

 
    def tb_animation(self,args):
        playerId=args['playerId']
        comp = serverApi.GetEngineCompFactory().CreateDimension(playerId)
        dim=comp.GetEntityDimensionId()

        if  args['key']=='yidong':
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(playerId)
            motionComp.SetPlayerMotion(args["motion"])

            
        if  args['key']=='tidal_claws':
            comp = compFactory.CreatePos(playerId)
            pos = comp.GetPos()
            if  args['data']!="gj":
                rot = serverApi.GetEngineCompFactory().CreateRot(playerId).GetRot()
                comp = compFactory.CreateProjectile(serverApi.GetLevelId())
                from_rot=serverApi.GetDirFromRot(rot)
                param = {
                        'power':3,
                        'position': pos,
                        'direction': (from_rot[0],from_rot[1],from_rot[2]),
                    }
                id = comp.CreateProjectileEntity(playerId, "zaibian:soulian", param)
                comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                comp.SetAttr('playerId', playerId)
                comp.SetAttr('position', pos)
                comp.SetAttr('direction', from_rot)

                if not self.data_init.get("tidal_claws"):
                    self.data_init["tidal_claws"]={}
                self.data_init["tidal_claws"][playerId]=id
        
                def io():
                    comp =serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                    comp.TriggerCustomEvent(id,"skill_use1")
            
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0.1,io)
            else:
                if   self.data_init.get("soulian1") and  self.data_init["soulian1"].get(playerId):
                    return
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                list_=comp.GetEntitiesAroundByType(playerId, 13, serverApi.GetMinecraftEnum().EntityType.Mob)

                stid=None
                stjl=99
                stid1=None
                
                                
                for i in list_:
                    comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                    TypeFamily=comp.GetTypeFamily()
                    comp = serverApi.GetEngineCompFactory().CreateGame(playerId)
                    if i!=playerId and    comp.CanSee(playerId,i,16.0,True,360.0,360.0) and   "pet_mob" not in  TypeFamily:
                        comp = serverApi.GetEngineCompFactory().CreatePos(i)
                        pos1 = comp.GetFootPos()
                        jl=self.calculate_distance(pos,pos1)
                        if stjl>jl:
                            stjl=jl
                            # comp = serverApi.GetEngineCompFactory().CreateCollisionBox(i)
                            # size=comp.GetSize()

                            stid=pos1[0],pos1[1],pos1[2]
                            stid1=i

                    
                if stid:
                    rot = serverApi.GetEngineCompFactory().CreateRot(playerId).GetRot()
                    comp = compFactory.CreateProjectile(serverApi.GetLevelId())
                    from_rot=serverApi.GetDirFromRot(rot)
                    comp = compFactory.CreateProjectile(serverApi.GetLevelId())
                    param = {
                            'power':0.11,
                            'position': pos,
                            'direction': from_rot,
                        }
                    id = comp.CreateProjectileEntity(playerId, "zaibian:soulian1", param)
                    self.BroadcastToAllClient('zhaohuan',{'key':'soulian1',"id": id})

                    if not  self.data_init.get("soulian1"):
                        self.data_init["soulian1"]={}
                    self.data_init["soulian1"][playerId]=id

                    comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                    comp.SetAttr('playerId', playerId)
                    def gongji(k,pos,hdlist,scid):


                        if k==6:
                            self.data_init["soulian1"][playerId]=None
                            self.DestroyEntity(id)
                            return
                        if not pos:
                            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                            list_=comp.GetEntitiesAroundByType(id, 2, serverApi.GetMinecraftEnum().EntityType.Mob)
                            if scid in  list_:
                                comp = serverApi.GetEngineCompFactory().CreateHurt(scid)
                                comp.Hurt(3, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, playerId, None, True)
                                comp = serverApi.GetEngineCompFactory().CreateEffect(scid)
                                effectDictList = comp.GetAllEffects()
                                dj=0
                                if effectDictList:
                                    for i in effectDictList:
                                        if i["effectName"]=="abyssal_curse":
                                            dj=i["amplifier"]+1
                                            if dj>4:
                                                dj=4
                                            break
                                comp = serverApi.GetEngineCompFactory().CreateEffect(scid)
                                res = comp.AddEffectToEntity("abyssal_curse", 8, dj, True)
                            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                            list_=comp.GetEntitiesAroundByType(id, 8, serverApi.GetMinecraftEnum().EntityType.Mob)
                            pos=None
                            stjl=99
                            for i in list_:
                                comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                                TypeFamily=comp.GetTypeFamily()
                                comp = serverApi.GetEngineCompFactory().CreateGame(id)
                                
                                if i!=id   and i not in hdlist and "pet_mob" not in  TypeFamily:
                                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                                    pos1 = comp.GetFootPos()
                                    jl=self.calculate_distance(pos,pos1)
                                    if stjl>jl:
                                        stjl=jl
                                        # comp = serverApi.GetEngineCompFactory().CreateCollisionBox(i)
                                        # size=comp.GetSize()
                                        pos=pos1[0],pos1[1],pos1[2]
                                        hdlist.append(i)
                                        scid=i

                            if not pos:
                                self.DestroyEntity(id)
                                self.data_init["soulian1"][playerId]=None
                                return
                           
                        self.BroadcastToAllClient('zhaohuan',{'pos': pos,'key':'soulian',"data":3})

                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
                        motions = motionComp.GetEntityMotions()
                        for i in motions:
                            motionComp.RemoveEntityMotion(i)
                        mID = motionComp.AddEntityTrackMotion((pos[0],pos[1]+1,pos[2]), 0.5, startPos=None, relativeCoord=False, isLoop=False, targetRot=None, startRot=None, useVelocityDir=False)
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
                        motionComp.StartEntityMotion(mID)

                        

                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.51,gongji,k+1,None,hdlist,scid)

                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(0,gongji,1,stid,[stid1,playerId],stid1)

                    
                    

        elif  args['key']=='shield':
            lock=[]
            def io():
                if  lock:
                    return
                def f2(id):
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.CloseMobHitBlockDetection(id)
                    comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                    comp.SetAttr('sun',False)
                comp = serverApi.GetEngineCompFactory().CreateAction(playerId)
                comp.SetMobKnockback(x, z, 3, 0, 0)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesAroundByType(playerId, 2, serverApi.GetMinecraftEnum().EntityType.Mob)
                lists.remove(playerId)
                p=[]
                for i in lists:
                    if i not in  p:
                        p.append(i)
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(5, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, playerId, None, False)
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                        if  i in serverApi.GetPlayerList():
                            motionComp.SetPlayerMotion((x * 2, 0, z * 2))
                        else:
                            motionComp.SetMotion((x * 2, 0, z * 2))
                        comp = serverApi.GetEngineCompFactory().CreateModAttr(i)
                        comp.SetAttr('sun',True)
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.OpenMobHitBlockDetection(i,0.000001)
                        comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp1.AddTimer(0.4,f2,i)
                        lock.append(1)
                if  lock:
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/playsound  random.anvil_land @s ~ ~ ~ 1",playerId)

                
                                
            rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
            rot = rotComp.GetRot()
            x, y, z = serverApi.GetDirFromRot(rot)
          
            for i in range(5):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0.1*i,io)

                

            

        elif args['key']=='the_incinerator' and args['data']=='fashe':
            if not args['rot']:
                return
            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
            comp.SetCommand("/camerashake add @s 0.1 1 rotational",playerId)
            comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
            def f1(pos1,k):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesInSquareArea(None, (pos1[0]-1,pos1[1],pos1[2]-1), (pos1[0]+1,pos1[1]+6,pos1[2]+1), dim)
                for i in lists:
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s 0.1 1 rotational",i)
                    if i != playerId:
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(12, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, playerId, None, True)
                if k==6:
                    def f2():
                        if  playerId in self.fangbao:
                            self.fangbao.remove(playerId)
                    self.fangbao.add(playerId)
                    comp1.AddTimer(0.1,f2)
                    
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/particle  min_baozha {} {} {}".format(pos1[0],pos1[1],pos1[2]))
                    comp.SetCommand("/playsound  random.explode @s {} {} {}".format(pos1[0],pos1[1],pos1[2]),playerId)


            def f(pos1):
                for i in xrange(7):
                    comp1.AddTimer(0.5*i,f1,pos1,i)
                
            i=0
            for pos in args['rot']:
                comp1.AddTimer(0.2*i,f,pos)
                i+=1

        elif args['key']=='gauntlet_of_bulwark' :
            if args['data']=='fashe':
                comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
                entityFootPos = comp.GetFootPos()
                                
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesAroundByType(playerId, 4, serverApi.GetMinecraftEnum().EntityType.Mob)

                for i in lists:
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    x,z=entityFootPos1[0]-entityFootPos[0],entityFootPos1[2]-entityFootPos[2]
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    comp.SetMobKnockback(x, z, 2.0, 0.0, 0.0)

                comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
                comp.OpenPlayerHitMobDetection()
                if not self.data_init.get(playerId):
                    self.data_init[playerId]={}

                # self.data_init[playerId]['gauntlet_of_bulwark']=True

            elif  args['data']=='fashe1':
                rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
                rot = rotComp.GetRot()
                x, y, z = serverApi.GetDirFromRot(rot)

                comp = serverApi.GetEngineCompFactory().CreateAction(playerId)
                comp.SetMobKnockback(x, z, 20.0, 0.0, 0.0)


                comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
                # def f():
                #     self.data_init[playerId]['gauntlet_of_bulwark']=False

                # comp1.AddTimer(1.2,f)

                def f1(k):
                    if k>8:
                        return
                    rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
                    rot = rotComp.GetRot()
                    x, y, z = serverApi.GetDirFromRot(rot)
                    comp = serverApi.GetEngineCompFactory().CreateAction(playerId)
                    comp.SetMobKnockback(x, z, 0.0, 0.0, 0.0)

                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    lists=comp.GetEntitiesAroundByType(playerId, 1, serverApi.GetMinecraftEnum().EntityType.Mob)
                    lists.remove(playerId)
                    s=0
                    for i in lists:
                        s=1
                        if i !=playerId:
                            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                            motionComp.SetMotion((x * 15, 0, z * 15))
                    if s:
                        return
                    comp1.AddTimer(0.0,f1,k+1)
                    

                    # self.data_init[args['mobId']]['gauntlet_of_bulwark']=False

                comp1.AddTimer(0.0,f1,0)



        elif args['key']=='wither_assault_shoulder_weapon' :
            if args['data']!='start':
                name="zaibian:the_harbinger_psw"
            else:
                name="zaibian:the_harbinger_pswd"
            rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
            rot = rotComp.GetRot()
            x, y, z = serverApi.GetDirFromRot(rot)
            comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
            entityFootPos1 = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)

            param = {
                'position': (entityFootPos1[0]+x*2,entityFootPos1[1]+1.4,entityFootPos1[2]+z*2),
                'direction': (x, y, z)
            }
            comp.CreateProjectileEntity(playerId, name, param)

        elif args['key']=='void_assault_shoulder_weapon' :
            name='zaibian:void_assault_shoulder_psw'
            rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
            rot = rotComp.GetRot()
            x, y, z = serverApi.GetDirFromRot(rot)
            comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
            entityFootPos1 = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            param = {
                'position': (entityFootPos1[0],entityFootPos1[1]+1.4,entityFootPos1[2]),
                'direction': (x, y, z)
            }
            comp.CreateProjectileEntity(playerId, name, param)
        self.BroadcastToAllClient('zhaohuan',args)
        

    def BlockStrengthChangedServerEvent(self,args):
        blockName=args['blockName']
        dimension=args['dimensionId']
        newStrength=args['newStrength']
        auxValue=args['auxValue']


        pos=(args['posX'],args['posY'],args['posZ'])
        if  blockName=='zaibian:emp':
            key=(blockName,dimension,pos)
            if newStrength>0  :
                if self.block_data[key]<=0:
                    self.block_data[key]=200
                    self.BroadcastToAllClient('zhaohuan',{'pos':(args['posX']+0.5,args['posY']+0.5,args['posZ']+0.5),'key':'emp'})

                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    lists=comp.GetEntitiesInSquareArea(None, (args['posX']-12,args['posY']-12,args['posZ']-12), (args['posX']+12,args['posY']+12,args['posZ']+12), dimension)
                    for i in lists:
                        comp = serverApi.GetEngineCompFactory().CreateEngineType(i)
                        name=comp.GetEngineTypeStr()
                        if name=="zaibian:the_harbinger":
                            comp = serverApi.GetEngineCompFactory().CreateControlAi(i)
                            comp.SetBlockControlAi(False, False)
                            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                            comp.Hurt(5, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, None, None, True)
                            def f(e):
                                comp = serverApi.GetEngineCompFactory().CreateControlAi(e)
                                comp.SetBlockControlAi(True, False)
                            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                            comp.AddTimer(2,f,i)
                        elif name=="zaibian:the_prowler":
                            comp = serverApi.GetEngineCompFactory().CreateControlAi(i)
                            comp.SetBlockControlAi(False, False)
                            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                            comp.Hurt(5, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, None, None, True)
                            def f(e):
                                comp = serverApi.GetEngineCompFactory().CreateControlAi(e)
                                comp.SetBlockControlAi(True, False)
                            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                            comp.AddTimer(2,f,i)
                        elif name=="zaibian:the_watcher":
                            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                            comp.KillEntity(i)
                            
                else:
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.SetNotifyMsg("电磁脉冲的位置x:{} y:{} z:{} 充能还未完毕 {}秒".format(args['posX'],args['posY'],args['posZ'],self.block_data[key]//20), serverApi.GenerateColor('RED'))
                    
        elif  'zaibian:sandstone_poison_dart_trap' in blockName:
            if newStrength>0  and blockName =='zaibian:sandstone_poison_dart_trap':
                blockDict = {
                    'name': 'zaibian:sandstone_poison_dart_trap1',
                    'aux': auxValue
                }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 0, dimension)
            elif newStrength==0   and blockName =='zaibian:sandstone_poison_dart_trap1':

                blockDict = {
                    'name': 'zaibian:sandstone_poison_dart_trap',
                    'aux': auxValue
                }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 0, dimension)

    def ServerBlockUseEvent(self,args):
        dimensionId=args["dimensionId"]
        blockName=args["blockName"]
        entityId=args["playerId"]
        pos1=(args['x'],args['y'],args['z'])

               

        if  self.tick_block_data.get(pos1):
            return

        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
        itemDict=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        self.tick_block_data[pos1]=15
        if blockName =='zaibian:altar_of_amethyst' :
            blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
            blockEntityData = blockEntitycomp.GetBlockEntityData(dimensionId, pos1)
            key=(pos1,dimensionId)

            if blockEntityData["data"]:
                itemEntityId = self.CreateEngineItemEntity(blockEntityData["data"], dimensionId, (args['x'],args['y']+1.2,args['z']+0.5))
                blockEntityData["data"]=None
                self.BroadcastToAllClient('zhaohuan',{"dim":dimensionId,"pos":pos1,'data':"close",'key':'altar_of_amethyst'})
                self.block_data_sx[key]=0
            else:
                if itemDict:
                    comp = serverApi.GetEngineCompFactory().CreateItem(levelId)
                    ItemBas=comp.GetItemBasicInfo(itemDict['newItemName'])
                    if ItemBas["weaponDamage"] or ItemBas["armorDefense"] or itemDict['newItemName']=="zaibian:amethyst_crab_meat":
                        self.BroadcastToAllClient('zhaohuan',{'data':"add","dim":dimensionId,"itemDict":itemDict,'pos':(args['x'],args['y'],args['z']),'key':'altar_of_amethyst'})
                        blockEntityData["data"]=itemDict
                        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                        comp.SpawnItemToPlayerCarried({}, entityId)
                        self.block_data_sx[key]=1
        elif blockName=="zaibian:miss":
            blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
            blockEntityData = blockEntitycomp.GetBlockEntityData(dimensionId, pos1)

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            entityid=comp.GetEntitiesInSquareArea(None, (pos1[0],pos1[1],pos1[2]), (pos1[0]+1,pos1[1]+1,pos1[2]+1), dimensionId)
            
            if blockEntityData["item"]:
                    itemEntityId = self.CreateEngineItemEntity( blockEntityData["item"], dimensionId, (pos1[0]+0.5, pos1[1]+1.2, pos1[2]+0.5))
                    blockEntityData["item"]=None
                    self.DestroyEntity(entityid[0])
                    entityid = self.CreateEngineEntityByTypeStr('zaibian:emiss', (pos1[0] + 0.5, pos1[1] + 0.5, pos1[2] + 0.5), (0.0,0), dimensionId)
            else:
                if itemDict and itemDict["newItemName"] in ["zaibian:music_disc_netherite_monstrosi","zaibian:music_disc_ender_guardian",
                                          "zaibian:music_disc_ignis","zaibian:music_disc_the_harbinger","zaibian:music_disc_ancient_remnant",
                                           "zaibian:music_disc_the_leviathan" ]:
                    
                    
                    blockEntityData["item"]=itemDict
                    comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                    comp.SpawnItemToPlayerCarried({}, entityId)
                    self.play_miss(pos1,dimensionId,itemDict["newItemName"],entityid[0] )
                    

    def play_miss(self,dim,pos,item,id):
        '''播放音乐'''
        miss_={"zaibian:music_disc_netherite_monstrosi":"monstrosity_theme","zaibian:music_disc_ender_guardian":"enderguardian_theme",
                                          "zaibian:music_disc_ignis":"ignis_theme","zaibian:music_disc_the_harbinger":"harbinger_theme",
                                          "zaibian:music_disc_ancient_remnant":"remnant_theme",
                                           "zaibian:music_disc_the_leviathan" :"leviathan_theme"}

        miss=miss_[item]
        self.BroadcastToAllClient("zhaohuan",{"dim":dim,"pos":pos,"miss":miss,'key':'play_miss',"id":id})

        

    def PlaceNeteaseStructureFeatureEvent(self,args):
        structureName=args['structureName']
        print args,11111111111111
        pos1=(args['x'],args['y'],args['z'])
        def sc(i2,i3,name,rot=(0,0),k=0):
            def op():
                def callback(data):
                    code = data.get('code', 0)
                    if code == 1:
                        def f():
                            if not self.stucture.get(structureName):
                                self.stucture[structureName]=[]
                            if i3 not in self.stucture[structureName]:
                                self.stucture[structureName].append(i3)
                                entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(levelId)
                                entitycomp.SetExtraData("stucture_bc", self.stucture) 
                            entityId = self.CreateEngineEntityByTypeStr(name, i2, rot, dim1,)
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(1,f)
                comp = serverApi.GetEngineCompFactory().CreateChunkSource(levelId)
                comp.DoTaskOnChunkAsync(dim1, (int(i2[0])-8,int(i2[1])-8,int(i2[2])-8),(int(i2[0])+8,int(i2[1])+8,int(i2[2])+8),callback)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(k*0.2,op)
        if structureName in ["zaibian:xiajie1_1","zaibian:sunken_1"]:
            d={"zaibian:xiajie1_1":1,"zaibian:sunken_1":0}
            if structureName=="zaibian:diaoling_1":
                pos=(args['x'],args['y'],args['z'],args['x']+70,args['y']+20,args['z']+80)
            elif structureName=="zaibian:xiajie_5":
                pos=(args['x']-16,args['y'],args['z'],args['x']+42,args['y']+20,args['z']+60)
            elif structureName=="zaibian:xiajie1_1":
                pos=(args['x'],args['y'],args['z'],args['x']+85,args['y']+20,args['z']+90)
            elif structureName=="zaibian:modi_1":
                pos=(args['x'],args['y'],args['z'],args['x']+100,args['y']+70,args['z']+90)
            elif structureName=="zaibian:sunken_1":
                pos=(args['x'],args['y'],args['z'],args['x']+230,args['y']+140,args['z']+160 )
            def f1():
                comp = serverApi.GetEngineCompFactory().CreateDimension(levelId)
                comp.RegisterEntityAOIEvent(d[structureName], structureName, pos, None, serverApi.GetMinecraftEnum().EntityType.Player)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(1,f1)      
        if  self.stucture.get(structureName) and pos1  in   self.stucture.get(structureName):
            return 
    
        elif 'zaibian:xiajie1_1'==structureName:
            dim1=1
            for ki,i in enumerate([[(pos1[0]+44,pos1[1]+35,pos1[2]+17),'zaibian:ignited_revenant',(0,0)],[(pos1[0]+72,pos1[1]+35,pos1[2]+42),'zaibian:ignited_revenant',(0,90)]
                      ,[(pos1[0]+45,pos1[1]+35,pos1[2]+67),'zaibian:ignited_revenant',(0,180)],[(pos1[0]+19,pos1[1]+35,pos1[2]+42),'zaibian:ignited_revenant',(0,270)]]):
                sc(i[0],pos1,i[1],i[2],ki)
        elif structureName=="zaibian:sunken_1":
            dim1=0

            def ram_name():
                skill_dict={"zaibian:deepling_warlock":3,"zaibian:deepling":10,"zaibian:deepling_brute":8,"zaibian:deepling_angler":7,"zaibian:deepling_priest":2}
                sum_=0
                for i in skill_dict.values():
                    sum_+=i
                vars=random.randint(1,sum_)
                sum_1=0
                for i in  skill_dict.keys():
                    sum_1+=skill_dict[i]
                    if sum_1>=vars:
                        return i
            for ki,i in enumerate([[(pos1[0]+12,pos1[1]+47,pos1[2]+58),ram_name(),(0,0)],
                      [(pos1[0]+12,pos1[1]+47,pos1[2]+85),ram_name(),(0,0)],
                      [(pos1[0]+12,pos1[1]+47,pos1[2]+85),ram_name(),(0,0)],
                      [(pos1[0]+12,pos1[1]+47,pos1[2]+85),ram_name(),(0,0)]
                      ,[(pos1[0]+18,pos1[1]+47,pos1[2]+76),ram_name(),(0,0)]
                      ,[(pos1[0]+37,pos1[1]+47,pos1[2]+67),ram_name(),(0,0)]
                      ,[(pos1[0]+37,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+52,pos1[1]+47,pos1[2]+77),ram_name(),(0,0)]
                      ,[(pos1[0]+51,pos1[1]+47,pos1[2]+67),ram_name(),(0,0)]
                      ,[(pos1[0]+69,pos1[1]+47,pos1[2]+67),ram_name(),(0,0)]
                      ,[(pos1[0]+69,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+87,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+87,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+86,pos1[1]+47,pos1[2]+66),ram_name(),(0,0)]
                      ,[(pos1[0]+94,pos1[1]+47,pos1[2]+55),ram_name(),(0,0)]
                      ,[(pos1[0]+106,pos1[1]+47,pos1[2]+42),ram_name(),(0,0)]
                      ,[(pos1[0]+125,pos1[1]+48,pos1[2]+8),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+119,pos1[1]+48,pos1[2]+18),ram_name(),(0,0)]
                      ,[(pos1[0]+130,pos1[1]+48,pos1[2]+18),ram_name(),(0,0)]
                      ,[(pos1[0]+105,pos1[1]+48,pos1[2]+25),ram_name(),(0,0)]
                      ,[(pos1[0]+105,pos1[1]+48,pos1[2]+25),ram_name(),(0,0)]
                      ,[(pos1[0]+105,pos1[1]+48,pos1[2]+25),ram_name(),(0,0)]
                      ,[(pos1[0]+94,pos1[1]+48,pos1[2]+21),ram_name(),(0,0)]
                      ,[(pos1[0]+119,pos1[1]+48,pos1[2]+33),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+55,pos1[2]+27),ram_name(),(0,0)]
                      ,[(pos1[0]+130,pos1[1]+48,pos1[2]+33),ram_name(),(0,0)]
                      ,[(pos1[0]+130,pos1[1]+48,pos1[2]+33),ram_name(),(0,0)]
                      ,[(pos1[0]+130,pos1[1]+48,pos1[2]+33),ram_name(),(0,0)]
                      ,[(pos1[0]+130,pos1[1]+48,pos1[2]+33),ram_name(),(0,0)]
                      ,[(pos1[0]+130,pos1[1]+48,pos1[2]+33),ram_name(),(0,0)]
                      ,[(pos1[0]+66,pos1[1]+55,pos1[2]+19),ram_name(),(0,0)]
                      ,[(pos1[0]+66,pos1[1]+55,pos1[2]+19),ram_name(),(0,0)]
                      ,[(pos1[0]+66,pos1[1]+55,pos1[2]+19),ram_name(),(0,0)]
                      ,[(pos1[0]+63,pos1[1]+55,pos1[2]+27),ram_name(),(0,0)]
                      ,[(pos1[0]+74,pos1[1]+55,pos1[2]+19),ram_name(),(0,0)]
                      ,[(pos1[0]+77,pos1[1]+48,pos1[2]+47),ram_name(),(0,0)]
                      ,[(pos1[0]+56,pos1[1]+48,pos1[2]+47),ram_name(),(0,0)]
                      ,[(pos1[0]+146,pos1[1]+46,pos1[2]+44),ram_name(),(0,0)]
                      ,[(pos1[0]+146,pos1[1]+46,pos1[2]+44),ram_name(),(0,0)]
                      ,[(pos1[0]+146,pos1[1]+46,pos1[2]+44),ram_name(),(0,0)]
                      ,[(pos1[0]+204,pos1[1]+38,pos1[2]+64),ram_name(),(0,0)]
                      ,[(pos1[0]+219,pos1[1]+38,pos1[2]+72),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+204,pos1[1]+38,pos1[2]+80),ram_name(),(0,0)]
                      ,[(pos1[0]+194,pos1[1]+38,pos1[2]+64),ram_name(),(0,0)]
                      ,[(pos1[0]+194,pos1[1]+38,pos1[2]+81),ram_name(),(0,0)]
                      ,[(pos1[0]+178,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+174,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+174,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+174,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]

                      ,[(pos1[0]+166,pos1[1]+47,pos1[2]+78),ram_name(),(0,0)]
                      ,[(pos1[0]+166,pos1[1]+46,pos1[2]+66),ram_name(),(0,0)]
                      ,[(pos1[0]+173,pos1[1]+46,pos1[2]+66),ram_name(),(0,0)]
                      ,[(pos1[0]+178,pos1[1]+46,pos1[2]+66),ram_name(),(0,0)]
                      ,[(pos1[0]+155,pos1[1]+46,pos1[2]+53),ram_name(),(0,0)]
                      ,[(pos1[0]+118,pos1[1]+52,pos1[2]+49),ram_name(),(0,0)]
                      ,[(pos1[0]+142,pos1[1]+51,pos1[2]+62),ram_name(),(0,0)]
                      ,[(pos1[0]+125,pos1[1]+47,pos1[2]+136),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+130,pos1[1]+47,pos1[2]+111),ram_name(),(0,0)]
                      ,[(pos1[0]+118,pos1[1]+47,pos1[2]+116),ram_name(),(0,0)]
                      ,[(pos1[0]+120,pos1[1]+47,pos1[2]+124),ram_name(),(0,0)]
                      ,[(pos1[0]+109,pos1[1]+47,pos1[2]+119),ram_name(),(0,0)]
                      ,[(pos1[0]+105,pos1[1]+47,pos1[2]+124),ram_name(),(0,0)]
                      ,[(pos1[0]+105,pos1[1]+47,pos1[2]+124),ram_name(),(0,0)]
                      ,[(pos1[0]+105,pos1[1]+47,pos1[2]+124),ram_name(),(0,0)]

                      ,[(pos1[0]+98,pos1[1]+47,pos1[2]+118),ram_name(),(0,0)]
                      ,[(pos1[0]+92,pos1[1]+47,pos1[2]+123),ram_name(),(0,0)]
                      ,[(pos1[0]+71,pos1[1]+53,pos1[2]+128),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+47,pos1[2]+141),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+47,pos1[2]+107),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+47,pos1[2]+107),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+47,pos1[2]+107),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+53,pos1[2]+118),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+53,pos1[2]+118),ram_name(),(0,0)]
                      ,[(pos1[0]+70,pos1[1]+53,pos1[2]+118),ram_name(),(0,0)]
                      ,[(pos1[0]+83,pos1[1]+46,pos1[2]+107),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+83,pos1[1]+46,pos1[2]+147),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+83,pos1[1]+46,pos1[2]+141),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+83,pos1[1]+46,pos1[2]+135),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+59,pos1[1]+46,pos1[2]+146),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+59,pos1[1]+40,pos1[2]+145),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+82,pos1[1]+40,pos1[2]+132),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+83,pos1[1]+40,pos1[2]+144),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+82,pos1[1]+53,pos1[2]+138),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+61,pos1[1]+53,pos1[2]+138),"zaibian:coralssus",(0,0)]
                      ,[(pos1[0]+59,pos1[1]+53,pos1[2]+145),"zaibian:coralssus",(0,0)]

                      ,[(pos1[0]+18,pos1[1]+47,pos1[2]+76),ram_name(),(0,0)],
                      [(pos1[0]+17,pos1[1]+47,pos1[2]+68),ram_name(),(0,0)]
                    ]):
                sc(i[0],pos1,i[1],i[2],ki)
        print args,456456



  




    def use_animation(self,args):
        playerId=args["playerId"]
        use_animation=args["animation"]
        comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
        comp1 = serverApi.GetEngineCompFactory().CreateItem(playerId)
        item=comp1.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        comp2 = serverApi.GetEngineCompFactory().CreateItem(levelId)
        if not item:
            item={"newItemName":"22"}
        
        base=comp2.GetItemBasicInfo(item["newItemName"])
        if use_animation!="init":
            if item  :
                if item["newItemName"]in ["zaibian:laser_gatling","zaibian:meat_shredder"]:
                    if not  self.sheji.get(playerId):
                        self.sheji[playerId]={}
                    if self.sheji[playerId].get(item["newItemName"]):
                        return
                    
                    comp4 = serverApi.GetEngineCompFactory().CreateItem(playerId)
                    nj=comp4.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 1)

                    comp3 = serverApi.GetEngineCompFactory().CreateItem(playerId)
                    k=comp3.GetSelectSlotId()
                    self.sheji[playerId][ item["newItemName"]]=[nj,k]
                    
                
            comp.SetCommand("/playanimation @s  {}".format(use_animation),playerId)
            if use_animation=="use_gauntlet_of_guard" :
                if base and base["itemType"]!="custom_ranged_weapon":
                    comp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
                    res = comp.AddEffectToEntity("slowness", 999, 1, False)
        else:
            if item["newItemName"]in["zaibian:laser_gatling","zaibian:meat_shredder"]:
                if not  self.sheji.get(playerId):
                    self.sheji[playerId]={}
                if self.sheji[playerId].get(item["newItemName"]):
                    if item["newItemName"]=="zaibian:laser_gatling":
                        comp4 = serverApi.GetEngineCompFactory().CreateItem(playerId)
                        try:
                            nj=0
                            if  self.sheji[playerId][ item["newItemName"]][0]==0:
                                nj=1
                            else:
                                nj=self.sheji[playerId][ item["newItemName"]][0]

                            comp4.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, self.sheji[playerId][ item["newItemName"]][1],nj)
                        except:
                            pass
                    del self.sheji[playerId][ item["newItemName"]]
                
                
            if args.get('key')=="tidal_claws":
                self.DestroyEntity(self.data_init["tidal_claws"][playerId])
            comp.SetCommand("/playanimation @s  {}".format("bob"),playerId)
            comp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
            res = comp.RemoveEffectFromEntity("slowness")




   
  
  


  

    def skill_bloom_stone_pauldrons(self,playerId):
        '''花岩肩甲技能'''

        comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
        entityFootPos = comp.GetFootPos()
        rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
        rot = rotComp.GetRot()
        for i1 in range(0,361,45):
            x,y,z= serverApi.GetDirFromRot((rot[0],rot[1]+i1))
            pos=(entityFootPos[0]+x*2,entityFootPos[1]+0.5,entityFootPos[2]+z*2)
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            param = {
                'position': pos,
                'direction': (x,0.23,z),
            }
            comp.CreateProjectileEntity(playerId, "zaibian:bloom_stone_pauldron_psw", param)
                    

    def yanjiang(self,pos,dim):
        '''岩浆变方块代码'''

        for x in range(-4,5):
            for y in range(-1,0):
                for z in range(-4,5):
                    pos1=pos[0]+x,pos[1]+y,pos[2]+z
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    blockDict1 = comp.GetBlockNew(pos1, dim)
                    if  (blockDict1["name"] in ["minecraft:flowing_lava","minecraft:lava"] and  blockDict1["aux"]==0)  or "zaibian:melting_netherrack" in blockDict1["name"]:
                        blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
                        blockDict = {
                            'name': 'zaibian:melting_netherrack',
                            'aux': 0
                        }
                        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                        comp.SetBlockNew(pos1, blockDict, 0, dim)
                        blockEntityData = blockEntitycomp.GetBlockEntityData(dim, (int(pos1[0]),int(pos1[1]),int(pos1[2])))
                        if "zaibian:melting_netherrack" in blockDict1["name"]:
                            blockEntityData["star"]={'aux': 0, 'name': 'minecraft:flowing_lava'} 
                        else:
                            blockEntityData["star"]=blockDict1

                                


    def ActuallyHurtServerEvent(self,args):
        # print '伤害后',args["damage"]
        srcId=args["srcId"]
        entityId=args["entityId"]
        cause=args["cause"]
        comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        EngineType=comp.GetEngineTypeStr()
        comp = serverApi.GetEngineCompFactory().CreateEngineType(srcId)
        EngineType1=comp.GetEngineTypeStr()
        if EngineType1=="zaibian:netherite_monstrosity" and cause=="block_explosion":
            comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
            entityFootPos1 = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreatePos(srcId)
            entityFootPos = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
            comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1.8, 0.8, 0.8)

        elif EngineType1=="zaibian:sandstorm" :
            comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
            res = comp.AddEffectToEntity("curse_of_desert", 5, 0, False)


        if EngineType and EngineType in   moster1.mosters.keys() :  #记录玩家伤害
            if cause!="none"and args["damage"]>21 and  moster1.boss:
                args["damage_f"]=21
            self.entity_boss_atk[entityId]=srcId
    

    
        
    def getLaunchPower(self, durationLeft, maxUseDuration):
        timeHeld = maxUseDuration - durationLeft
        pow = timeHeld / 20.0
        pow = ((pow * pow) + pow * 2) / 3
        return min(pow, 1.0)
    def durable_consume_durable(self,playerId):
        """消耗耐久"""
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        gameType = comp.GetPlayerGameType(playerId)
        if gameType!=1:
            PlayerItem_comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            durable=PlayerItem_comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
            PlayerItem_comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, durable-1)
            if durable<=1:
                PlayerItem_comp.SpawnItemToPlayerCarried({}, playerId)

   


    def gauntlet_of_guardJn(self,args):
        entityFootPos,entities,playerId=args
        for i in entities:
        
            comp = serverApi.GetEngineCompFactory().CreatePos(i)
            entityFootPos1 = comp.GetFootPos()
            if entityFootPos1 and entityFootPos:
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(i)
                motionComp.SetMotion(((entityFootPos[0]-entityFootPos1[0])/8 ,(entityFootPos[1]-entityFootPos1[1])/8, (entityFootPos[2]-entityFootPos1[2])/8))
            
        self.BroadcastToAllClient("bind_lz",{"playerId":playerId,"offset":(0, -0.5, 0),"path":"effects/gauntlet_of_guard.json","key":False,"def":"gauntlet_of_guardJn",
        "data":[entities,entityFootPos]})




    def void_core_jn(self,args): #虚空核心放技能
        
        entityFootPos=args["entityFootPos"]
        GetForward=args["GetForward"]
        playerId=args["playerId"]
        key=args["key"]

        def void_core_evocation(rot,pos,DimensionId):  #延迟放技能
            id=self.CreateEngineEntityByTypeStr('zaibian:void_rune', pos, rot, DimensionId)
            comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
            comp.SetAttr('zr',playerId)

        # comp = serverApi.GetEngineCompFactory().CreateDimension(playerId)
        # comp.ChangePlayerDimension(1, (1000,30,0))
        

        comp = serverApi.GetEngineCompFactory().CreateRot(playerId)
        rot=comp.GetRot()  #获取实体头与水平方向的俯仰角度和竖直方向的旋转角度，获得角度后可用GetDirFromRot接口转换为朝向的单位向量 MC坐标系说明
 
        comp = serverApi.GetEngineCompFactory().CreateDimension(playerId)
        DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
        if key=="q":
            for i in range(2,15):    #放置15个磨牙
                pos=(entityFootPos[0]+GetForward[0]*i+1,entityFootPos[1],entityFootPos[2]+GetForward[2]*i+1)
                comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                comp.AddTimer(0.05*i,void_core_evocation,rot,pos,DimensionId)
        else:
            for i in range(1,3):
                for i1 in range(0,360,30):    #放置15个磨牙
                    x, y, z = serverApi.GetDirFromRot((0.5,i1))
                    pos=(entityFootPos[0]+x*1.5*i,entityFootPos[1],entityFootPos[2]+z*1.5*i)
                    comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                    comp.AddTimer(0.05*i,void_core_evocation,rot,pos,DimensionId)

    
                                    
     
    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        
        # for entityId in self.die_list[0]:
        #     comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        #     comp.KillEntity(entityId)
        # 调用上面的反监听函数来销毁
        pass


    
    # -*- coding: utf-8 -*-

      

        


    # 玩家破坏方块
    def DestroyBlockEvent(self,data):
        blockPos = (data.get("x"),data.get("y"),data.get("z"))
        fullName = data.get("fullName")
        auxData = data.get("auxData")
        dimensionId = data.get("dimensionId")
        if fullName in modConfig.allStairs:
            self.calcStairsState(blockPos,dimensionId,auxData,state="Destroy")
            pass
        pass

        if fullName =="minecraft:sand" :
            if random.randint(0,20)==0:
                itemDict = {
                'itemName': 'zaibian:necklace_of_the_desert',
                'count': 1,
                }
                itemEntityId = self.CreateEngineItemEntity(itemDict,dimensionId, (blockPos[0],blockPos[1]+0.5,blockPos[2]))

    # 实体放置方块
    def EntityPlaceBlockAfterServerEvent(self,data):
        blockPos = (data.get("x"),data.get("y"),data.get("z"))
        fullName = data.get("fullName")
        auxData = data.get("auxData")
        dimensionId = data.get("dimensionId")
        if fullName in modConfig.allStairs:
            self.calcStairsState(blockPos,dimensionId,auxData,blockName = fullName,state="place")
            pass

        pass

    # 活塞推动方块
    def PistonActionServerEvent(self,data):
        pass

    # 爆炸破坏方块
    def ExplosionServerEvent(self,data):
        pass

    # 计算楼梯方块的状态
    def calcStairsState(self,pos,dimensionId,auxValue,blockName = "",state="place"):
        directionDirFrom = modConfig.blockAuxValueToDirFrom.get(auxValue)
        isChangeSelf = False
        # 放置需要看4个方向前后改变自己的状态，左右改变左右两边的状态
        if state == "place":
            # 正方向变形
            northDirFrom = directionDirFrom["north"]["DirFrom"]
            changeSelfDict = directionDirFrom["north"]["changeSelfDict"]
            northPos = (pos[0]+northDirFrom[0],pos[1]+northDirFrom[1],pos[2]+northDirFrom[2])
            flog = self.judge_block_is_stairs_func(northPos,dimensionId)
            # 如果返回的不是false 则为aux
            if flog and flog[0][-2:] =="_0":
                if flog[1] in changeSelfDict.keys():
                    blockDict = {
                        'name': blockName[:-2]+changeSelfDict[flog[1]][0],
                        'aux': changeSelfDict[flog[1]][1]
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                    comp.SetBlockNew(pos, blockDict, 0, dimensionId, True)
                    isChangeSelf = True
                    pass
            # 背方向变形
            southDirFrom = directionDirFrom["south"]["DirFrom"]
            changeSelfDict = directionDirFrom["south"]["changeSelfDict"]
            southPos = (pos[0] + southDirFrom[0], pos[1] + southDirFrom[1], pos[2] + southDirFrom[2])
            flog = self.judge_block_is_stairs_func(southPos, dimensionId)
            # 如果返回的不是false 则为aux
            if flog and isChangeSelf is False:
                if flog[1] in changeSelfDict.keys() and flog[0][-2:] =="_0":
                    blockDict = {
                        'name': blockName[:-2] + changeSelfDict[flog[1]][0],
                        'aux': changeSelfDict[flog[1]][1]
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                    comp.SetBlockNew(pos, blockDict, 0, dimensionId, True)
                    pass
            # 右方向变形
            westDirFrom = directionDirFrom["west"]["DirFrom"]
            changeOtherDict = directionDirFrom["west"]["changeOtherDict"]
            westPos = (pos[0] + westDirFrom[0], pos[1] + westDirFrom[1], pos[2] + westDirFrom[2])
            flog = self.judge_block_is_stairs_func(westPos, dimensionId)
            # 如果返回的不是false 则为aux
            if flog:
                if flog[1] in changeOtherDict.keys() and flog[0][-2:] =="_0":
                    blockDict = {
                        'name': flog[0][:-2] + changeOtherDict[flog[1]][0],
                        'aux': changeOtherDict[flog[1]][1]
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                    comp.SetBlockNew(westPos, blockDict, 0, dimensionId, True)
                    pass
            # 左方向变形
            eastDirFrom = directionDirFrom["east"]["DirFrom"]
            changeOtherDict = directionDirFrom["east"]["changeOtherDict"]
            eastPos = (pos[0] + eastDirFrom[0], pos[1] + eastDirFrom[1], pos[2] + eastDirFrom[2])
            flog = self.judge_block_is_stairs_func(eastPos, dimensionId)
            # 如果返回的不是false 则为aux
            if flog:
                if flog[1] in changeOtherDict.keys() and flog[0][-2:] =="_0":
                    blockDict = {
                        'name': flog[0][:-2] + changeOtherDict[flog[1]][0],
                        'aux': changeOtherDict[flog[1]][1]
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                    comp.SetBlockNew(eastPos, blockDict, 0, dimensionId, True)
                    pass
        # 破坏只用判断左右两个方向上的是否需要还原
        elif state == "Destroy":
            # 右方向变形
            westDirFrom = directionDirFrom["west"]["DirFrom"]
            destroyReductionDict = directionDirFrom["west"]["destroyReduction"]
            westPos = (pos[0] + westDirFrom[0], pos[1] + westDirFrom[1], pos[2] + westDirFrom[2])
            flog = self.judge_block_is_stairs_func(westPos, dimensionId)
            # 如果返回的不是false 则为aux
            if flog:
                key = (flog[0][-2:],flog[1])
                if key in destroyReductionDict.keys():
                    blockDict = {
                        'name': flog[0][:-2] + "_0",
                        'aux': destroyReductionDict[key]
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                    comp.SetBlockNew(westPos, blockDict, 0, dimensionId, True)
                    pass
            # 左方向变形
            eastDirFrom = directionDirFrom["east"]["DirFrom"]
            destroyReductionDict = directionDirFrom["east"]["destroyReduction"]
            eastPos = (pos[0] + eastDirFrom[0], pos[1] + eastDirFrom[1], pos[2] + eastDirFrom[2])
            flog = self.judge_block_is_stairs_func(eastPos, dimensionId)
            # 如果返回的不是false 则为aux
            if flog:
                key = (flog[0][-2:],flog[1])
                if key in destroyReductionDict.keys():
                    blockDict = {
                        'name': flog[0][:-2] + "_0",
                        'aux': destroyReductionDict[key]
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                    comp.SetBlockNew(eastPos, blockDict, 0, dimensionId, True)
                    pass
            pass
        pass

    def judge_block_is_stairs_func(self,pos,dimensionId):
        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
        blockDict = comp.GetBlockNew(pos, dimensionId)
        blockName = blockDict.get("name",None)
        aux = blockDict.get("aux",None)
        if blockName in modConfig.allStairs:
            return (blockName,aux)
        else:
            return False


    def item_consume(self,playerId,imName,nex_count=1):
        '''消耗对应物品'''
        Type_=1
        gameType_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        gameType = gameType_comp.GetPlayerGameType(playerId)
        if gameType==1:Type_=0
        AllItems_comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        AllItems=AllItems_comp.GetPlayerAllItems(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)
        arrowSlotDict = [(slot,AllItems[slot].get('count'),AllItems[slot].get('auxValue')) for slot in range(36) if AllItems[slot] and imName in  AllItems[slot].get('itemName')]
        gameType_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        gameType = gameType_comp.GetPlayerGameType(playerId)
        if Type_==0:
            count=0
        else:
            count=nex_count
        for itemtuple in arrowSlotDict:
            if itemtuple[2] == 0 : 
                if count - itemtuple[1] <= 0:
                    itemDict = {'itemName':imName,"count":itemtuple[1]-count,"auxValue":itemtuple[2]}
                    serverApi.GetEngineCompFactory().CreateItem(playerId).SpawnItemToPlayerInv(itemDict,playerId,itemtuple[0])
                    count=0
                    break
                else:
                    serverApi.GetEngineCompFactory().CreateItem(playerId).SetInvItemNum(itemtuple[0],0)
                    count -= itemtuple[1]
        master_hand=AllItems_comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if (22,1) in master_hand['enchantData']: count=0

        return nex_count-count