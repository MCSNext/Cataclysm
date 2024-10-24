# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class lionfish(public):
    def __init__(self,args):
        super(lionfish,self).__init__(args)




    def start_death(self):
        time=0.5
        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        def f():
            for i1 in range(0,360,36):
                x,y,z= serverApi.GetDirFromRot((rot[0],rot[1]+i1))
                pos=(entityFootPos[0]+x*2,entityFootPos[1]+0.5,entityFootPos[2]+z*2)
                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                param = {
                    'position': pos,
                    'direction': (x,0,z),
                }
                comp.CreateProjectileEntity(self.entityId, "zaibian:lionfish1", param)
        f()
        def die():
            self.serverapi.die_list[1].append(self.entityId)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.KillEntity(self.entityId)
            self.serverapi.die_list[1].remove(self.entityId)
            self.serverapi.die_list[0].remove(self.entityId)

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 
    def stop(self):
        pass