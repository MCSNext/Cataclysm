# -*- coding: utf-8 -*-
# 上面这行是让这个文件按utf-8进行编码，这样就可以在注释中写中文了

# 这行是import到MOD的绑定类Mod，用于绑定类和函数
from mod.common.mod import Mod
# 这行import到的是引擎服务端的API模块
import mod.server.extraServerApi as serverApi
# 这行import到的是引擎客户端的API模块
import mod.client.extraClientApi as clientApi
import modCommon.modConfig as modConfig

# 用Mod.Binding来绑定MOD的类，引擎从而能够识别这个类是MOD的入口类
@Mod.Binding(name = modConfig.ModName, version = "0.0.1")
class water_lucky(object):
    # 类的初始化函数
    def __init__(self):
        pass

    @Mod.InitServer()
    def ChoppingBoardServerInit(self):
        serverApi.RegisterSystem(modConfig.ModName,modConfig.ServerSystemName, modConfig.ServerSystemClsPath)

    @Mod.InitClient()
    def ChoppingBoardClientInit(self):
        clientApi.RegisterSystem(modConfig.ModName, modConfig.ClientSystemName, modConfig.ClientSystemClsPath)
    
    @Mod.DestroyServer()
    def ChoppingBoardServerDestroy(self):
        pass

    @Mod.DestroyClient()
    def ChoppingBoardClientDestroy(self):
        pass
    
    