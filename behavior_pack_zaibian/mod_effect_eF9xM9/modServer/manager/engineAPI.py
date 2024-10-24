# -*- coding:utf-8 -*-

import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()
import random
levelId=serverApi.GetLevelId()

def GetAttr(id, paramName, defaultValue=None):
    '''获取属性值
    paramName:属性名称，str的名称建议以mod命名为前缀
    defaultValue:属性默认值，属性不存在时返回该默认值
    '''
    comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
    return comp.GetAttr(paramName, defaultValue)

def SetAttr(id, paramName, paramValue, needRestore=False):
    '''设置属性值
    paramName:属性名称，str的名称建议以mod命名为前缀
    paramValue:属性值，支持python基础数据
    needRestore:是否需要恢复，如果选择是，会自动存档并在实体加载时恢复，默认为False
    '''
    comp = serverApi.GetEngineCompFactory().CreateModAttr(id)
    return comp.SetAttr(paramName, paramValue, needRestore)

def SetEntityScale(entityId, scale):
    comp = serverApi.GetEngineCompFactory().CreateScale(entityId)
    return comp.SetEntityScale(entityId, scale)

def CreateExplosion(pos, radius, fire=False, breaks=True, sourceId='', playerId=''):
    '''用于生成爆炸
    radius:爆炸范围
    breaks: engineAPI.GetGameRulesInfoServer()['cheat_info']['mob_griefing']   若需要破坏方块,那还需要查询世界规则是否可破坏  
    sourceId: 爆炸伤害源的实体id
    playerId: 爆炸创造的实体id
    '''
    comp = serverApi.GetEngineCompFactory().CreateExplosion(levelId)
    return comp.CreateExplosion(pos, radius, fire, breaks, sourceId, playerId)

def randomTp(entityId):
    '''随机传送'''
    pos = get_pos(entityId)
    if not pos:
        return
    dimensionId = GetEntityDimensionId(entityId)
    num1 = random.randint(5,30)
    num2 = random.randint(5,30)
    cacheList = [(num1,num2),(-num1,num2),(num1,-num2),(-num1,-num2)]
    random.shuffle(cacheList)
    for i in cacheList:
        newPos = findCouldStandPos((pos[0]+i[0],pos[1],pos[2]+i[1]),dimensionId)
        if newPos:
            set_pos(entityId,newPos)
            return
    pass

def resetPlayerItemSlotFunc(playerId):
    '''对玩家物品栏重排序'''
    itemComp = serverApi.GetEngineCompFactory().CreateItem(playerId)   
    baseData = {}
    for i in xrange(36):
        itemDict =  itemComp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY,i, True) 
        baseData[i] = itemDict
    newList = baseData.values()
    random.shuffle(newList)
    for slot,itemDict in enumerate(newList):
        if itemDict == baseData[slot]:
            continue
        if itemDict == None:
            itemDict = {
                    "newItemName": "minecraft:air",
                    "count": 1,
                    "newAuxValue": 0,
                }
        itemComp.SpawnItemToPlayerInv(
                    itemDict, playerId, slot)
        pass
    pass

def SetModel(entityId, modelName):
    '''设置骨骼模型'''
    comp = serverApi.GetEngineCompFactory().CreateModel(entityId)
    comp.SetModel(modelName)

def SetEntityOnFire(entityId,seconds, burn_damage=1):
    '''设置实体着火'''
    comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
    comp.SetEntityOnFire(seconds, burn_damage)

def GetGameDiffculty(entityId):
    '''获取游戏难度'''
    comp = compFactory.CreateGame(entityId)
    return comp.GetGameDiffculty()

def HasEffect(entityId,effectName):
    '''获取实体是否存在当前状态效果'''
    comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
    return comp.HasEffect(effectName)

def SpawnItemToLevel(itemDict, dimensionId=0, pos=(0, 0, 0)):
    '''生成物品掉落物，如果需要获取物品的entityId，可以调用服务端系统接口CreateEngineItemEntity
    {'newItemName': itemName, 'count': count, 'newAuxValue': auxValue}
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(levelId)
    comp.SpawnItemToLevel(itemDict, dimensionId, pos)

def AddActorComponentGroup(entityId,groupName):
    """
    给指定实体添加实体json中配置的ComponentGroup
    """
    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
    return comp.AddActorComponentGroup(groupName)

def RemoveActorComponentGroup(entityId,groupName):
    """
    移除指定实体在实体json中配置的ComponentGroup
    """
    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
    return comp.RemoveActorComponentGroup(groupName)

def SetEntityTamed(playerId, tamedId):
    '''设置生物驯服，需要配合 entityEvent组件使用。该类驯服不包含骑乘功能。'''
    tameComp = serverApi.GetEngineCompFactory().CreateTame(tamedId)
    return tameComp.SetEntityTamed(playerId, tamedId)

def SetRiderRideEntity(riderId, riddenEntityId, riderIndex=-1):
    '''设置实体骑乘生物（或者船与矿车）
    riderId:骑乘生物id
    riddenEntityId:被骑乘生物id
    riderIndex:指定实体成为第n个骑乘者，范围为0~SeatCount-1，默认不指定
    '''
    comp = serverApi.GetEngineCompFactory().CreateRide(riddenEntityId)
    return comp.SetRiderRideEntity(riderId,riddenEntityId,riderIndex)
    
def CreateEngineEntityByTypeStr(server, engineTypeStr, pos, rot=(0, 0), dimensionId=0, isNpc=False):
    '''创建指定identifier的实体'''
    return server.CreateEngineEntityByTypeStr(engineTypeStr, pos, rot, dimensionId,isNpc)

def isSneaking(playerId):
    '''获取玩家是否处于潜行状态'''
    comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
    return comp.isSneaking()

def ChangePlayerItemTipsAndExtraId(playerId, posType=serverApi.GetMinecraftEnum().ItemPosType.CARRIED, slotPos=0, customTips='', extraId=''):
    '''
    修改物品栏物品的自定义数据
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    return comp.ChangePlayerItemTipsAndExtraId(posType, slotPos, customTips, extraId)

