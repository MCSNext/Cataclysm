# -*- coding: utf-8 -*-

# 获取引擎服务端API的模块
import mod.server.extraServerApi as serverApi
from zaibianStatus.Status_factory import StatusFactory
import zaibianStatus.storage as storage

import zaibianStatus.storage as storage

# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
ServerSystem = serverApi.GetServerSystemCls()
levelId=serverApi.GetLevelId()
ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()
# 在modMain中注册的Server System类

class TutorialServerSystem(ServerSystem):

    # ServerSystem的初始化函数
    def __init__(self, namespace, systemName):
        # 首先调用父类的初始化函数
        super(TutorialServerSystem, self).__init__(namespace, systemName)
        print "===== TutorialServerSystem init ====="
        # 初始时调用监听函数监听事件
        self.ListenEvent()
        storage.set_serverapi(self)




    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):
        
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEffectServerEvent",self, self.AddEffectServerEvent) #实体获得状态效果时
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "RemoveEffectServerEvent",self, self.RemoveEffectServerEvent) #实体身上状态效果被移除时
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self, self.OnScriptTickServer) # tick

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "RefreshEffectServerEvent",self, self.RefreshEffectServerEvent) #实体获得状态效果时
        # 在自定义的ServerSystem中监听引擎的事件ServerChatEvent，回调函数为OnServerChat

    def AddEffectServerEvent(self,args):
        StatusFactory.status_start(args['effectName'],args,cs=True)
        self.BroadcastToAllClient("AddEffectServerEvent",args)

    def RefreshEffectServerEvent(self,args):
        StatusFactory.status_start(args['effectName'],args,cs=True)
        self.BroadcastToAllClient("RefreshEffectServerEvent",args)
        pass

    def RemoveEffectServerEvent(self,args):
        StatusFactory.status_end(args['effectName'],args)
        self.BroadcastToAllClient("RemoveEffectServerEvent",args)
        
    def OnScriptTickServer(self):
        StatusFactory.tick(True)



    # 反监听函数，用于反监听事件，在代码中有创建注册就对应了销毁反注册是一个好的编程习惯，不要依赖引擎来做这些事。
    def UnListenEvent(self):
        pass
    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        print "===== TutorialServerSystem Destroy ====="
        # 调用上面的反监听函数来销毁
        self.UnListenEvent()
