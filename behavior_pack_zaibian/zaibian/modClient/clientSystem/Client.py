# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import zaibian.modCommon.modConfig as modConfig
import zaibian.modCommon.storage as storage
import time
from common.utils.mcmath import Vector3

# 获取客户端system的基类ClientSystem
playerId=clientApi.GetLocalPlayerId()
levelId=clientApi.GetLevelId()
# 在modMain中注册的Client System类

compFactory = clientApi.GetEngineCompFactory()
NativeScreenManager = clientApi.GetNativeScreenManagerCls()

class ClientSystem(clientApi.GetClientSystemCls()):
    def __init__(self, namespace, name):
        super(ClientSystem, self).__init__(namespace, name)
        self.ListenEvent()
        self.tick={}
        self.lock={}
        self.alltick=0
        self.mEntityId=None
        self.mTimer=None
        comp = clientApi.GetEngineCompFactory().CreatePlayer(playerId)
        comp.OpenPlayerHitMobDetection()
        storage.set_clientApi(self)

        self.sttexiao={}

        self.postexiao={}


        self.UI_node={}
        '''ui类'''

        self.BountifulBaublesMod=None #装饰品类




        print NativeScreenManager.instance().RegisterScreenProxy(
            "hud.hud_screen", "zaibian.modClient.ui.clientScreen.PyClientScreen"
        ),7777


        comp = clientApi.GetEngineCompFactory().CreateQueryVariable(levelId)
        result = comp.Register('query.mod.revenantq', 1)
        result = comp.Register('query.mod.revenanth', 1)
        result = comp.Register('query.mod.revenantz', 1)
        result = comp.Register('query.mod.revenanty', 1)
        result = comp.Register('query.mod.tidal_claws_x', 0)
        result = comp.Register('query.mod.tidal_claws_y', 0)
        result = comp.Register('query.mod.tidal_claws', 0)
        result = comp.Register('query.mod.ling', 144)


        result = comp.Register('query.mod.sneaking', 0)

        self.UIInitFinished=False
        self.init=[]

        query_comp = compFactory.CreateQueryVariable(levelId)
        query_comp.Register('query.mod.syzaibian', 0.0) 
        query_comp.Register('query.mod.bianti', 0.0) 

        query_comp.Register('query.mod.fengbao', 0.0) 
        query_comp.Register('query.mod.sticky_gloves', 0.0) 


        query_comp.Register('query.mod.wea', 90.0) 
        query_comp.Register('query.mod.scale', 1.0) 

        query_comp.Register('query.mod.gao', 1000.0) 

        query_comp.Register('query.mod.bfb', 10.0) 

        query_comp.Register('query.mod.leftitemys', 0.0)   #左手隐身
        query_comp.Register('query.mod.zspshow', 1.0)   #装饰品隐身




        # query_comp.Register('query.mod.the_incinerator_attack_time', 0.0) 






        self.jv_sgcaow=None #记录上个槽位信息



        self.texiao_block={}  #展示台id


        self.dq_miss=None #当前实时音乐


        self.jump_val=False  #当前是否点击跳跃
        self.set_data={}
  
        self.click_cooldown=0

        self.boss_ui=None
        self.tick_ui=0

    def OnGameTick(self):
        return
        if self.boss_ui:
            self.boss_ui.OnGameTick()
            # def coroutineTest():
            #     for i in xrange(30):
            #         self.boss_ui.OnGameTick()
            #         yield
            # generator = clientApi.StartCoroutine(coroutineTest, None)
                

    def ListenEvent(self):
      
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "HealthChangeClientEvent", self, self.HealthChangeClientEvent) #点击屏幕
   
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientItemTryUseEvent", self, self.ClientItemTryUseEvent) #点击屏幕
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", self, self.OnScriptTickClient) #tick
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "StartDestroyBlockClientEvent", self, self.StartDestroyBlockClientEvent) #tick
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "AddEntityClientEvent", self, self.AddEntityClientEvent) #tick
        self.ListenForEvent(clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(), "UiInitFinished", self, self.OnUIInitFinished)
        
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "TapOrHoldReleaseClientEvent", self, self.TapOrHoldReleaseClientEvent) #玩家点击屏幕后松手时触发
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnCarriedNewItemChangedClientEvent", self, self.OnCarriedNewItemChangedClientEvent) #：玩家切换主手物品时触发该事件

        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "TapBeforeClientEvent", self, self.TapBeforeClientEvent) #：玩家切换主手物品时触发该事件
        self.ListenForEvent(clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(), "PushScreenEvent", self, self.onPushScreen)

        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientJumpButtonPressDownEvent", self, self.ClientJumpButtonPressDownEvent) #：玩家切换主手物品时触发该事件
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientJumpButtonReleaseEvent", self, self.ClientJumpButtonReleaseEvent) #：玩家切换主手物品时触发该事件
    
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "PlaySoundClientEvent", self, self.PlaySoundClientEvent) #：玩家切换主手物品时触发该事件

        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "RightClickReleaseClientEvent", self, self.TapOrHoldReleaseClientEvent) #：玩家切换主手物品时触发该事件
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "LeftClickBeforeClientEvent", self, self.TapOrHoldReleaseClientEvent) #：玩家切换主手物品时触发该事件
        # # # 服务端通信客户端
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "void_scatter_arrowlz", self, self.void_scatter_arrowlz)
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "bind_lz", self, self.bind_lz)
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "block_entity", self, self.OnReceiveBlockPalette)
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "stage_lizi", self, self.stage_lizi)

        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "Ontraction", self, self.traction)

        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "eyetexiao", self, self.eyetexiao)

        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "zhaohuan", self, self.zhaohuan)
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "ignited_revenant_dun", self, self.ignited_revenant_dun)
        self.ListenForEvent(modConfig.ModName,modConfig.ServerSystemName, "ClientLoadAddonsFinishServerEvent", self, self.ClientLoadAddonsFinishServerEvent)
        self.ListenForEvent(modConfig.ModName,modConfig.ServerSystemName, "tb_data", self, self.tb_data)

        self.ListenForEvent(modConfig.ModName,modConfig.ServerSystemName,  "players_wear_accessories", self, self.players_wear_accessories)  #数据传输
        self.ListenForEvent(modConfig.ModName,modConfig.ServerSystemName,  "ServerChatEvent", self, self.ServerChatEvent)  #数据传输

    def ServerChatEvent(self,args):
        print args

    def HealthChangeClientEvent(self,args):
        entityId=args["entityId"]
        to=args["to"]
        comp = clientApi.GetEngineCompFactory().CreateEngineType(entityId)
        if comp.GetEngineTypeStr()=="zaibian:ignis":
            comp = clientApi.GetEngineCompFactory().CreateAttr(entityId)
            MaxHEALTH=comp.GetAttrMaxValue(clientApi.GetMinecraftEnum().AttrType.HEALTH)
            if to/float(MaxHEALTH)<=0.1:
                s=2
            elif to/float(MaxHEALTH)<=0.2:
                s=1
            elif  to/float(MaxHEALTH)<=0.3:
                s=0
            else:
                s=10
            query_comp = compFactory.CreateQueryVariable(entityId)
            query_comp.Set("query.mod.bfb",s)


    # def attack_click(self, event):
    #     # return
    #     current_time = time.time()
    #     carried_item = compFactory.CreateItem(clientApi.GetLocalPlayerId()).GetCarriedItem()
    #     if current_time - self.click_cooldown > 0.2 and carried_item and carried_item['newItemName'] == 'zaibian:the_incinerator':
    #         self.click_cooldown = time.time()
    #         self.send_attacked_packet(0.0, {# 动画开始的时间点
    #             'playerId': clientApi.GetLocalPlayerId(),
    #             'type': 'start'
    #         })
    #         self.send_attacked_packet(0.2, { # 动画结束时间点
    #             'playerId': clientApi.GetLocalPlayerId(),
    #             'type': 'end'
    #         })
    #         event['cancel'] = True

    #     else:
    #         # 正在播放动画时，若重复点击，则取消点击
    #         if carried_item and carried_item['newItemName'] == 'zaibian:the_incinerator':
    #             event['cancel'] = True

    # def send_attacked_packet(self, _time, data):
    #     game_comp = compFactory.CreateGame(clientApi.GetLevelId())
    #     game_comp.AddTimer(
    #         _time,
    #         compFactory.CreateQueryVariable(clientApi.GetLocalPlayerId()).Set, # 设置本地玩家客户端播放动画所需的query节点的值
    #         'query.mod.the_incinerator_attack_time',
    #         1.0 if data['type'] == 'start' or data['type'] == 'will_hit' else 0.0
    #     )
      
    def tb_data(self,args):
        self.set_data=args
        if self.set_data.get("7")!=None:
            query_comp = compFactory.CreateQueryVariable(playerId)
            query_comp.Set("query.mod.leftitemys",1 if self.set_data.get("7") else 0)
        if self.set_data.get("8")!=None:
            query_comp = compFactory.CreateQueryVariable(playerId)
            query_comp.Set("query.mod.zspshow",0 if self.set_data.get("8") else 1)
            print 0 if self.set_data.get("8") else 1

    def ClientJumpButtonReleaseEvent(self,args):
        self.jump_val=False
    def ClientJumpButtonPressDownEvent(self,args):
        self.jump_val=True

    def onPushScreen(self, args):
        print args,45646

    def Update(self):
        self.OnGameTick()
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        item=comp.GetPlayerAllItems(clientApi.GetMinecraftEnum().ItemPosType.CARRIED)
        query_comp = compFactory.CreateQueryVariable(playerId)
        if self.dq_miss==None  and query_comp.Get('query.mod.syzaibian') ==1 and item[0] and item[0]['newItemName']=="zaibian:meat_shredder":
            comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
            musicId = comp.PlayCustomMusic("shredder_loop", (1,1,1), 1, 1, True,playerId)
            self.dq_miss=musicId
        elif query_comp.Get('query.mod.syzaibian') ==0 and self.dq_miss!=None  :
            comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
            comp.StopCustomMusicById(self.dq_miss)
            self.dq_miss=None

        if query_comp.Get('query.mod.bianti'):
            comp = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())
            left, up = comp.GetInputVector()
            rot = clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).GetRot()
            if not rot:
                return
            comp = clientApi.GetEngineCompFactory().CreatePlayer(playerId)
            is_sneaking = comp.isSneaking()
            isSprinting = comp.isSprinting()
            yi=0
            
            if is_sneaking:
                yi=-0.18
            if self.jump_val:
                yi=0.18

            if isSprinting:
                d=0.25
            else:
                d=0.2



            rot = (0,rot[1])
            upMotionVector = clientApi.GetDirFromRot(rot)
            vq2 = Vector3(upMotionVector[0],0,upMotionVector[2])*up
            if left>=0:
                rot = (0,rot[1]-90)
            else:
                rot = (0,rot[1]+90)
            leftMotionVector = clientApi.GetDirFromRot(rot)
            vq1 = Vector3(leftMotionVector[0],0,leftMotionVector[2])*abs(left)
            x,y,z=(vq2+vq1).Normalized()*d+Vector3(0,yi,0)
            inputMotion = (x,y,z)

            

            self.NotifyToServer("tb_animation", {"key":"yidong","playerId":clientApi.GetLocalPlayerId(),"motion":inputMotion})


                

    #给玩家施加作用力
    def traction(self, args):
        motionComp = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())
        motionComp.SetMotion(args) 

    def PlaySoundClientEvent(self,args):
        a={
            # "random.explode":"zaibian:netherite_monstrosity"
        #    ,"ignis_shield01":"zaibian:ignis"
           "deepling_swing":"zaibian:deepling_angler",
           "sword_stomp":"zaibian:coralssus"
        #    ,"leviathan_bite":"zaibian:the_leviathan"
        #    ,"leviathan_bite_x":"zaibian:the_baby_leviathan" 
           
           
           }
        if args['name']in a.keys():
            comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
            dimId = comp.GetCurrentDimension()
            self.NotifyToServer("boss_artk",{"dimId":dimId,"playerId":playerId,'name':a[args['name']],'pos':args["pos"],"miss_name":args['name']})


    def OnUIInitFinished(self,args):
        self.jiazai()
        while self.init:
            func=self.init.pop()
            func[0](func[1])
        self.UIInitFinished=True

        comp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)
        comp.AddPlayerAnimation("yinsheng","animation.yinsheng.first_scale")
        comp.AddPlayerAnimation("yinsheng1","animation.yinsheng.first_scale1")

        comp.AddPlayerScriptAnimate("yinsheng", "(variable.is_first_person && (query.main_hand_item_use_duration > 0.0f  ||  query.mod.syzaibian))")    
        comp.AddPlayerScriptAnimate("yinsheng1", "(variable.is_first_person && query.mod.leftitemys )")     

        uiData = modConfig.UI_DEFS.get("part1_part2")
        uiName = uiData['uiName']
        clientApi.RegisterUI(modConfig.ModName, uiName, uiData["uiClassPath"], uiData["uiScreenDef"])
        self.UI_node["part1_part2"]=clientApi.CreateUI(modConfig.ModName, uiName, {"isHud": 1})

        self.BountifulBaublesMod=clientApi.GetSystem("BountifulBaublesMod","PyClientSystem").cls
        self.is_not_sandstorm_in_a_bottle()

        comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
        list_=comp.GetEntitiesAroundByType(playerId, 64, clientApi.GetMinecraftEnum().EntityType.ItemEntity)
        for i in list_:
            self.AddEntityClientEvent({"id":i,"engineTypeStr":"minecraft:item"})
        
        list_=comp.GetEntitiesAroundByType(playerId, 64, clientApi.GetMinecraftEnum().EntityType.Mob)
        for i in list_:
            comp = clientApi.GetEngineCompFactory().CreateEngineType(i)
            s=comp.GetEngineTypeStr()
            if s and s=="zaibian:ignis":
                args={}
                args["entityId"]=i
                comp = clientApi.GetEngineCompFactory().CreateAttr(i)
                HEALTH=comp.GetAttrValue(clientApi.GetMinecraftEnum().AttrType.HEALTH)
                args["to"]=HEALTH
                self.HealthChangeClientEvent(args)





    def players_wear_accessories(self,args):
        playerId = args["playerId"]
        itemName = args["itemName"]
        type = args["type"]           #"bring"为穿上
        if itemName=="zaibian:sandstorm_in_a_bottle":
            if type=="bring":
                self.UI_node["part1_part2"].open()
                query_comp = compFactory.CreateQueryVariable(playerId)
                query_comp.Set("query.mod.fengbao",1)
            else:
                query_comp = compFactory.CreateQueryVariable(playerId)
                query_comp.Set("query.mod.fengbao",0)
                self.UI_node["part1_part2"].close()
        
        elif itemName=="zaibian:sticky_gloves":
            if type=="bring":
                query_comp = compFactory.CreateQueryVariable(playerId)
                query_comp.Set("query.mod.sticky_gloves",1)
            else:
                query_comp = compFactory.CreateQueryVariable(playerId)
                query_comp.Set("query.mod.sticky_gloves",0)
        
        

    def is_not_sandstorm_in_a_bottle(self):
        '''沙龍捲瓶是否在装饰品'''
        if self.BountifulBaublesMod.GetItemBountiful("zaibian:sandstorm_in_a_bottle"):
            self.UI_node["part1_part2"].open()
            query_comp = compFactory.CreateQueryVariable(playerId)
            query_comp.Set("query.mod.fengbao",1)
        else:
            self.UI_node["part1_part2"].close()
            query_comp = compFactory.CreateQueryVariable(playerId)
            query_comp.Set("query.mod.fengbao",0)

        if self.BountifulBaublesMod.GetItemBountiful("zaibian:sticky_gloves"):
            query_comp = compFactory.CreateQueryVariable(playerId)
            query_comp.Set("query.mod.sticky_gloves",1)
        else:
            query_comp = compFactory.CreateQueryVariable(playerId)
            query_comp.Set("query.mod.sticky_gloves",0)

    def ClientLoadAddonsFinishServerEvent(self,args):

        def f(args):
            comp = clientApi.GetEngineCompFactory().CreateActorRender(args)
            ###
            comp.AddPlayerGeometry("sandstorm", "geometry.sandstorm")
            comp.AddPlayerTexture("sandstorm", "textures/entity/ancient_remnant/sandstorm")

            comp.AddPlayerTexture("sandstorm_in_a_bottle", "textures/entity/sandstorm_in_a_bottle")
            comp.AddPlayerTexture("sticky_gloves", "textures/entity/sticky_gloves")
            comp.AddPlayerGeometry("sandstorm_in_a_bottle", "geometry.sandstorm_in_a_bottle")
            comp.AddPlayerGeometry("sticky_gloves", "geometry.sticky_gloves")

            ##添加动画
            comp.AddPlayerAnimation("sandstorm_idle", "animation.sandstorm.idle")
            comp.AddPlayerAnimation("sandstorm_yins", "animation.sandstorm.yins")
            comp.AddPlayerAnimation("swimming1", "animation.player.swim1")
            comp.AddPlayerAnimation("trident", "animation.player.trident1")

            comp.AddPlayerAnimation("use_gauntlet_of_guard", "animation.player.gauntlet_of_guard")
            # comp.AddPlayerAnimation("first_ack", "animation.the_incinerator.ack")
            ###
            ###添加动画控制器
            # comp.AddPlayerAnimationController("wq_ack", "controller.animation.wq_ack")
            ###
            
            ###添加scripts
            comp.AddPlayerScriptAnimate("sandstorm_idle", "query.mod.bianti")  
            comp.AddPlayerAnimation("yins", "animation.humanoid.yins")
            comp.AddPlayerScriptAnimate("yins", "query.mod.bianti && !variable.is_first_person")  
            comp.AddPlayerScriptAnimate("sandstorm_yins", "query.mod.bianti && variable.is_first_person") 
            # comp.AddPlayerScriptAnimate("wq_ack", "variable.is_first_person")  
            comp.AddPlayerScriptAnimate("trident", "((query.get_equipped_item_name == 'coral_spear'&& !variable.is_first_person) || (query.get_equipped_item_name == 'coral_bardiche' && !variable.is_first_person))&& query.main_hand_item_use_duration > 0.0f")
            ###动画控制器中的状态添加动画
            comp.AddPlayerAnimationIntoState("root", "third_person", "sneaking", "query.is_sneaking && !query.is_sleeping")
            comp.AddPlayerAnimationIntoState("root", "third_person", "swimming", "variable.swim_amount > 0.0 || (query.mod.sneaking==2 && !query.is_sleeping && query.modified_move_speed>0.1 )")
            comp.AddPlayerAnimationIntoState("root", "third_person", "swimming1", "query.mod.sneaking==2 && !query.is_sleeping")

            # ##风暴
            # comp.AddPlayerRenderController("controller.render.sandstorm", "query.mod.bianti==1") 
            # comp.AddPlayerRenderController("controller.render.sandstorm_in_a_bottle", " query.mod.zspshow && query.mod.fengbao==1 && query.mod.bianti==0")
            # comp.AddPlayerRenderController("controller.render.sticky_gloves", "query.mod.zspshow && query.mod.sticky_gloves==1 && query.mod.bianti==0")

            comp.RebuildPlayerRender()


            return
        
        if not self.UIInitFinished:
            self.init.append([f,args])
        else:
            f(args)

        pass
    def jiazai(self):
        comp = clientApi.GetEngineCompFactory().CreatePos(playerId)
        entityFootPos = comp.GetFootPos()
        comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
        entities = comp.GetEntityInArea(playerId, (entityFootPos[0]-80,entityFootPos[1]-80,entityFootPos[2]-80), (entityFootPos[0]+80,entityFootPos[1]+80,entityFootPos[2]+80))
        for entityId in entities:
            comp = clientApi.GetEngineCompFactory().CreateEngineType(entityId)
            TypeStr=comp.GetEngineTypeStr()
            if TypeStr=="zaibian:ignited_revenant":
                self.ignited_revenant_dun({'id':entityId})


    def TapBeforeClientEvent(self,args):
        # self.attack_click(args)

        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        item=comp.GetPlayerAllItems(clientApi.GetMinecraftEnum().ItemPosType.OFFHAND)
        if item[0] and item[0]['newItemName']=="zaibian:shield":
            comp = clientApi.GetEngineCompFactory().CreatePlayer(playerId)
            is_sneaking = comp.isSneaking()
            if is_sneaking :
                if not self.tick.get("shield",0):
                    self.tick['shield']=150
                    self.NotifyToServer('tb_animation',{'key':'shield',"playerId":playerId})
                else:
                    comp = clientApi.GetEngineCompFactory().CreateGame(playerId)
                    comp.SetTipMessage(clientApi.GenerateColor("RED") + "冷却中：{}秒".format(round(float(self.tick["shield"])/30.0,2)))

                        
    def AddEntityClientEvent(self,args):
        engineTypeStr=args['engineTypeStr']
        id=args['id']
        if engineTypeStr =='zaibian:the_harbinger_psw' or  engineTypeStr =='zaibian:the_harbinger_pswd' :
            particleEntityId = self.CreateEngineParticle("effects/the_harbinger_psw.json", (0,0,0))
            comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
            comp.Bind(id, (0,0,0), (0, 0, 0),True)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()
        
        elif engineTypeStr =='zaibian:ignited_revenant':
            self.ignited_revenant_dun({'id':id})
        elif engineTypeStr =='zaibian:netherite_monstrosity':
            comp = clientApi.GetEngineCompFactory().CreateQueryVariable(id)
            comp.Set("query.mod.ling",144)
        elif engineTypeStr=="minecraft:item" and self.set_data.get("3"):
            comp = clientApi.GetEngineCompFactory().CreateActorRender(id)
            comp.SetNotRenderAtAll(True)

        elif engineTypeStr=="zaibian:item" :
            print 222222
            dict_={"zaibian:infernal_forge":[108,-5],"zaibian:void_forge":[100,-3],
                   "zaibian:wither_assault_shoulder_weapon":[-90,-25,0.3],
                   "zaibian:void_assault_shoulder_weapon":[-90,-25,0.3],
                   "zaibian:gauntlet_of_guard":[-90,-19,0.3],
                   "zaibian:gauntlet_of_bulwark":[-90,-19,0.3],
                   "zaibian:meat_shredder":[-90,-8],
                   "zaibian:laser_gatling":[90,-15,0.5],
                   "zaibian:tidal_claws":[90,-17],
                   "zaibian:shield":[-80,-12],
                   "zaibian:coral_bardiche":[-92,-8],
                   "zaibian:the_incinerator":[90,6],

                   "zaibian:coral_spear":[-93,-12]
                   }
            def f():
                comp = clientApi.GetEngineCompFactory().CreateModAttr(id)
                items=comp.GetAttr("Item")
                id1=comp.GetAttr("id")
                if items["newItemName"]=="zaibian:bow":
                    comp = clientApi.GetEngineCompFactory().CreateActorRender(id1)
                    comp.SetNotRenderAtAll(False)
                comp = clientApi.GetEngineCompFactory().CreateQueryVariable(id)
                data=dict_.get(items["newItemName"],[90,-11,0.55])
                s=1
                if len(data)>2:
                    x,y,s=data
                else:
                    x,y=data
                comp.Set("query.mod.scale",s)
                comp.Set("query.mod.wea",x)
                comp.Set("query.mod.gao",y)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0,f)


            




    def ignited_revenant_dun(self,args):
        id=args["id"] 
        LUCK=args.get("luck")

        comp = clientApi.GetEngineCompFactory().CreateAttr(id)
        if  LUCK==None:
            LUCK=int(comp.GetAttrValue(clientApi.GetMinecraftEnum().AttrType.LUCK))
        a=["0","0","0","0"]
        for index,i in enumerate(list(str(LUCK))[::-1]):
            index+=1
            a[-index]=i
        for index,i in enumerate(a):
            s={0:'query.mod.revenantq',1:'query.mod.revenantz',2:'query.mod.revenanth',3:'query.mod.revenanty'}
            comp = clientApi.GetEngineCompFactory().CreateQueryVariable(id)
            result = comp.Set(s[index],int(i))
    def StartDestroyBlockClientEvent(self,args):
        blockName=args['blockName']
        if  blockName=='zaibian:emp':
            args['cancel']=True
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        carriedData = comp.GetCarriedItem()
        if carriedData and  carriedData["newItemName"].split(":")[-1] in  ["meat_shredder","gauntlet_of_guard"]:
            args['cancel']=True
        elif carriedData and  carriedData["newItemName"].split(":")[-1] in ["the_incinerator","gauntlet_of_bulwark","gauntlet_of_guard","void_core","void_assault_shoulder_weapon","wither_assault_shoulder_weapon"] \
        and  self.tick.get(carriedData["newItemName"].split(":")[-1]):
            args['cancel']=True
            

    def zhaohuan(self,args):
        '''召唤炎魔特效'''
        key=args['key']
        pos=args.get('pos')
        if key=='sandstorm':
            id=args.get('playerId')
            query_comp = compFactory.CreateQueryVariable(id)
            query_comp.Set("query.mod.bianti",args["data"])
            actorRenderComp = clientApi.GetEngineCompFactory().CreateActorRender(playerId)
            actorRenderComp.SetPlayerItemInHandVisible(False if args["data"] else True, 1)
            

        elif key=='laser_gatling':
            id=args.get('id')
            # self.tick["laser_gatling"]=150
        elif key=='zhendong':
            id=args.get('id')
            comp = clientApi.GetEngineCompFactory().CreateDevice(playerId)
            comp.SetDeviceVibrate(500)

        elif key=='play_miss':
            miss=args.get('miss')
            id=args.get('id')
            comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
            musicId = comp.PlayCustomMusic(miss, (1,1,1), 1, 1, True, id)
        elif key=='lb11_5':
            id=args.get('id')
            particleEntityId = self.CreateEngineParticle("effects/lb11_5.json", pos)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()


        elif key=='sneaking':
            id=args.get('id')
            comp = clientApi.GetEngineCompFactory().CreateQueryVariable(id)
            result = comp.Set("query.mod.sneaking",pos)

        elif key=='tidal_claws1':
            rot=args.get('rot')
            id=args.get('id')
            comp = clientApi.GetEngineCompFactory().CreateQueryVariable(id)
            result = comp.Set("query.mod.tidal_claws_x",rot[0])
            result = comp.Set("query.mod.tidal_claws_y",rot[1])
            result = comp.Set("query.mod.tidal_claws",1)
        elif key=='soulian1':
            particleEntityId = self.CreateEngineParticle("effects/tidal_claws.json", (0,0,0))
            comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
            comp.Bind(args["id"], (-0.5,0.5,0), (0, 0, 0),False)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()
        elif key=='netherite_monstrosity':
            data=args["data"]

            if data==1:
                particleEntityId = self.CreateEngineParticle("effects/infernal_forge.json", (pos[0],pos[1]+1,pos[2]))
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()
            elif data==2:
                comp = clientApi.GetEngineCompFactory().CreateQueryVariable(args["id"])
                result = comp.Set("query.mod.ling",0)

                comp = clientApi.GetEngineCompFactory().CreateQueryVariable(args["id"])
                result = comp.GetMolangValue('query.mark_variant')
                print result

        elif key=='soulian':
            data=args["data"]

            if data==1:
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
                musicId = comp.PlayCustomMusic("tidal_hook_hit", pos, 1, 1, False, None)
            elif data==2:
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
                musicId = comp.PlayCustomMusic("tidal_hook_loop", pos, 1, 1, False, None)
            elif data==3:
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
                musicId = comp.PlayCustomMusic("tidal_tentacle", pos, 1, 1, False, None)
        elif key=='deepling_priest':
            frameEntityId = self.CreateEngineSfxFromEditor("effects/lightning.json")
            # frameAniTransComp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frameEntityId)
            # frameAniTransComp.SetRot((0,0,0))
            comp = clientApi.GetEngineCompFactory().CreateFrameAniEntityBind(frameEntityId)
            comp.Bind(args["id"], (-0.5, 3.8, 0), (0, 0,0))
            frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frameEntityId)
            frameAniControlComp.Play()

            def f():
                self.DestroyEntity(frameEntityId)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(2.5,f)
        elif key=='the_leviathan':
            data=args["data"]
            if data==2:
                particleEntityId = self.CreateEngineParticle("effects/syi.json", pos)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()
            elif data==8:
                particleEntityId = self.CreateEngineParticle("effects/silie.json", pos)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()


        elif key=='zhaohuan':
            particleEntityId = self.CreateEngineParticle("effects/zhao.json", pos)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()
        elif key=='ender_guardian':
            particleEntityId = self.CreateEngineParticle("effects/zhao.json", pos)
            comp = clientApi.GetEngineCompFactory().CreateParticleSystem(None)
            parId = comp.Create("zaibian:fei.particle", pos, (0, 0, 0))

            def f():
                particleEntityId = self.CreateEngineParticle("effects/ender_guardian_tx2.json", pos)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()
            particleEntityId = self.CreateEngineParticle("effects/ender_guardian_tx1.json", pos)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()


            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            time_=comp1.AddTimer(1,f)






        elif key=='abyssal_egg':
            pos =pos[0]+0.5,pos[1]+1.5,pos[2]+0.5
            comp = clientApi.GetEngineCompFactory().CreateTextBoard(clientApi.GetLevelId())
            if not self.postexiao.get(pos):
                boardId=comp.CreateTextBoardInWorld("孵化剩余时间 \n{}秒".format(args['time']),(0, 0, 0,1),(1, 1, 1, 0.5), True)
                self.postexiao[pos]=[boardId,40]
            else:
                self.postexiao[pos][1]=40
            boardId=self.postexiao[pos][0]
            comp.SetBoardScale(boardId, (2.0, 2.0))
            comp.SetBoardPos(boardId,pos)
            comp.SetText(boardId,"孵化剩余时间 \n{}秒".format(args['time']))

                                
        elif key=='altar_of_amethyst':
            data=args["data"]
            dim = args.get('dim')
            if data=="add":
                itemDict = args.get('itemDict')
                if itemDict["newItemName"]=="zaibian:amethyst_crab_meat":
                    comp = clientApi.GetEngineCompFactory().CreateParticleSystem(None)
                    parId = comp.Create("daojis", (pos[0]+0.5,pos[1]+0.5,pos[2]+0.5), (90, 0, 0))
                    def fu():
                        itemDict["newItemName"]="zaibian:amethyst_crab_meat1"
                        itemDict["itemName"]="zaibian:amethyst_crab_meat1"
                        self.NotifyToServer("data_event",{"key":"amethyst_crab_meat","pos":(pos,dim),"item":itemDict})
                    comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                    time_=comp1.AddTimer(16,fu)
                    self.sttexiao["amethyst_crab_meat"]=[parId,time_]
                comp = clientApi.GetEngineCompFactory().CreateItem(levelId)
                stid=comp.AddDropItemToWorld(itemDict, dim, (pos[0]+0.5,pos[1]+1.2,pos[2]+0.5), 0, 1)
                key=(pos,dim)
                self.texiao_block[key]=stid
            else:
                if self.sttexiao.get("amethyst_crab_meat"):
                    comp = clientApi.GetEngineCompFactory().CreateParticleSystem(None)
                    comp.Remove(self.sttexiao["amethyst_crab_meat"][0])
                    comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                    comp1.CancelTimer(self.sttexiao["amethyst_crab_meat"][1])
                    self.sttexiao["amethyst_crab_meat"]=None
                key=(pos,dim)
                id=self.texiao_block[key]
                comp = clientApi.GetEngineCompFactory().CreateItem(levelId)
                comp.DeleteClientDropItemEntity(id)
        elif key=='altar_of_abyss':
            comp = clientApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            comp.SetBlockEntityMolangValue(pos, "variable.start", 1.0)
            def f():
                comp = clientApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                comp.SetBlockEntityMolangValue(pos, "variable.start", 0.0)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(4.1,f)

        elif key=='zhaohuanq':
            particleEntityId = self.CreateEngineParticle("effects/ignis0.json", pos)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()
        elif key=='ignis':
            data=args['data']
            if data=="skill3":
                particleEntityId = self.CreateEngineParticle("effects/ignis3.json", pos)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()
            elif data=="skill5_0":
                particleEntityId = self.CreateEngineParticle("effects/ignis_z0.json", pos)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()
            elif data=="skill5_1":
                entityFootPos=args.get('entityFootPos')
                particleEntityId = self.CreateEngineParticle("effects/ignis_z3.json", entityFootPos)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()

                entityFootPos=args.get('entityFootPos1')
                for i in entityFootPos:
                    particleEntityId = self.CreateEngineParticle("effects/ignis_z1.json", i)
                    particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                    particleControlComp.Play()

                    particleEntityId = self.CreateEngineParticle("effects/ignis_z2.json", i)
                    particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                    particleControlComp.Play()

  
                
        elif key=='emp':
            particleEntityId = self.CreateEngineParticle("effects/emp.json", pos)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()
        elif key=='the_incinerator':
            print args
            if args['data']=='start':
                particleEntityId = self.CreateEngineParticle("effects/the_incinerator.json", (0,0,0))
                comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
                comp.Bind(args['playerId'], (0,-1.5,0), (0, 0, 0),True)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()
                if  not self.sttexiao.get(args['playerId']): 
                    self.sttexiao[args['playerId']]={}
                comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
                timedata=comp1.AddTimer(3,comp.PlayCustomMusic,"flame_burst", (1,1,1), 1, 1, False, args['playerId'])
                self.sttexiao[args['playerId']]['the_incinerator']=[particleEntityId,timedata]

            elif args['data']=='stop':
                self.DestroyEntity(self.sttexiao[args['playerId']]['the_incinerator'][0])
                comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                comp1.CancelTimer(self.sttexiao[args['playerId']]['the_incinerator'][1])


            elif args['data']=='fashe':
                i=0
                comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                def f(pos1):
                    particleEntityId = self.CreateEngineParticle("effects/the_incinerator1.json", pos1)
                    particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                    particleControlComp.Play()
                    particleEntityId = self.CreateEngineParticle("effects/the_incinerator2.json", pos1)
                    particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                    particleControlComp.Play()
                for pos in args['rot']:
                    comp1.AddTimer(0.2*i,f,pos)
                    i+=1

        elif key=='gauntlet_of_bulwark':
            if args['data']=='start':
                def f():
                    particleEntityId = self.CreateEngineParticle("effects/gauntlet_of_bulwark.json", (0,0,0))
                    comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
                    comp.Bind(args['playerId'], (0,-1.2,0), (0, 0, 0),True)
                    particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                    particleControlComp.Play()
                    o={
                    'playerId':playerId,
                    'key':'gauntlet_of_bulwark',
                    'data':'fashe',
                    }
                    self.NotifyToServer('tb_animation',o)

                if  not self.sttexiao.get(args['playerId']): 
                    self.sttexiao[args['playerId']]={}
                comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                self.sttexiao[args['playerId']]['gauntlet_of_bulwark']=comp1.AddTimer(1.5,f)
            elif args['data']=='stop':
                comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                comp1.CancelTimer(self.sttexiao[args['playerId']]['gauntlet_of_bulwark'])


        elif  key=='ignited_revenant' :
            particleEntityId = self.CreateEngineParticle("effects/fire_dragon_skill.json", (0,0,0))
            comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
            comp.Bind(args['id'], (-1,2.35,0), (0, 0, 0),True)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()

        elif  key=='the_harbinger' :
            if args['data']==4:
                particleEntityId = self.CreateEngineParticle("effects/particle0.json", (0,0,0))
                comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
                comp.Bind(args['id'], (0,2,0), (0, 0, 0))
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
                musicId = comp.PlayCustomMusic("harbinger_stun", (1,1,1), 1, 2, True, args['id'])

                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)

                comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                comp1.AddTimer(5,comp.StopCustomMusicById,musicId,0.7)
            elif args['data']==3:
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
                musicId = comp.PlayCustomMusic("harbinger_charge_prepare", (1,1,1), 1, 0.6, False, args['id'])
            elif args['data']==100:
                particleEntityId = self.CreateEngineParticle("effects/harbingerdie.json", (0,0,0))
                comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
                comp.Bind(args['id'], (0,3,0), (0, 0, 0),True)
                particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                particleControlComp.Play()


        elif  key=='the_harbinger_psw' :
            comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
            musicId = comp.PlayCustomMusic("harbinger_laser", (1,1,1), 0.3, 0.3, False, args['id'])


    def eyetexiao(self,args):
        '''影眼特效'''
        entityId=args["entityId"]
        particleEntityId = self.CreateEngineParticle("effects/eye.json", (0,5,0))
        comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
        comp.Bind(entityId, (0,0,0), (0, 0, 0))
        particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
        particleControlComp.Play()


    def OnCarriedNewItemChangedClientEvent(self,args):
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        slot = comp.GetSlotId()
        if self.jv_sgcaow==None or  self.jv_sgcaow!=slot:
            self.lock_set()
            self.jv_sgcaow=slot
        
        # itemDict=args["itemDict"]
        # def f():
        #     if itemDict and itemDict["newItemName"]=="zaibian:laser_gatling":
        #         self.UI_node.get("part1_part2").open(None)
        #     else:
        #         self.UI_node.get("part1_part2").close(None)

        # if self.UI_node.get("part1_part2")==None:
        #     comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
        #     comp.AddTimer(8.0,f)
        # else:
        #     f()
        

    def stage_lizi(self,args): #焰魔2阶段粒子
        if args["key"]=="1":
            a=["ignis1"]
        else:
            a=["ignis0","ignis1"]
        for i in a:
            particleEntityId = self.CreateEngineParticle("effects/{}.json".format(i), (0,5,0))
            comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
            comp.Bind(args["entityId"], (0,1,0), (0, 0, 0))
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()


    # 收到从服务端获取的方块调色板
    def OnReceiveBlockPalette(self, data):
        
        paletteData = data['palette']
        self.mEntityId = data['entityId']
        blockPos=data['pos']
        name="zaibian"+self.mEntityId+str(blockPos)
        # 获取一个空白的方块调色板
        comp = compFactory.CreateBlock(playerId)
        self.mBlockPalette = comp.GetBlankBlockPalette()
        
        # 反序列化方块调色板数据
        self.mBlockPalette.DeserializeBlockPalette(paletteData)
        # 合并方块组合并生成方块几何体模型
        blockGeometryComp = compFactory.CreateBlockGeometry(playerId)
        blockGeometryComp.CombineBlockPaletteToGeometry(self.mBlockPalette, name)
        # 添加定时器，直到实体真正存在时才为该实体添加方块几何体模型
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        self.mTimer = gameComp.AddTimer(0.1, self.CheckEntityAndAddBlockGeometry, self.mEntityId,name)
        
    
    def CheckEntityAndAddBlockGeometry(self, entityId,name):
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        exist = gameComp.HasEntity(entityId)
        if exist:
            gameComp.CancelTimer(self.mTimer)
            # 添加到实体中
            actorRenderComp = compFactory.CreateActorRender(entityId)
            actorRenderComp.AddActorBlockGeometry(name, (0,0,0))
            return
        
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        self.mTimer = gameComp.AddTimer(0.1, self.CheckEntityAndAddBlockGeometry,entityId,name)

    def void_scatter_arrowlz(self,args):
        particleEntityId = self.CreateEngineParticle("effects/void_scatter_arrow.json", args[0])
        particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
        particleControlComp.Play()



    def TapOrHoldReleaseClientEvent(self,args):
        # self.attack_click(args)
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        carriedData = comp.GetCarriedItem()
        if carriedData:
            if self.lock.get("tidal_claws",False)==False and carriedData["newItemName"]=="zaibian:tidal_claws":
                o={
                'playerId':playerId,
                'key':'tidal_claws',
                'data':'gj'
                }
                self.NotifyToServer('tb_animation',o)

            self.lock_set()
                
    def lock_set(self):
        comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
        carriedData = comp.GetCarriedItem()

        if  self.lock.get("gauntlet_of_guard"):
            self.lock["gauntlet_of_guard"]=False

            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"init"})
            query_comp = compFactory.CreateQueryVariable(playerId)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0.1,query_comp.Set('query.mod.syzaibian', 0.0) )

        elif self.lock.get("the_incinerator") and self.lock["the_incinerator"][0]   :
            self.lock["the_incinerator"][0]=False
            o={
                'playerId':playerId,
                'key':'the_incinerator',
                'data':'stop',
            }
            self.NotifyToServer('tb_animation',o)
            if time.time()- self.lock["the_incinerator"][1]>3:
                print '释放'
                comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
                musicId = comp.PlayCustomMusic("sword_stomp_a", (1,1,1), 1, 1, False, playerId)
                rotComp = clientApi.GetEngineCompFactory().CreateRot(playerId)
                rot = rotComp.GetRot()
                x, y, z = clientApi.GetDirFromRot(rot)

                comp = clientApi.GetEngineCompFactory().CreatePos(playerId)
                entityFootPos = comp.GetFootPos()

                lists=[]
                for i in range(2,21,2):
                    pos1=(entityFootPos[0]+x*i,entityFootPos[1]+0.1,entityFootPos[2]+z*i)
                    pos2=(entityFootPos[0]+x*i,entityFootPos[1]-1,entityFootPos[2]+z*i)
                    pos3=(entityFootPos[0]+x*i,entityFootPos[1]-2,entityFootPos[2]+z*i)
                    comp = clientApi.GetEngineCompFactory().CreateBlockInfo(levelId)
                    if comp.GetBlock(pos2)[0]!="minecraft:air":
                        lists.append(pos1)
                    elif comp.GetBlock(pos3)[0]!="minecraft:air" :
                        lists.append((pos3[0],pos3[1],pos3[2]))
                o={
                'playerId':playerId,
                'key':'the_incinerator',
                'data':'fashe',
                'rot':lists,
                }
                self.NotifyToServer('tb_animation',o)
            else:
                print '取消'
            query_comp = compFactory.CreateQueryVariable(playerId)
            query_comp.Set('query.mod.syzaibian', 0.0) 
            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"init"})
            

        elif self.lock.get("gauntlet_of_bulwark") and self.lock["gauntlet_of_bulwark"][0]   :
            self.lock["gauntlet_of_bulwark"][0]=False

            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"init"})
            if time.time()- self.lock["gauntlet_of_bulwark"][1]<1.5:
                o={
                'playerId':playerId,
                'key':'gauntlet_of_bulwark',
                'data':'stop',
                }
                self.NotifyToServer('tb_animation',o)
            else:
                
                o={
                'playerId':playerId,
                'key':'gauntlet_of_bulwark',
                'data':'fashe1',
                }
                self.NotifyToServer('tb_animation',o)
            query_comp = compFactory.CreateQueryVariable(playerId)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0,query_comp.Set('query.mod.syzaibian', 0.0) )
        elif self.lock.get("wither_assault_shoulder_weapon") and self.lock["wither_assault_shoulder_weapon"]:
            comp = clientApi.GetEngineCompFactory().CreatePlayer(playerId)
            is_sneaking = comp.isSneaking()

            if not is_sneaking:
                o={
                'playerId':playerId,
                'key':'wither_assault_shoulder_weapon',
                'data':'start',
            }
            else:
                o={
                    'playerId':playerId,
                    'key':'wither_assault_shoulder_weapon',
                    'data':'start1',
                }
            
                
            self.NotifyToServer('tb_animation',o)
            self.lock["wither_assault_shoulder_weapon"]=False
            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"init"})
            self.fovlock(False,"weapon")

                

        elif self.lock.get("void_assault_shoulder_weapon") and self.lock["void_assault_shoulder_weapon"] :
            self.lock["void_assault_shoulder_weapon"]=False
            o={
                        'playerId':playerId,
                        'key':'void_assault_shoulder_weapon',
                        'data':'start',
                    }
            self.NotifyToServer('tb_animation',o)
            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"init"})
            self.fovlock(False,"weapon")
            

        elif self.lock.get("tidal_claws") and self.lock["tidal_claws"] :
            self.lock["tidal_claws"]=False
            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"init",'key':"tidal_claws"})

        else:
            query_comp = compFactory.CreateQueryVariable(playerId)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0,query_comp.Set('query.mod.syzaibian', 0.0) )
            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"init"})

    def fovlock(self,val,key):
        '''视野不变'''
        comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
        comp.SetSpeedFovLock(val)
        if key=="weapon" and val==False:
            comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
            musicId = comp.PlayCustomMusic("rocket_launch", (1,1,1), 0.6, 1.2, False, playerId)


    def bind_lz(self,args):
        playerId1=args["playerId"]
        offset=args["offset"]
        path=args["path"]
        key=args["key"]
        def_=args.get("def")
        data=args.get("data")


        if key or playerId1!=playerId :
            particleEntityId = self.CreateEngineParticle(path, (0,5,0))
            comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particleEntityId)
            comp.Bind(playerId1, offset, (0, 0, 0),True)
            particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
            particleControlComp.Play()
        if def_=="gauntlet_of_guardJn":
            i,entityFootPos=data
            for i1 in i:
                comp = clientApi.GetEngineCompFactory().CreatePos(i1)
                entityFootPos1 = comp.GetFootPos()
                motionComp = clientApi.GetEngineCompFactory().CreateActorMotion(i1)
                if entityFootPos and entityFootPos1:
                    motionComp.SetMotion(((entityFootPos[0]-entityFootPos1[0] ),(entityFootPos[1]-entityFootPos1[1]), (entityFootPos[2]-entityFootPos1[2])))



    def OnScriptTickClient(self):
        self.alltick+=1
        for name,tiem in self.tick.items():
            if self.tick[name]==0:
                continue
            else:
                self.tick[name]-=1
        
        for name,key in self.lock.items():
            if name=="gauntlet_of_guard" and key and self.alltick%20:
                self.bind_lz({"playerId":playerId,"offset":(0, -0.5, 0),"path":"effects/gauntlet_of_guard.json","key":True})
                
                comp = clientApi.GetEngineCompFactory().CreatePos(playerId)
                entityFootPos = comp.GetFootPos()
                comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
                entities = comp.GetEntityInArea(playerId, (entityFootPos[0]-6,entityFootPos[1]-6,entityFootPos[2]-6), (entityFootPos[0]+6,entityFootPos[1]+6,entityFootPos[2]+6),True)
                        
                
                self.NotifyToServer("gauntlet_of_guardJn",[entityFootPos,entities,playerId])
        a=[]
        for key_,i in self.postexiao.items():
            self.postexiao[key_][1]-=1
            if i[1]==0:
                comp = clientApi.GetEngineCompFactory().CreateTextBoard(clientApi.GetLevelId())
                comp.RemoveTextBoard(i[0])
                a.append(key_)
        for i in a:
            del self.postexiao[i]

        if self.alltick>100000:
            self.alltick=0
    def ClientItemTryUseEvent(self,args):#点击屏幕
        itemDict=args["itemDict"]
        playerId=args["playerId"]

        
        # comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
        # result = comp.GetMolangValue("query.surface_particle_color(r)")
        # print result

        

        if playerId!=clientApi.GetLocalPlayerId():
            return
        comp = clientApi.GetEngineCompFactory().CreatePlayer(playerId)
        is_sneaking = comp.isSneaking()
        if itemDict and   itemDict['newItemName'] in ["zaibian:void_forge" ,"zaibian:infernal_forge"] and  not is_sneaking:
            args["cancel"]=True

        if itemDict  and  itemDict['newItemName']=="zaibian:meat_shredder" :
            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})
            query_comp = compFactory.CreateQueryVariable(playerId)

            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0,query_comp.Set('query.mod.syzaibian', 1.0) )


        if itemDict  and  itemDict['newItemName']=="zaibian:laser_gatling" :
            if not self.tick.get("laser_gatling"):
                self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})
            if itemDict["durability"]<=1:
                self.tick["laser_gatling"]=1
            query_comp = compFactory.CreateQueryVariable(playerId)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0,query_comp.Set('query.mod.syzaibian', 1.0) )
            # else:w
            #     args["cancel"]=True

        elif itemDict  and  itemDict['newItemName']=="zaibian:the_incinerator" :
            if self.tick.get('the_incinerator',0)==0  :
                if (self.lock.get("the_incinerator")==None or self.lock["the_incinerator"][0]==False):

                    self.tick["the_incinerator"]=300

                    self.lock["the_incinerator"]=[True,time.time()]
                    o={
                        'playerId':playerId,
                        'key':'the_incinerator',
                        'data':'start',
                    }
                    
                    self.NotifyToServer('tb_animation',o)
                    self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})
                    query_comp = compFactory.CreateQueryVariable(playerId)
                    
                    comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                    comp1.AddTimer(0,query_comp.Set('query.mod.syzaibian', 1.0) )



      
        elif itemDict  and  itemDict['newItemName']=="zaibian:void_assault_shoulder_weapon" :
            if self.tick.get('void_assault_shoulder_weapon',0)==0  :
                if (self.lock.get("void_assault_shoulder_weapon")==None or self.lock["void_assault_shoulder_weapon"]==False):
                    self.fovlock(True,"weapon")
                    self.tick["void_assault_shoulder_weapon"]=210
                    self.lock["void_assault_shoulder_weapon"]=True
                    
                    self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})
           
        elif itemDict  and  itemDict['newItemName']=="zaibian:gauntlet_of_bulwark" :
            if self.tick.get('gauntlet_of_bulwark',0)==0  :
                if (self.lock.get("gauntlet_of_bulwark")==None or self.lock["gauntlet_of_bulwark"][0]==False):
                    self.tick["gauntlet_of_bulwark"]=300

                    self.lock["gauntlet_of_bulwark"]=[True,time.time()]
                    o={
                        'playerId':playerId,
                        'key':'gauntlet_of_bulwark',
                        'data':'start',
                    }
                    self.NotifyToServer('tb_animation',o)

                    query_comp = compFactory.CreateQueryVariable(playerId)
                    comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
                    comp1.AddTimer(0,query_comp.Set('query.mod.syzaibian', 1.0) )
                    
                    self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})
        elif itemDict  and  itemDict['newItemName']=="zaibian:wither_assault_shoulder_weapon"   :
            if self.tick.get('wither_assault_shoulder_weapon',0)==0  :
                self.fovlock(True,"weapon")
                self.lock["wither_assault_shoulder_weapon"]=True
                self.tick["wither_assault_shoulder_weapon"]=180

                self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})
    
        
        elif itemDict  and  itemDict['newItemName']=="zaibian:tidal_claws"   :
            if self.tick.get('tidal_claws',0)==0  :
                self.lock["tidal_claws"]=True
                self.tick["tidal_claws"]=10
                self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})
        
                o={
                        'playerId':playerId,
                        'key':'tidal_claws',
                        'data':'start',
                    }
                self.NotifyToServer('tb_animation',o)
        elif "void_core" in itemDict["newItemName"] :  #判断是否是虚空核心
            if (self.tick.get("void_core")==None or self.tick["void_core"]==0  ):
                self.tick["void_core"]=120
                comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
                carriedData = comp.GetCarriedItem()#获取右手物品的信息

                comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
                GetForward=comp.GetForward() #返回相机向前的方向

                comp = clientApi.GetEngineCompFactory().CreatePos(playerId)
                entityFootPos = comp.GetFootPos()   #获取位置：
                if -1<GetForward[1]<-0.95:
                    key="jiao"
                else:
                    key="q"

                args={
                    "GetForward":GetForward,
                    "entityFootPos":entityFootPos,
                    "playerId":playerId,
                    "key":key,

                    "carriedData":carriedData
                }
                self.NotifyToServer("void_core_jn",args)  #放技能

        elif "gauntlet_of_guard" in itemDict["newItemName"] :
            self.lock["gauntlet_of_guard"]=True

            query_comp = compFactory.CreateQueryVariable(playerId)
            comp1 = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp1.AddTimer(0,query_comp.Set,'query.mod.syzaibian', 1.0) 
            self.NotifyToServer("use_animation",{"playerId":playerId,"animation":"use_gauntlet_of_guard"})

        
        


        


    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        pass