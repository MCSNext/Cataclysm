# -*- coding: utf-8 -*-

# 获取引擎服务端API的模块
import random,copy
import mod.server.extraServerApi as serverApi
from mod_effect_eF9xM9.modServer.manager import get_singleton,engineAPI
import mod_effect_eF9xM9.modCommon.modConfig as modConfig
import collections,math
from common.utils.mcmath import Vector3

# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()

# 在modMain中注册的Server System类
class PyServerSystem(ServerSystem):
    # ServerSystem的初始化函数
    def __init__(self, namespace, systemName):
        # 首先调用父类的初始化函数
        super(PyServerSystem, self).__init__(namespace, systemName)
        single_mgr = get_singleton()
        single_mgr.set_server_system(self)
        # 初始时调用监听函数监听事件
        self.ListenEvent()
        self.mFrameCount = 0
        self.returns_damage_dict = {"玩家ID":["0/1 是否反伤","反伤百分比"]}
        self.repairing_dict = {"玩家ID":["0/1 是否有修复效果","每秒修复效果"]}
        self.playerEffectDict = collections.defaultdict(set)
        '''标记玩家都有什么状态'''
        self.SFlyStartDict = collections.defaultdict(int)
        '''用于玩家起飞时添加动力'''
        self.useMoveBtnDict = collections.defaultdict(bool)
        '''用于标记玩家是否正在使用移动按钮'''

        self.elytraFireworksDict = {}
        '''鞘翅飞行中使用烟花的玩家'''

        self.usingSystemInfo = {
            "hasInit":False,
            "hasUsing":False,
            "usingModMark":[],
            "needNoticeList":[]
        }
        ''''
        正在使用的状态包信息
            未使用的包不激活功能
        '''
        self.usingSystem = None
        '''激活功能包的实例'''

        self.thisModMark = {
            "time":20231210,
            "ModName":modConfig.ModName,
            "ServerSystemName":modConfig.ServerSystemName,
            "ClientSystemName":modConfig.ClientSystemName
        }
        '''这个包的唯一标识,[版本时间,包名,服务端类名]
        用于只激活最新版本包
        '''
        self.queryWhetherNeedActivateFunc()

        # engineAPI.SetGameRulesInfoServer({
        #     'option_info': {
        #     },
        #     'cheat_info': {
        #         'always_day': True,  # 终为白日
        #         "weather_cycle": False
        #     }
        # })  # TODO 待删除
        
    def getSystemInUseFunc(self):
        '''获得被激活的状态包的实例'''
        return self.usingSystem

    def queryWhetherNeedActivateFunc(self):
        '''查询是否需要激活这个包'''
        comp = serverApi.GetEngineCompFactory().CreateModAttr(serverApi.GetLevelId())
        cacheList = comp.GetAttr('yeffectmod_sign',[])
        cacheList.append(self.thisModMark)
        comp.SetAttr('yeffectmod_sign',cacheList)
        def func0():
            cacheList = comp.GetAttr('yeffectmod_sign',[])
            cacheList = sorted(cacheList,key=lambda x:x["time"],reverse=True)
            if cacheList[0] == self.thisModMark:
                self.usingSystemInfo['hasUsing'] = True
            
            self.usingSystem = serverApi.GetSystem(cacheList[0]["ModName"],cacheList[0]["ServerSystemName"])
            self.usingSystemInfo['hasInit'] = True
            self.usingSystemInfo['usingModMark'] = cacheList[0]
            for playerId in self.usingSystemInfo['needNoticeList']:
                self.NotifyToClient(playerId,"yEffectInfoToClient",{
                    "class":"PyClientSystem",
                    "funcName":"getSFSignInfoFunc",
                    "playerId":playerId,
                    "data":self.usingSystemInfo
                })
                pass
            self.usingSystemInfo['needNoticeList'] = []
        engineAPI.add_timer(1,func0)  #这里不确定1秒是否所有包都被启用了,但感觉应该够了
        pass


    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.DamageEvent) #伤害事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEffectServerEvent", self, self.AddEffectServerEvent) #状态增加
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "RemoveEffectServerEvent", self, self.RemoveEffectServerEvent) #状态移除
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "RefreshEffectServerEvent", self, self.RefreshEffectServerEvent) #状态更新
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'DelServerPlayerEvent', self, self.DelServerPlayerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddServerPlayerEvent", self, self.AddServerPlayerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerItemTryUseEvent", self, self.ServerItemTryUseEvent)


        self.ListenForEvent(modConfig.ModName, modConfig.ClientSystemName,'yEffectInfoToServer', self, self.yEffectInfoToServer) 


    def ServerItemTryUseEvent(self, args):
        '''玩家点击右键尝试使用物品时服务端抛出的事件。注：如果需要取消物品的使用需要同时在ClientItemTryUseEvent和ServerItemTryUseEvent中将cancel设置为True才能正确取消。'''
        playerId = args["playerId"]
        itemDict = args["itemDict"]

        if itemDict['itemName'] == "minecraft:fireworks" and playerId in self.playerEffectDict['elytraFly']:
            self.elytraFireworksDict[playerId] = 2
            pass
        pass

    def AddServerPlayerEvent(self, args):
        '''玩家加入时触发该事件。'''
        # print("134------------0",self.mFrameCount)
        pass

    def playerStopLoadFunc(self, args):
        if not self.usingSystemInfo['hasInit']:
            self.usingSystemInfo['needNoticeList'].append(args['playerId'])
            return
        playerId = args['playerId']
        self.NotifyToClient(playerId,"yEffectInfoToClient",{
            "class":"PyClientSystem",
            "funcName":"getSFSignInfoFunc",
            "playerId":playerId,
            "data":self.usingSystemInfo
        })


    def playerChangeUseMoveBtnFunc(self, args):
        '''玩家开始/结束使用移动按钮'''
        self.useMoveBtnDict[args['playerId']] = args['data']
        pass

    def changeSFlyAnimatToServerFunc(self, args):
        '''开始/结束 特殊飞行'''
        args['class'] = 'PyClientSystem'
        args['funcName'] = 'changeSFlyAnimatToClientFunc'
        self.BroadcastToAllClient("yEffectInfoToClient", args)
        playerId = args['playerId']
        if args['willStart']:
            self.playerEffectDict['specialFly'].add(playerId)
            self.SFlyStartDict[playerId] = 45
        else:
            self.playerEffectDict['specialFly'].discard(playerId)
            if playerId in self.SFlyStartDict:
                del self.SFlyStartDict[playerId]
        pass

    def yEffectInfoToServer(self, args):
        if args['class'] == "PyServerSystem":
            cacheFunc = getattr(self,args['funcName'],None)
            if cacheFunc:
                cacheFunc(args)
        pass


    def DelServerPlayerEvent(self, args):
        '''删除玩家时触发该事件。'''
        playerId = args['id']
        if playerId in self.returns_damage_dict:
            del self.returns_damage_dict[playerId]
        if playerId in self.repairing_dict:
            del self.repairing_dict[playerId]
             
        for val in self.playerEffectDict.values():
            val.discard(playerId)

        pass

    def AddEffectServerEvent(self, args):
        '''状态增加'''
        entityId = args['entityId']
        if args['effectName'] == "y_returns_damage":
            '''反伤'''
            _cache = {
                0:0.333,
                1:0.5,
                2:1.0
            }
            self.returns_damage_dict[args['entityId']] = [1,_cache[args['effectAmplifier']]]
        elif args['effectName'] == "y_repairing":
            '''原地复活'''
            _cache = {
                0:1,
                1:3,
                2:10
            }
            self.repairing_dict[args['entityId']] = [1,_cache[args['effectAmplifier']]]
            pass
        elif args['effectName'] == "y_stepup":
            '''上台阶能力提升'''
            comp = serverApi.GetEngineCompFactory().CreateAttr(args['entityId'])
            _cache = {
                0:2.0,
                1:3.0,
                2:50.0
            }
            comp.SetStepHeight(_cache[args['effectAmplifier']]+0.0625)
        
        elif args['effectName'] == "y_weight":
            '''超重'''
            engineAPI.SetGravity(entityId,-0.1)
            pass
        elif args['effectName'] in ["y_ooo","y_spin","y_random_tp","y_lightning","y_flytwo","y_solidcore","y_elytra"]:
            self.playerEffectDict[args['effectName']].add(entityId)
            if args['effectName'] == "y_flytwo":
                self.NotifyToClient(entityId,"yEffectInfoToClient",{
                    "class":"PyClientSystem",
                    "funcName":"sFlyEffectChangeFunc",
                    "entityId":entityId,
                    "changeTo":"add"
                })
            elif args['effectName'] == "y_elytra":
                self.NotifyToClient(entityId,"yEffectInfoToClient",{
                    "class":"PyClientSystem",
                    "funcName":"yElytraffectChangeFunc",
                    "entityId":entityId,
                    "changeTo":True
                })

                pass
            pass

    
    def RefreshEffectServerEvent(self, args):
        '''状态更新'''
        entityId = args['entityId']
        if args['effectName'] == "y_returns_damage":
            _cache = {
                0:0.333,
                1:0.5,
                2:1.0
            }
            self.returns_damage_dict[args['entityId']] = [1,_cache[args['effectAmplifier']]]
        elif args['effectName'] == "y_repairing":
            _cache = {
                0:1,
                1:3,
                2:10
            }
            self.repairing_dict[args['entityId']] = [1,_cache[args['effectAmplifier']]]
            pass

        elif args['effectName'] == "y_stepup":
            comp = serverApi.GetEngineCompFactory().CreateAttr(args['entityId'])
            _cache = {
                0:2.0,
                1:3.0,
                2:50.0
            }
            comp.SetStepHeight(_cache[args['effectAmplifier']]+0.0625)

    def RemoveEffectServerEvent(self, args):
        '''状态移除'''
        entityId = args['entityId']
        if args['effectName'] == "y_returns_damage":
            self.returns_damage_dict[args['entityId']] = [0,0]
        elif args['effectName'] == "y_repairing":
            self.repairing_dict[args['entityId']] = [0,0]
        elif args['effectName'] == "y_stepup":
            comp = serverApi.GetEngineCompFactory().CreateAttr(args['entityId'])
            comp.ResetStepHeight()
        elif args['effectName'] == "y_weight":
            '''超重'''
            engineAPI.SetGravity(entityId,0)
        elif args['effectName'] in ["y_ooo","y_spin","y_random_tp","y_lightning","y_flytwo","y_solidcore","y_elytra"]:
            self.playerEffectDict[args['effectName']].discard(entityId)
            if args['effectName'] == "y_flytwo":
                self.changeSFlyAnimatToServerFunc({
                    "class":"PyClientSystem",
                    "funcName":"changeSFlyAnimatToClientFunc",
                    "playerId":entityId,
                    "willStart":False,
                    "needCloseBtnShow":True
                })
            elif args['effectName'] == "y_elytra":
                self.NotifyToClient(entityId,"yEffectInfoToClient",{
                    "class":"PyClientSystem",
                    "funcName":"yElytraffectChangeFunc",
                    "entityId":entityId,
                    "changeTo":False
                })

                pass
            pass

    def DamageEvent(self,args):
        '''
        伤害事件
        '''
        if not self.usingSystemInfo['hasUsing']:
            return

        srcId = args['srcId']
        entityId = args['entityId']

        if args["cause"] == "fall" and (entityId in self.playerEffectDict['elytraFly'] or entityId in self.playerEffectDict['y_flytwo']):
            args['damage'] = 0
            args['knock'] = False
            return

        comp = serverApi.GetEngineCompFactory().CreateAttr(args['entityId'])
        blood = comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        if self.returns_damage_dict.get(entityId) != None and self.returns_damage_dict[entityId][0] == 1:
            damage = int(copy.deepcopy(args['damage']*self.returns_damage_dict[entityId][1]))
            hurtcomp = serverApi.GetEngineCompFactory().CreateHurt(srcId)
            hurtcomp.Hurt(damage,serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack,"-1", None, True)#设置实体伤害
        
        if args['damage'] >= blood:
            comp0 = serverApi.GetEngineCompFactory().CreateEffect(entityId)
            effectDictList = comp0.GetAllEffects()
            if effectDictList != None:
                for effect_i in effectDictList:
                    if effect_i['effectName'] == "y_revival":
                        args['damage'] = 0
                        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
                        res = comp0.AddEffectToEntity("instant_health", 1, 0, True)
                        if effect_i['amplifier'] == 0:
                            # comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, max_blood)
                            res = comp0.AddEffectToEntity("instant_health", 1, 0, True)
                        elif effect_i['amplifier'] == 1:
                            comp0.AddEffectToEntity("instant_health", 1, 1, True)
                        elif effect_i['amplifier'] == 2:
                            comp0.AddEffectToEntity("instant_health", 1, 5, True)
                        comp0.RemoveEffectFromEntity("y_revival")
                        self.BroadcastToAllClient("luckyfiverevivaleffect", {"entityId":entityId})
        
        if entityId in self.playerEffectDict['y_solidcore']:
            args['knock'] = False
            pass
        comp = serverApi.GetEngineCompFactory().CreateEngineType(args['projectileId'])
        project_name = comp.GetEngineTypeStr()
        if project_name != None:
            comp0 = serverApi.GetEngineCompFactory().CreateEffect(srcId)
            effectDictList = comp0.GetAllEffects()
            if effectDictList != None:
                for effect_i in effectDictList:
                    if effect_i['effectName'] == "y_trueshot":
                        if effect_i['amplifier'] == 0:
                            args['damage'] *= 2
                        elif effect_i['amplifier'] == 1:
                            args['damage'] *= 4
                        elif effect_i['amplifier'] == 2:
                            args['damage'] *= 6
                        pass
            pass

    # tick事件
    def Update(self):
        self.mFrameCount += 1

        # if self.mFrameCount%30 == 0: # TODO 测试使用
        #     for i in serverApi.GetPlayerList():
        #         engineAPI.AddEffectToEntity(i,"y_elytra",2,0)
            
        if not self.usingSystemInfo['hasUsing']:
            return

        if self.mFrameCount%30 == 0:

            for entityId in self.playerEffectDict["y_random_tp"]:
                engineAPI.randomTp(entityId)
                pass

            for entityId in self.playerEffectDict["y_lightning"]:
                pos = engineAPI.get_foot_pos(entityId)
                if pos:
                    engineAPI.SetCommand("/summon minecraft:lightning_bolt {} {} {}".format(str(pos[0]),str(pos[1]),str(pos[2])))
                pass

            
            
            for entityId in self.playerEffectDict["y_ooo"]:
                engineAPI.resetPlayerItemSlotFunc(entityId)
                pass

            #这里是自动修复功能
            for player_i,val in self.repairing_dict.items():
                if val[0] == 1:
                    #这里要遍历背包查找耐久未满的物品,进行增加耐久
                    comp = serverApi.GetEngineCompFactory().CreateItem(player_i)
                    #这里遍历背包
                    for slot_i in range(0, 36):
                        cache_dict = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, slot_i) #获取背包物品信息
                        if cache_dict != None:
                            MaxDurability = comp.GetItemMaxDurability(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, slot_i, False)
                            Durability = comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, slot_i)
                            if Durability < MaxDurability:
                                #这里增加指定耐久度
                                if val[1] >= MaxDurability-Durability:
                                    comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, slot_i, MaxDurability)
                                else:
                                    comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, slot_i, Durability+val[1])
                                    pass
                    
                    #这里遍历盔甲栏
                    for slot_i in range(0, 4):
                        cache_dict = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, slot_i) #获取背包物品信息
                        if cache_dict != None:
                            MaxDurability = comp.GetItemMaxDurability(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, slot_i, False)
                            Durability = comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, slot_i)
                            if Durability < MaxDurability:
                                #这里增加指定耐久度
                                if val[1] >= MaxDurability-Durability:
                                    comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, slot_i, MaxDurability)
                                else:
                                    comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, slot_i, Durability+val[1])
                                    pass
                    
                    #这里查询副手
                    cache_dict = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, 0) #获取背包物品信息
                    # print '----------1231',cache_dict
                    if cache_dict != None:
                        MaxDurability = comp.GetItemMaxDurability(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, 0, False)
                        Durability = comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, 0)
                        if Durability < MaxDurability:
                            #这里增加指定耐久度
                            if val[1] >= MaxDurability-Durability:
                                comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, 0, MaxDurability)
                            else:
                                comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, 0, Durability+val[1])
                                pass
   
        
        if self.mFrameCount%3 == 0:
            for entityId in self.playerEffectDict['y_spin']:
                engineAPI.set_rot(entityId,(-90,random.randint(-180,180)))
                pass
            pass
        for i in self.playerEffectDict['elytraFly']:
            self.elytraFlyTick(i)
        for i in self.playerEffectDict['specialFly']:
            self.specialFlyTick(i)

    def specialFlyTick(self, playerId):
        '''特殊飞行'''
        rx,ry,rz = engineAPI.GetDirFromRot(engineAPI.GetRot(playerId))
        uv1 = Vector3(rx,ry+0.4,rz).Normalized()
        vx0,vy0,vz0 = engineAPI.GetMotion(playerId)
        vt0 = Vector3(vx0,vy0,vz0)
        vLen0 = vt0.Length()
        if self.useMoveBtnDict[playerId]:
            if vLen0 > 2:
                '''减速'''
                endV = uv1*(vLen0)
            else:
                endV = uv1*(vLen0+0.08*math.cos(((vLen0*math.pi)/(2*5))))  
                pass
        else:
            '''无操作时'''
            if vLen0 > 0.2 and (not self.SFlyStartDict[playerId] or vLen0 > 1):
                gravityV = Vector3(0,-0.25,0)
                if ry < -0.4:
                    gravityV*=(ry+1)
                    vLen1 = vLen0+0.08*(ry+0.6)
                else:
                    vLen1 = vLen0+0.08
                endV = uv1*vLen1+gravityV
            else:
                if self.SFlyStartDict[playerId]:
                    '''刚起飞,添加一点动力'''
                    uv1 = Vector3(rx,0,rz).Normalized()
                    uv1 += Vector3(0,0.5,0)
                    endV = uv1*(0.2)
                else:
                    endV = uv1*(vLen0)+Vector3(0,-0.17,0)
        engineAPI.SetMotion(playerId,tuple(endV))
        # engineAPI.add_timer(0,engineAPI.SetMotion,playerId,tuple(endV))
            
        if self.SFlyStartDict[playerId]:
            self.SFlyStartDict[playerId] -= 1
        # print("406--------",vLen0)
        pass

    def elytraFlyTick(self, playerId):
        '''鞘翅状态飞行'''
        rx,ry,rz = engineAPI.GetDirFromRot(engineAPI.GetRot(playerId))
        if playerId in self.elytraFireworksDict:
            '''使用烟花冲刺'''
            if self.elytraFireworksDict[playerId] == 2:
                endV = Vector3(rx,ry,rz).Normalized()*5
                self.elytraFireworksDict[playerId] -= 1
            else:
                del self.elytraFireworksDict[playerId]
                '''空一帧不处理'''
                return
        else:
            uv1 = Vector3(rx,ry+0.4,rz).Normalized()
            vx0,vy0,vz0 = engineAPI.GetMotion(playerId)
            vt0 = Vector3(vx0,vy0,vz0)
            vLen0 = vt0.Length()

            gravityV = Vector3(0,-0.45,0)
            if ry < 0:
                gravityV*=(ry+1)
                vLen1 = vLen0+0.1*(ry+1)
            else:
                vLen1 = vLen0+0.1
            endV = uv1*vLen1+gravityV
        engineAPI.SetMotion(playerId,tuple(endV))
        # print("1051---------",round(ry,2),round(vLen0,2))


    def changeEEStateFunc(self, args):
        '''变更鞘翅飞行'''
        args['class'] = 'PyClientSystem'
        args['funcName'] = 'changeEEStateToClientFunc'
        self.BroadcastToAllClient("yEffectInfoToClient", args)
        playerId = args['playerId']
        if args['data']:
            self.playerEffectDict['elytraFly'].add(playerId)
            # comp = serverApi.GetEngineCompFactory().CreateFly(playerId)
            # # comp.ChangePlayerFlyState(False)
            def funcOne():
                comp = serverApi.GetEngineCompFactory().CreateFly(playerId)
                if comp.IsPlayerFlying():
                    self.NotifyToClient(playerId,"yEffectInfoToClient",{
                        "class":"PyClientSystem",
                        "funcName":"canselEEFlyFunc",
                        "playerId":playerId
                    })
                    pass
                pass
            engineAPI.add_timer(0,funcOne)
            
            
        else:
            self.playerEffectDict['elytraFly'].discard(playerId)
            if playerId in self.elytraFireworksDict:
                del self.elytraFireworksDict[playerId]
            # comp = serverApi.GetEngineCompFactory().CreateFly(playerId)
            # # comp.ChangePlayerFlyState(False)
            # engineAPI.add_timer(0,comp.ChangePlayerFlyState,True)
        pass
            
    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        # 调用上面的反监听函数来销毁
        pass
