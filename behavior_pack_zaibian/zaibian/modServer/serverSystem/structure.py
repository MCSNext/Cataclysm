
import mod.server.extraServerApi as serverApi
levelId=serverApi.GetLevelId()

def sc_enid(i2,name,dim1,rot=(0,0),k=0):
    def op():
        def callback(data):
            code = data.get('code', 0)
            if code == 1:
                def f():
                    entityId =  serverApi.GetSystem("zaibian","zaibianServerSystem").CreateEngineEntityByTypeStr(name, i2, rot, dim1,)
                    if name=='zaibian:the_prowler':
                        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
                        comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,135)
                        comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,135)


                comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
                comp.AddTimer(1,f)
        comp = serverApi.GetEngineCompFactory().CreateChunkSource(levelId)
        comp.DoTaskOnChunkAsync(dim1, (int(i2[0])-8,int(i2[1])-8,int(i2[2])-8),(int(i2[0])+8,int(i2[1])+8,int(i2[2])+8),callback)
    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
    comp.AddTimer(k*0.1,op)

def tick_yiji(self,tick,args):
    '''生成遗迹怪物及成就'''
    blockName=args['blockName']
    dimension=args['dimension']
    pos=(args['posX'],args['posY'],args['posZ'])
    key=(blockName,dimension,pos)

    if not (blockName in ["zaibian:the_harbinger","zaibian:netherite_monstrosity_tick","zaibian:desert","zaibian:ender_guardian_tick"] and tick==0):
        return
    self.block_data[key]=60
    
    
    blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
    blockEntityData = blockEntitycomp.GetBlockEntityData(dimension, pos)
    if blockName=="zaibian:ender_guardian_tick":
        for i in [(0,1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1)]:
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew((args['posX']+i[0],args['posY']+i[1],args['posZ']+i[2]), dimension)
            if blockDict["name"]=="minecraft:end_stone" :
                pass
            else:
                return
        if   not  blockEntityData["stid"]:
            # comp = serverApi.GetEngineCompFactory().CreatePos(serverApi.GetPlayerList()[0])
            # entityFootPos = comp.GetFootPos()
            blockEntityData["stid"]=True
            for k,i in enumerate([[(pos[0]+3.5,pos[1]+39,pos[2]+8),'zaibian:ender_golem'],[(pos[0]-15,pos[1]+46,pos[2]-9),'zaibian:ender_golem'],
                                  [(pos[0]+20,pos[1]+38,pos[2]+26),'zaibian:ender_golem'],
                      [(pos[0]+22.5,pos[1]+48,pos[2]-6),'minecraft:shulker'],
                      ]):
                if len(i)==2:
                    rot=(0,0)
                else:
                    rot=i[2]
                sc_enid(i[0],i[1],dimension,rot,k=k)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        list_=comp.GetEntitiesInSquareArea(None, (args['posX']-64,args['posY']-2,args['posZ']-64), (args['posX']+64,args['posY']+70,args['posZ']+64), dimension)
        for  i in  list_:
            if i in serverApi.GetPlayerList():
                comp = serverApi.GetEngineCompFactory().CreateAchievement(levelId)
                comp.SetNodeFinish(i, "z1", callback = None )

    elif blockName=="zaibian:the_harbinger":
        for i in [(0,1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1)]:
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew((args['posX']+i[0],args['posY']+i[1],args['posZ']+i[2]), dimension)
            if i==(0,1,0) and blockDict["name"]=="minecraft:deepslate_bricks":
                pass
            elif blockDict["name"]=="zaibian:dungeon_block" :
                pass
            else:
                return
        if  not  blockEntityData["stid"]:
            blockEntityData["stid"]=True
            for k,i in enumerate([
                [(pos[0]+46,pos[1]+6,pos[2]-4),'zaibian:the_watcher'],
                [(pos[0]+44,pos[1]+6,pos[2]+13),'zaibian:the_watcher'],
                [(pos[0]+44,pos[1]+6,pos[2]+13),'zaibian:the_watcher'],
                [(pos[0]+48,pos[1]+6,pos[2]+17),'zaibian:the_watcher'],
                [(pos[0]+14,pos[1]+6,pos[2]+3.5),'zaibian:the_prowler',(0,270)],
                [(pos[0]+5,pos[1]+3.5,pos[2]+24),'zaibian:the_watcher'],
                [(pos[0]+5.5,pos[1]+3.5,pos[2]-17),'zaibian:the_watcher'],
                [(pos[0],pos[1]+3.5,pos[2]+3.5),'zaibian:the_watcher'],
                [(pos[0]-32,pos[1]+3.5,pos[2]+24),'zaibian:the_watcher'],
                [(pos[0]-32,pos[1]+3.5,pos[2]-17),'zaibian:the_watcher'],
                [(pos[0]-32,pos[1]+2,pos[2]-7),'zaibian:the_watcher'],
                [(pos[0]-26,pos[1]+3,pos[2]+3),'zaibian:the_watcher'],
                [(pos[0]-40.5,pos[1]+4.2,pos[2]+3.5),'zaibian:the_harbinger',(0,270)],

                ]): 
                if len(i)==2:
                    rot=(0,0)
                else:
                    rot=i[2]
                sc_enid(i[0],i[1],dimension,rot,k=k)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        list_=comp.GetEntitiesInSquareArea(None, (args['posX']-60,args['posY']-2,args['posZ']-40), (args['posX']+60,args['posY']+30,args['posZ']+40), dimension)
        for  i in  list_:
            if i in serverApi.GetPlayerList():
                comp = serverApi.GetEngineCompFactory().CreateAchievement(levelId)
                comp.SetNodeFinish(i, "z3", callback = None )
                
    elif blockName=="zaibian:netherite_monstrosity_tick":
        for k,i in enumerate([(0,1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1)]):
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew((args['posX']+i[0],args['posY']+i[1],args['posZ']+i[2]), dimension)
            if i==(0,1,0) and blockDict["name"]=="minecraft:bedrock":
                pass
            elif blockDict["name"]=="minecraft:polished_blackstone_bricks" :
                pass
            else:
                return
        if  not  blockEntityData["stid"]:
            blockEntityData["stid"]=True
            for i in [[(pos[0]+1.5,pos[1]+5.5,pos[2]+3),'zaibian:netherite_monstrosity']]: 
                if len(i)==2:
                    rot=(0,0)
                else:
                    rot=i[2]
                sc_enid(i[0],i[1],dimension,rot,k=k)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        list_=comp.GetEntitiesInSquareArea(None, (args['posX']-25,args['posY'],args['posZ']-10), (args['posX']+25,args['posY']+40,args['posZ']+60), dimension)
        for  i in  list_:
            if i in serverApi.GetPlayerList():
                comp = serverApi.GetEngineCompFactory().CreateAchievement(levelId)
                comp.SetNodeFinish(i, "z2", callback = None )

    elif blockName=="zaibian:desert":
        for i in [(0,1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1)]:
            comp = serverApi.GetEngineCompFactory().CreateBlockInfo(levelId)
            blockDict = comp.GetBlockNew((args['posX']+i[0],args['posY']+i[1],args['posZ']+i[2]), dimension)
            if i==(0,1,0) and blockDict["name"]=="minecraft:bedrock":
                pass
            elif blockDict["name"]=="minecraft:sandstone" and blockDict["aux"]==3:
                pass
            else:
                return
        if  not  blockEntityData["stid"]:
            blockEntityData["stid"]=True
            for k,i in enumerate([
                [(pos[0]-14,pos[1]+39,pos[2]+20),'zaibian:koboleton'],
                [(pos[0]+14,pos[1]+39,pos[2]+20),'zaibian:koboleton'],
                [(pos[0]+30,pos[1]+39,pos[2]+24),'zaibian:koboleton'],
                [(pos[0]+37,pos[1]+39,pos[2]+23),'zaibian:koboleton'],
                [(pos[0]+30,pos[1]+39,pos[2]+6),'zaibian:koboleton'],
                [(pos[0]-37,pos[1]+39,pos[2]),'zaibian:koboleton'],
                [(pos[0]+30,pos[1]+39,pos[2]-5),'zaibian:koboleton'],
                [(pos[0]+16,pos[1]+39,pos[2]-39),'zaibian:koboleton'],
                [(pos[0]+38,pos[1]+39,pos[2]-36),'zaibian:koboleton'],
                [(pos[0]+38,pos[1]+39,pos[2]-10),'zaibian:koboleton'],
                [(pos[0]-12,pos[1]+39,pos[2]+7),'zaibian:koboleton'],
                [(pos[0]-36,pos[1]+39,pos[2]+30),'zaibian:koboleton'],
                [(pos[0]-33,pos[1]+39,pos[2]-45),'zaibian:koboleton'],
                [(pos[0]-23,pos[1]+53,pos[2]-20),'zaibian:koboleton'],
                [(pos[0]-2,pos[1]+52,pos[2]-32),'zaibian:koboleton'],
                [(pos[0]-25,pos[1]+53,pos[2]-30),'zaibian:koboleton'],
                [(pos[0]+15,pos[1]+53,pos[2]-4),'zaibian:koboleton'],
                [(pos[0]+14,pos[1]+53,pos[2]+17),'zaibian:koboleton'],
                [(pos[0]+18,pos[1]+5,pos[2]+4),'zaibian:koboleton'],
                [(pos[0]-18,pos[1]+5,pos[2]-8),'zaibian:koboleton'],
                [(pos[0]+8,pos[1]+5,pos[2]-33),'zaibian:koboleton'],
                [(pos[0]-9,pos[1]+5,pos[2]-33),'zaibian:koboleton'],
                [(pos[0]-16,pos[1]+5,pos[2]-24),'zaibian:koboleton'],
                [(pos[0]-17,pos[1]+5,pos[2]-8),'zaibian:koboleton'],
                [(pos[0]-14,pos[1]+5,pos[2]+7),'zaibian:koboleton'],
                [(pos[0]-9,pos[1]+5,pos[2]+18),'zaibian:koboleton'],
                [(pos[0]+2,pos[1]+5,pos[2]+8),'zaibian:koboleton'],
                [(pos[0]+26,pos[1]+39,pos[2]-27),'zaibian:koboleton'],
                [(pos[0]+16,pos[1]+39,pos[2]-13),'zaibian:koboleton'],
                [(pos[0]+6,pos[1]+39,pos[2]+8),'zaibian:koboleton'],
                [(pos[0]-29,pos[1]+39,pos[2]+21),'zaibian:koboleton'],
                [(pos[0]-36,pos[1]+39,pos[2]+17),'zaibian:koboleton'],
                [(pos[0]-16,pos[1]+53,pos[2]-26),'zaibian:koboleton'],
                [(pos[0]+1,pos[1]+8,pos[2]+27),'zaibian:ancient_remnant',(0,-90)],

                ]): 
                if len(i)==2:
                    rot=(0,0)
                else:
                    rot=i[2]
                sc_enid(i[0],i[1],dimension,rot,k=k)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        list_=comp.GetEntitiesInSquareArea(None, (args['posX']-70,args['posY']-5,args['posZ']-70), (args['posX']+70,args['posY']+90,args['posZ']+70), dimension)
        for  i in  list_:
            if i in serverApi.GetPlayerList():
                comp = serverApi.GetEngineCompFactory().CreateAchievement(levelId)
                comp.SetNodeFinish(i, "z6", callback = None )
        