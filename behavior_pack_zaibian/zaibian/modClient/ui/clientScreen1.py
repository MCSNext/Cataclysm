# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import mod.client.extraClientApi as clientApi
import zaibian.modCommon.modConfig as modConfig
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
playerId=clientApi.GetLocalPlayerId()

# 获取组件工厂，用来创建组件
compFactory = clientApi.GetEngineCompFactory()
client=clientApi.GetSystem(modConfig.ModName,modConfig.ClientSystemName)
# 所有的UI类需要继承自引擎的ScreenNode类
LevelId=clientApi.GetLevelId()
class PyClientScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.nengliang=6*30
        self.lock=False
        self.tick=0

    @ViewBinder.binding(ViewBinder.BF_BindString, "#main.pinga")
    def OnGameTick(self):
        return
        if client:
            client.OnGameTick()

    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.AddTouchEventHandler("/button", self.OnAimButtonTouch, {"isSwallow": False})
        self.SetScreenVisible(False)


    def OnAimButtonTouch(self,args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args.get("TouchEvent")
        ButtonPath= args.get("ButtonPath")
        # 按钮按下时
        if touchEvent == touchEventEnum.TouchDown:
            self.bianhuan()
            
        
    def bianhuan(self):
        query_comp = compFactory.CreateQueryVariable(playerId)
        if query_comp.Get('query.mod.bianti'):
            k=0
        else:
            k=1
        o={
            'playerId':playerId,
            'key':'sandstorm',
            'data':k,
        }
        client.NotifyToServer('tb_animation',o)

        labelUIControl = self.GetBaseUIControl("/button/button_label").asLabel()
        labelUIControl.SetText("变形" if not k else "还原")

            

    def show_ui(self,path,key=True):
        baseUIControl = self.GetBaseUIControl(path)
        if baseUIControl:
            baseUIControl.SetVisible(key)

    def nengliangbianhua(self):
        imageUIControl = self.GetBaseUIControl("/button/image").asImage()
        imageUIControl.SetSpriteClipRatio(1-self.nengliang/(6.0*30))

    def Update(self):
        if client:
            super(PyClientScreen, self).Update()
            self.tick+=1
            if self.tick%1==0:
                query_comp = compFactory.CreateQueryVariable(playerId)
                if query_comp.Get('query.mod.bianti'):
                    if self.nengliang>0:
                        self.nengliang-=1
                        self.nengliangbianhua()
                        if self.nengliang==0:
                            self.bianhuan()
                else:
                    if self.nengliang<6*30:
                        self.nengliang+=1
                        self.nengliangbianhua()
                comp = clientApi.GetEngineCompFactory().CreateModAttr(playerId)
                comp.SetAttr('uisand', self.nengliang)



                    


    def open(self,args={}):
        '''打开'''
        self.SetScreenVisible(True)

    def close(self):
        '''关闭'''
        self.SetScreenVisible(False)
        