def GetItemDurability(playerId, posType=serverApi.GetMinecraftEnum().ItemPosType.CARRIED, slotPos=0):
    '''获取指定槽位的物品耐久'''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    return comp.GetItemDurability(posType, slotPos)

def SetItemDurability(playerId, durability,posType=serverApi.GetMinecraftEnum().ItemPosType.CARRIED, slotPos=0):
    '''设置物品的耐久值'''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    return comp.SetItemDurability(posType, slotPos, durability)

def SetItemMaxDurability(playerId, maxDurability,posType=serverApi.GetMinecraftEnum().ItemPosType.CARRIED, slotPos=0, isUserData=True):
    '''设置物品的最大耐久值
    isUserData:如果为True，则该设置只对指定物品生效，如果为False，则对同一类所有物品生效
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    return comp.SetItemMaxDurability(posType, slotPos, maxDurability, isUserData)

def GetItemMaxDurability(playerId,posType=serverApi.GetMinecraftEnum().ItemPosType.CARRIED,slotPos=1,isUserData=False):
    '''获取指定槽位的物品耐最大耐久(默认主手槽位物品)
    isUserData:如果为True，则只尝试获取该物品userData特殊设置的值，没有特殊设置过则返回0。如果为False，则会先尝试获取userData中的值，没有的话获取该类物品通用值。
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    return comp.GetItemMaxDurability(posType, slotPos, isUserData)

def isSwimming(playerId):
    '''是否游泳'''
    comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
    return comp.isSwimming()

def GetPlayerGameType(playerId):
    '''获取指定玩家的游戏模式'''
    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
    return comp.GetPlayerGameType(playerId)

