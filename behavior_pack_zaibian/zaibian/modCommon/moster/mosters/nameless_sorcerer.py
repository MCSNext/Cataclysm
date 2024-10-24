# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()

class nameless_sorcerer(public):
    def __init__(self,args):
        super(nameless_sorcerer,self).__init__(args)
        
    def use(self):
        data={
            "skill_use1":15,
        }
        skill_name=self.random_skill(data)
        self.skill_jn(skill_name,[2])

    def skill_1(self):

        comp = serverApi.GetEngineCompFactory().CreateAction(self.entityId)
        attarId=comp.GetAttackTarget()
        if attarId:
            comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
            entityFootPos = comp.GetFootPos()
            if entityFootPos:
                comp = serverApi.GetEngineCompFactory().CreatePos(attarId)
                comp.SetPos(entityFootPos)
        else:
            self.romve_skill("异常skill_1")
            

    def start_death(self):
        time=0.1
        def die():
            comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
            comp.ImmuneDamage(False)
            self.serverapi.die_list[1].append(self.entityId)
            comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
            comp.Hurt(10000, serverApi.GetMinecraftEnum().ActorDamageCause.NONE, self.shid, None, False)
            self.serverapi.die_list[0].remove(self.entityId)

        comp1 = serverApi.GetEngineCompFactory().CreateControlAi(self.entityId)
        comp1.SetBlockControlAi(False, False)

        comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
        comp.ImmuneDamage(True)

        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 
    


    def stop(self):
        pass


class nameless_sorcerer_fs(public):
    def __init__(self,args):
        super(nameless_sorcerer_fs,self).__init__(args)
    
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