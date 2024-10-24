# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

import zaibianStatus.storage as storage

from zaibianStatus.status.monstrous import monstrous
from zaibianStatus.status.abyssal_curse import abyssal_curse

from zaibianStatus.status.blazing_brand import blazing_brand
from zaibianStatus.status.bone_fracture import bone_fracture


from zaibianStatus.status.abyssal_fear import abyssal_fear


from zaibianStatus.status.abyssal_burn import abyssal_burn

from zaibianStatus.status.stun import stun
from zaibianStatus.status.blessing_of_amethyst import blessing_of_amethyst
from zaibianStatus.status.curse_of_desert import curse_of_desert





Status={"monstrous":monstrous,"blazing_brand":blazing_brand,"abyssal_curse":abyssal_curse
        ,"bone_fracture":bone_fracture,"abyssal_fear":abyssal_fear,"abyssal_fear":abyssal_burn,"stun":stun,"blessing_of_amethyst":blessing_of_amethyst
        ,"curse_of_desert":curse_of_desert 
        }

Status_class={}
tick_={"tick":0}
class StatusFactory(object):

    # 客户端System的初始化函数
    def __init__(self):
        pass

    @classmethod
    def status_start(cls,Statusname,args,k=0,cs=False):  #开始运行状态
        entityId=args["entityId"]
        if  (cs==False and clientApi.GetSystem("zaibianStatus", "TutorialClientSystem")) or (cs==True and serverApi.GetSystem("zaibianStatus", "TutorialServerSystem")):
            if Status.get(Statusname):
                if not Status_class.get(entityId):
                    Status_class[entityId]={}                

                if Status_class[entityId].get(Statusname):
                        cla=Status_class[entityId][Statusname]
                else:
                    cla=Status[Statusname](entityId)

                    Status_class[entityId][Statusname]=cla
                cla.init(args)
                cla.status_start(cs)
        else:
            if k<6:
                comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
                comp.AddTimer(3.0,cls.status_start,Statusname,args,k+1,cs)
    
    @classmethod
    def status_end(cls,Statusname,args): #结束状态
        entityId=args["entityId"]
        if Status.get(Statusname):
            Status_class[entityId][Statusname].status_end()

    @classmethod
    def tick(cls,sc=False): #tick
        tick_["tick"]+=1
        for entityId in Status_class.keys():
            if sc==True:
                comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
                alive = comp.IsEntityAlive(entityId)
            else:
                comp = clientApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
                alive = comp.IsEntityAlive(entityId)
            for Statusname,cl in Status_class[entityId].items():
                if cl.key==True:
                    effectRes=True
                    if  tick_["tick"]%30==0:
                        if sc==False:
                            comp = clientApi.GetEngineCompFactory().CreateEffect(entityId)
                            effectRes = comp.HasEffect(Statusname)
                        else:
                            comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
                            effectRes = comp.HasEffect(Statusname)

                    if (not alive  or  not  effectRes) :
                        cls.status_end(Statusname,{"entityId":entityId})
                    cl.tick(sc)
            