def GetDroppedItem(itemEntityId,getUserData=False):
    '''
    获取掉落物的物品信息
        如果掉落物实体不存在，返回值为None
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(levelId)
    return comp.GetDroppedItem(itemEntityId,getUserData)

def loadingChunkFuncTwo(startPos, endPos,dimensionId,re_func,*args):
    '''异步加载指定区域区块'''
    def cache_func(data):
        code = data.get('code', 0)
        if code == 0:
            #区块加载失败
            print '------------区块加载失败!!!!!!!!!!!!'
            return
        re_func(*args)
    startPos = SetIntPosInfo(startPos)
    comp = serverApi.GetEngineCompFactory().CreateChunkSource(levelId)
    comp.DoTaskOnChunkAsync(dimensionId, (startPos[0]-16,startPos[1]-16,startPos[2]-16),(endPos[0]+16,endPos[1]+16,endPos[2]+16),cache_func)

def loadingChunkFuncOne(target_pos,dimensionId,re_func,*args):
    '''异步加载指定坐标区块'''
    def cache_func(data):
        code = data.get('code', 0)
        if code == 0:
            #区块加载失败
            print '------------区块加载失败!!!!!!!!!!!!'
            return
        re_func(*args)
    target_pos = SetIntPosInfo(target_pos)
    comp = serverApi.GetEngineCompFactory().CreateChunkSource(levelId)
    comp.DoTaskOnChunkAsync(dimensionId, (target_pos[0]-16,target_pos[1]-16,target_pos[2]-16),(target_pos[0]+16,target_pos[1]+16,target_pos[2]+16),cache_func)

def getWeightChoiceFunc(baseDict):
    '''根据权重返回目标'''
    sum_ = 0
    for val_i in baseDict.values():
        sum_ += val_i
    putnum = random.uniform(0, sum_)
    for key, value in baseDict.items():
        if value >= putnum:
            return key
        else:
            putnum -= value
        pass
    pass

def GetFaceSurfacePos(x,y,z, face):
    '''获取方块旁的坐标'''
    if face == 2:
        x, y, z = x, y, z-1
    elif face == 3:
        x, y, z = x, y, z+1
    elif face == 4:
        x, y, z = x-1, y, z
    elif face == 5:
        x, y, z = x+1, y, z
    elif face == 1:
        x, y, z = x, y+1, z
    elif face == 0:
        x, y, z = x, y-1, z

    return x, y, z

def GetBlockEntityData(pos, dimension):
    '''用于获取可操作某个自定义方块实体数据的对象，操作方式与dict类似'''
    blockEntitycomp = serverApi.GetEngineCompFactory().CreateBlockEntityData(levelId)
    # GetBlockEntityData在某些情况下会返回None，对返回结果进行操作前务必先判断它是否为空
    return blockEntitycomp.GetBlockEntityData(dimension, pos)

def getEntityRot(entityId):
    '''获取实体角度'''
    rot = serverApi.GetEngineCompFactory().CreateRot(entityId).GetRot()
    # 根据不同角度返回不同的数字用于判断
    if 135.0 < rot[1] <= 180.0:
        return 2
    elif 90.0 < rot[1] <= 135.0:
        return 1
    elif 45.0 < rot[1] <= 90.0:
        return 1
    elif 0.0 < rot[1] <= 45.0:
        return 0
    elif -45.0 < rot[1] <= 0.0:
        return 0
    elif -90.0 < rot[1] <= -45.0:
        return 3
    elif -135.0 < rot[1] <= -90.0:
        return 3
    elif -180.0 < rot[1] <= -135.0:
        return 2
    else:
        return 0

def ConsumeCurrentSlotItem(playerId,num=1):
    '''消耗当前选中槽位物品'''
    slotNum = GetSelectSlotId(playerId)
    itemDict = GetPlayerItem(playerId)
    if itemDict and itemDict['count'] >= num:
        SetInvItemNum(playerId,slotNum,itemDict['count']-num)
        return True
    return False

def CreateProjectileEntityOne(entityId, direction, arrowName="minecraft:snowball"):
    '''发射抛射物 测试使用'''
    x,y,z = get_pos(entityId)
    comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
    param = {
        'direction': direction,
        "position":(x,y+2,z)
    }
    return comp.CreateProjectileEntity(entityId, arrowName, param)

def CreateProjectileEntity(spawnerId, entityIdentifier, param=None):
    '''发射抛射物
    param = {
        'direction': direction,
        "position":(x,y,z)
    }
    '''
    comp = serverApi.GetEngineCompFactory().CreateProjectile(levelId)
    return comp.CreateProjectileEntity(spawnerId, entityIdentifier, param)

def SetMoveSetting(entityId,pos,myCallback = None,speed = 1.0):
    '''寻路组件'''
    if not myCallback:
        def funcOne(entityId0, result):
            pass
        myCallback = funcOne
    comp = serverApi.GetEngineCompFactory().CreateMoveTo(entityId)
    comp.SetMoveSetting(pos,speed,200,myCallback)

def posAddFunc(pos0, pos1):
    '''二个坐标相加(兼容多维)'''
    data = []
    for index,val in enumerate(pos0):
        data.append(val+pos1[index])
    return tuple(data)

def posReduceFunc(pos0, pos1):
    '''二个坐标相减(兼容多维)'''
    data = []
    for index,val in enumerate(pos0):
        data.append(val-pos1[index])
    return tuple(data)

def posMultFunc(pos, num):
    '''坐标乘除(兼容多维)'''
    data = []
    for i in pos:
        data.append(i*num)
    return tuple(data)

def SpawnItemToPlayerInvTwo(playerId, itemName, count=1,auxValue=0, slotPos=-1):
    '''不指定槽位给物品'''
    itemDict = {'newItemName': itemName, 'count': count, 'newAuxValue': auxValue}
    comp = compFactory.CreateItem(playerId)
    comp.SpawnItemToPlayerInv(itemDict, playerId, slotPos)
    pass

def SpawnItemToPlayerInv(playerId, itemDict, slotPos=-1):
    '''生成物品到玩家背包'''
    comp = compFactory.CreateItem(playerId)
    return comp.SpawnItemToPlayerInv(itemDict, playerId, slotPos)

def DeleteAllArea():
    '''删除所有常加载区域'''
    comp = serverApi.GetEngineCompFactory().CreateChunkSource(levelId)
    comp.DeleteAllArea()

def DeleteArea(key):
    '''删除一个常加载区域'''
    comp = serverApi.GetEngineCompFactory().CreateChunkSource(levelId)
    comp.DeleteArea(key)

def SetAddArea(key,dimensionId,minPos,maxPos):
    '''设置区块的常加载'''
    comp = serverApi.GetEngineCompFactory().CreateChunkSource(levelId)
    comp.SetAddArea(key,dimensionId,minPos,maxPos)

def SetGameRulesInfoServer(ruleDict):
    '''设置游戏规则。所有参数均可选
    gameRuleDict ={
    'option_info': {
        'pvp': bool, #玩家伤害
        'show_coordinates': bool, #显示坐标
        'fire_spreads': bool, #火焰蔓延
        'tnt_explodes': bool, #tnt爆炸
        'mob_loot': bool, #生物战利品
        'natural_regeneration': bool, #自然生命恢复
        'tile_drops': bool, #方块掉落
        'immediate_respawn':bool #立即重生
        },
    'cheat_info': {
        'enable': bool, #是否开启作弊
        'always_day': bool, #终为白日
        'mob_griefing': bool, #生物破坏方块
        'keep_inventory': bool, #保留物品栏
        'weather_cycle': bool, #天气更替
        'mob_spawn': bool, #生物生成
        'entities_drop_loot': bool, #实体掉落
        'daylight_cycle': bool, #开启昼夜交替
        'command_blocks_enabled': bool, #启用方块命令
        'random_tick_speed': int,#随机方块tick速度
        }
    }
    '''
    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
    return comp.SetGameRulesInfoServer(ruleDict)

def GetGameRulesInfoServer():
    '''获取游戏规则'''
    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
    return comp.GetGameRulesInfoServer()

def SetIntPosInfo(pos):
    '''返回整型坐标'''
    return (int(pos[0]),int(pos[1]),int(pos[2]))

def GetDistanceBetweenTwoPos(pos0, pos1):
    '''获得两个位置之间的距离'''
    return ((pos0[0]-pos1[0])**2+(pos0[1]-pos1[1])**2+(pos0[2]-pos1[2])**2)**0.5

def SetPersistent(entityId,persistent=True):
    '''设置实体不会因为离玩家太远而被清除'''
    comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
    comp.SetPersistent(persistent)

def GetInventoryItemNameList(playerId):
    '''获取背包里的物品名称列表'''
    _list = []
    itemComp = serverApi.GetEngineCompFactory().CreateItem(playerId)   
    for i in xrange(36):
        itemDict =  itemComp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY,i, True) 
        if itemDict:
            _list.append(itemDict['newItemName'])
    return _list

def GetItemBasicInfo(itemname,itemAux=0):
    '''获取物品的基础信息'''
    comp = serverApi.GetEngineCompFactory().CreateItem(levelId)
    return comp.GetItemBasicInfo(itemname,itemAux)

def SetEntityLookAtPos(entityId,targetPos,minTime,maxTime,reject=True):
    '''设置非玩家的实体看向某个位置
    reject:在进行凝视行为时,是否禁止触发其他行为
    '''
    comp = serverApi.GetEngineCompFactory().CreateRot(entityId)
    return comp.SetEntityLookAtPos(targetPos, minTime, maxTime, reject)

def SetEntityOwner(entityId,ownerId):
    '''设置实体的属主'''
    comp = serverApi.GetEngineCompFactory().CreateActorOwner(entityId)
    return comp.SetEntityOwner(ownerId)

def AddEntityVelocityMotion(entityId,velocity,accelerate=None,useVelocityDir=True):
    '''给实体（不含玩家）添加速度运动器
    velocity:速度,包含大小、方向
    accelerate:加速度,包含大小、方向,默认为None,表示没有加速度
    useVelocityDir:是否使用当前速度的方向作为此刻实体的朝向,默认为True
    '''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.AddEntityVelocityMotion(velocity, accelerate, useVelocityDir=True)

def AddEntityTrackMotion(entityId,targetPos,duraTime,startPos=None,relativeCoord=False,isLoop=False):
    '''给实体（不含玩家）添加轨迹运动器
    startPos:轨迹起点,默认为None,表示以自身位置作为起点。
    relativeCoord:是否使用相对坐标设置起点和终点,默认为False。
    isLoop:是否循环,若设为True,则实体会在起点和终点之间往复运动。
    '''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.AddEntityTrackMotion(targetPos, duraTime, startPos, relativeCoord, isLoop)

def AddEntityAroundPointMotion(entityId,center,angularVelocity,axis=(0,1,0),lockDir=False,stopRad=0):
    '''给实体（不含玩家）添加对点环绕运动器'''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.AddEntityAroundPointMotion(center, angularVelocity, axis, lockDir=False, stopRad=0)

def AddEntityAroundEntityMotion(entityId,eID,angularVelocity,axis=(0,1,0),lockDir=False,stopRad=0,radius=-1):
    '''给实体（不含玩家）添加对实体环绕运动器'''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.AddEntityAroundEntityMotion(eID, angularVelocity, axis, lockDir, stopRad, radius)

def StopEntityMotion(entityId,mID):
    '''停止实体（不含玩家）身上的某个运动器'''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.StopEntityMotion(mID)

def StartEntityMotion(entityId,mID):
    '''启动实体（不含玩家）身上的某个运动器'''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.StartEntityMotion(mID)

def RemoveEntityMotion(entityId,mID):
    '''移除实体（不含玩家）身上的运动器'''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.RemoveEntityMotion(mID)

def GetEntityMotions(entityId):
    '''获取实体（不含玩家）身上的所有运动器'''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.GetEntityMotions()

def CanSee(entityId,targetId,viewRange=8,onlySolid=True,angleX=180.0,angleY=180.0):
    '''判断起始对象是否可看见目标对象,基于对象的Head位置判断'''
    comp = serverApi.GetEngineCompFactory().CreateGame(entityId)
    return comp.CanSee(entityId,targetId,viewRange,onlySolid,angleX,angleY)

def PlaceStructure(pos,structureName,dimensionId,rotation=0):
    '''放置结构体'''
    comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
    # comp.PlaceStructure(None, (100, 70, 100), "test:structureName", 0, 0)
    return comp.PlaceStructure(None, pos, structureName, dimensionId, rotation)

def get_dir(playerId):
    '''获取实体朝向向量'''
    rotComp = serverApi.GetEngineCompFactory().CreateRot(playerId)
    rot = rotComp.GetRot()
    return serverApi.GetDirFromRot(rot)

def ChangeEntityDimension(entityId,place,dimensionId):
    '''传送实体(包括维度)'''
    comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
    return comp.ChangeEntityDimension(dimensionId, place)

def GetEntityOwner(entityId):
    '''获取实体的属主'''
    comp = serverApi.GetEngineCompFactory().CreateActorOwner(entityId)
    return comp.GetEntityOwner()

def GetAllEffects(entityId):
    '''获取实体当前所有状态效果'''
    comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
    return comp.GetAllEffects()

def ResetAttackTarget(entityId):
    '''清除仇恨目标'''
    comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
    return comp.ResetAttackTarget()

def SetAttackTarget(entityId,targetId):
    '''设置仇恨目标'''
    comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
    return comp.SetAttackTarget(targetId)
    
def GetAttackTarget(entityId):
    '''获取仇恨目标'''
    comp = serverApi.GetEngineCompFactory().CreateAction(entityId)
    return comp.GetAttackTarget()

def correct_position(pos):
    """矫正坐标位置"""
    x11, y11, z11 = int(pos[0]),int(pos[1]),int(pos[2])
    z02 ,x02=0.0,0.0
    if x11 < 0:
        x02 = -1.0
    if z11 < 0:
        z02 = -1.0
    return x11+x02, y11, z11 + z02

def GetSelectSlotId(playerId):
    '''
    获取玩家当前选中槽位
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    return comp.GetSelectSlotId()

