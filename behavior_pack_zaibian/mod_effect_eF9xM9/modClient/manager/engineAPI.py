# -*- coding:utf-8 -*-
import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
playerId = clientApi.GetLocalPlayerId()

def PlayCustomMusic(name, pos=(0, 0, 0), volume=1, pitch=1, loop=False, entityId=None):
    '''播放场景音效，包括原版音效及自定义音效
    volume:音量倍率，范围0-1
    pitch:播放速度，范围0-256，1表示原速
    '''
    comp = clientApi.GetEngineCompFactory().CreateCustomAudio(levelId)
    return comp.PlayCustomMusic(name, pos, volume, pitch, loop, entityId)


def GetInputVector():
    '''获取方向键（移动轮盘）的输入
    :返回一个单位向量，向量第一项为向左的大小，第二项为向前的大小'''
    comp = clientApi.GetEngineCompFactory().CreateActorMotion(playerId)
    return comp.GetInputVector()


def get_unit_vector(args, mult = 1):
    '''
    返回固定大小值的方向向量 (单位向量)
    args:(x,z)或者(x,y,z). 传入两个值或三个值
    mult:最后返回的向量的大小,默认为1
    '''
    if len(args) == 2:
        rx,rz = args
        if rx == rz == 0:
            return args
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
        if rx == ry == rz == 0:
            return args
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
    

def GetDirFromRot(rot):
    '''通过旋转角度获取朝向
    rot = engineAPI.GetRot(entityId)
    '''
    return clientApi.GetDirFromRot(rot)

def SetText(uiNode,path,text):
    '''设置Label的文本信息'''
    return uiNode.GetBaseUIControl(path).asLabel().SetText(text)

def getVariable(entityId,variableName):
    '''获取某一个实体计算节点的值，如果不存在返回注册时的默认值'''
    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(entityId)
    return comp.Get(variableName)

def setVariable(entityId,variableName, defalutValue):
    '''设置某一个实体计算节点的值'''
    return compFactory.CreateQueryVariable(entityId).Set(variableName,defalutValue)

def SetMotion(motion):
    '''设置瞬时的移动方向向量，用于本地玩家'''
    motionComp = clientApi.GetEngineCompFactory().CreateActorMotion(playerId)
    return motionComp.SetMotion(motion)

def animatCFunc1(cacheList):
    '''手持物品放大 列表转成字符串'''
    #注意:武器名中的大写需改成小写
    cacheStr = "(query.get_equipped_item_full_name('main_hand') == '{}')".format(cacheList[0])
    for i in cacheList[1:]:
        cacheStr += "||(query.get_equipped_item_full_name('main_hand') == '{}')".format(i)
        pass
    return str(cacheStr)

def Swing():
    '''本地玩家播放原版攻击动作'''
    comp = clientApi.GetEngineCompFactory().CreatePlayer(levelId)
    return comp.Swing()

def GetMotion(entityId):
    '''获取生物的瞬时移动方向向量。与服务端不同，客户端不会计算摩擦等因素，获取到的是上一帧的向量，与服务器获取到的值会不相等'''
    motionComp = clientApi.GetEngineCompFactory().CreateActorMotion(entityId)
    return motionComp.GetMotion()

def GetAllEffects(entityId):
    '''获取实体当前所有状态效果'''
    comp = clientApi.GetEngineCompFactory().CreateEffect(entityId)
    return comp.GetAllEffects()

def GetOwnerId(entityId):
    '''获取驯服生物的主人id'''
    comp = clientApi.GetEngineCompFactory().CreateTame(entityId)
    return comp.GetOwnerId()

def HasEffect(entityId, effectName):
    '''获取实体是否存在当前状态效果'''
    comp = clientApi.GetEngineCompFactory().CreateEffect(entityId)
    return comp.HasEffect(effectName)

def GetAttackTarget(entityId):
    '''获取仇恨目标'''
    comp = clientApi.GetEngineCompFactory().CreateAction(entityId)
    return comp.GetAttackTarget()

