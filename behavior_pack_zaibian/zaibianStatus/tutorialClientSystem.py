# -*- coding: utf-8 -*-

# 获取客户端引擎API模块
import mod.client.extraClientApi as clientApi
import zaibianStatus.storage as storage

from zaibianStatus.Status_factory import StatusFactory

# 获取客户端system的基类ClientSystem
ClientSystem = clientApi.GetClientSystemCls()
localPlayerId=clientApi.GetLocalPlayerId()
levelId=clientApi.GetLevelId()

# 在modMain中注册的Client System类
class TutorialClientSystem(ClientSystem):

    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        # 首先初始化TutorialClientSystem的基类ClientSystem
        super(TutorialClientSystem, self).__init__(namespace, systemName)
        print "==== TutorialClientSystem Init ===="
        storage.set_clientApi(self)
        comp = clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId())
        comp.OpenPlayerHitBlockDetection(0.0001)
        self.ListenEvent()

    def ListenEvent(self): 
        self.ListenForEvent("zaibianStatus", "TutorialServerSystem", "RefreshEffectServerEvent",self, self.RefreshEffectServerEvent) #实体获得状态效果时
        self.ListenForEvent("zaibianStatus", "TutorialServerSystem", "RemoveEffectServerEvent",self, self.RemoveEffectServerEvent) #实体获得状态效果时
        self.ListenForEvent("zaibianStatus", "TutorialServerSystem", "AddEffectServerEvent",self, self.AddEffectServerEvent) #实体获得状态效果时
    

    def AddEffectServerEvent(self,args):
        StatusFactory.status_start(args['effectName'],args,cs=False)

    def RefreshEffectServerEvent(self,args):
        StatusFactory.status_start(args['effectName'],args,cs=False)
        pass

    def RemoveEffectServerEvent(self,args):
        StatusFactory.status_end(args['effectName'],args)
        pass
        
    def Update(self):
        StatusFactory.tick(False)
        pass    
    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        pass