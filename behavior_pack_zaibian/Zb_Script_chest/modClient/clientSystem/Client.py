# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Zb_Script_chest.modCommon.modConfig as modConfig
from Zb_Script_chest.modClient.clientUtil.liu_util import LiuClientStaticVar
from Zb_Script_chest.modCommon.modCommonUtils.Items import Items
# 获取客户端system的基类ClientSystem
playerId=clientApi.GetLocalPlayerId()
levelId=clientApi.GetLevelId()
# 在modMain中注册的Client System类

compFactory = clientApi.GetEngineCompFactory()

class ClientSystem(clientApi.GetClientSystemCls()):
    def __init__(self, namespace, name):
        super(ClientSystem, self).__init__(namespace, name)

        self.strengthenUINode={}

        self.before_cls=None #当前都UI类名
        self.itemname="" #当前UI使用name

        self.ListenEvent()
        
        

    def ListenEvent(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), 'UiInitFinished', self, self.OnUIInitFinished)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),  'ClientBlockUseEvent', self, self.ClientBlockUseEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),  'OnCarriedNewItemChangedClientEvent', self, self.OnCarriedNewItemChangedClientEvent)

        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "OnBagChangedEvent", self, self.OnBagChangedEvent)
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "die_ui_pet", self, self.die_ui_pet)
        self.ListenForEvent(modConfig.ModName, modConfig.ServerSystemName, "setMultipleItemFlyAnimation", self, self.setMultipleItemFlyAnimation)



    # 监听引擎初始化完成事件，在这个事件后创建我们的设置UI
    def OnUIInitFinished(self, args):
        # 注册UI 详细解释参照《UI API》
        for i,data in modConfig.UI_DEFS.items():
            uiName = data['uiName']
            clientApi.RegisterUI(modConfig.ModName, uiName, data["uiClassPath"], data["uiScreenDef"])
            clientApi.CreateUI(modConfig.ModName, uiName, {"isHud": 1})
            self.strengthenUINode[i] = clientApi.GetUI(modConfig.ModName, uiName)

    def OnCarriedNewItemChangedClientEvent(self,args):
        '''物品打开UI'''
        itemDict = args["itemDict"]
        itemName = itemDict["newItemName"]


        def f():
            before_cls=modConfig.UI_CLS.get(itemName,"")

            if itemDict['newItemName'] in  modConfig.itemNamesUI.keys()  and self.strengthenUINode[before_cls].show==False:
                open=self.strengthenUINode[before_cls].open
                comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
                slotId = comp.GetSlotId()
                self.strengthenUINode[before_cls].slotId=slotId
                self.strengthenUINode[before_cls].show_ui(open)
            else:
                if self.before_cls:
                    open=self.strengthenUINode[self.before_cls].open
                    self.strengthenUINode[self.before_cls].show_ui(open,False)
                


        if self.strengthenUINode=={}:
            comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(8.0,f)
        else:
            f()


    def ClientBlockUseEvent(self,args):
        '''方块打开UI'''

        playerId=args["playerId"]
        blockName=args["blockName"]
        pos=(args["x"],args["y"],args["z"])
        comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
        dimension=comp.GetCurrentDimension()

        self.before_cls=modConfig.UI_CLS.get(blockName)
        self.itemname=blockName
        if playerId==playerId and blockName in modConfig.blockNamesUI.keys() and self.strengthenUINode[self.before_cls].show==False:
            self.strengthenUINode[self.before_cls].openBth({"playerId":playerId,"dimension":dimension,"pos":pos,"use_way":"block","type_UI":modConfig.blockNamesUI[blockName]})
            
            


    def die_ui_pet(self,args):
        if self.before_cls and self.strengthenUINode[self.before_cls].show==True:
            self.strengthenUINode[self.before_cls].gbinBth({})


    def OnBagChangedEvent(self,args):
        if self.before_cls and self.strengthenUINode[self.before_cls].show==True:
            self.strengthenUINode[self.before_cls].UpdateBagUI(args)


    def setMultipleItemFlyAnimation(self, args):
        """
        设置多个物品飞行动画。
        """
        data = args['data']
        if self.before_cls and self.strengthenUINode[self.before_cls].show==True:
            self.strengthenUINode[self.before_cls].setMultipleItemFlyAnimation(data)

    

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        pass