def GetChosenEntity():
    '''获取屏幕点击位置的实体id'''
    comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
    return comp.GetChosenEntity()

def GetEngineTypeStr(entityId):
    '''获取实体的类型名称'''
    comp = clientApi.GetEngineCompFactory().CreateEngineType(entityId)
    return comp.GetEngineTypeStr()

def isSwimming(entityId):
    '''是否游泳'''
    comp = clientApi.GetEngineCompFactory().CreatePlayer(entityId)
    return comp.isSwimming()

def SetSpeedFovLock(isLocked=True):
    '''是否锁定相机视野fov，锁定后不随速度变化而变化'''
    comp = clientApi.GetEngineCompFactory().CreateCamera(levelId)
    return comp.SetSpeedFovLock(isLocked)

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

def GetPlayerGameType():
    '''获取指定玩家的游戏模式'''
    comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
    return comp.GetPlayerGameType(playerId)

def GetFov():
    '''获取视野大小'''
    return compFactory.CreateCamera(levelId).GetFov()

def SetFov(fov):
    '''设置视野大小'''
    return compFactory.CreateCamera(levelId).SetFov(fov)

def SetLeftCornerNotify(message):
    '''客户端设置左上角通知信息'''
    comp = clientApi.GetEngineCompFactory().CreateTextNotifyClient(levelId)
    return comp.SetLeftCornerNotify(message)

def getEntityRot(entityId):
    '''获取实体角度'''
    rot = clientApi.GetEngineCompFactory().CreateRot(entityId).GetRot()
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

def GetPlayerItem(val=clientApi.GetMinecraftEnum().ItemPosType.CARRIED,slotPos=0,getUserData=False):
    '''获取玩家物品
    默认主手物品
    '''
    comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
    return comp.GetPlayerItem(val, slotPos, getUserData)

def GetBlock(pos):
    '''获取某一位置的block'''
    comp = clientApi.GetEngineCompFactory().CreateBlockInfo(levelId)
    return comp.GetBlock(pos)

def GetBlockEntityMolangValue(pos,name):
    '''获取自定义方块实体的Molang变量的值。'''
    comp = clientApi.GetEngineCompFactory().CreateBlockInfo(levelId)
    return comp.GetBlockEntityMolangValue(pos, name)

def SetBlockEntityMolangValue(pos,name,value):
    '''设置自定义方块实体的Molang变量'''
    comp = clientApi.GetEngineCompFactory().CreateBlockInfo(levelId)
    # 设置molang变量的值来转变动画状态
    return comp.SetBlockEntityMolangValue(pos, name, value)

def GetDistanceBetweenTwoPos(pos0, pos1):
    '''获得两个位置之间的距离'''
    return ((pos0[0]-pos1[0])**2+(pos0[1]-pos1[1])**2+(pos0[2]-pos1[2])**2)**0.5

def SetConfigData(configName,value,isGlobal = True):
    '''以本地配置文件的方式存储数据'''
    comp = clientApi.GetEngineCompFactory().CreateConfigClient(levelId)
    comp.SetConfigData(configName, value, isGlobal)

def GetConfigData(configName,isGlobal = True):
    '''获取本地配置文件中存储的数据'''
    comp = clientApi.GetEngineCompFactory().CreateConfigClient(levelId)
    return comp.GetConfigData(configName, isGlobal)

def GetItemBasicInfo(itmeName,itemAux=0):
    '''获取物品的基础信息'''
    comp = clientApi.GetEngineCompFactory().CreateItem(levelId)
    return comp.GetItemBasicInfo(itmeName,itemAux)

def PickFacing():
    '''获取准星选中的实体或者方块'''
    comp = clientApi.GetEngineCompFactory().CreateCamera(get_level_id())
    return comp.PickFacing()

def get_topblock_height(x,z):
    '''
    获取当前维度某一位置最高的非空气方块的高度
    '''
    comp = clientApi.GetEngineCompFactory().CreateBlockInfo(get_level_id())
    return comp.GetTopBlockHeight((x, z))

