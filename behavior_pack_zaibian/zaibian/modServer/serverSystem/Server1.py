# -*- coding: utf-8 -*-
#
import mod.server.extraServerApi as serverApi
import zaibian.modCommon.modConfig as modConfig
import zaibian.modCommon.storage as storage

from zaibian.modCommon.moster.moster_G import moster
import zaibian.modCommon.moster.moster_G as moster1
import random,math,copy
from zaibian.modServer.serverSystem.Server import ServerSystem
from zaibian.modServer.serverSystem.structure import tick_yiji

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


class ServerSystem1(ServerSystem):
    def __init__(self, namespace, name):
        super(ServerSystem1, self).__init__(namespace, name)
        # 初始时调用监听函数监听事件
        self.BountifulBaublesMod=None

    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):        
        super(ServerSystem1, self).ListenEvent()
        #描述触发时机：玩家使用盾牌抵挡伤害之后触发
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerSpawnMobEvent",self, self.ServerSpawnMobEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ClientLoadAddonsFinishServerEvent",self, self.ClientLoadAddonsFinishServerEvent)

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnPlayerBlockedByShieldAfterServerEvent",self, self.OnPlayerBlockedByShieldAfterServerEvent)
        #触发时机：当玩家攻击时触发该事件。
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerAttackEntityEvent",self, self.PlayerAttackEntityEvent)
        #触发时机：当抛射物碰撞时触发该事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ProjectileDoHitEffectEvent",self, self.ProjectileDoHitEffectEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ItemReleaseUsingServerEvent", self, self.OnRangedWeaponReleaseUsingServerEvent) # 触发时机：释放正在使用的物品时
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "HealthChangeBeforeServerEvent", self, self.HealthChangeBeforeServerEvent) # 生物生命值发生变化之前触发
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.DamageEvent) # 实体受到伤害时触发
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self, self.OnScriptTickServer) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerItemTryUseEvent", self, self.ServerItemTryUseEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ItemUseOnAfterServerEvent", self, self.ItemUseOnAfterServerEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "StartDestroyBlockServerEvent", self, self.StartDestroyBlockServerEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerBlockEntityTickEvent", self, self.ServerBlockEntityTickEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "MobDieEvent", self, self.MobDieEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "SpawnProjectileServerEvent", self, self.SpawnProjectileServerEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityTickServerEvent", self, self.EntityTickServerEvent) # tick

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerJoinMessageEvent", self, self.PlayerJoinMessageEvent) # tick

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "NewOnEntityAreaEvent", self, self.NewOnEntityAreaEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnMobHitMobServerEvent", self, self.OnMobHitMobServerEvent) # tick

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerItemUseOnEvent", self, self.ServerItemUseOnEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "WillAddEffectServerEvent", self, self.WillAddEffectServerEvents)

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerDoInteractServerEvent", self, self.PlayerDoInteractServerEvent) # tick


        #生物定义json文件中设置的event触发时同时触发。生物行为变更事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityDefinitionsEventServerEvent", self, self.EntityDefinitionsEventServerEvent) # tick
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AttackAnimBeginServerEvent", self, self.AttackAnimBeginServerEvent) # 当攻击动作开始时触发
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEntityServerEvent", self, self.AddEntityServerEvent) # 服务端侧创建新实体，或实体从存档加载时触发
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnStandOnBlockServerEvent", self, self.OnStandOnBlockServerEvent) #当实体站立到方块上时服务端持续触发
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerPlayerTryTouchEvent", self, self.ServerPlayerTryTouchEvent) #当实体站立到方块上时服务端持续触发



        # #客户端通信事件

    def players_wear_accessories(self,args):
        playerId = args["playerId"]
        itemName = args["itemName"]
        type = args["type"]           #"bring"为穿上
        self.BroadcastToAllClient("players_wear_accessories",args)



    def ClientLoadAddonsFinishServerEvent(self,args):
        playerId=args["playerId"]

        if serverApi.GetSystem("BountifulBaublesMod","PyServerSystem"):
            self.BountifulBaublesMod=serverApi.GetSystem("BountifulBaublesMod","PyServerSystem").cls
            self.BountifulBaublesMod.AddItem(modConfig.item_zsl)
            self.ListenForEvent(self.BountifulBaublesMod.modname,"PyServerSystem",  "players_wear_accessories", self, self.players_wear_accessories)  #数据传输
            a={
                "mod_id": "zaibian_yf",
                "mod_name": "灾变模组-叶枫工作室",
                "set_class_order":['zaibian1'],
                "set_class": {
                    "zaibian1": {
                        "class_name": "设置",
                        "class_text": "设置",
                        "class_image": "textures/items/void_core",
                        "set_list_order":['0','1',"2","3","6","7","8","5"],
                        "set_list": {
                            "0": {
                                "data_type": 'bool',
                                "ui_type": 'SwitchToggle',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": False,
                                "text": "boss破坏方块"
                            },
                            "1": {
                                "data_type": 'bool',
                                "ui_type": 'SwitchToggle',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": True,
                                "text": "炎魔技能破坏方块"
                            },
                            "2": {
                                "data_type": 'bool',
                                "ui_type": 'SwitchToggle',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": True,
                                "text": "利维坦离水无敌"
                            },
                            "3": {
                                "data_type": 'bool',
                                "ui_type": 'SwitchToggle',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": False,
                                "text": "3D掉落物（测试版）"
                            },
                            "6": {
                                "data_type": 'bool',
                                "ui_type": 'SwitchToggle',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": False,
                                "text": "除灾变模组以外boss血条为白色"
                            },
                            "7": {
                                "data_type": 'bool',
                                "ui_type": 'SwitchToggle',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": False,
                                "text": "隐藏第一人称左手物品"
                            },
                            "8": {
                                "data_type": 'bool',
                                "ui_type": 'SwitchToggle',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": False,
                                "text": "隐藏灾变装饰品模型"
                            },
                            "5": {
                                "data_type": 'range_number',
                                "ui_type": 'Slider',
                                "save_place": "server_world",
                                "need_op_level": 2,
                                "default_data": 100,
                                "step":1,
                                "min":0,
                                "max":100,
                                "handle":"become_int",
                                "text": "设置震起方块概率 0到100",
                                "data": {
                                    0:'最低',
                                    100:'最大'
                                }
                            },
                        }
                    }
                    },
                
            }
            serverApi.GetSystem("setmod_yf", "setmod_yftem").init_setmod_data(a,playerId)
        else:
            self.set_data={
                "0":False,
                "1":False,
                "2":True,
                "3":False,
                "5":100,
                "6":False,
                "7":False,
                "8":False,
            }
            
            self.BroadcastToAllClient("tb_data",self.set_data)
            comp = serverApi.GetEngineCompFactory().CreateMsg(playerId)
            comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(12.0,comp.NotifyOneMessage,playerId, "未安装（模组助手）前置模组，部分功能无法使用", "§c")

        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(playerId)
        stucture_data=entitycomp.GetExtraData(modConfig.ModName+"book")
        if not stucture_data:
            itemDict = {
                'itemName': 'zaibian:book',
                'count': 1,
            }
            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            comp.SpawnItemToPlayerInv(itemDict, playerId)
            entitycomp.SetExtraData(modConfig.ModName+"book",True)


        self.BroadcastToAllClient("ClientLoadAddonsFinishServerEvent",playerId)
        for i in serverApi.GetPlayerList():
            if i==playerId:
                continue
            self.NotifyToClient(playerId,"ClientLoadAddonsFinishServerEvent",i)

    def outrtrom(self,solt_dict,playerId): #装备判断
        set_=set(())
        for i in  solt_dict.values():
            if i :
                set_.add(i["newItemName"] )
                if  i["newItemName"] in zb_zuantai.keys():
                    for i1 in zb_zuantai[i["newItemName"] ]:
                        list_=i1
                        comp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
                        res = comp.AddEffectToEntity(list_[0], list_[1], list_[2], False)

    def PlayerDoInteractServerEvent(self,args):
        playerId=args["playerId"]
        itemDict=args["itemDict"]
        interactEntityId=args["interactEntityId"]

        comp = serverApi.GetEngineCompFactory().CreateEngineType(interactEntityId)
        EngineType=comp.GetEngineTypeStr()
        if itemDict["newItemName"]=="minecraft:water_bucket" and EngineType=="zaibian:the_baby_leviathan":
            comp = serverApi.GetEngineCompFactory().CreateTame(interactEntityId)
            ownerId = comp.GetOwnerId()
            def f():
                comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                PlayerItem=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                if PlayerItem["newItemName"]=="zaibian:the_baby_leviathan_bucket" and ownerId:
                    PlayerItem["extraId"]=ownerId
                    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                    comp.SpawnItemToPlayerCarried(PlayerItem, playerId)
            comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0.0,f)
            self.DestroyEntity(interactEntityId)

        
        
  

    def OnMobHitMobServerEvent(self,args):
        hittedMobList=args["hittedMobList"]
        mobId=args["mobId"]

        comp = serverApi.GetEngineCompFactory().CreateEngineType(mobId)
        TypeStr=comp.GetEngineTypeStr()
        if TypeStr in ["zaibian:abyss_mine"]:
            comp = serverApi.GetEngineCompFactory().CreateModAttr(mobId)
            if not comp.GetAttr('baozha'):
                comp.SetAttr('baozha',1)
                comp =serverApi.GetEngineCompFactory().CreateEntityEvent(mobId)
                comp.TriggerCustomEvent(mobId,"zaibian:abyss_mine")
            return
        elif TypeStr in moster1.boss:
            for i in hittedMobList:
                if i in serverApi.GetPlayerList():
                    comp = serverApi.GetEngineCompFactory().CreatePos(mobId)
                    entityFootPos = comp.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreatePos(i)
                    entityFootPos1 = comp.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 1, 0,0)


        for i in hittedMobList:
            comp = serverApi.GetEngineCompFactory().CreateEngineType(i)
            TypeStr=comp.GetEngineTypeStr()
            if not TypeStr:
                continue
            if TypeStr in ["zaibian:coral_spear_st","zaibian:coral_bardiche_st"]:
                comp = serverApi.GetEngineCompFactory().CreateModAttr(i)
                if comp.GetAttr('ImmuneDamage')==0:
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.KillEntity( i)


    def ServerSpawnMobEvent(self,args):
        '''实体生成'''
        dimensionId=args["dimensionId"]
        pos=args["x"],args["y"],args["z"]
        # if args["identifier"]=='zaibian:endermaptera':
        #     print 22222222222
            # for i in range(random.randint(1,2)):
            #     entityId = self.CreateEngineEntityByTypeStr('zaibian:endermaptera', pos, (0,0),args["dimensionId"])
    
                                
            

    def PlayerJoinMessageEvent(self,args):
        comp = serverApi.GetEngineCompFactory().CreateAchievement(levelId)
        #设置该成就完成：
        comp.SetNodeFinish(args['id'], "zaibian", callback = None )
        comp = serverApi.GetEngineCompFactory().CreatePlayer(args['id'])
        comp.OpenPlayerHitMobDetection()

    def NewOnEntityAreaEvent(self,args):
        name=args["name"]
        enteredEntities=args["enteredEntities"]
        a={"zaibian:xiajie1_1":'z4',"zaibian:sunken_1":'z5'}
        if name in a.keys():
            for i in enteredEntities:
                comp = serverApi.GetEngineCompFactory().CreateAchievement(levelId)
                comp.SetNodeFinish(i, a[name], callback = None )

        

    def EntityTickServerEvent(self,args):
        identifier=args["identifier"]
        entityId=args["entityId"]
        if not self.st_tick.get(entityId):
                self.st_tick[entityId]=0
        self.st_tick[entityId]+=1

        if identifier=='zaibian:the_harbinger':

            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            comp = serverApi.GetEngineCompFactory().CreateEntityComponent(entityId)

            if entitycomp.GetExtraData("stage")!=2 and self.st_tick[entityId]%10==0 and "follow_range" in  comp.GetAllComponentsName():
                comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                entityFootPos = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
                dim=comp.GetEntityDimensionId()

                height=0
                for i in range(5):
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    blockDict = comp.GetBlockNew((entityFootPos[0], entityFootPos[1]-i, entityFootPos[2]), dim)
                    if "air" in blockDict["name"]:
                        height+=1
                                
                if height<=3 :
                    def f():
                        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
                        motionComp.SetMotion((0, 0.2, 0))
                    for i in range(3):
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.1*i,f)

            comp = serverApi.GetEngineCompFactory().CreateEntityComponent(entityId)
            if self.st_tick[entityId]%25==0 and "follow_range" in  comp.GetAllComponentsName():
                entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                if random.randint(0,3)==1:
                    s=random.choice(["shoot","shoot1","shoot1"])
                    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                    comp.TriggerCustomEvent(entityId,s)
                    comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                    if s=="shoot1":
                        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                        itemDict = {
                            'itemName': 'minecraft:bow',
                            'count': 1,
                        }
                        comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, itemDict, 0)
                    else:
                        comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, None, 0)
        elif  identifier=='zaibian:abyss_mark':
            comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
            id=comp.GetAttr('mark_id')
            comp = compFactory.CreatePos(id)
            entityFootPos2 = comp.GetPos()
            comp = compFactory.CreatePos(entityId)
            entityFootPos1 = comp.GetPos()
            if entityFootPos2 :
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
                mID = motionComp.AddEntityTrackMotion((entityFootPos2[0],entityFootPos1[1],entityFootPos2[2]),0.3, startPos=None, relativeCoord=False, isLoop=False, useVelocityDir=False)
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
                motionComp.StartEntityMotion(mID)
                if  -0.1<abs(entityFootPos2[0])-abs(entityFootPos1[0])<0.1 and -0.1<abs(entityFootPos2[2])-abs(entityFootPos1[2])<0.1 :
                    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                    comp.TriggerCustomEvent(entityId,"sc_abyss_mark")

            
        elif  identifier=='zaibian:abyss_blast_portal':
       
            comp = serverApi.GetEngineCompFactory().CreateEntityComponent(entityId)
            if self.st_tick[entityId]%10==0 and "breathable" in  comp.GetAllComponentsName():
                comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                entityFootPos = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
                dim=comp.GetEntityDimensionId()
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                list_=comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-2,entityFootPos[1]-1,entityFootPos[2]-2),(entityFootPos[0]+2,entityFootPos[1]+10,entityFootPos[2]+2), dim)
                if entityId in list_:
                    list_.remove(entityId)
                for i in list_:
                    comp = serverApi.GetEngineCompFactory().CreateEngineType(i)
                    TypeStr=comp.GetEngineTypeStr()
                    if TypeStr and  (TypeStr in ["zaibian:the_leviathan","zaibian:abyss_blast_portal","zaibian:deepling_warlock"]):
                        continue
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(19, serverApi.GetMinecraftEnum().ActorDamageCause.Magic, entityId, None, True)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                    res = comp.AddEffectToEntity("abyssal_burn", 3, 0, False)

                                
        elif  identifier=='zaibian:netherite_monstrosity':
      
            comp = serverApi.GetEngineCompFactory().CreateEntityComponent(entityId)
            if self.st_tick[entityId]%100==0 and "boss" in  comp.GetAllComponentsName():
                comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
                EngineTypeStr=comp.GetEngineTypeStr()
                args["EngineTypeStr"]=EngineTypeStr
                args["key"]="k1"

                moster.use_skill(args)
        elif  identifier=='zaibian:soulian':
      
            comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
            playerId=comp.GetAttr('playerId')
            position=comp.GetAttr('position')
            direction=comp.GetAttr('direction')
            targetId= comp.GetAttr('id')

            comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
            entityFootPos = comp.GetFootPos()
            entityFootPos=entityFootPos[0]-direction[0],entityFootPos[1],entityFootPos[2]-direction[2]
            jl=self.calculate_distance(position,entityFootPos)
            if jl>30 or not entityFootPos :
                self.DestroyEntity(entityId)
            motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
            Motion=motionComp.GetMotion()

            
            comp = compFactory.CreatePos(playerId)
            entityFootPos1 = comp.GetPos()

            

            if Motion==(0,0,0) and not targetId:
                if  self.st_tick[entityId]%7==0:
                    self.BroadcastToAllClient('zhaohuan',{'pos': entityFootPos1,'key':'soulian',"data":2})
                entityFootPos1=entityFootPos1[0],entityFootPos1[1]-1.6,entityFootPos1[2]
                jl=self.calculate_distance(entityFootPos1,entityFootPos)
                if jl<5:
                    jl=10
                motio=entityFootPos[0]-entityFootPos1[0],entityFootPos[1]-entityFootPos1[1],entityFootPos[2]-entityFootPos1[2]
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(playerId)
                motionComp.SetPlayerMotion((motio[0]/float(jl),motio[1]/float(jl),motio[2]/float(jl)))
            elif targetId:
                if  self.st_tick[entityId]%7==0:
                    self.BroadcastToAllClient('zhaohuan',{'pos': entityFootPos1,'key':'soulian',"data":2})
                comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
                playerId=comp.GetAttr('playerId')
                comp = compFactory.CreatePos(playerId)
                pos = comp.GetPos()
                rot = serverApi.GetEngineCompFactory().CreateRot(playerId).GetRot()
                comp = compFactory.CreateProjectile(serverApi.GetLevelId())
                from_rot=serverApi.GetDirFromRot(rot)
                pos=pos[0]+from_rot[0],pos[1]+from_rot[1],pos[2]+from_rot[2]
                comp = compFactory.CreatePos(entityId)
                pos1 = comp.GetPos()
                comp = compFactory.CreatePos(targetId)
                pos2 = comp.GetPos()

                comp = serverApi.GetEngineCompFactory().CreateCollisionBox(targetId)
                ys=0
                if comp.GetSize():
                    ys= -comp.GetSize()[1]/2.0

                jl=float(self.calculate_distance(pos,pos2))
                if jl<1:
                    jl=1
                pos3=pos[0]-pos1[0],pos[1]-pos1[1],pos[2]-pos1[2]
                pos4=pos[0]-pos2[0],pos[1]-pos2[1]+ys,pos[2]-pos2[2]
                motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
                motionComp.SetMotion((pos3[0]/ jl, pos3[1] / jl, pos3[2] / jl))
                if targetId in serverApi.GetPlayerList():
                    if jl<5:
                        jl=10
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(playerId)
                    motionComp.SetPlayerMotion((motio[0]/float(jl),motio[1]/float(jl),motio[2]/float(jl)))
                else:
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(targetId)
                    motionComp.SetMotion((pos4[0]/ jl, pos4[1] / jl, pos4[2] / jl))


        elif  identifier=='zaibian:item' and self.st_tick[entityId]%60==0:
            comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
            w=comp.GetAttr('id')
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            alive = comp.IsEntityAlive(w)
            if not alive:
                self.DestroyEntity(entityId)




    def SpawnProjectileServerEvent(self,args):
        projectileIdentifier=args["projectileIdentifier"]
        # if projectileIdentifier in ["zaibian:the_harbinger_psw","zaibian:the_harbinger_pswd"]:
        #     self.BroadcastToAllClient('zhaohuan',{'id':args['spawnerId'],'key':'the_harbinger_psw'})


    def MobDieEvent(self,args):
        attacker=args['attacker']
        if attacker!= '-1':
            comp = serverApi.GetEngineCompFactory().CreateEngineType(attacker)
            idname=comp.GetEngineTypeStr()
            if idname and idname=="zaibian:the_harbinger":
                comp = serverApi.GetEngineCompFactory().CreateAttr(attacker)
                health=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,health+30)
                                
    def StartDestroyBlockServerEvent(self,args):
        '''玩家开始挖方块时触发。创造模式下不触发。'''
        blockName=args['blockName']
        if  blockName=='zaibian:emp':
            args['cancel']=True



    def ServerBlockEntityTickEvent(self,args):
        blockName=args['blockName']
        dimension=args['dimension']
        pos=(args['posX'],args['posY'],args['posZ'])
        key=(blockName,dimension,pos)
        if  not self.block_data.get(key):
            p={"zaibian:ancient_desert_stele":20,"zaibian:ancient_desert_stele1":30}
            self.block_data[key]=p.get(blockName,0)
           
        if self.block_data[key]>0:
            self.block_data[key]-=1

        tick_yiji(self,self.block_data[key],args)
        if  blockName=="zaibian:ancient_desert_stele" and self.block_data[key]==0:
            blockDict = {
                'name': 'minecraft:air',
                'aux': 0
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict, 1, dimension)
        elif  blockName=="zaibian:ancient_desert_stele1" and self.block_data[key]==0:
            blockDict = {
                'name': 'zaibian:ancient_desert_stele',
                'aux': 0
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict, 0, dimension)

        elif blockName=="zaibian:baoxian":
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimension)
            a={1:"90_degrees",0:"0_degrees",2:"180_degrees",3:"270_degrees"}
            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
            comp.SetCommand("/structure load zaibian:baoxian {} {} {} {}".format(args['posX'],args['posY'],args['posZ'],a[blockDict["aux"]]))#传送指令
            if random.randint(0,1)==1:
                entityId = self.CreateEngineEntityByTypeStr("minecraft:shulker", (pos[0]+random.randint(-2,2),pos[1],pos[2]+random.randint(-2,2)), (0,0),dimension)
        elif  "zaibian:melting_netherrack" in blockName and self.block_data[key]==0:
            blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
            blockEntityData = blockEntitycomp.GetBlockEntityData(dimension, pos)
            star=blockEntityData["star"]
            if not blockEntityData["time"]:
                blockEntityData['time']=1
            else:
                try:
                    k=int(blockName[-1])
                except:
                    k=0
                k+=1
                if k>3:
                    o=1
                    blockDict = star
                else:
                    o=0
                    blockDict = {
                        'name': 'zaibian:melting_netherrack'+str(k),
                        'aux': 0
                    }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, o, dimension)
                blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
                blockEntityData1 = blockEntitycomp.GetBlockEntityData(dimension, pos)
                if blockEntityData1:
                    blockEntityData1["star"]=star
             
            self.block_data[key]=50

        
        elif blockName=="zaibian:sunkenbaoxian":
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimension)
            a={1:"90_degrees",0:"0_degrees",2:"180_degrees",3:"270_degrees"}
            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
            comp.SetCommand("/structure load zaibian:box_sunken {} {} {} {}".format(args['posX'],args['posY'],args['posZ'],a[blockDict["aux"]]))#传送指令
            if dimension==1:
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                suc = comp.SetChestLootTable((args['posX'],args['posY'],args['posZ']), dimension, "loot_tables/ing_loot.json")
        elif blockName=="zaibian:ancient_factory_bx":
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimension)
            blockDict1 = {
                'name': 'minecraft:chest',
                'aux': blockDict["aux"]
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict1, 0, dimension)

        elif blockName=="zaibian:temple_baoxian":
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimension)
            blockDict1 = {
                'name': 'minecraft:chest',
                'aux': blockDict["aux"]
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict1, 0, dimension)
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            suc = comp.SetChestLootTable((args['posX'],args['posY'],args['posZ']), dimension, "loot_tables/chests/jungle_temple.json")

        elif blockName=="zaibian:temple_xianjing":
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimension)
            blockDict1 = {
                'name': 'minecraft:chest',
                'aux': blockDict["aux"]
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew(pos, blockDict1, 0, dimension)
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            suc = comp.SetChestLootTable((args['posX'],args['posY'],args['posZ']), dimension, "loot_tables/cursed_pyramid.json")


        elif blockName=="zaibian:altar_of_void":
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            pop=comp.GetEntitiesInSquareArea(None, (pos[0]-5,pos[1]-4,pos[2]-5), (pos[0]+5,pos[1]+4,pos[2]+5), dimension)
            for i in pop:
                comp = serverApi.GetEngineCompFactory().CreateEngineType(i)
                entityType = comp.GetEngineType()
                EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType
                if entityType & EntityTypeEnum.Player == EntityTypeEnum.Player:
                    blockDict = {
                        'name': 'minecraft:air',
                        'aux': 0
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    comp.SetBlockNew(pos, blockDict, 1, dimension)
                    entityId = self.CreateEngineEntityByTypeStr('zaibian:ender_guardian', pos, (0, 0), dimension)     
                    break
        elif  blockName=="zaibian:altar_of_amethyst" and self.block_data[key]==0:
            blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
            blockEntityData = blockEntitycomp.GetBlockEntityData(dimension, pos)
            if blockEntityData["data"] and not self.block_data_sx.get((pos,dimension)):
                self.BroadcastToAllClient('zhaohuan',{'data':"add","dim":dimension,"itemDict":blockEntityData["data"],'pos':pos,'key':'altar_of_amethyst'})
                self.block_data_sx[(pos,dimension)]=1

        elif  blockName=="zaibian:abyssal_egg" and self.block_data[key]==0:
            self.block_data[key]=20
            blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
            blockEntityData = blockEntitycomp.GetBlockEntityData(dimension, pos)
            if not  blockEntityData["time"]:
                blockEntityData["time"]=0
            blockEntityData["time"]+=1
            if blockEntityData["time"]>=600:
                entityId = self.CreateEngineEntityByTypeStr('zaibian:the_baby_leviathan', pos, (0, 0), dimension) 
                blockDict = {
                    'name': 'minecraft:air',
                    'aux': 0
                }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 0, dimension)
            else:
                self.BroadcastToAllClient('zhaohuan',{"dim":dimension,'pos':pos,'key':'abyssal_egg',"time":600-blockEntityData["time"]})
        
        elif  blockName=="zaibian:miss" and self.block_data[key]==0:
            self.block_data[key]=30
            blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
            blockEntityData = blockEntitycomp.GetBlockEntityData(dimension, pos)
            if blockEntityData['item']:
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/particle  zaibian:miss {} {} {}".format(pos[0],pos[1]+1,pos[2]))
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            entityid=comp.GetEntitiesInSquareArea(None, (pos[0],pos[1],pos[2]), (pos[0]+1,pos[1]+1,pos[2]+1), dimension)
            if entityid and len(entityid) > 1:
                entityid.pop(0)
                for entityids in entityid:
                    self.DestroyEntity(entityids)
            if not entityid:
                entityid = self.CreateEngineEntityByTypeStr('zaibian:emiss', (pos[0] + 0.5, pos[1] + 0.5, pos[2] + 0.5), (0.0,0), dimension)
        elif  blockName=="zaibian:sandstone_poison_dart_trap1" and self.block_data[key]==0:
            lis_={1:[-1,0],3:[1,0],0:[0,1],2:[0,-1]}
            self.block_data[key]=30
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            data= comp.GetBlockNew(pos, dimension)
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            p1,p2=lis_[data['aux']][0],lis_[data['aux']][1]
            param = {
                'position':(pos[0] + 0.5+p1*0.6, pos[1] + 0.5, pos[2] + 0.5+p2*0.6),
                'direction': (p1,0,p2)
            }
            comp.CreateProjectileEntity(serverApi.GetPlayerList()[0], "zaibian:dujian", param) 

        elif  blockName=="zaibian:sandstone_ignite_trap1" :
            if self.block_data[key]==0:
                blockDict = {
                    'name': 'zaibian:sandstone_ignite_trap',
                    'aux': 0
                }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 0, dimension)
            if  self.block_data[key]%3==0 :
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                entityid=comp.GetEntitiesInSquareArea(None, (pos[0]-2,pos[1]-2,pos[2]-2), (pos[0]+2,pos[1]+10,pos[2]+2), dimension)
                for entityId in entityid:
                    comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                    entityFootPos = comp.GetFootPos()
                    pos1=pos[0]+0.5,pos[1],pos[2]+0.5
                    pl=self.calculate_distance(pos1,entityFootPos)
                    g=pos[1]-entityFootPos[1]
                    if -2<g<10 and pl<1.5:
                        comp = serverApi.GetEngineCompFactory().CreateHurt(entityId)
                        comp.Hurt(5, serverApi.GetMinecraftEnum().ActorDamageCause.FireTick, None, None, False)
                        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
                        comp.SetEntityOnFire(3, 2)



    def WillAddEffectServerEvents(self, args):
        # 阻止物品实体被给予药水效果。
        entityId = args['entityId']
        entityStr = CF.CreateEngineType(entityId).GetEngineTypeStr()
        if entityStr == 'zaibian:emiss':
            args['cancel'] = True

    
        

    
    def ItemUseOnAfterServerEvent(self,args):
        blockName=args['blockName']
        entityId=args['entityId']
        dimensionId=args['dimensionId']

        pos1=(args['x'],args['y'],args['z'])


     
        itemDict=args['itemDict']
        if blockName =='zaibian:altar_of_fire' and itemDict['newItemName']=='zaibian:burning_ashes' and not self.bolck_time.get(pos1):
            self.bolck_time[pos1]=6
            comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
            itemDict['count']-=1
            comp.SpawnItemToPlayerCarried(itemDict, entityId)
            self.BroadcastToAllClient('zhaohuan',{'pos': (args['x']+0.5,args['y']+0.1,args['z']+0.5),'key':'zhaohuan'})

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(entityId, 20, serverApi.GetMinecraftEnum().EntityType.Player)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/camerashake add @s 0.2 5 rotational",i)
            def f():
                entityId = self.CreateEngineEntityByTypeStr('zaibian:ignis', (args['x'],args['y']+2,args['z']), (0,0), dimensionId)
            def f1():
                self.BroadcastToAllClient('zhaohuan',{'pos':(args['x']+0.5,args['y']+3,args['z']+0.5),'key':'zhaohuanq'})
                
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(6,f)
            comp.AddTimer(5.6,f1)
            
        elif blockName =='zaibian:altar_of_abyss' and itemDict['newItemName']=='zaibian:abyssal_sacrifice':
            if not self.data_init.get("boss_time"):
                self.data_init["boss_time"]=[]
            if pos1 not in self.data_init["boss_time"]:
                self.data_init["boss_time"].append(pos1)
                self.BroadcastToAllClient('zhaohuan',{'pos':(args['x'],args['y'],args['z']),'key':'altar_of_abyss'})
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesInSquareArea(None, (pos1[0]-8,pos1[1]-2,pos1[2]-8), (pos1[0]+8,pos1[1]+8,pos1[2]+8), dimensionId)
                for i in lists:
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s 0.1 4 rotational",i)
                def f():
                    entityId = self.CreateEngineEntityByTypeStr('zaibian:the_leviathan', (args['x'],args['y']+2,args['z']), (0,0), dimensionId)
                    self.data_init["boss_time"].remove(pos1)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(4,f)

  


    def ServerItemTryUseEvent(self,args):
        '''玩家使用物品生效之前服务端抛出的事件'''
        playerId=args['playerId']
        itemDict=args['itemDict']
        entityId=args['playerId']
        comp = serverApi.GetEngineCompFactory().CreateDimension(playerId)
        dim=comp.GetEntityDimensionId()

        
        if itemDict["newItemName"]=="minecraft:firework_rocket":
            cls=serverApi.GetSystem("mod_effect_eF9xM9","PyServerSystem").getSystemInUseFunc()
            
            if   playerId in cls.playerEffectDict['elytraFly']:
                comp1 = serverApi.GetEngineCompFactory().CreatePos(playerId)
                pos1=comp1.GetPos()
                rotComp = serverApi.GetEngineCompFactory().CreateRot(entityId)
                rot = rotComp.GetRot()
                x, y, z = serverApi.GetDirFromRot(rot)
                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                param = {
                    'position': pos1,
                    'direction': serverApi.GetDirFromRot((rot[0]+180,rot[1]))
                }
                comp.CreateProjectileEntity(playerId, "zaibian:yanhua", param)

                if itemDict["count"]-1==0:
                    d={}
                else:
                    d=copy.deepcopy(itemDict)
                    d["count"]-=1
                comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                comp.SpawnItemToPlayerCarried(d, playerId)

        # comp = serverApi.GetEngineCompFactory().CreateItem(playerId)

        # itemDict = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, True)
        # itemDict['userData'] = {"LootTableSeed":{"__type__":4,"__value__": 0},"Items":[],
        #                         "LootTable":{"__type__":8,"__value__":"loot_tables/box_sunken.json"},
        #                         "Findable":{"__type__":1,"__value__": 0},
        #                         "display":{"Lore":[{"__type__":8,"__value__": "(+DATA)"}]}}
        # comp.SetCustomName(itemDict, '箱子')
        # comp.SpawnItemToPlayerCarried(itemDict, playerId)
        comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
        is_sneaking = comp.isSneaking()

        if itemDict and is_sneaking  and  itemDict['newItemName'] in ["zaibian:void_forge" ,"zaibian:infernal_forge"]:
            args["cancel"]=True
        if itemDict['itemName'] in self.ip.keys():
            comp1 = serverApi.GetEngineCompFactory().CreatePos(playerId)
            pos1=comp1.GetPos()
            

            comp = serverApi.GetEngineCompFactory().CreateFeature(levelId)
            if self.ip[itemDict['itemName']][1]==dim:
                pos = comp.LocateNeteaseFeatureRule(self.ip[itemDict['itemName']][0], dim, pos1)
                if pos:
                    print pos,"结构体位置"
                    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                    items=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                    items['count']-=1
                    comp.SpawnItemToPlayerCarried(items, playerId)
                    entityId = self.CreateEngineEntityByTypeStr(itemDict['itemName'], pos1, (0, 0), dim)
                    self.NotifyToClient(playerId,'eyetexiao',{'entityId':entityId})
               
                    io=[pos[0]-pos1[0],pos[1]-pos1[1],pos[2]-pos1[2]]

                    def f(io,entityId):
                        if abs(io[0])<3 and abs(io[2])<3:
                            if -10<io[1]<0:
                                p=0
                            elif  io[1]<-10:
                                p=-0.15
                            else:
                                p=0.15
                            comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
                            comp.SetMobKnockback(0 , 0, 3, p, p)
                        
                        else:
                            comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
                            comp.SetMobKnockback(io[0] ,  io[2], 3, 0.15, 0.15)

                        
                    def f1(entityId):
                        comp1 = serverApi.GetEngineCompFactory().CreatePos(entityId)
                        pos1=comp1.GetPos()
                        if random.randint(0,5)!=0:
                            itemDict1 = {
                                'itemName': itemDict['itemName'],
                                'count': 1,
                            }
                            itemEntityId = self.CreateEngineItemEntity(itemDict1, dim, pos1)
                        self.DestroyEntity(entityId)

                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    for i in xrange (0,7):
                        comp.AddTimer(0.15*i,f,io,entityId)

                    comp.AddTimer(3,f1,entityId)
                else:
                    comp = serverApi.GetEngineCompFactory().CreateGame(playerId)
                    comp.SetOneTipMessage(playerId, serverApi.GenerateColor("RED") + "附近没有该结构体请换个位置")
            else:
                comp = serverApi.GetEngineCompFactory().CreateGame(playerId)
                w={0:'主世界',1:'下界',2:'末地'}
                comp.SetOneTipMessage(playerId, serverApi.GenerateColor("RED") + "该维度没有此特征，在{}才会生成".format(w[self.ip[itemDict['itemName']][1]]))

        elif  itemDict and is_sneaking and "infernal_forge" in itemDict["newItemName"] :
            if self.tick_block_data.get(entityId+"infernal_forge",0)==0 :
                self.NotifyToClient(entityId,"zhaohuan",{"key":"zhendong","id":entityId})

                comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
                dimensionId=comp.GetEntityDimensionId() #获取实体所在维度
                self.tick_block_data[entityId+"infernal_forge"]=90
                comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                entityFootPos = comp.GetFootPos() 
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/particle  zaibian:close_di6 {} {} {}".format(entityFootPos[0],entityFootPos[1],entityFootPos[2]))
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                
                entities = comp.GetEntitiesInSquareArea(None, (entityFootPos[0]-6,entityFootPos[1]-3,entityFootPos[2]-6), (entityFootPos[0]+6,entityFootPos[1]+3,entityFootPos[2]+6),dimensionId)
                if entityId in entities:
                    entities.remove(entityId)
                
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/camerashake add @s  0.1 1 rotational",entityId)   
                comp.SetCommand("/playsound  random.explode @s ",playerId)
                for i in entities:
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s  0.1 1 rotational",i)
                    comp = serverApi.GetEngineCompFactory().CreateEngineType(i)
                    TypeStr=comp.GetEngineTypeStr()
                    if TypeStr=="minecraft:item":
                        return

                    comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                    hralth=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                    hralth_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                    if (hralth_max and  hralth) and  hralth_max//2>=hralth:
                        comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                        comp.SetEntityOnFire(5, 3)
                    comp = serverApi.GetEngineCompFactory().CreateAction(i)
                    comp.SetMobKnockback(0, 0, 0, 0.8, 0.8)
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(13, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, entityId, None, False)
        elif itemDict  and is_sneaking and   itemDict['newItemName']=="zaibian:void_forge" :
            if self.tick_block_data.get(entityId+'void_forge',0)==0  :
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/camerashake add @s 0.1 1.5 rotational",entityId)   
                comp.SetCommand("/playsound  random.explode @s ",playerId)
 
                self.NotifyToClient(entityId,"zhaohuan",{"key":"zhendong","id":entityId})
                
                self.tick_block_data[entityId+'void_forge']=150
                comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                entityFootPos = comp.GetFootPos()
                def void_core_evocation(rot,pos,DimensionId):  #延迟放技能
                    id=self.CreateEngineEntityByTypeStr('zaibian:void_rune', pos, rot, DimensionId)
                    comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                    comp.SetAttr('zr',entityId)
                rotComp = serverApi.GetEngineCompFactory().CreateRot(entityId)
                rot = rotComp.GetRot()
                comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
                DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
                for i1 in [-40,-30,-20,-10,0,10,20,30,40]:
                    for i in range(3,13,3):    #放置15个磨牙
                        x, y, z = serverApi.GetDirFromRot((rot[0],rot[1]+i1))
                        pos=(entityFootPos[0]+x*i,entityFootPos[1],entityFootPos[2]+z*i)
                        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())  
                        comp.AddTimer(0.1*i,void_core_evocation,rot,pos,DimensionId)

        elif itemDict and   itemDict['newItemName']=="zaibian:laser_gatling" :
            if itemDict["durability"]<=1:
                if  self.item_consume(entityId,"minecraft:redstone")!=0:
                    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                    nj=comp.GetItemMaxDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 1,False)
                    comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, nj)
                    comp3 = serverApi.GetEngineCompFactory().CreateGame(playerId)
                    comp3.SetOneTipMessage(playerId, serverApi.GenerateColor("GREEN") + "换弹中")
                    self.NotifyToClient(entityId,"zhaohuan",{"key":"laser_gatling","id":entityId})
                    if not  self.sheji.get(playerId):
                        self.sheji[playerId]={}
                    if self.sheji[playerId].get(itemDict["newItemName"]):
                        del self.sheji[playerId][ itemDict["newItemName"]]
                else:
                    comp3 = serverApi.GetEngineCompFactory().CreateGame(playerId)
                    comp3.SetOneTipMessage(playerId, serverApi.GenerateColor("RED") + "该武器已没弹药，可以用红石粉进行填充")
                    args["cancel"]=True

            else:
                args["cancel"]=True




   


    def OnStandOnBlockServerEvent(self,args):
        entityId=args["entityId"]
        pos=(args["blockX"],args["blockY"],args["blockZ"])
        blockName=args["blockName"]
        dimensionId=args["dimensionId"]


        if blockName in ["zaibian:end_stone_teleport_trap_bricks_off","zaibian:obsidian_explosion_trap_bricks_off","zaibian:purpur_void_rune_trap_block_off"]:
            comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
            if (not self.bolck_time.get(pos) or self.bolck_time[pos]==0) and "zaibian" not  in comp.GetEngineTypeStr():
                if blockName=="zaibian:end_stone_teleport_trap_bricks_off"  :
                    self.bolck_time[pos]=10
                    comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
                    res = comp.AddEffectToEntity("blindness", 2, 3, True)
                    comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                    x=random.randint(-10,10)
                    y=random.randint(-10,10)
                    comp.SetPos((pos[0]+x,pos[1]+1,pos[2]+y))

                elif blockName=="zaibian:obsidian_explosion_trap_bricks_off" :
                    def setwz(entityId,pos):
                        comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                        pos1=comp.GetPos()
                        if pos1 and pos:
                            comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
                            comp.SetMobKnockback(pos[0]-pos1[0], pos[2]-pos1[2], 0.2, 0, 0)

                    self.bolck_time[pos]=15
                    comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    for i in range(100):
                        comp1.AddTimer(0.05*i,setwz,entityId,pos)
                    comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
                    comp1.AddTimer(5,comp.CreateExplosion,pos,5,False,False,None,serverApi.GetPlayerList()[0])
                        
                    
                elif blockName=="zaibian:purpur_void_rune_trap_block_off" :
                    self.bolck_time[pos]=10
                    comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
                    res = comp.AddEffectToEntity("slowness", 2, 3, True)
                    self.CreateEngineEntityByTypeStr('zaibian:void_rune', pos, (0,0), args['dimensionId'])
        elif blockName =="zaibian:sandstone_falling_trap":
            pos1=(pos[0],pos[1]-1,pos[2])
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            block=comp.GetBlockNew(pos1, dimensionId)
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            liquidBlockDict = comp.GetLiquidBlock(pos1, dimensionId)
            if block['name']=="minecraft:air" or liquidBlockDict:
                blockDict = {
                    'name': 'zaibian:sandstone_falling_trap1',
                    'aux': 0
                }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 0, dimensionId)

        elif blockName =="zaibian:sandstone_ignite_trap":
            comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            TypeFamily=comp.GetTypeFamily()
            if TypeFamily and  "desert" not in TypeFamily :
                blockDict = {
                        'name': 'zaibian:sandstone_ignite_trap1',
                        'aux': 0
                    }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 0, dimensionId)
                key=('zaibian:sandstone_ignite_trap1',dimensionId,pos)
                self.block_data[key]=900
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/particle  ranshao {} {} {}".format(pos[0],pos[1]+1,pos[2]))

       
    def AddEntityServerEvent(self,args):
        engineTypeStr=args["engineTypeStr"]
        entityId=args["id"]
        dimensionId=args["dimensionId"]
        pos=args["posX"],args["posY"],args["posZ"]
        itemName=args.get('itemName',"")


        if engineTypeStr in moster1.pa_monster:
            comp = serverApi.GetEngineCompFactory().CreateModel(entityId)
            comp.SetModel("xuenv")
            

        if engineTypeStr=="zaibian:abyss_mine":
            comp = serverApi.GetEngineCompFactory().CreatePlayer(entityId)
            comp.OpenPlayerHitMobDetection()
        elif engineTypeStr=="zaibian:void_rune":
            x11, y11, z11 = int(args["posX"]), int(args["posY"]), int(args["posZ"])
            z02, x02 = 0.0, 0.0
            if x11 < 0:
                x02 = -1.0
            if z11 < 0:
                z02 = -1.0
            pos_=x11 + x02, y11, z11 + z02
            pos=pos_[0],round(pos_[1],0)-1,pos_[2]
            pos1=pos_[0],round(pos_[1],0),pos_[2]
            pos2=pos_[0],round(pos_[1],0)+1,pos_[2]
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimensionId) 
            blockDict1 = comp.GetBlockNew(pos1, dimensionId) 
            blockDict2 = comp.GetBlockNew(pos2, dimensionId) 
            if blockDict["name"]=="minecraft:air"  or  blockDict1["name"]!="minecraft:air" or blockDict2["name"]!="minecraft:air":
                self.DestroyEntity(entityId)
        elif engineTypeStr in moster1.boss:
            comp = serverApi.GetEngineCompFactory().CreatePlayer(entityId)
            comp.OpenPlayerHitMobDetection()
        
                            
        elif engineTypeStr=="zaibian:ignited_revenant":
            comp = serverApi.GetEngineCompFactory().CreateModAttr(args["id"])
            init=comp.GetAttr('init')
            if not  init:
                init=comp.SetAttr('init',1,True)

                comp = serverApi.GetEngineCompFactory().CreateAttr(args["id"])
                comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.LUCK,10000)
                comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.LUCK,1111)
                p=[0,90,180,270]
                p1=["h","y","q","z"]
                
                for i in range(4):
                    comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                    entityFootPos1 = comp.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
                    DimensionId=comp.GetEntityDimensionId() #获取实体所在维度
                    entityId1 = self.CreateEngineEntityByTypeStr('zaibian:ignited_revenant1',entityFootPos1, (0, p[i]), DimensionId,False)
                    comp = serverApi.GetEngineCompFactory().CreateRide(entityId)
                    comp.SetRiderRideEntity(entityId1,entityId,i )
                    comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId1)
                    init=comp.SetAttr('data',{'id':args["id"],"fx":p1[i],'r':i},True)
                comp = serverApi.GetEngineCompFactory().CreateRide(entityId)
                comp.SetEntityLockRider(True)
                
        comp2 = serverApi.GetEngineCompFactory().CreateExtraData(levelId)

        if engineTypeStr in moster1.mosters.keys():
            comp = serverApi.GetEngineCompFactory().CreateHurt(args["id"])
            comp.ImmuneDamage(False)
            comp = serverApi.GetEngineCompFactory().CreateEntityEvent(args["id"])
            comp.TriggerCustomEvent(args["id"],"romve_skill")
            comp1 = serverApi.GetEngineCompFactory().CreateControlAi(args["id"])
            comp1.SetBlockControlAi(True, False)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(args["id"])
            if entitycomp.GetExtraData("die"):
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.KillEntity(args["id"])

            
    

        elif comp2.GetExtraData("zaibian_yf_3") and engineTypeStr=="minecraft:item" :
       
            comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
            if not comp.GetAttr('id'):
                def func():
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
                    po=motionComp.GetMotion()
                    id=self.CreateEngineEntityByTypeStr("zaibian:item",pos,(0,0),0)
                    comp1 = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
                    comp1.SetAttr('id',id,True)
                    comp = serverApi.GetEngineCompFactory().CreateItem(levelId)
                    items=comp.GetDroppedItem(entityId)
                    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(id)
                    if not motionComp:
                        return
                    motionComp.SetMotion((po[0]*2,po[1]*2,po[2]*2))
                    compitem = CF.CreateItem(id)
                    

                    comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                    comp.SetAttr('id',entityId,True)
                    comp.SetAttr('Item',items,True,True)

                    if not compitem.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, items, 0):
                        compitem.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, items, 0)
                        compitem.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, items, 1)
                        compitem.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, items, 2)
                        compitem.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, items, 3)
                    compentityevent = CF.CreateEntityEvent(id)

                    comp = serverApi.GetEngineCompFactory().CreateItem(levelId)
                    BasicInfo=comp.GetItemBasicInfo(items["newItemName"])
                    types=BasicInfo["itemType"]

                    if   types in [ 'armor',"shovel","pickaxe","hoe","axe","sword","custom_ranged_weapon"] or  "shield"  in items["newItemName"]:   #武器
                        print '#武器'
                        compentityevent.TriggerCustomEvent(id, 'disp_wea')
                    elif types == 'block':#方块
                        compentityevent.TriggerCustomEvent(id, 'disp_blocks')
                    else :
                        print '物品'
                        compentityevent.TriggerCustomEvent(id, 'disp_items')
                    compentityevent.TriggerCustomEvent(id, 'dips_action')
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0,func)
        l=[
            "zaibian:entity_zb1",
            "zaibian:entity_zb2",
            "zaibian:entity_zb3",
            "zaibian:entity_zb1_1",
            "zaibian:zb1_2",
            "zaibian:entity_zb4"]
        if itemName in  l:
            self.DestroyEntity(entityId)

            
    
    
    def ServerPlayerTryTouchEvent(self,args):
        entityId=args["entityId"]
        comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
        id=comp.GetAttr('id')
        if id:
            self.DestroyEntity(id)

            
            
    def AttackAnimBeginServerEvent(self,args):
        id=args['id']
        comp = serverApi.GetEngineCompFactory().CreateEngineType(id)
        args["entityId"]=id
        args["EngineTypeStr"]=comp.GetEngineTypeStr()
        if args["EngineTypeStr"] in moster1.pa_monster:
            moster.use_attack(args)


    def EntityDefinitionsEventServerEvent(self,args):
        entityId=args["entityId"]
        eventName=args["eventName"]
    # and comp.GetAttackTarget()!="-1" TODO
        comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        EngineTypeStr=comp.GetEngineTypeStr()

        comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
        DimensionId=comp.GetEntityDimensionId()
        comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
        if eventName=="sc_abyss_mark" and EngineTypeStr=="zaibian:abyss_mark"  :
            entitypos = CF.CreatePos(entityId).GetPos()
            entityId = self.CreateEngineEntityByTypeStr('zaibian:abyss_blast_portal', entitypos, (0, 0), DimensionId)
        elif EngineTypeStr=="zaibian:modern_remnant"  :
            if eventName=="zt2":
                comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(entityId)
                result = comp.SetSitting(True)
            elif eventName=="zt0":
                comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(entityId)
                result = comp.SetSitting(False)

        elif eventName=="minecraft:explode" and EngineTypeStr=="zaibian:yanhua"  :
            entitypos = CF.CreatePos(entityId).GetPos()
            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
            self.BroadcastToAllClient("zhaohuan",{"key":"lb11_5","id":entityId,'pos':entitypos})
        elif eventName=="skill_use"   and comp.GetAttackTarget()!="-1" :#TODO
            args["EngineTypeStr"]=EngineTypeStr
            moster.use_skill(args)
        elif eventName=="start_ack"  :
            args["EngineTypeStr"]=EngineTypeStr
            moster.use_attack(args)
        
        elif "zaibian:abyss_mine"==eventName:
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            lists=comp.GetEntitiesAroundByType(entityId, 4, serverApi.GetMinecraftEnum().EntityType.Mob)
            lists.remove(entityId)
            for i in lists:
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(int(7), serverApi.GetMinecraftEnum().ActorDamageCause.EntityExplosion, entityId, None, True)
                comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                res = comp.AddEffectToEntity("abyssal_fear", 8, 0, False)
            comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
            comp.AddEffectToEntity("invisibility", 3, 0, False )
            comp = serverApi.GetEngineCompFactory().CreateHurt(entityId)
            comp.Hurt(10000, serverApi.GetMinecraftEnum().ActorDamageCause.NONE, None, None, False)
        elif "zaibian:abyss_blast_portal"==eventName:
            comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
            comp.AddEffectToEntity("invisibility", 3, 0, False )
            comp = serverApi.GetEngineCompFactory().CreateHurt(entityId)
            comp.Hurt(10000, serverApi.GetMinecraftEnum().ActorDamageCause.NONE, None, None, False)

        elif eventName == 'disp_remove':
            # 从json事件那边的每秒触发检测该实体在不在展示台方块里面，不在即销毁
            entitypos = CF.CreatePos(entityId).GetPos()
            # 调整获取的实体坐标，让他更精准。
            enpos = (round(entitypos[0]) if entitypos[0] < 0 else entitypos[0],round(entitypos[1]) if entitypos[1] < 0 else entitypos[1], round(entitypos[2]) if entitypos[2] < 0 else entitypos[2])
            dia = CF.CreateDimension(entityId).GetEntityDimensionId()
            blockinfo = CF.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew(enpos, dia)
            if blockinfo and not blockinfo['name'] in "zaibian:miss":
                self.DestroyEntity(entityId)

    def OnScriptTickServer(self):
        if not serverApi:
            return
        self.tick+=1
        if self.tick>=20:
            self.tick=0
            for playerId,solt_dict in self.damagelist1.items():
                self.outrtrom(solt_dict,playerId)
        for name in self.baozhajl.keys():
            if self.baozhajl[name][1]==0:
                continue
            self.baozhajl[name][1]-=1

        
      
        

        if self.tick%4==0:
            for player_list in self.sheji:
                for item in self.sheji[player_list]:
                    if item=="zaibian:laser_gatling":
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        gameType = comp.GetPlayerGameType(player_list)
                        comp = serverApi.GetEngineCompFactory().CreateItem(player_list)
                        nj=self.sheji[player_list][item][0]
                        if nj-1!=0 or gameType==1:
                            if gameType!=1:
                                self.sheji[player_list][item][0]-=1
                            comp = compFactory.CreatePos(player_list)
                            pos = comp.GetFootPos()
                            rot = serverApi.GetEngineCompFactory().CreateRot(player_list).GetRot()
                            comp = compFactory.CreateProjectile(serverApi.GetLevelId())
                            from_rot=serverApi.GetDirFromRot(rot)
                            param = {
                                    'power': 2,
                                    'position': (pos[0]+from_rot[0]*0.8,pos[1]+1.12+from_rot[1]*0.8,pos[2]+from_rot[2]*0.8),
                                    'direction': (from_rot[0],from_rot[1],from_rot[2]),
                                }
                            id = comp.CreateProjectileEntity(player_list, "zaibian:laser_gatling_st", param)
                            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                            comp.SetCommand("/playsound harbinger_laser @s ~ ~ ~ 0.3",player_list)#传送指令
                    elif item=="zaibian:meat_shredder":
                        
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        LIST_=comp.GetEntitiesAroundByType(player_list, 3, serverApi.GetMinecraftEnum().EntityType.Mob)
                        if player_list in  LIST_ :
                            LIST_.remove(player_list)
                        st=None

                        comp = serverApi.GetEngineCompFactory().CreateItem(player_list)
                        item_=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                        fh=None
                        sh=0
                        for i in item_["enchantData"]:
                            if i[0]==13:
                                fh=i[1]
                            elif i[0]==9:
                                sh=1.25*i[1]
                        for i in LIST_:
                            comp = serverApi.GetEngineCompFactory().CreateGame(player_list)
                            if comp.CanSee(player_list,i,3.0,True,180.0,180.0):
                                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                                comp.Hurt(4, serverApi.GetMinecraftEnum().ActorDamageCause.Override, player_list, None, False)
                                if fh!=None:
                                    comp = serverApi.GetEngineCompFactory().CreateAttr(i)
                                    comp.SetEntityOnFire(2+fh, 1)
                                st=i
                        if st:
                            comp = compFactory.CreatePos(st)
                            pos = comp.GetFootPos()
                            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                            comp1 = serverApi.GetEngineCompFactory().CreateCollisionBox(st)
                            y=comp1.GetSize()[1]/2.0
                            for i in range(3):
                                comp.SetCommand("/particle  minecraft:lava_particle  {} {} {}".format(pos[0]+random.uniform(-0.3,0.3),pos[1]+y+random.uniform(-0.2,0.2),pos[2]+random.uniform(-0.3,0.3)))



            for plyerid in self.zb_xq:
                if self.zb_xq[plyerid].get(3)=="zaibian:ignitium_boots":
                    comp1 = serverApi.GetEngineCompFactory().CreatePos(plyerid)
                    pos1 = comp1.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateDimension(plyerid)
                    dim=comp.GetEntityDimensionId()
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    blockDict = comp.GetBlockNew((pos1[0], pos1[1]-1, pos1[2]), dim)
                    if blockDict['name']!='minecraft:air':
                        comp = serverApi.GetEngineCompFactory().CreatePlayer(plyerid)
                        is_sneaking = comp.isSneaking()
                        if not is_sneaking:
                            self.yanjiang(pos1,dim)

            # comp = serverApi.GetEngineCompFactory().CreateEffect(serverApi.GetPlayerList()[0])
            # res = comp.AddEffectToEntity("curse_of_desert", 15, 2, True)

            # comp = serverApi.GetEngineCompFactory().CreateAttr(serverApi.GetPlayerList()[0]) #TODO
            # # 如果设置的值超过属性当前的最大值，需要先扩充该属性的最大值，否则不生效。
            # comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 500)
            # comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 500)
            # comp = serverApi.GetEngineCompFactory().CreateAttr(serverApi.GetPlayerList()[1]) #TODO
            # # 如果设置的值超过属性当前的最大值，需要先扩充该属性的最大值，否则不生效。
            # comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 500)
            # comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 500)
            # comp1 = serverApi.GetEngineCompFactory().CreatePos(serverApi.GetPlayerList()[0])
            # pos1=comp1.GetPos()

            # pos2={'y': 30, 'x': 640, 'z': -640}

            # print pos1[0]-pos2['x'],pos1[1]-pos2['y'],pos1[2]-pos2['z']


            # comp = serverApi.GetEngineCompFactory().CreateBiome(levelId)
            # biomeName = comp.GetBiomeName(comp1.GetPos(), 1)
            # print biomeName
            for name in self.bolck_time.keys():
                if self.bolck_time[name]==0:
                    continue
                self.bolck_time[name]-=1

        del_=[]
        for i in self.tick_block_data:
            self.tick_block_data[i]-=1
            if self.tick_block_data[i]<=0:
                del_.append(i)
        for i in del_:
            del self.tick_block_data[i]
            
        for i in serverApi.GetPlayerList():
            comp = serverApi.GetEngineCompFactory().CreatePlayer(i)
            is_sneaking = comp.isSneaking()
            if self.playerid_sneaking.get(i,'0')!='0' and  is_sneaking ==self.playerid_sneaking[i][0]  :
                if self.playerid_sneaking[i][1]!=0:
                    self.playerid_sneaking[i][1]-=1
            else:
                k=0
                if self.playerid_sneaking.get(i,'0')=='0':
                    self.playerid_sneaking[i]={}
                    self.playerid_sneaking[i][1]=0

                if is_sneaking:
                    comp = serverApi.GetEngineCompFactory().CreateItem(i)
                    PlayerItem=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, 1)
                    if PlayerItem and PlayerItem["newItemName"]=="zaibian:bloom_stone_pauldrons" and  self.playerid_sneaking[i][1]==0:
                        comp1 = serverApi.GetEngineCompFactory().CreatePos(i)
                        pos1 = comp1.GetFootPos()
                        comp = serverApi.GetEngineCompFactory().CreateDimension(i)
                        dim=comp.GetEntityDimensionId()
                        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                        blockDict = comp.GetBlockNew((int(pos1[0]), int(pos1[1])-1, int(pos1[2])), dim)
                        if blockDict['name']=="minecraft:air":
                            k=1
                        else:
                            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                            comp.SetCommand("/particle  zaibian:close_di5 {} {} {}".format(pos1[0],pos1[1],pos1[2]))
                            comp.SetCommand("/playsound  dig.grass @s {} {} {}".format(pos1[0],pos1[1],pos1[2]),i)
                            k=2
                    else:
                        if  PlayerItem and PlayerItem["newItemName"]=="zaibian:bloom_stone_pauldrons":
                            comp = serverApi.GetEngineCompFactory().CreateMsg(i)
                            comp.NotifyOneMessage(i, '冷却中 剩余{}秒'.format(self.playerid_sneaking[i][1]/30+1), "§c")
                        k=1
                else:
                    if  self.playerid_sneaking[i].get(2)==2:
                        self.playerid_sneaking[i][1]=150
                        self.skill_bloom_stone_pauldrons(i)

                    
                self.playerid_sneaking[i][0]=is_sneaking
                self.playerid_sneaking[i][2]=k


                self.BroadcastToAllClient("zhaohuan",{"key":"sneaking","id":i,'pos':k})

                    

 
    def DamageEvent(self,args):
        def func():
            comp = serverApi.GetEngineCompFactory().CreateGravity(entityId)
            comp.SetGravity(0)
        srcId=args["srcId"]
        entityId=args["entityId"]
        cause=args["cause"]
        # return 
        # if entityId in serverApi.GetPlayerList():
        #     args["damage"]=0
        #     args["knock"]=False
            
 
        if entityId in serverApi.GetPlayerList():
            comp2 = serverApi.GetEngineCompFactory().CreateItem(entityId)
            item=comp2.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, 2)
            if item and item["newItemName"]=="zaibian:ignitium_leggings":
                comp = serverApi.GetEngineCompFactory().CreateAttr(srcId)
                comp.SetEntityOnFire(3, 2)

            item=comp2.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, 1)
            if item and item["newItemName"]=="zaibian:bloom_stone_pauldrons" and cause=="projectile" and self.playerid_sneaking[entityId][0]:
                args["damage"]=0
                args["ignite"]=False
                args["knock"]=False

            
            comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
            item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, 3)
            if item and item["newItemName"]=="zaibian:ignitium_boots" and cause in ["lava" ,"fire","fire_tick"]:
                args["damage"]=0
                args["ignite"]=False
                args["knock"]=False
                comp = serverApi.GetEngineCompFactory().CreateAttr(srcId)
                comp.SetEntityOnFire(0, 0)

        if srcId in serverApi.GetPlayerList():
            comp = serverApi.GetEngineCompFactory().CreateItem(srcId)
            item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 2)
            if item and item["newItemName"]in["zaibian:coral_spear" ,"zaibian:coral_bardiche","zaibian:tidal_claws"] :
                sh={"zaibian:coral_spear":7,"zaibian:coral_bardiche":11,"zaibian:tidal_claws":8}
                p=0
                if   item["newItemName"] in ["zaibian:coral_spear","zaibian:coral_bardiche"]:
                    comp1 = serverApi.GetEngineCompFactory().CreatePos(srcId)
                    pos1 = comp1.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateDimension(srcId)
                    dim=comp.GetEntityDimensionId()
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    blockDict = comp.GetBlockNew((pos1[0], pos1[1]-1, pos1[2]), dim)
                    if blockDict['name']=='minecraft:air':
                        p=5
                args["damage"]=sh[item["newItemName"]]+p
            elif  item and item["newItemName"]in["zaibian:infernal_forge"]:
                comp = serverApi.GetEngineCompFactory().CreatePos(srcId)
                entityFootPos = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                entityFootPos1 = comp.GetFootPos()
                comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
                comp.SetMobKnockback(entityFootPos1[0]-entityFootPos[0], entityFootPos1[2]-entityFootPos[2], 2.5, 0.3,0.3)
                args["knock"]=False
        if args["cause"]=="entity_explosion":
            if  entityId in self.fangbao:
                args["damage"]=0
                args["knock"]=False
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0,func)
                comp = serverApi.GetEngineCompFactory().CreateGravity(entityId)
                comp.SetGravity(100)

        if entityId in self.baozhajl.keys() and self.baozhajl[entityId][0]:
            args["damage"]=0
            args["knock"]=False
            self.baozhajl[entityId][0]=False
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0,func)

        comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        EngineType=comp.GetEngineTypeStr()
        comp = serverApi.GetEngineCompFactory().CreateEngineType(srcId)
        EngineType1=comp.GetEngineTypeStr()

        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
        TypeFamily=comp.GetTypeFamily()



        

        if EngineType1 in moster1.pa_monster:
            '''自动攻击移除json攻击伤害列表'''
            if cause=="entity_attack":
                args['damage']=0
                args["knock"]=False

        if (EngineType=="zaibian:abyss_mine" or EngineType=="zaibian:abyss_blast_portal" ) and  args["cause"]!="none":
            args["damage"]=0
            args["knock"]=False
        elif EngineType in self.ip.keys() and cause=="suffocation":
            args["damage"]=0
            args["knock"]=False
        elif TypeFamily and  "pet_mob" in  TypeFamily:
            comp = serverApi.GetEngineCompFactory().CreateActorOwner(entityId)
            ownerId = comp.GetEntityOwner()
            if ownerId ==srcId:
                args['damage']=0
                args["knock"]=False
        elif EngineType1=="zaibian:koboleton":
            if random.randint(0,2)==1:
                if entityId in serverApi.GetPlayerList() and not  self.BountifulBaublesMod.GetItemBountiful(entityId,"zaibian:sticky_gloves"):
                    comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                    item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0,True)
                    if item:
                        comp1 = serverApi.GetEngineCompFactory().CreatePos(srcId)
                        pos1 = comp1.GetFootPos()
                        comp = serverApi.GetEngineCompFactory().CreateDimension(srcId)
                        dim=comp.GetEntityDimensionId()
                        itemEntityId = self.CreateEngineItemEntity(item, dim,(pos1[0],pos1[1]+0.5,pos1[2]))
                    comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                    comp.SpawnItemToPlayerCarried({}, entityId)
        elif EngineType=="zaibian:ignited_revenant1":
            if cause=="entity_attack":
                comp = serverApi.GetEngineCompFactory().CreateItem(srcId)
                item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                if item:
                    comp = serverApi.GetEngineCompFactory().CreateItem(levelId)
                    if comp.GetItemBasicInfo(item["newItemName"])["itemType"]=="axe":
                        return
            args['damage']=0
            args["knock"]=False
        elif EngineType1=="zaibian:lingzhu":
            comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
            res = comp.AddEffectToEntity("abyssal_fear", 4, 0, False)
        
        elif EngineType=="zaibian:lionfish" or  EngineType1=="zaibian:lionfish1":
            if EngineType=="zaibian:lionfish":
                comp = serverApi.GetEngineCompFactory().CreateEffect(srcId)
                res = comp.AddEffectToEntity("poison", 2, 0, True)
            else:
                comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
                res = comp.AddEffectToEntity("poison", 2, 0, True)
        elif EngineType=="zaibian:the_leviathan" :
            comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
            entityFootPos1 = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
            dim=comp.GetEntityDimensionId()
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            liquidBlockDict = comp.GetLiquidBlock(entityFootPos1, dim)
            if not liquidBlockDict and args["cause"]!="none" and self.set_data.get("2"):
                print "离水无敌（被动）"
                if srcId in serverApi.GetPlayerList():
                    comp = serverApi.GetEngineCompFactory().CreateGame(srcId)
                    # playerId 变量改为具体的玩家Id
                    comp.SetOneTipMessage(srcId, serverApi.GenerateColor("RED") + "利维坦 离水无敌（被动）")
                args["damage"]=0
                args["knock"]=False
                args["ignite"]=False

        elif  EngineType1=="zaibian:deepling_angler":
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(srcId)
            k=entitycomp.GetExtraData("skill")
            if k==4:
                comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
                res = comp.AddEffectToEntity("poison", 4, 1, True)

        elif EngineType1 and  EngineType1=="zaibian:ignis" :
            if cause=="entity_attack":
                args['damage']=0
                args["knock"]=False
            elif cause=="block_explosion" and EngineType and EngineType!="withered:withered_block"  and args['damage']>0 :
                comp = serverApi.GetEngineCompFactory().CreateAttr(srcId)
                dq_HEALTH=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,dq_HEALTH+10)
                comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
                dq_HEALTH=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                if dq_HEALTH:
                    args['damage']+=int(dq_HEALTH*0.02)

        elif EngineType1=="zaibian:void_rune":
            comp = serverApi.GetEngineCompFactory().CreateModAttr(srcId)
            args["damage"]=0
            args["knock"]=False
            if comp.GetAttr('zr')==entityId:
                return
            for i in range(7):
                comp = serverApi.GetEngineCompFactory().CreateHurt(entityId)
                comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp1.AddTimer(i*0.3,comp.Hurt,random.randint(1,1), serverApi.GetMinecraftEnum().ActorDamageCause.Magic, None, None, True)


        elif EngineType and EngineType=="zaibian:ignis_psw1":
            if cause!="entity_attack":
                args["damage"]=0
                args["knock"]=False
            rotComp = serverApi.GetEngineCompFactory().CreateRot(srcId)
            rot = rotComp.GetRot()
            if not rot:
                return
            x, y, z = serverApi.GetDirFromRot(rot)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            entitycomp.SetExtraData("teshu", '1') 
            self.DestroyEntity(entityId)
            comp = serverApi.GetEngineCompFactory().CreatePos(srcId)
            entityFootPos1 = comp.GetFootPos()
            comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
            param = {
                'position': (entityFootPos1[0]+x*2,entityFootPos1[1]+1.5,entityFootPos1[2]+z*2),
                'direction': (x, y, z),
                'power':3
            }
            id=comp.CreateProjectileEntity(srcId, "zaibian:ignis_psw", param)
            comp = serverApi.GetEngineCompFactory().CreateEntityEvent(id)
            comp.TriggerCustomEvent(id, "minecraft:mark_v")


        if EngineType and  EngineType1 and ( (EngineType in moster1.mosters.keys() and EngineType==EngineType1) or (EngineType in ["zaibian:nameless_sorcerer","zaibian:nameless_sorcerer_fs" ] and EngineType1 in ["zaibian:nameless_sorcerer","zaibian:nameless_sorcerer_fs" ])):
            args["damage"]=0
            args["knock"]=False
            args["ignite"]=False
        if EngineType=="zaibian:ender_guardian" :
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if  (args["cause"]=="projectile" and  entitycomp.GetExtraData("stage")==None) :
                args["damage"]=0
                args["knock"]=False
                args["ignite"]=False
            comp1 = serverApi.GetEngineCompFactory().CreatePos(entityId)
            pos1=comp1.GetPos()
            if not self.bolck_time.get(entityId) and args["damage"]>0:
                self.bolck_time[entityId]=40
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/playanimation @e[x={},y={},z={},r=0.1] injure".format(pos1[0],pos1[1],pos1[2],))#传送指令
        elif EngineType=="zaibian:ender_golem" :
            comp = serverApi.GetEngineCompFactory().CreateEntityComponent(entityId)
            if  "timer" not  in  comp.GetAllComponentsName() :
                comp =  serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                comp.TriggerCustomEvent(entityId,"skill_use10")
            comp1 = serverApi.GetEngineCompFactory().CreatePos(entityId)
            pos1=comp1.GetPos()
            if  args["damage"]>0:
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/playanimation @e[x={},y={},z={},r=0.1] injure0".format(pos1[0],pos1[1],pos1[2],))#传送指令
        elif EngineType=="zaibian:the_prowler" :
            comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(entityId)
            result = comp.GetVariant()
            if not self.bolck_time.get(entityId) and result==1:
                self.bolck_time[entityId]=40
                comp1 = serverApi.GetEngineCompFactory().CreatePos(entityId)
                pos1=comp1.GetPos()
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/playanimation @e[x={},y={},z={},r=0.1] injure0".format(pos1[0],pos1[1],pos1[2],))#传送指令
        elif EngineType=="zaibian:netherite_monstrosity" :
            comp = serverApi.GetEngineCompFactory().CreateEntityComponent(entityId)
            if  "timer" not  in  comp.GetAllComponentsName() :
                comp =  serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                comp.TriggerCustomEvent(entityId,"start")
            comp1 = serverApi.GetEngineCompFactory().CreatePos(entityId)
            pos1=comp1.GetPos()
            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
            comp.SetCommand("/playanimation @e[x={},y={},z={},r=0.1] idle".format(pos1[0],pos1[1],pos1[2]))#传送指令
        
        elif EngineType=="zaibian:ignis" :
            comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
            item=comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, 0)
     
            if  item and item["newItemName"]=='zaibian:bulwark_of_the_flame_boss':
                dun_=True
            else:
                dun_=False
                
            comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
            if comp.GetAttr("skill_11"):
                args["damage"]=0
                args["knock"]=False
                args["ignite"]=False
                comp.SetAttr("skill_11",False)
                args["EngineTypeStr"]=EngineType
                moster1.mosters[EngineType](args).romve_skill("组合:None")
                comp.SetAttr("skill",True)
                comp1 = serverApi.GetEngineCompFactory().CreatePos(entityId)
                pos1=comp1.GetPos()
                comp = serverApi.GetEngineCompFactory().CreateEntityDefinitions(entityId)
                result = comp.SetMarkVariant(0)
                if dun_:
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/playanimation @e[x={},y={},z={},r=0.1] attack12e".format(pos1[0],pos1[1],pos1[2]))#传送指令
                else:
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/playanimation @e[x={},y={},z={},r=0.1] attack12e_1".format(pos1[0],pos1[1],pos1[2]))#传送指令
                def func2():
                    self.entity_boss_jl[entityId]=False
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    Entities=comp.GetEntitiesAroundByType(entityId, 8, serverApi.GetMinecraftEnum().EntityType.Mob)
                    for i in Entities:
                        if i==entityId :
                            continue
                        if not dun_:
                            break
                        if dun_:
                            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                            comp.SetCommand("/camerashake add @s 0.1 1 rotational",i)
                            comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                            comp.Hurt(random.randint(15,15), serverApi.GetMinecraftEnum().ActorDamageCause.BlockExplosion, entityId, None, True)
                    if  dun_:
                        comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
                        res = comp.AddEffectToEntity("regeneration", 1, 2, False)
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.1,moster1.mosters[EngineType](args).romve_skill)
                    else:
                        moster1.mosters[EngineType](args).skill_8()
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.5,moster1.mosters[EngineType](args).romve_skill)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0.5,func2)

                
                    

            
            if  dun_:
                if args["cause"]=="projectile" and srcId in serverApi.GetPlayerList():
                    comp = serverApi.GetEngineCompFactory().CreateEngineType(args["projectileId"])
                    EngineType2=comp.GetEngineTypeStr()

                    if EngineType2 and EngineType2=="zaibian:ignis_psw":
                        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                        dun=entitycomp.GetExtraData("dun") 
                        if dun=='ok':
                            return
                        
                        if dun:
                            dun+=1
                        else:
                            dun=1
                        if dun>=3:
                            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                            dun=entitycomp.SetExtraData("dun","ok") 
                            comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                            comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, None, 0)
                            return
                        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                        dun=entitycomp.SetExtraData("dun",dun) 
                        return
                    # comp = serverApi.GetEngineCompFactory().CreateItem(srcId)
                    # items=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                    # if items:
                    #     for i in items["enchantData"]:
                    #         if i[0]==34:
                    #             return
                comp = serverApi.GetEngineCompFactory().CreateGame(entityId)
                comp1 = serverApi.GetEngineCompFactory().CreateAction(entityId)
                comp2 = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
                if comp.CanSee(entityId,srcId,20.0,True,180.0,60.0)  and not comp2.GetAttr("skill") and comp1.GetAttackTarget()!="-1":
                    args["damage"]=0
                    args["knock"]=False
                    args["ignite"]=False


    def HealthChangeBeforeServerEvent(self,args):
        entityId=args["entityId"]
        if entityId in serverApi.GetPlayerList():
            comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
            dict_item =comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, 0)
            if dict_item and  dict_item["newItemName"]=="zaibian:monstrous_helm":
                comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
                health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                if health_max//2>args["to"] and (self.baozhajl.get(entityId)==None or self.baozhajl[entityId][1]==0 ):
                    comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
                    entityFootPos = comp.GetFootPos()
                    comp = serverApi.GetEngineCompFactory().CreateGravity(entityId)
                    comp.SetGravity(5)
                    comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
                    self.baozhajl[entityId]=[True,450]
                    comp.CreateExplosion(entityFootPos,5,False,False,entityId,entityId)
                    comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
                    res = comp.AddEffectToEntity("monstrous", 10, 1, True)

                    comp1 = serverApi.GetEngineCompFactory().CreateGravity(entityId)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(0.1,comp1.SetGravity,0)

        comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        EngineType=comp.GetEngineTypeStr()

        comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        EngineTypeStr=comp.GetEngineTypeStr()
        


        if EngineType == 'zaibian:emiss':
            args['cancel'] = True
        elif EngineType=="zaibian:ender_guardian":
            comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if  args["to"]>0:
                if health_max//2>args["to"] and entitycomp.GetExtraData("stage")==None:
                    entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                    entitycomp.SetExtraData("stage", 2)
                    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                    comp.TriggerCustomEvent(entityId,"star_use")
                    arg={"entityId":entityId,"EngineTypeStr":EngineType}
                    moster.use_stage(arg)
                    self.stage[entityId]=True
        elif EngineType=="zaibian:ancient_remnant":
            comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if  args["to"]>0:
                if health_max//2>args["to"] and entitycomp.GetExtraData("stage")==None:
                    entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                    entitycomp.SetExtraData("stage", 2)
                    
                    arg={"entityId":entityId,"EngineTypeStr":EngineType}
                    moster.use_stage(arg)
                    self.stage[entityId]=True
        
        elif EngineType=="zaibian:the_leviathan":
            comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if  args["to"]<=0 and entitycomp.GetExtraData("stage")==None:
                args['cancel']=True
                entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                entitycomp.SetExtraData("stage", 2)
                comp1 = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(1.0,comp1.TriggerCustomEvent,entityId,"star")
                arg={"entityId":entityId,"EngineTypeStr":EngineType}
                moster.use_stage(arg)
                comp.AddTimer(1.1,comp1.TriggerCustomEvent,entityId,"strr1")
                return

        elif EngineType=="zaibian:ignis":
            comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if  args["to"]>0:
                if health_max*0.67>args["to"] and entitycomp.GetExtraData("stage")==None:
                    entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                    entitycomp.SetExtraData("stage", 2)

                    
                    
                    comp1 = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp1.TriggerCustomEvent(entityId,"star")
                    # comp.AddTimer(1.0,)
                    arg={"entityId":entityId,"EngineTypeStr":EngineType}
                    moster.use_stage(arg)
                    comp.AddTimer(1.1,comp1.TriggerCustomEvent,entityId,"strr1")
                    self.stage[entityId]=2
                elif health_max//3>args["to"] and entitycomp.GetExtraData("stage")==2:
                    entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                    entitycomp.SetExtraData("stage", 3)
                    comp1 = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp1.TriggerCustomEvent(entityId,"star1")
                    # comp.AddTimer(1.0,comp1.TriggerCustomEvent,entityId,"star1")
                    self.stage[entityId]=3
                    arg={"entityId":entityId,"EngineTypeStr":EngineType}
                    moster.use_stage1(arg)

                    comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
                    comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, None, 0)
                                

        elif EngineType=="zaibian:netherite_monstrosity":
            comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if  args["to"]>0:
                if health_max//3>args["to"] and entitycomp.GetExtraData("stage")==None and args["to"]>0:
                    entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                    entitycomp.SetExtraData("stage", 2)
                    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                    comp.TriggerCustomEvent(entityId,"star_use")
                    arg={"entityId":entityId,"EngineTypeStr":EngineType}
                    moster.use_stage(arg)
                    self.stage[entityId]=True
        elif EngineType=="zaibian:the_harbinger":
            comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            health_max=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
            if  args["to"]>0:
                if health_max//2>args["to"] :
                    if entitycomp.GetExtraData("stage")==None or entitycomp.GetExtraData("stage")!=2:
                        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                        entitycomp.SetExtraData("stage", 2)
                        comp1 = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.0,comp1.TriggerCustomEvent,entityId,"star1")
                        comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                        arg={"entityId":entityId,"EngineTypeStr":EngineType}
                        moster.use_stage(arg)
                        self.stage[entityId]=True
                else:
                    if entitycomp.GetExtraData("stage")==2  :
                        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(entityId)
                        entitycomp.SetExtraData("stage", 0)
                        comp1 = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                        comp.AddTimer(0.0,comp1.TriggerCustomEvent,entityId,"star")
                        self.stage[entityId]=False

        elif EngineType=="zaibian:ignited_revenant1":
            if args["to"] <=0:
                comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
                data=comp.GetAttr('data')
                p={"q":0,"h":1,"z":2,"y":3}
                comp = serverApi.GetEngineCompFactory().CreateAttr(data["id"])
                LUCK=int(comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.LUCK))
                list1=["0","0","0","0"]
                for index,i in enumerate(list(str(LUCK))[::-1]):
                    index+=1
                    list1[-index]=i
                list1[p[data["fx"]]]='0'
                LUCK=int(''.join(list1))
                comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.LUCK,LUCK)
                self.BroadcastToAllClient("ignited_revenant_dun",{'id':data["id"],"luck":LUCK})
                self.DestroyEntity(entityId)

         

        if args["to"]<=0 and entityId not in  self.die_list[1]  and EngineTypeStr in moster1.mosters.keys() :
            
            args['cancel']=True
            args["EngineTypeStr"]=EngineTypeStr
            args["self"]=self
            args['shid']=self.entity_boss_atk.get(entityId)
            moster.start_death(args)
            def f():
                comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
                comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 1)
            comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
            comp.AddTimer(0.1,f)

                    

    def OnRangedWeaponReleaseUsingServerEvent(self, args):
        bow_item={
            "zaibian:bow":{"imName":"zaibian:void_scatter_arrow","MAX_count":1,"arrow_hurt":None,"durable":False}
        }
        playerId = args["playerId"]

        itemname=args["itemDict"]["newItemName"]
    


        if  args["itemDict"]["newItemName"] in ["zaibian:coral_spear" ,"zaibian:coral_bardiche"] :
            st={}
            pow=(args["maxUseDuration"]-args["durationLeft"])
            if pow>=10:
                comp = compFactory.CreatePos(playerId)
                pos = comp.GetPos()
                rot = serverApi.GetEngineCompFactory().CreateRot(playerId).GetRot()
                comp = compFactory.CreateProjectile(serverApi.GetLevelId())
                from_rot=serverApi.GetDirFromRot(rot)

                param = {
                        'power': 4 * 1,
                        'position': pos,
                        'direction': (from_rot[0]+random.uniform(-0.03,0.03),from_rot[1]+random.uniform(-0.03,0.03),from_rot[2]+random.uniform(-0.03,0.03)),
                    }
                id = comp.CreateProjectileEntity(playerId, args["itemDict"]["newItemName"]+"_st", param)
                comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                comp.SetAttr('ImmuneDamage', 1)
                comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp1.AddTimer(0.1,comp.SetAttr,'ImmuneDamage', 0)

                Type_=1
                gameType_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
                gameType = gameType_comp.GetPlayerGameType(playerId)
                if gameType==1:Type_=0
                if Type_!=0 :
                    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                    comp.SpawnItemToPlayerCarried({}, playerId)

        elif args["itemDict"]["newItemName"] in bow_item.keys():
            playerId = args["playerId"]
            comp = compFactory.CreatePos(playerId)
            pos = comp.GetPos()
            rot = serverApi.GetEngineCompFactory().CreateRot(playerId).GetRot()
            comp = compFactory.CreateProjectile(serverApi.GetLevelId())
            power = self.getLaunchPower(args['durationLeft'], args['maxUseDuration'])
            from_rot=serverApi.GetDirFromRot(rot)


            imName=bow_item[itemname]["imName"]
            MAX_count=bow_item[itemname]["MAX_count"]
            arrow_hurt=bow_item[itemname]["arrow_hurt"]
            durable=bow_item[itemname]["durable"]

            Type_=1
            gameType_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
            gameType = gameType_comp.GetPlayerGameType(playerId)
            if gameType==1:Type_=0

            AllItems_comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            AllItems=AllItems_comp.GetPlayerAllItems(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)
            arrowSlotDict = [(slot,AllItems[slot].get('count'),AllItems[slot].get('auxValue')) for slot in range(36) if AllItems[slot] and imName in  AllItems[slot].get('itemName')]
            gameType_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
            gameType = gameType_comp.GetPlayerGameType(playerId)
 
            master_hand=AllItems_comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
            if (22,1) in master_hand['enchantData']: count=0
            if Type_==0:
                count=0
            else:
                count=MAX_count
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

     
            for i in range(MAX_count-count):
                if arrow_hurt:
                    param = {
                        'power': 2 * power,
                        'position': pos,
                        'direction': (from_rot[0]+random.uniform(-0.03,0.03),from_rot[1]+random.uniform(-0.03,0.03),from_rot[2]+random.uniform(-0.03,0.03)),
                        'damage':arrow_hurt
                    }
                else:
                    param = {
                        'power': 2 * power,
                        'position': pos,
                        'direction': (from_rot[0]+random.uniform(-0.03,0.03),from_rot[1]+random.uniform(-0.03,0.03),from_rot[2]+random.uniform(-0.03,0.03)),
                    }
                    
                id = comp.CreateProjectileEntity(playerId, imName, param)


            if Type_!=0 and MAX_count-count>0:
                if durable:
                    comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
                    comp.AddTimer(0.1,self.durable_consume_durable,playerId)
        


    def ProjectileDoHitEffectEvent(self, args):
        # 设为True后，将取消这次的抛射物碰撞事件
        # arg={"entityId":serverApi.GetPlayerList()[0],"EngineTypeStr":"zaibian:ender_guardian"}
        # moster.use_skill(arg)
        id=args["id"]
        srcId=args["srcId"]
        targetId=args["targetId"]

        comp = serverApi.GetEngineCompFactory().CreateEngineType(args["id"])
        EngineTypeStr=comp.GetEngineTypeStr()
        if not EngineTypeStr:
            return
        comp = serverApi.GetEngineCompFactory().CreateDimension(args["id"])
        dim=comp.GetEntityDimensionId()
        if args['hitTargetType']=="ENTITY":
                x,y,z=args["x"],args["y"],args["z"]
        else:
            x,y,z=args["blockPosX"],args["blockPosY"],args["blockPosZ"]
        if EngineTypeStr and "void_scatter_arrow" in EngineTypeStr :
            self.BroadcastToAllClient("void_scatter_arrowlz",[(x,y+0.5,z)])
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesInSquareArea(None, (x-5,y-5,z-5), (x+5,y+5,z+5), dim) 
            for i in  Entities:
                if i== args['srcId'] :
                    continue
                else:
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(6, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, args['srcId'], None, False)
        elif "ignis_psw" in EngineTypeStr :
            comp = serverApi.GetEngineCompFactory().CreateEngineType(targetId)
            EngineTypeStr1=comp.GetEngineTypeStr()
            if EngineTypeStr1 in ["withered:withered_block","zaibian:ignis","zaibian:ignis_psw","zaibian:ignis_psw1"]:
                args["cancel"]=True
                return
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesInSquareArea(None, (x-5,y-5,z-5), (x+5,y+5,z+5), dim) 
            for i in  Entities:
                if i== args['srcId'] :
                    continue
                else:
                    comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                    comp.Hurt(20, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, args['srcId'], None, False)
            comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
            comp.CreateExplosion(( x,y,z),1,False,False,None,serverApi.GetPlayerList()[0])      
        elif "laser_gatling_st" in EngineTypeStr :
            blockDict = {
                'name': 'minecraft:fire',
                'aux': 0
            }
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockNew((x,y+1,z), blockDict, 0, dim)
                
        elif "netherite_monstrosity_zd" in EngineTypeStr :
            for i in range(0,2):
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                dict_=comp.GetBlockNew((x,y+i,z), dim)
                if dict_["name"]=="minecraft:air":
                    blockDict = {
                        'name': 'minecraft:flowing_lava',
                        'aux': 0
                    }
                    comp.SetBlockNew((x,y+1,z), blockDict, 0, dim)
                    break

            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesInSquareArea(None, (x-5,y-5,z-5), (x+5,y+5,z+5), dim) 
            for i in  Entities:
                if i== id :
                    continue
                comp = serverApi.GetEngineCompFactory().CreatePos(i)
                entityFootPos = comp.GetFootPos()
                pl=self.calculate_distance(entityFootPos,(x,y,z))
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                if 5-pl==0:
                    return
                comp.Hurt(int((5-pl)*20/5), serverApi.GetMinecraftEnum().ActorDamageCause.EntityExplosion, args['srcId'], None, True)

        elif "zaibian:soulian1" == EngineTypeStr :
            args["cancel"]=True

    

     
        
        elif "zaibian:soulian" == EngineTypeStr :
            comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
            playerId=comp.GetAttr('playerId')

            comp = compFactory.CreatePos(playerId)
            pos = comp.GetPos()
            comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
            is_sneaking = comp.isSneaking()

            comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
            if not comp.GetAttr('id'):
                self.BroadcastToAllClient('zhaohuan',{'pos': pos,'key':'soulian',"data":1})

            if args["hitTargetType"]=="ENTITY" :
                args["cancel"]=True
                if is_sneaking:
                    comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                    comp.SetAttr('id',args["targetId"])
                    def f():
                        comp =serverApi.GetEngineCompFactory().CreateEntityEvent(id)
                        comp.TriggerCustomEvent(id,"skill_use2")

            
                    comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
                    comp.AddTimer(0.2,f)
                
            else:
                comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
                if comp.GetAttr('id'):
                    args["cancel"]=True
            
                


        elif EngineTypeStr =='zaibian:the_harbinger_psw'  or  EngineTypeStr =='zaibian:the_harbinger_pswd'or  EngineTypeStr =='zaibian:the_harbinger_psw2':

            if  EngineTypeStr =='zaibian:the_harbinger_psw2':
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesInSquareArea(None, (x-3,y-3,z-3), (x+3,y+3,z+3), dim) 
                for i in Entities:
                    if i!= args['srcId']:
                        comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                        res = comp.AddEffectToEntity("wither", 2, 1, True)
                comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
                comp.CreateExplosion(( x,y,z),1,False,False,None,serverApi.GetPlayerList()[0])
            elif  EngineTypeStr =='zaibian:the_harbinger_pswd':
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesInSquareArea(None, (x-6,y-6,z-6), (x+6,y+6,z+6), dim) 
                for i in Entities:
                    if i!= args['srcId']:
                        comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                        res = comp.AddEffectToEntity("wither", 20, 2, True)
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/particle  min_baozha {} {} {}".format( x,y+1,z))
                comp.SetCommand("/playsound  random.explode @s {} {} {} 5000".format(x,y,z),srcId)
            else:
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                Entities=comp.GetEntitiesInSquareArea(None, (x-5,y-5,z-5), (x+5,y+5,z+5), dim) 
                for i in Entities:
                    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                    comp.SetCommand("/camerashake add @s 0.1 0.6 rotational",i)
                    if i!= args['srcId']:
                        comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                        res = comp.AddEffectToEntity("wither", 10, 2, True)
                comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
                comp.CreateExplosion(( x,y,z),2,False,False,None,serverApi.GetPlayerList()[0])
                comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
                comp.SetCommand("/particle  the_harbinger_diao {} {} {}".format( x,y+1,z))
                def f(x,y,z,srcId,s):
                    time=s/2
                    if time<6:
                        r=2.5
                    else:
                        r=round(2.5-((time-5)/4),0)
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    Entities=comp.GetEntitiesInSquareArea(None, (x-r,y-5,z-r), (x+r,y+5,z+r), dim) 
                    for i in Entities:
                        if i!= srcId:
                            comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                            res = comp.AddEffectToEntity("wither", 3, 2, True)
                for i in range(24):
                    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                    comp.AddTimer(0.5*i,f,x,y,z, args['srcId'],i)


        elif EngineTypeStr =='zaibian:void_assault_shoulder_psw':
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            Entities=comp.GetEntitiesInSquareArea(None, (x-8,y-8,z-8), (x+8,y+8,z+8), dim) 
            comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
            for i in Entities:
                comp.SetCommand("/camerashake add @s 0.1 1 rotational",i)
            comp.SetCommand("/playsound  random.explode @s {} {} {} 5000".format(x,y,z),srcId)
            def yq(r):
                a,b = 0,0  #圆点坐标
                aa=[]
                w = r*3  # 圆平均分为10份
                m = (2*math.pi)/w #一个圆分成10份，每一份弧度为 m
                point_list =[]
                for i in range(0, w+1):
                    x = round( a+r*math.sin(m*i),2) 
                    y = round( b+r*math.cos(m*i),2)
                    point_list .append([x,y])
                aa.append(point_list)
                return point_list
            comp = serverApi.GetEngineCompFactory().CreatePos(args['id'])
            entityFootPos = comp.GetFootPos()
            pos1=entityFootPos[0],round(entityFootPos[1],0)-1,entityFootPos[2]
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict_ = comp.GetBlockNew(pos1, dim) 
            if blockDict_["name"]=="minecraft:air" :
                entityFootPos=entityFootPos[0],round(entityFootPos[1],0)-1,entityFootPos[2]


            o=0
            for i1 in [yq(2),yq(3),yq(4),yq(5)]:
                def f(i1):
                    for i in i1:    #放置15个磨牙
                        iop=self.CreateEngineEntityByTypeStr('zaibian:void_rune', (i[0]+entityFootPos[0],entityFootPos[1],i[1]+entityFootPos[2]), (0,0), dim)
                        comp = serverApi.GetEngineCompFactory().CreateModAttr(iop)
                        comp.SetAttr('zr',srcId)

                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(0.1*o,f,i1)
                o+=1


    def OnPlayerBlockedByShieldAfterServerEvent(self,args):
        playerId=args["playerId"]
        sourceId=args["sourceId"]
        if sourceId!="-1" and args['itemDict']["newItemName"]=="zaibian:shield":
            comp = serverApi.GetEngineCompFactory().CreateAttr(sourceId)
            comp.SetEntityOnFire(5, 3)

    def PlayerAttackEntityEvent(self,args):
        playerId=args["playerId"]
        victimId=args["victimId"]

        # comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        # Entities=comp.GetEntitiesAroundByType(victimId, 10, serverApi.GetMinecraftEnum().EntityType.Mob)
        # Entities.remove(victimId)
        # comp = serverApi.GetEngineCompFactory().CreateAction(victimId)
        # comp.SetAttackTarget(Entities[0]) #TODO

        # args['damage']=52
        # args["isValid"]=1
        comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        dict_item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if dict_item:
            if "final_fractal" in dict_item["newItemName"]:
                comp = serverApi.GetEngineCompFactory().CreateAttr(victimId)
                hralth=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
                args['damage']=int(11+hralth*0.03)
                args["isValid"]=1
            elif "zweiender" in dict_item["newItemName"]:
                comp = serverApi.GetEngineCompFactory().CreateGame(victimId)
                if not comp.CanSee(victimId,playerId,8.0,True,150.0,150.0):
                    args['damage']=22
                    args["isValid"]=1


    def ServerItemUseOnEvent(self,args):
        '''台阶'''
        pos=args['x'],args['y'],args['z']
        blockName=args['blockName']
        entityId=args['entityId']
        dimensionId=args['dimensionId']
        face=args['face']
        itemDict=args['itemDict']


        if itemDict["newItemName"] =="zaibian:chorus_slab_0":
            if face==0:
                pos1=args['x'],args['y']-1,args['z']
            elif face==1:
                pos1=args['x'],args['y']+1,args['z']
            elif face==4:
                pos1=args['x']-1,args['y'],args['z']
            elif face==3:
                pos1=args['x'],args['y'],args['z']+1
            elif face==5:
                pos1=args['x']+1,args['y'],args['z']
            elif face==2:
                pos1=args['x'],args['y'],args['z']-1
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew(pos, dimensionId)
            if "zaibian:chorus_slab_" in blockDict["name"] and face in [1,0]:
                blockDict = {
                    'name': 'zaibian:chorus_planks',
                    'aux': 0
                }
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockNew(pos, blockDict, 0, dimensionId)

                def f():
                    blockDict = {
                    'name': 'minecraft:air',
                    'aux': 0
                    }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    comp.SetBlockNew(pos1, blockDict, 0, dimensionId)

                comp1 = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp1.AddTimer(0,f)
            else:
                comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                blockDict=comp.GetBlockNew(pos1, dimensionId)
                if args['clickY']>0.5 and face in [4,3,5,2]:
                    if "zaibian:chorus_slab_" in blockDict["name"] :
                        blockDict = {
                        'name': 'zaibian:chorus_planks',
                        'aux': 0
                        }
                    else:
                        blockDict = {
                        'name': 'zaibian:chorus_slab_1',
                        'aux': 0
                        }

                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    comp.SetBlockNew(pos1, blockDict, 0, dimensionId)
                elif "zaibian:chorus_slab_" in blockDict["name"] :
                    blockDict = {
                        'name': 'zaibian:chorus_planks',
                        'aux': 0
                        }
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    comp.SetBlockNew(pos1, blockDict, 0, dimensionId)


        elif itemDict["newItemName"] =="zaibian:the_baby_leviathan_bucket":
            if face==0:
                pos1=args['x'],args['y']-1,args['z']
            elif face==1:
                pos1=args['x'],args['y']+1,args['z']
            elif face==4:
                pos1=args['x']-1,args['y'],args['z']
            elif face==3:
                pos1=args['x'],args['y'],args['z']+1
            elif face==5:
                pos1=args['x']+1,args['y'],args['z']
            elif face==2:
                pos1=args['x'],args['y'],args['z']-1
            entityId = self.CreateEngineEntityByTypeStr('zaibian:the_baby_leviathan', pos1, (0, 0), dimensionId)
            if  itemDict["extraId"]!="":
                tameComp = serverApi.GetEngineCompFactory().CreateTame(entityId)
                tameComp.SetEntityTamed(itemDict["extraId"],entityId)
                envComp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
                envComp.TriggerCustomEvent(entityId,'the_baby_leviathan_tame')

        
                                    
     
    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(levelId)
        entitycomp.SetExtraData("stucture_bc", self.stucture) 
        # for entityId in self.die_list[0]:
        #     comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        #     comp.KillEntity(entityId)
        # 调用上面的反监听函数来销毁
        pass


    
    # -*- coding: utf-8 -*-

      

        


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
    