def TriggerCustomEvent(entityId,eventName):
    '''
    触发实体自定义事件
    '''
    comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entityId)
    comp.TriggerCustomEvent(entityId,eventName)

def GetSize(entityId):
    """
    获取实体碰撞盒大小
    """
    comp = serverApi.GetEngineCompFactory().CreateCollisionBox(entityId)
    return comp.GetSize()

def GetEntitiesAround(entityId, radius, filters={}):
    """
    获取区域内的某类型的entity列表

    filters = {
                    "any_of": [
                        {
                            "subject" : "other",
                            "test" :  "is_family",
                            "value" :  "player"
                        },
                        {
                            "test" :  "has_equipment",
                            "domain": "head",
                            "subject" : "other",
                            "operator" : "not",
                            "value" : "carved_pumpkin"
                        },
                        {
                            "subject" : "other",
                            "test" :  "has_component",
                            "value" :  "minecraft:type_family"
                        }
                    ]
                }
    """
    comp = serverApi.GetEngineCompFactory().CreateGame(entityId)
    return comp.GetEntitiesAround(entityId, radius, filters) 

def get_entity_distance(entityId1, entityId2):
    '''
    获取两个实体之间的距离
    '''
    pos1 = get_foot_pos(entityId1)
    pos2 = get_foot_pos(entityId2)
    return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2+(pos1[2]-pos2[2])**2)**0.5