def get_level_id():
    return levelId


def get_local_player_id():
    return clientApi.GetLocalPlayerId()


def get_namespace():
    return clientApi.GetEngineNamespace()


def get_system_name():
    return clientApi.GetEngineSystemName()


def get_engine_version():
    return clientApi.GetEngineVersion()


def particle_play(particle_id):
    """
    播放粒子特效
    :param str particle_id:
    :return:
    """
    comp = compFactory.CreateParticleControl(particle_id)
    comp.Play()


def set_particle_pos(particle_id, pos):
    """
    设置粒子位置
    :param particle_id:
    :param tuple pos:
    :return:
    """
    comp = compFactory.CreateParticleTrans(particle_id)
    comp.SetPos(pos)


def set_sfx_pos(frame_id, pos):
    """
    设置序列帧位置
    :param frame_id:
    :param tuple pos:
    :return:
    """
    comp = compFactory.CreateFrameAniTrans(frame_id)
    comp.SetPos(pos)


def set_sfx_rot(frame_id, rot):
    comp = compFactory.CreateFrameAniTrans(frame_id)
    # 旧的接口是以按顺序绕局部坐标系的+x，-y，+z轴旋转的角度
    # 新的接口是以局部坐标系的+z，+x，+y轴旋转的角度
    # 为兼容之前的用法，参数调整
    rot = (rot[2], rot[0], -rot[1])
    comp.SetRotUseZXY(rot)


def sfx_play(sfx_id):
    """
    播放序列帧动画
    :param str sfx_id:
    :return:
    """
    comp = compFactory.CreateFrameAniControl(sfx_id)
    return comp.Play()


def particle_bind_entity(
    particleEntityId, entityId, offset=(
        0, 0, 0), rot=(
            0, 0, 0), is_new=False):
    comp = compFactory.CreateParticleEntityBind(particleEntityId)
    return comp.Bind(entityId, offset, rot,True)


def sfx_bind_entity(frame_id, entity_id, offset=(0, 0, 0), rot=(0, 0, 0)):
    """
    将序列帧与entity绑定
    :param frame_id: 序列帧Id
    :param str entity_id: 绑定到的entity_id
    :param tuple offset: 偏移
    :param tuple rot: 旋转
    :return:
    """
    comp = compFactory.CreateFrameAniEntityBind(frame_id)
    return comp.Bind(entity_id, offset, rot)

def get_pos(entity_id):
    """
    返回实体位置
    :param str entity_id: 实体id
    :rtype: tuple
    :return: 实体位置
    """
    comp = compFactory.CreatePos(entity_id)
    return comp.GetPos()


def set_can_move(is_can):
    comp = compFactory.CreateOperation(get_level_id())
    comp.SetCanMove(is_can)


def set_can_jump(is_can):
    comp = compFactory.CreateOperation(get_level_id())
    comp.SetCanJump(is_can)


def set_move_lock(is_can):
    comp = compFactory.CreateOperation(get_level_id())
    comp.SetMoveLock(is_can)


def has_entity(entityId):
    comp = clientApi.GetEngineCompFactory().CreateGame(get_level_id())
    exist = comp.HasEntity(entityId)
    return exist


def add_timer(delay, func, *args):
    '''
    delay:时间
    func:函数
    args(可选):参数
    '''
    comp = compFactory.CreateGame(get_level_id())
    return comp.AddTimer(delay, func, *args)

def CancelTimer(timer):
    '''取消定时器'''
    comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
    return comp.CancelTimer(timer)

def GetRot(entityId):    
    comp = clientApi.GetEngineCompFactory().CreateRot(entityId)
    return comp.GetRot()

def SetRot(entityId,rot):    
    comp = clientApi.GetEngineCompFactory().CreateRot(entityId)
    return comp.SetRot(rot)

def GetCurrentDimension():
    comp = clientApi.GetEngineCompFactory().CreateGame(get_level_id())
    return comp.GetCurrentDimension()