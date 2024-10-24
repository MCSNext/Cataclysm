
# -*- coding: utf-8 -*-

from zaibian.modCommon.moster.mosters.ender_golem import ender_golem
from zaibian.modCommon.moster.mosters.ender_guardian import ender_guardian
from zaibian.modCommon.moster.mosters.ignis import ignis
from zaibian.modCommon.moster.mosters.nameless_sorcerer import nameless_sorcerer
from zaibian.modCommon.moster.mosters.nameless_sorcerer import nameless_sorcerer_fs

from zaibian.modCommon.moster.mosters.endermaptera import endermaptera

from zaibian.modCommon.moster.mosters.ignited_revenant import ignited_revenant
from zaibian.modCommon.moster.mosters.the_harbinger import the_harbinger
from zaibian.modCommon.moster.mosters.the_baby_leviathan import the_baby_leviathan
from zaibian.modCommon.moster.mosters.lionfish import lionfish
from zaibian.modCommon.moster.mosters.deepling_priest import deepling_priest

from zaibian.modCommon.moster.mosters.coralssus import coralssus
from zaibian.modCommon.moster.mosters.the_leviathan import the_leviathan



import mod.server.extraServerApi as serverApi


from zaibian.modCommon.moster.mosters.netherite_monstrosity import netherite_monstrosity
from zaibian.modCommon.moster.mosters.amethyst_crab import amethyst_crab

from zaibian.modCommon.moster.mosters.ancient_remnant import ancient_remnant
from zaibian.modCommon.moster.mosters.deepling_warlock import deepling_warlock
from zaibian.modCommon.moster.mosters.the_prowler import the_prowler







mosters={"zaibian:ender_golem":ender_golem,"zaibian:ender_guardian":ender_guardian,"zaibian:ignis":ignis,"zaibian:netherite_monstrosity":netherite_monstrosity,
"zaibian:nameless_sorcerer":nameless_sorcerer,"zaibian:nameless_sorcerer_fs":nameless_sorcerer_fs,"zaibian:endermaptera":endermaptera,
"zaibian:ignited_revenant":ignited_revenant,"zaibian:the_harbinger":the_harbinger,"zaibian:the_baby_leviathan":the_baby_leviathan,"zaibian:lionfish":lionfish
,"zaibian:deepling_priest":deepling_priest,"zaibian:coralssus":coralssus,"zaibian:the_leviathan":the_leviathan,"zaibian:amethyst_crab":amethyst_crab
,"zaibian:deepling_warlock":deepling_warlock
,"zaibian:the_prowler":the_prowler

,"zaibian:ancient_remnant":ancient_remnant

}
boss=[
    "zaibian:ignis",
    "zaibian:the_harbinger"
    ,"zaibian:ender_guardian",
    "zaibian:netherite_monstrosity",
    "zaibian:ancient_remnant",
    "zaibian:the_leviathan"
]
pa_monster=[
    # "zaibian:ignis",
    "zaibian:ender_guardian",
    "zaibian:netherite_monstrosity",
    "zaibian:the_leviathan",
    "zaibian:the_baby_leviathan",
    "zaibian:ender_golem",
    "zaibian:ancient_remnant",
    "zaibian:the_prowler",

]

entity_list={}
class moster():
    def __init__(self):
        pass
    
    @classmethod
    def use_skill(cls,args):
        if args["EngineTypeStr"] in mosters:
            entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(args['entityId'])
            if not entitycomp.GetExtraData("die"):
                comp = serverApi.GetEngineCompFactory().CreateModAttr(args['entityId'])
                if   comp.GetAttr("skill"):
                    return
                mosters[args["EngineTypeStr"]](args).use()
        
    @classmethod
    def use_stage(cls,args):
        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(args['entityId'])
        if not  entitycomp.GetExtraData("die"):
            cc=mosters[args["EngineTypeStr"]](args)
            cc.romve_skill("死亡")
            cc.use_stage()
    
    @classmethod
    def use_stage1(cls,args):
        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(args['entityId'])
        if not  entitycomp.GetExtraData("die"):
            cc=mosters[args["EngineTypeStr"]](args)
            cc.romve_skill("死亡")
            cc.use_stage1()


    @classmethod
    def use_attack(cls,args):
        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(args['entityId'])
        if not entitycomp.GetExtraData("die"):
            comp = serverApi.GetEngineCompFactory().CreateModAttr(args['entityId'])
            if   comp.GetAttr("skill"):
                return
            mosters[args["EngineTypeStr"]](args).use_attack(args)

    @classmethod
    def start_death(cls,args):

        args["self"].die_list[0].append(args['entityId'])

        cc=mosters[args["EngineTypeStr"]](args)
        cc.romve_skill("死亡")
        cc.start_death()
        comp1 = serverApi.GetEngineCompFactory().CreateEntityEvent(args['entityId'])
        comp1.TriggerCustomEvent(args['entityId'],"start_death")
        comp = serverApi.GetEngineCompFactory().CreateModAttr(args['entityId'])
        comp.SetAttr('skill',True)

        entitycomp = serverApi.GetEngineCompFactory().CreateExtraData(args['entityId'])
        entitycomp.SetExtraData("die",True)

