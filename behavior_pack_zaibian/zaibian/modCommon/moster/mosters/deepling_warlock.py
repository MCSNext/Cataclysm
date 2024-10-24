# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class deepling_warlock(public):
    def __init__(self,args):
        super(deepling_warlock,self).__init__(args)
        
    def use(self):
        data={
            "skill_use1":20,
        }
        skill_name=self.random_skill(data)
        self.skill_jn(skill_name,[3],[0])

    def skill_1(self):
        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)
        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        entId=comp.GetAttackTarget()

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()
        dimensionComp = compFactory.CreateDimension(self.entityId)
        dimensionId = dimensionComp.GetEntityDimensionId()

        entityId = self.serverapi.CreateEngineEntityByTypeStr('zaibian:abyss_mark', entityFootPos, (0, 0), dimensionId)
        comp = serverApi.GetEngineCompFactory().CreateModAttr(entityId)
        comp.SetAttr('mark_id',entId,True)




        
       
    def start_death(self):
        time=0.1
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