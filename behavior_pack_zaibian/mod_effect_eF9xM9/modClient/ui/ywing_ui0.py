# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from mod_effect_eF9xM9.modCommon import modConfig
from mod_effect_eF9xM9.modClient.manager import get_singleton, engineAPI
import math
import random

playerId = clientApi.GetLocalPlayerId()
levelId = clientApi.GetLevelId()
ScreenNode = clientApi.GetScreenNodeCls()

from common.utils.mcmath import Vector3

class ywing_ui0(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.client = None
        self.isWingFlying = False
        '''是否正在使用翅膀飞行'''
        self.justChange = 0
        '''是否 才启用 功能'''
        self.needClick = True
        '''标识是否需要触发按钮功能'''

    def Create(self):
        self.client = clientApi.GetSystem(
            modConfig.ModName, modConfig.ClientSystemName)

        path = "/panel0/button0"
        self.RegisterBtnFunc({
            "path": path,
            "refunc": self.itemBtn0Func,
            "need_type": 3
        })
        hasEffectList = engineAPI.GetAllEffects(playerId)
        if hasEffectList:
            for i in hasEffectList:
                if i["effectName"] == "y_flytwo" and i["duration"] > 0:
                    self.client.needWingBtn = True
                    break
        self.changeBtnShowFunc()

    def changeBtnShowFunc(self):
        self.SetVisible("/panel0/button0", self.client.needWingBtn)
        if self.client.needWingBtn:
            engineAPI.SetText(self,"/panel0/button0/button_label","开始\n飞行")
        elif self.isWingFlying:
            self.isWingFlying = False
            self.changeFlyFunc()



    def itemBtn0Func(self, args):
        '''使用物品按钮'''
        # print("53-----------",args)
        if args['TouchEvent'] == 1:
            self.needClick = True
            pass
        elif args['TouchEvent'] == 4 and self.needClick:
            self.needClick = False
            pass
        elif args['TouchEvent'] == 0 and self.needClick:
            self.triggerBtn0Func()
            pass

        

    def triggerBtn0Func(self):
        self.isWingFlying = not self.isWingFlying
        self.client.NotifyToServer("yEffectInfoToServer", {
            "class": "PyServerSystem",
            "funcName": "changeSFlyAnimatToServerFunc",
            "playerId": playerId,
            "willStart" : self.isWingFlying
        })
        if self.isWingFlying:
            engineAPI.SetText(self,"/panel0/button0/button_label","结束\n飞行")
        else:
            engineAPI.SetText(self,"/panel0/button0/button_label","开始\n飞行")


        self.changeFlyFunc()

        pass
    
    def changeFlyFunc(self):
        '''更改了可飞行能力'''
        if self.isWingFlying:
            comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
            comp.SetCameraOffset((0, -1, 0))
            # comp.DepartCamera()
            self.justChange = 45

        else:
            comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
            comp.SetCameraOffset((0, 0, 0))
        
        '''
        2023-10-25 18:40:11 TODO
        这里发送信息给服务端开始tick
         
        还需要将移动按钮按下/松开事件发送给服务端
            用于加速
        
        '''
        pass

    def Update(self):
        # if self.isWingFlying:
        #     engineAPI.SetMotion((0,0,0))
        #     engineAPI.add_timer(1.0/60,engineAPI.SetMotion,(0,0,0))
        #     pass
        return
        if self.isWingFlying:
            comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
            isInWater = comp.GetMolangValue('query.is_in_water')

            rx,ry,rz = engineAPI.GetDirFromRot(engineAPI.GetRot(playerId))
            uv1 = Vector3(rx,ry+0.4,rz).Normalized()
            left, up = engineAPI.GetInputVector()
            vx0,vy0,vz0 = engineAPI.GetMotion(playerId)
            vt0 = Vector3(vx0,vy0,vz0)
            vLen0 = vt0.Length()
            if isInWater:
                vLen0*=0.9
            if left or up:
                if vLen0 < 0.2 and up > 0 and not isInWater:
                    endV = uv1*(0.5)
                elif vLen0 < 0.1 and up <= 0:
                    endV = uv1*(0.1)
                elif vLen0 > 2:
                    '''速度特别快的时候,大量减速'''
                    endV = uv1*(vLen0-0.1)
                else:
                    endV = uv1*(vLen0-0.02*(math.atan((vLen0-0.2)*2.5)/1.19))
                    if ry < -0.5:
                        cacheN0 = vLen0
                        if (cacheN0 > 1.8 and ry >= -1 and ry < -0.6) or (cacheN0 > 1.4 and ry >= -0.6 and ry < -0.5):
                            cacheN1 = 0
                        else:
                            cacheN1 = 1.1
                            if cacheN0 < cacheN1*0.1:
                                cacheN0 = cacheN1*0.1
                        gravityV = Vector3(0,-0.17,0)*(math.atan((cacheN1/cacheN0)*0.3)/1.249)
                        endV+=gravityV
                        pass
                engineAPI.SetMotion(tuple(endV))
            else:
                '''无操作时'''
                if vLen0 > 0.2 and (not self.justChange or vLen0 > 1):
                    cacheN0 = vLen0
                    if cacheN0 > 1.2:
                        cacheN1 = 0
                    else:
                        cacheN1 = 1.1
                        if cacheN0 < cacheN1*0.1:
                            cacheN0 = cacheN1*0.1
                        pass
                    gravityV = Vector3(0,-0.17,0)*(math.atan((cacheN1/cacheN0)*0.3)/1.249)

                    endV = uv1*(vLen0-0.0026)+gravityV
                    engineAPI.SetMotion(tuple(endV))
                else:
                    if self.justChange:
                        '''刚起飞,添加一点动力'''
                        uv1 = Vector3(rx,0,rz).Normalized()
                        uv1 += Vector3(0,0.5,0)
                        endV = tuple(uv1*(0.2))
                        engineAPI.SetMotion(endV)
                    else:
                        endV = uv1*(vLen0)+Vector3(0,-0.17,0)
                        engineAPI.SetMotion(tuple(endV))
            if self.justChange:
                self.justChange -= 1
            # print("110---------",vt0.Length(), '------',)

        pass

    def RegisterBtnFunc(self, _data, isSwallow=True):
        '''注册按钮'''
        btn = self.GetBaseUIControl(_data['path']).asButton()
        btn.AddTouchEventParams({"isSwallow": isSwallow})
        if _data['need_type'] == 0:
            btn.SetButtonTouchUpCallback(_data['refunc'])
        elif _data['need_type'] == 1:
            btn.SetButtonTouchUpCallback(_data['refunc'])
            btn.SetButtonTouchDownCallback(_data['refunc'])
            btn.SetButtonTouchCancelCallback(_data['refunc'])
            btn.SetButtonTouchMoveOutCallback(_data['refunc'])
        elif _data['need_type'] == 2:
            btn.SetButtonTouchUpCallback(_data['refunc'])
            btn.SetButtonTouchDownCallback(_data['refunc'])
            btn.SetButtonTouchCancelCallback(_data['refunc'])
            btn.SetButtonTouchMoveInCallback(_data['refunc'])
            btn.SetButtonTouchMoveOutCallback(_data['refunc'])
        elif _data['need_type'] == 3:
            btn.SetButtonTouchDownCallback(_data['refunc'])
            btn.SetButtonTouchMoveCallback(_data['refunc'])
            btn.SetButtonTouchUpCallback(_data['refunc'])
            btn.SetButtonTouchCancelCallback(_data['refunc'])
            pass
        pass
