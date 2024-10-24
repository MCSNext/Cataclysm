# -*- coding: utf-8 -*-
# 这个文件保存了MOD中使用的一些变量

# Mod Version
ModName = "zaibian"
ModVersion = "0.0.1"

# Server System
ServerSystemName = "zaibianServerSystem"
ServerSystemClsPath = "zaibian.modServer.serverSystem.Server1.ServerSystem1"

# Client System
ClientSystemName = "zaibianClientSystem"
ClientSystemClsPath = "zaibian.modClient.clientSystem.Client.ClientSystem"

# Engine
Minecraft = "Minecraft"
Engine = "Engine"
# ————————————————————————————————————————————————————————————————————————————————————————————————————
# Server Event 服务端事件
## Engine 服务端引擎事件


# 客户端通信服务端事件

#-----#


# Client Event 客户端事件


## Engine 客户端引擎事件
UiInitFinished = "UiInitFinished" # 注册

#服务端通信客户端事件


#UI界面
UI_DEFS = {
    "part1_part2": {
        "uiName": "pinga",
        "uiClassPath": "zaibian.modClient.ui.clientScreen1.PyClientScreen",
        "uiScreenDef": "pinga.main"
    }
}



# 所有楼梯的集合
allStairs = {
    "zaibian:chorus_stairs_0",
    "zaibian:chorus_stairs_1",
    "zaibian:chorus_stairs_2",
}
# auxValue对应的前后左右的单位向量
blockAuxValueToDirFrom = {
    0:{
        "north":{"DirFrom":(0,0,1),"changeSelfDict":{1:("_1",1),3:("_1",0)}},
        "south":{"DirFrom":(0,0,-1),"changeSelfDict":{1:("_2",1),3:("_2",0)}},
        "west":{"DirFrom":(1,0,0),"changeOtherDict":{1:("_1",1),3:("_2",0)},"destroyReduction":{("_1",1):1,("_2",0):2}},
        "east":{"DirFrom":(-1,0,0),"changeOtherDict":{1:("_2",1),3:("_1",0)},"destroyReduction":{("_2",1):1,("_1",0):3}},
    },
    1:{
        "north":{"DirFrom":(-1,0,0),"changeSelfDict":{2:("_1",2),0:("_1",1)}},
        "south":{"DirFrom":(1,0,0),"changeSelfDict":{2:("_2",2),0:("_2",1)}},
        "west":{"DirFrom":(0,0,-1),"changeOtherDict":{2:("_2",2),0:("_1",1)},"destroyReduction":{("_2",2):2,("_1",1):0}},
        "east":{"DirFrom":(0,0,1),"changeOtherDict":{2:("_1",2),0:("_2",1)},"destroyReduction":{("_1",2):2,("_2",1):0}},
    },
    2:{
        "north":{"DirFrom":(0,0,-1),"changeSelfDict":{3:("_1",3),1:("_1",2)}},
        "south":{"DirFrom":(0,0,1),"changeSelfDict":{3:("_2",3),1:("_2",2)}},
        "west":{"DirFrom":(-1,0,0),"changeOtherDict":{3:("_1",3),1:("_2",2)},"destroyReduction":{("_1",3):3,("_2",2):1}},
        "east":{"DirFrom":(1,0,0),"changeOtherDict":{3:("_2",3),1:("_1",2)},"destroyReduction":{("_2",3):3,("_1",2):1}},
    },
    3:{
        "north":{"DirFrom":(1,0,0),"changeSelfDict":{0:("_1",0),2:("_1",3)}},
        "south":{"DirFrom":(-1,0,0),"changeSelfDict":{0:("_2",0),2:("_2",3)}},
        "west":{"DirFrom":(0,0,1),"changeOtherDict":{0:("_2",0),2:("_1",3)},"destroyReduction":{("_2",0):0,("_1",3):2}},
        "east":{"DirFrom":(0,0,-1),"changeOtherDict":{0:("_1",0),2:("_2",3)},"destroyReduction":{("_1",0):0,("_2",3):2}},
    }
}

item_zsl={
        "zaibian:sandstorm_in_a_bottle": [
        8
    ],
      "zaibian:sticky_gloves": [
        6
    ]
}