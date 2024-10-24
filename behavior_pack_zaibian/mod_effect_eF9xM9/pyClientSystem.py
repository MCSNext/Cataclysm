# -*- coding: utf-8 -*-

# 获取客户端引擎API模块
import mod.client.extraClientApi as clientApi
import mod_effect_eF9xM9.modCommon.modConfig as modConfig
from mod_effect_eF9xM9.modClient.manager import get_singleton, engineAPI
import collections,math,random
from common.utils.mcmath import Vector3

# 获取客户端system的基类ClientSystem
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()
# 在modMain中注册的Client System类
playerId = clientApi.GetLocalPlayerId()
levelId = clientApi.GetLevelId()

class PyClientSystem(ClientSystem):
    def __init__(self, namespace, name):
        super(PyClientSystem, self).__init__(namespace, name)
        single_mgr = get_singleton()
        single_mgr.set_client_system(self)
        self.ListenEvent()
        self.animatRegisterDict = collections.defaultdict(bool)
        '''用于标记玩家是否注册动画'''
        self.needWingBtn = False
        '''是否需要飞行按钮'''
        self.UINode1 = None
        self.hasSeePlayerSet = set()
        '''能看到的玩家集合'''
        self.waitChangeShowDict = {}
        '''等待更新显示飞行动画的玩家'''
        self.hasPressMoveBtn = False
        '''是否按下移动按键'''
        self.isElytraFlying = False
        '''是否正在使用鞘翅状态滑行'''
        self.hasElytraEffect = False
        '''是否拥有鞘翅状态'''
        self.lastJumpInfo = {
            "time":0,
            "sign":False
        }
        '''上一次跳跃的信息'''
        self.mFrameCount = 0
        '''tick'''
        self.FTESign = False
        '''标识这个包的特殊飞行状态是否起作用'''
        self.loadUiInfo = {
            "stopLoad":False,
            "uiInit":False
        }
        '''标识是否停止加载'''
        self.wingAnimatWaitChangeDict = {}
        '''用于翅膀动画变更'''
        self.usingSystem = None
        '''激活功能包的实例'''

    def getSystemInUseFunc(self):
        '''获得被激活的状态包的实例'''
        return self.usingSystem

    def ListenEvent(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),"OnLocalPlayerStopLoading", self, self.OnLocalPlayerStopLoading)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),'AddPlayerCreatedClientEvent', self, self.AddPlayerCreatedClientEvent) 
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),'RemovePlayerAOIClientEvent', self, self.RemovePlayerAOIClientEvent) 
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),'UiInitFinished', self, self.UiInitFinished) 
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),'OnClientPlayerStartMove', self, self.OnClientPlayerStartMove) 
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),'OnClientPlayerStopMove', self, self.OnClientPlayerStopMove) 
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),'OnGroundClientEvent', self, self.OnGroundClientEvent) 
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),'ClientJumpButtonPressDownEvent', self, self.ClientJumpButtonPressDownEvent) 

        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName,"luckyfiverevivaleffect", self, self.luckyfiverevivaleffect)
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName,'yEffectInfoToClient', self, self.yEffectInfoToClient) 

    def ClientJumpButtonPressDownEvent(self, args):
        '''跳跃按钮按下事件，返回值设置参数只对当次按下事件起作用'''
        # print("1624-------------")
        if not (self.FTESign and self.hasElytraEffect):
            return
        if self.lastJumpInfo['sign']:
            return
        self.lastJumpInfo['sign'] = True
        def funcTwo():
            self.lastJumpInfo['sign'] = False
        engineAPI.add_timer(0.4,funcTwo)
        
        comp = clientApi.GetEngineCompFactory().CreateAttr(playerId)
        isOnGound = comp.isEntityOnGround()
        if isOnGound == False:
            timeNow = self.mFrameCount
            def funcOne():
                if self.lastJumpInfo['time'] == timeNow:
                    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
                    isInWater = comp.GetMolangValue('query.is_in_water')
                    comp = clientApi.GetEngineCompFactory().CreateAttr(playerId)
                    isOnGound = comp.isEntityOnGround()
                    if not isInWater and not isOnGound:
                        self.changeEEValue(not self.isElytraFlying)
                    pass
                pass
            engineAPI.add_timer(0.4,funcOne)
        self.lastJumpInfo['time'] = self.mFrameCount
        pass

    def changeEEStateToClientFunc(self, args):
        '''修改鞘翅飞行动作变体'''
        engineAPI.setVariable(args['playerId'],"query.mod.yelytraval1",1 if args['data'] else 0)
        '''
        2023-10-25 17:47:59 TODO
        这里还需要判断该玩家是否可见
        '''
        pass

    def canselEEFlyFunc(self, args):
        self.changeEEValue(False)
        pass

    def changeEEValue(self, val, needChangeCamera = True):
        '''变更鞘翅飞行状态'''
        if not self.FTESign:
            return
        self.isElytraFlying = val

        self.NotifyToServer("yEffectInfoToServer", {
            "class": "PyServerSystem",
            "funcName": "changeEEStateFunc",
            "playerId": playerId,
            "data":val
        })

        if not needChangeCamera:
            return
        if self.isElytraFlying:
            comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
            comp.SetCameraOffset((0, -0.5, 0))
        else:
            comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
            comp.SetCameraOffset((0, 0, 0))
        pass

    def yElytraffectChangeFunc(self, args):
        '''鞘翅状态变更事件'''
        # print("55----------", args)
        # {'entityId': '-4294967295', 'changeTo': False, 'class': 'PyClientSystem', 'funcName': 'yElytraffectChangeFunc'}
        self.hasElytraEffect = args['changeTo']
        if not self.hasElytraEffect and self.isElytraFlying:
            self.changeEEValue(False)
        
        pass

    def Update(self):
        self.mFrameCount += 1
        if self.isElytraFlying and self.FTESign:
            if  self.UINode1 and self.UINode1.isWingFlying:
                self.changeEEValue(False,False)
                return
            comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
            isInWater = comp.GetMolangValue('query.is_in_water')
            if isInWater:
                self.changeEEValue(False)
                return
        
        for key, val in self.wingAnimatWaitChangeDict.items():
            val['tickTime'] -= 1
            if val['tickTime'] <= 0:
                engineAPI.setVariable(key,"query.mod.yflytwoval1",val['willTO'])
                del self.wingAnimatWaitChangeDict[key]
                pass
            pass
        pass


    def OnGroundClientEvent(self, args):
        '''实体着地事件。玩家，沙子，铁砧，掉落的物品，点燃的TNT掉落地面时触发，其余实体着地不触发。'''
        if args['id'] == playerId:
            def funcOne():
                if self.UINode1 and self.UINode1.isWingFlying:
                    self.UINode1.triggerBtn0Func()
                if self.isElytraFlying:
                    self.changeEEValue(False)
            
            engineAPI.add_timer(0.1,funcOne)
            
        pass


    def OnClientPlayerStopMove(self):
        '''移动按钮按下释放时触发事件，同时按下多个方向键，需要释放所有的方向键才会触发事件'''
        self.hasPressMoveBtn = False
        self.NotifyToServer("yEffectInfoToServer", {
            "class": "PyServerSystem",
            "funcName": "playerChangeUseMoveBtnFunc",
            "playerId": playerId,
            "data":False
        })
        pass

    def OnClientPlayerStartMove(self):
        '''移动按钮按下触发事件，在按住一个方向键的同时，去按另外一个方向键，不会触发第二次'''
        self.hasPressMoveBtn = True
        self.NotifyToServer("yEffectInfoToServer", {
            "class": "PyServerSystem",
            "funcName": "playerChangeUseMoveBtnFunc",
            "playerId": playerId,
            "data":True
        })
        pass


    def RemovePlayerAOIClientEvent(self, args):
        '''玩家离开当前玩家视野时触发的事件'''
        self.hasSeePlayerSet.discard(args['playerId'])


    def AddPlayerCreatedClientEvent(self, args):
        '''玩家进入当前玩家所在的区块AOI后，玩家皮肤数据异步加载完成后触发的事件    (本地玩家也会触发)'''
        self.hasSeePlayerSet.add(args['playerId'])
        if args['playerId'] not in self.animatRegisterDict:
            self.addPlayerAnimalModelFunc(args['playerId'])
            pass
        if args['playerId'] in self.waitChangeShowDict:
            engineAPI.setVariable(args['playerId'],"query.mod.yflytwoval0", self.waitChangeShowDict[args['playerId']])
            del self.waitChangeShowDict[args['playerId']]

    def changeSFlyAnimatToClientFunc(self, args):
        '''变更每位玩家的飞行动作'''
        entityId = args['playerId']
        if entityId in self.hasSeePlayerSet:
            '''在视线内,直接修改'''
            engineAPI.setVariable(entityId,"query.mod.yflytwoval0",1 if args['willStart'] else 0)
            self.changeWingsFlyAnimationShow(entityId,1 if args['willStart'] else 0)
            pass
        else:
            '''不在视线内,等进入视线了再修改'''
            self.waitChangeShowDict[entityId] = 1 if args['willStart'] else 0
            pass

        if entityId == playerId and args.get("needCloseBtnShow"):
            self.sFlyEffectChangeFunc({"changeTo":"remove"})

    def changeWingsFlyAnimationShow(self, entityId, start):
        '''变更翅膀动画'''
        if start:
            engineAPI.setVariable(entityId,"query.mod.yflytwoval1",1)
            self.wingAnimatWaitChangeDict[entityId] = {
                "tickTime":17,
                "willTO":2
            }

            pass
        else:
            engineAPI.setVariable(entityId,"query.mod.yflytwoval1",3)
            self.wingAnimatWaitChangeDict[entityId] = {
                "tickTime":17,
                "willTO":0
            }

            pass
        pass

    def UiInitFinished(self,args):
        '''
        UI初始化框架完成,此时可以创建UI
        '''
        self.loadUiInfo['uiInit'] = True
        if self.loadUiInfo['stopLoad']:
            self.registerUIFunc()
            pass


    def OnLocalPlayerStopLoading(self, event):
        '''玩家进入存档，出生点地形加载完成时触发'''
        query_comp = compFactory.CreateQueryVariable(levelId)
        query_comp.Register('query.mod.yflytwoval0', 0.0)   #标记是否正在飞行
        query_comp.Register('query.mod.yflytwoval1', 0.0)   #用于控制具体的飞行动画

        def funcOne():
            
            pass
        
        engineAPI.add_timer(random.uniform(0,2),funcOne)

        query_comp.Register('query.mod.yelytraval1', 0.0) 
        '''用于播放鞘翅飞行动作'''

        hasEffectList = engineAPI.GetAllEffects(playerId)
        if hasEffectList:
            for i in hasEffectList:
                if i["effectName"] == "y_elytra" and i["duration"] > 0:
                    self.hasElytraEffect = True
                    break

        self.addPlayerAnimalModelFunc(playerId)

        self.NotifyToServer("yEffectInfoToServer", {
            "class": "PyServerSystem",
            "funcName": "playerStopLoadFunc",
            "playerId": playerId
        })

    def getSFSignInfoFunc(self, args):
        '''获得是否需要处理特殊飞行状态的标识信息'''
        self.FTESign = args['data']['hasUsing']
        self.usingSystem = clientApi.GetSystem(args['data']['usingModMark']["ModName"],args['data']['usingModMark']["ClientSystemName"])
        self.loadUiInfo['stopLoad'] = True
        if self.loadUiInfo['uiInit']:
            self.registerUIFunc()
        pass
        

    def registerUIFunc(self):
        '''开始注册UI'''
        if self.FTESign:
            '''若需要特殊飞行按钮,再注册'''
            uiData = modConfig.UI_DEFS.get("ywing_ui0")
            uiName = uiData['uiName']
            clientApi.RegisterUI(modConfig.ModName, uiName, uiData["uiClassPath"], uiData["uiScreenDef"])
            self.UINode1 = clientApi.CreateUI(modConfig.ModName, uiName, {'isHud': 1})

        pass

    def addPlayerAnimalModelFunc(self, entityId):
        '''增加玩家动画模型'''
        comp = compFactory.CreateActorRender(entityId)
        comp.AddPlayerAnimation('yfly0',"animation.ywing.yfly0") 
        comp.AddPlayerAnimation('yfly2',"animation.ywing.yfly2") 
        comp.AddPlayerAnimation('yfly3',"animation.ywing.yfly3") 
        
        comp.AddPlayerAnimationController('ywing_fly0','controller.animation.ywing.fly0') 
        comp.AddPlayerScriptAnimate("ywing_fly0", "1")

        comp.AddPlayerAnimation('yfly1',"animation.ywing.yfly1") 
        comp.AddPlayerAnimationController('ywing.fly1','controller.animation.ywing.fly1') 
        comp.AddPlayerScriptAnimate("ywing.fly1", "query.mod.yflytwoval0")

        comp.AddPlayerAnimation('yelytra1',"animation.ywing.yelytra1") 
        comp.AddPlayerAnimationController('yect1','controller.animation.ywing.elytra1') 
        comp.AddPlayerScriptAnimate("yect1", "query.mod.yelytraval1")


        # comp.AddPlayerAnimation('yelytra1',"animation.ywing.yelytra0") 

        
        comp.RebuildPlayerRender() # 保存上面的所有操作并立刻显示上面修改的所有内容
        self.animatRegisterDict[entityId] = True
        pass


    def sFlyEffectChangeFunc(self, args):
        '''变更飞行状态'''
        if args['changeTo'] == 'add':
            self.needWingBtn = True
        else:
            self.needWingBtn = False
        if self.UINode1:
            self.UINode1.changeBtnShowFunc()
        pass

    def yEffectInfoToClient(self, args):
        if args['class'] == "PyClientSystem":
            cacheFunc = getattr(self,args['funcName'],None)
            if cacheFunc:
                cacheFunc(args)
        pass

    def luckyfiverevivaleffect(self, args):
        entityId = args['entityId']
        comp = clientApi.GetEngineCompFactory().CreatePos(entityId)
        # 获取位置：
        entityPos = comp.GetPos()
        particleEntityId = self.CreateEngineParticle(
            "effects/revival_green_effect.json", entityPos)
        particleControlComp = clientApi.GetEngineCompFactory(
        ).CreateParticleControl(particleEntityId)
        particleControlComp.Play()

        comp0 = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        comp0.AddTimer(2, self.DestroyEntity, particleEntityId)
        pass
