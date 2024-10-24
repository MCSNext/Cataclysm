# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.public import public
import mod.server.extraServerApi as serverApi
import random
compFactory = serverApi.GetEngineCompFactory()
levelId=serverApi.GetLevelId()
CompFactory=serverApi.GetEngineCompFactory()

class ignited_revenant(public):
    def __init__(self,args):
        super(ignited_revenant,self).__init__(args)
        
    def use(self):
        data={
            "skill_use1":3,
            "skill_use2":2,
            "skill_use3":1,

        }
        skill_name=self.random_skill(data)
        if skill_name=='skill_use1':
            comp =CompFactory.CreateEntityEvent(self.entityId)
            comp.TriggerCustomEvent(self.entityId,skill_name)
            def f():
                comp = CompFactory.CreateEntityEvent(self.entityId)
                comp.TriggerCustomEvent(self.entityId,"romve_skill")
            comp = CompFactory.CreateGame(levelId)
            comp.AddTimer(4,f) 
            for i in range(0,8):
                comp.AddTimer(0.5*i,self.skill_1) 

        else:
            self.skill_jn(skill_name,[0,2,2],None)

        

    def skill_1(self):
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        lists=comp.GetEntitiesAroundByType(self.entityId, 1, serverApi.GetMinecraftEnum().EntityType.Mob)
        for i in lists:
            if i != self.entityId:
                comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                comp.Hurt(4, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)

    def skill_2(self):
        # self.serverapi.data_init[self.entityId]=True

        # def f1():
        #     self.serverapi.data_init[self.entityId]=False
        # comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        # comp.AddTimer(2,f1)

        comp = serverApi.GetEngineCompFactory().CreatePos(self.entityId)
        entityFootPos = comp.GetFootPos()

        rotComp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = rotComp.GetRot()
        def f(k):
            for i1 in range(0,360,18):
                x,y,z= serverApi.GetDirFromRot((rot[0],rot[1]+i1))
                pos=(entityFootPos[0]+x*2,entityFootPos[1]+3,entityFootPos[2]+z*2)
                comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
                param = {
                    'position': pos,
                    'direction': (x,0.2-k*0.1,z),
                }
                comp.CreateProjectileEntity(self.entityId, "zaibian:ignited_revenant_psw", param)
        for i in range(6):
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.AddTimer(0.33*i,f,i)
            
    def skill_3(self):
        def yo():
            self.serverapi.BroadcastToAllClient('zhaohuan',{'id':self.entityId,'key':'ignited_revenant'})
            def f():
                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                lists=comp.GetEntitiesAroundByType(self.entityId, 6, serverApi.GetMinecraftEnum().EntityType.Mob)
                if self.entityId in lists:
                    lists.remove(self.entityId)
                for i in lists:
                    comp = serverApi.GetEngineCompFactory().CreateGame(self.entityId)
                    if comp.CanSee(self.entityId,i,6.0,True,180.0,180.0):
                        comp = serverApi.GetEngineCompFactory().CreateHurt(i)
                        comp.Hurt(12, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, self.entityId, None, True)
                        comp = serverApi.GetEngineCompFactory().CreateEffect(i)
                        res = comp.AddEffectToEntity("blindness", 3, 2, True)
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            for i in range(0,7):
                comp.AddTimer(0.2*i,f) 
         
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(0.6,yo)

        


    def start_death(self):
        time=0
        def die():
            self.serverapi.die_list[1].append(self.entityId)
            comp = serverApi.GetEngineCompFactory().CreateHurt(self.entityId)
            comp.Hurt(10000, serverApi.GetMinecraftEnum().ActorDamageCause.NONE, self.shid, None, False)
            self.serverapi.die_list[0].remove(self.entityId)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time,die) 
    
        
    def stop(self):
        pass