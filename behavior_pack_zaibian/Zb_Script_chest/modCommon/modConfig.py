# -*- coding: utf-8 -*-
# 这个文件保存了MOD中使用的一些变量

# Mod Version
ModName = "Zb_Zb_Script_chest"
ModVersion = "0.0.1"

# Server System
ServerSystemName = "Zb_Script_chestServerSystem"
ServerSystemClsPath = "Zb_Script_chest.modServer.serverSystem.Server.ServerSystem"

# Client System
ClientSystemName = "Zb_Script_chestClientSystem"
ClientSystemClsPath = "Zb_Script_chest.modClient.clientSystem.Client.ClientSystem"

# Engine
Minecraft = "Minecraft"
Engine = "Engine"
# ————————————————————————————————————————————————————————————————————————————————————————————————————
# Server Event 服务端事件
## Engine 服务端引擎事件


# 客户端通信服务端事件

#-----#


# Client Event 客户端事件

UI_CLS={"zaibian:mechanical_fusion_anvil":'chest',"cptvy:item":'chest'}  # 对应 UI_DEFS

blockNamesUI={"zaibian:mechanical_fusion_anvil":"ui"}   #对应 UI内部type_UI
itemNamesUI={"cptvy:item":"ui"}


UI_index={"ui":"/panel/zhaohuan"}   #对应blockNamesUI 的子uI


not_archives=["zaibian:mechanical_fusion_anvil"]

## Engine 客户端引擎事件
UiInitFinished = "UiInitFinished" # 注册

#服务端通信客户端事件


#UI界面
UI_DEFS = {
    "chest": {
        "uiName": "zaibian_chest",
        "uiClassPath": "Zb_Script_chest.modClient.ui.clientScreen.PyClientScreen",
        "uiScreenDef": "zaibian_chest.main"
    }
}