def get_entity_name(entityId):
    '''
    获取实体类型名称
    '''
    comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
    return comp.GetEngineTypeStr()

def change_PlayerItemTipsAndExtraId(playerId,slot,key,value):
    '''
    修改物品栏物品的自定义数据
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    comp.ChangePlayerItemTipsAndExtraId(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, slot, str(key), str(value))
    pass

def SetExtraData(id,key,value):
    '''
    设置自定义数据
    '''
    levelcomp = serverApi.GetEngineCompFactory().CreateExtraData(id)
    return levelcomp.SetExtraData(key,value)

def GetExtraData(id,key):
    '''
    查询自定义数据
    '''
    comp = serverApi.GetEngineCompFactory().CreateExtraData(id)
    return comp.GetExtraData(key)

def GetTypeFamily(entityId):
    '''
    获取生物行为包字段 type_family
    entityId:实体ID
    '''
    comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
    return comp.GetTypeFamily()
   

def get_unit_vector(args, mult = 1):
    '''
    返回固定大小值的方向向量 (单位向量)
    args:(x,z)或者(x,y,z). 传入两个值或三个值
    mult:最后返回的向量的大小,默认为1
    '''
    if len(args) == 2:
        rx,rz = args
        rx *= 1.0
        if rz == 0:
            rz = 0.01
        if rx == 0:
            rx = 0.01
        Rz = ((rz**2)/(rx**2+rz**2))**0.5
        Rz = Rz * mult
        Rx = Rz*(rx/rz)

        if rz < 0 and Rz > 0:
            Rz = Rz*-1
        elif rz > 0 and Rz < 0:
            Rz = Rz*-1
        if rx < 0 and Rx > 0:
            Rx = Rx*-1
        elif rx > 0 and Rx < 0:
            Rx = Rx*-1
        return (Rx,Rz)
    elif len(args) == 3:
        rx,ry,rz = args
        rx *= 1.0
        if ry == 0:
            ry = 0.01
        Ry = ((ry**2)/(rx**2+ry**2+rz**2))**0.5
        Ry = Ry * mult
        Rx = (rx*Ry)/ry
        Rz = (rz*Ry)/ry

        if rz < 0 and Rz > 0:
            Rz = Rz*-1
        elif rz > 0 and Rz < 0:
            Rz = Rz*-1
        if rx < 0 and Rx > 0:
            Rx = Rx*-1
        elif rx > 0 and Rx < 0:
            Rx = Rx*-1
        if ry < 0 and Ry > 0:
            Ry = Ry*-1
        elif ry > 0 and Ry < 0:
            Ry = Ry*-1
        return (Rx, Ry, Rz)
    
def findCouldStandPos(place,dimension):
    '''寻找可站立坐标
    
    prohibitblock = ["minecraft:air", "minecraft:snow_layer"] #如果是火焰就不能在水里
    '''
    x1,y1,z1 = place

    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
    prohibitblock = ["minecraft:air", "minecraft:snow_layer","minecraft:water","minecraft:flowing_water"]

    blockDict_down = comp.GetBlockNew((x1, y1, z1), dimension)
    blockDict_up = comp.GetBlockNew((x1, y1+1, z1), dimension)
    # 寻找能用来站立的方块高度
    if blockDict_down['name'] in prohibitblock or blockDict_up['name'] not in prohibitblock:
        sign = 0
        for n1 in xrange(10):
            blockDict = comp.GetBlockNew((x1, y1+n1, z1), dimension)
            blockDict1 = comp.GetBlockNew((x1, y1-n1, z1), dimension)
            if blockDict['name'] not in prohibitblock:
                blockDict_up = comp.GetBlockNew((x1, y1+n1+1, z1), dimension)
                if blockDict_up['name'] in prohibitblock:
                    y1 = y1+n1
                    sign = 1
                    break
            elif blockDict1['name'] not in prohibitblock:
                blockDict_up = comp.GetBlockNew((x1, y1-n1+1, z1), dimension)
                if blockDict_up['name'] in prohibitblock:
                    y1 = y1-n1
                    sign = 1
                    break
        if sign == 0:
            return None
    return (x1, y1+1, z1)




def spawn_flame(place,dimension,radius,flame_num):
    '''
    生成火焰
    place:坐标(x,y,z)
    dimension:维度
    radius:生成半径
    flame_num:生成火焰的数量
    return:生成了火焰的坐标列表
    '''
    x,y,z = place
    blockDict00 = {
        'name': "minecraft:fire",
        'aux': 0
    }
    pos_list = []
    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
    prohibitblock = ["minecraft:air", "minecraft:snow_layer"]
    for i in xrange(flame_num):
        x1 = x + random.uniform(-radius,radius)
        y1 = y
        z1 = z + random.uniform(-radius,radius)
        blockDict_down = comp.GetBlockNew((x1, y1, z1), dimension)
        blockDict_up = comp.GetBlockNew((x1, y1+1, z1), dimension)
        # 寻找能用来站立的方块高度
        if blockDict_down['name'] in prohibitblock or blockDict_up['name'] not in prohibitblock:
            sign = 0
            for n1 in xrange(10):
                blockDict = comp.GetBlockNew((x1, y1+n1, z1), dimension)
                blockDict1 = comp.GetBlockNew((x1, y1-n1, z1), dimension)
                if blockDict['name'] not in prohibitblock:
                    blockDict_up = comp.GetBlockNew((x1, y1+n1+1, z1), dimension)
                    if blockDict_up['name'] in prohibitblock:
                        y1 = y1+n1
                        sign = 1
                        break
                elif blockDict1['name'] not in prohibitblock:
                    blockDict_up = comp.GetBlockNew((x1, y1-n1+1, z1), dimension)
                    if blockDict_up['name'] in prohibitblock:
                        y1 = y1-n1
                        sign = 1
                        break
            if sign == 0:
                continue
        comp.SetBlockNew((x1, y1+1, z1), blockDict00, 0, dimension)
        pos_list.append((x1, y1+1, z1))
    
    return pos_list


def SetMotion(entityId, motion):
    '''
    设置生物（含玩家）的瞬时移动方向向量
    '''
    if entityId not in serverApi.GetPlayerList():
        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
        return motionComp.SetMotion(motion)
    else:
        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
        return motionComp.SetPlayerMotion(motion)

def GetMotion(entityId):
    '''
    获取生物（含玩家）的瞬时移动方向向量
    '''
    motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.GetMotion()

def probability_trigger(num):
    '''
    输入一个0~100的概率数字,会根据概率值,返回是否触发这次事件
    '''
    luck_num = random.uniform(0,100)
    if luck_num <= num:
        return True
    else:
        return False

def AddEffectToEntity(entityId,effectName,duration,amplifier,showParticles=False):
    """
    添加状态
    effectName:状态效果名称字符串，包括自定义状态效果和原版状态效果，原版状态效果可在wiki查询
    duration:状态效果持续时间，单位秒(int)
    amplifier:状态效果的额外等级。必须在0至255之间（含）。若未指定，默认为0。注意，状态效果的第一级（如生命恢复 I）对应为0，因此第二级状态效果，如生命回复 II，应指定强度为1。部分效果及自定义状态效果没有强度之分，如夜视
    showParticles:是否显示粒子效果，True显示，False不显示
    """
    comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
    return comp.AddEffectToEntity(effectName,duration,amplifier,showParticles)

def RemoveEffectFromEntity(entityId,effectName):
    '''为实体删除指定状态效果'''
    comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
    return comp.RemoveEffectFromEntity(effectName)

def ConsumePlayerBagItem(playerId, itemName, need_num):
    """
    消耗玩家背包中某个物品的某个数量, 若不足则不消耗直接返回false. 消耗成功返回true
    playerId:玩家ID
    itemName:物品名称
    need_num:需要消耗的数量
    """
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    sum_num = 0
    info_list = []
    for i in xrange(0, 36):
        data = comp.GetPlayerItem(
            serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, i)
        if data and data['itemName'] == itemName:
            sum_num += data['count']
            if sum_num >= need_num:
                info_list.append([data['count'],i])
                break
    
    if sum_num >= need_num:
        comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        for count,slot in info_list:
            if count >= need_num:
                comp.SetInvItemNum(slot, count-need_num)
            else:
                comp.SetInvItemNum(slot, 0)
                need_num -= count
        return True
    else:
        return False

def getPlayerBagItemNum(playerId, itemName):
    """
    获得玩家背包中某个物品的数量
    playerId:玩家ID
    itemName:物品名称
    """
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    sum_num = 0

    for i in xrange(0, 36):
        data = comp.GetPlayerItem(
            serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, i)
        if data and data['itemName'] == itemName:
            sum_num += data['count']
    return sum_num
    


def consumption_durability(playerId, need_durability, trench=-1): #指定槽位消耗指定耐久
    '''
    对物品栏的物品进行耐久消耗
    playerId:玩家ID
    need_durability:需要消耗的耐久,输入负数可以增加耐久
    trench:默认为当前选中槽位,可输入槽位值,对指定槽位消耗耐久
    '''
    comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
    if trench == -1:
        trench = comp.GetSelectSlotId()
    have_durability = comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, trench)
    if (have_durability-need_durability) > 0: #若还剩有耐久
        comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, trench, have_durability-need_durability)
    else:#耐久消耗完
        comp.SetInvItemNum(trench, 0) #删除该物品
    pass

def get_level_id():
    return serverApi.GetLevelId()

def get_namespace():
    return serverApi.GetEngineNamespace()

def get_system_name():
    return serverApi.GetEngineSystemName()

def NotifyOneMessage(playerId, msg, color='\xc2\xa7f'):
    '''
    向指定玩家发送信息
    '''
    comp = serverApi.GetEngineCompFactory().CreateMsg(playerId)
    comp.NotifyOneMessage(playerId, msg, color)

def get_player_list():
    """
    获取level中所有玩家的id列表
    :return: list 返回玩家id列表
    """
    return serverApi.GetPlayerList()


def get_pos(entityId):
    """
    返回实体位置
    :param str entityId: 实体id
    :rtype: tuple
    :return: 实体位置
    """
    comp = compFactory.CreatePos(entityId)
    return comp.GetPos()


def get_foot_pos(entityId):
    comp = compFactory.CreatePos(entityId)
    return comp.GetFootPos()


def GetRot(entity_id):
    """
    返回实体角度
    """
    comp = compFactory.CreateRot(entity_id)
    return comp.GetRot()


def set_rot(entity_id, rot):
    """
    设置实体角度
    """
    comp = compFactory.CreateRot(entity_id)
    return comp.SetRot(rot)


def GetDirFromRot(rot):
    return serverApi.GetDirFromRot(rot)


def get_player_all_items(pid):
    """
    获取玩家的批量物品信息
    """
    comp = compFactory.CreateItem(pid)
    return comp.GetPlayerAllItems(
        serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)


def SetInvItemNum(playerId, slotNum, num):
    """
    设置玩家背包物品数目
    :param pid: 玩家id
    :param slot: 物品栏槽位(从0开始)
    :param num: 物品数目,可以通过设置数量为0来达到清除背包物品的效果
    :return:
    """
    comp = compFactory.CreateItem(playerId)
    return comp.SetInvItemNum(slotNum, num)


def set_block_new(pos, blockDict, oldBlockHandling=0, dimensionId=0):
    """
    设置某一位置的方块
    :param pos: 位置坐标(x,y,z)
    :param blockDict: 方块字典信息
        {
            'name': 'minecraft:wool',
            'aux': 0
        }
    :param oldBlockHandling: 0：替换,1：销毁,2：保留,默认为0
    :param dimensionId: 维度id
    :return: bool 设置结果
    """
    comp = compFactory.CreateBlockInfo(dimensionId)
    return comp.SetBlockNew(pos, blockDict, oldBlockHandling, dimensionId)


def set_attr(entityId, attrType, val):
    comp = compFactory.CreateAttr(entityId)
    return comp.SetAttrValue(attrType, val)


def get_attr(entityId, attrType):
    comp = compFactory.CreateAttr(entityId)
    return comp.GetAttrValue(attrType)

def get_mattr(entityId, attrType):
    comp = compFactory.CreateAttr(entityId)
    return comp.GetAttrMaxValue(attrType)

def KillEntity(entityId):
    '''杀死某个Entity'''
    comp = compFactory.CreateGame(levelId)
    return comp.KillEntity(entityId)


def get_attr_types():
    return serverApi.GetMinecraftEnum().AttrType


def SetGravity(entityId, gravity):
    comp = compFactory.CreateGravity(entityId)
    return comp.SetGravity(gravity)


def GetGravity(entityId):
    comp = compFactory.CreateGravity(entityId)
    return comp.GetGravity()


def SetAttrMaxValue(entityId, attrType, val):
    comp = compFactory.CreateAttr(entityId)
    comp.SetAttrMaxValue(attrType, val)


def SetCommand(cmdStr, playerId=None, showOutput=False):
    """
    使用游戏内指令
    cmdStr:指令
    playerId:玩家id:可选，如果playerId不设置，则随机选择玩家
    showOutput:	是否输出到聊天窗口：可选，默认False，
    """
    comp = compFactory.CreateCommand(levelId)
    return comp.SetCommand(cmdStr, playerId, showOutput)


def set_pos(entity_id, pos):
    """
    设置实体位置
    :param str entity_id:
    :param tuple pos:
    :rtype: bool
    :return: 设置结果
    # """
    comp = compFactory.CreatePos(entity_id)
    return comp.SetPos(pos)


def get_entities_around(entityId, radius, except_entity=False):
    """
获取区域内的entity列表
"""
    comp = compFactory.CreateGame(entityId)
    filters = {"any_of": [
        {
            "subject": "other",
            "test": "is_family",
                    "value": "enemy"
        },
        {
            "subject": "other",
            "test": "is_family",
                    "value": "mob"
        },
        {
            "subject": "other",
            "test": "is_family",
                    "value": "player"
        },
    ]}
    entity_ids = comp.GetEntitiesAround(entityId, radius, filters)
    if except_entity:
        if entityId in entity_ids:
            entity_ids.remove(entityId)
    return entity_ids


def GetEntitiesInSquareAreaOne(startPos, endPos, dimensionId):
    '''获取范围内所有 有家族的实体'''
    comp = compFactory.CreateGame(get_level_id())
    list_=comp.GetEntitiesInSquareArea(None, startPos, endPos, dimensionId)
    list_1=list(list_)
    for i in list_:
        comp = serverApi.GetEngineCompFactory().CreateAttr(i)
        if not comp.GetTypeFamily():
            list_1.remove(i)
            
    return list_1

def GetEntitiesInSquareAreaTwo(startPos, endPos, dimensionId):
    '''获取范围内所有实体'''
    comp = compFactory.CreateGame(get_level_id())
    list_=comp.GetEntitiesInSquareArea(None, startPos, endPos, dimensionId)
    
    return list_



def GetEntityDimensionId(entityId):
    '''
    获取实体所在维度
    '''
    comp = serverApi.GetEngineCompFactory().CreateDimension(entityId)
    return comp.GetEntityDimensionId()

def Hurt(targetId, damage, attackerId=None,cause=serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, childAtkId=None, knocked=True):
    '''设置伤害
    targetId:伤害目标
    attackerId:伤害来源的实体id,默认为None
    cause:伤害类型
    knocked:实体是否被击退
    childAtkId:伤害来源的子实体ID(比如抛射物ID)
    '''
    comp = serverApi.GetEngineCompFactory().CreateHurt(targetId)
    return comp.Hurt(damage, cause, attackerId, childAtkId, knocked)

def GetPlayerItem(playerId, posType=serverApi.GetMinecraftEnum().ItemPosType.CARRIED, slotPos=0, getUserData=False):
    '''
    获取指定槽位物品信息
    posType:物品位置类型
    '''
    comp = compFactory.CreateItem(playerId)
    return comp.GetPlayerItem(posType, slotPos, getUserData)


def get_item_pos_type():
    '''物品位置类型'''
    return serverApi.GetMinecraftEnum().ItemPosType


def set_entity_max_health_value(entityId, maxv):
    """
    设置生命最大值
    :param entityId:
    :param maxv:
    :return:
    """
    comp = compFactory.CreateAttr(entityId)
    return comp.SetAttrMaxValue(
        serverApi.GetMinecraftEnum().AttrType.HEALTH, maxv)


def SetBlockControlAi(entityId, isBlock, freezeAnim=False):
    '''
    设置屏蔽生物原生AI
    isBlock:是否保留AI，False为屏蔽
    freezeAnim:屏蔽AI时是否冻结动作，默认为False，仅当isBlock为False时生效。重进世界会恢复成初始动作
    (效果存档)
    '''
    comp = compFactory.CreateControlAi(entityId)
    return comp.SetBlockControlAi(isBlock, freezeAnim)


def may_place(identifier, blockPos, facing, dimensionId=0):
    '''
    判断方块是否可以放置
    :param identifier: 方块标识类型
    :param blockPos: 待放置的坐标
    :param facing: 朝向
    :param dimensionId: 维度id
    :return:
    '''
    comp = compFactory.CreateBlockInfo(dimensionId)
    return comp.MayPlace(identifier, blockPos, facing, dimensionId)


def get_block_new(pos, dimensionId=0):
    '''
    获取某一位置的block
    :param pos:
    :param dimensionId:
    :return:
    '''
    comp = compFactory.CreateBlockInfo(dimensionId)
    return comp.GetBlockNew(pos, dimensionId)


def GetTopBlockHeightAdd1(pos, dimensionId=0):
    '''
    获取当前维度某一位置最高的非空气方块的高度+1
    :param pos: (x,z)
    :return: int 高度
    '''
    comp = compFactory.CreateBlockInfo(dimensionId)
    height = comp.GetTopBlockHeight(pos)
    if height is None:
        height = 0
    return height + 1

def GetTopBlockHeight(pos, dimensionId=0):
    comp = compFactory.CreateBlockInfo(dimensionId)
    height = comp.GetTopBlockHeight(pos)


def set_player_movalbe(pid, isMovable):
    '''
    设置玩家是否可移动
    :param pid:
    :param isMovable:
    :return:
    '''
    comp = compFactory.CreatePlayer(pid)
    return comp.SetPlayerMovable(isMovable)


def add_timer(delay, func, *args):
    '''
    delay:时间
    func:函数
    args(可选):参数
    '''
    comp = compFactory.CreateGame(get_level_id())
    return comp.AddTimer(delay, func, *args)


def listen_on_block_remove_event(block_id, isListen):
    comp = compFactory.CreateBlockInfo(get_level_id())
    comp.ListenOnBlockRemoveEvent(block_id, isListen)



def set_actor_pushable(eid, is_pushable):
    '''
    设置实体不可推动
    '''
    comp = compFactory.CreateActorPushable(eid)
    return comp.SetActorPushable(is_pushable)

def ImmuneDamage(entityId, immune=True):
    '''
    设置实体是否免疫伤害（该属性存档）
    '''
    comp = compFactory.CreateHurt(entityId)
    return comp.ImmuneDamage(immune)


def set_player_max_exhaustion_value(pid, foodExhaustionLevel):
    '''
    设置玩家的最大消耗度
    '''
    comp = compFactory.CreatePlayer(pid)
    comp.SetPlayerMaxExhaustionValue(foodExhaustionLevel)


def tp_player(playerId, dimesion, pos):
    '''
    传送玩家到指定维度和位置
    '''
    comp = serverApi.GetEngineCompFactory().CreateDimension(playerId)
    comp.ChangePlayerDimension(dimesion, pos)
