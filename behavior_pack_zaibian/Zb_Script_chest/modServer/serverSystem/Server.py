# -*- coding: utf-8 -*-
#
import mod.server.extraServerApi as serverApi
import Zb_Script_chest.modCommon.modConfig as modConfig

from Zb_Script_chest.modCommon.modCommonUtils.util import *


import json


minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()
ServerCompFactory = serverApi.GetEngineCompFactory()
LevelItemComp = ServerCompFactory.CreateItem(serverApi.GetLevelId())
# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
levelId=serverApi.GetLevelId()
# 在modMain中注册的Server System类
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()
ItemPosType=serverApi.GetMinecraftEnum().ItemPosType
class ServerSystem(serverApi.GetServerSystemCls()):
    def __init__(self, namespace, name):
        super(ServerSystem, self).__init__(namespace, name)
        # 初始时调用监听函数监听事件
        self.ListenEvent()
   

    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):        
        pass
        # self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerPlayerTryDestroyBlockEvent",self, self.ServerPlayerTryDestroyBlockEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerItemUseOnEvent", self, self.ServerItemUseOnEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerRespawnFinishServerEvent", self, self.PlayerRespawnFinishServerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerPlayerTryDestroyBlockEvent", self, self.ServerPlayerTryDestroyBlockEvent)





        # #客户端通信事件
        # self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "trident_Projectile", self, self.trident_Projectile)  
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "OnItemSwap", self, self.OnItemSwap)  
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "openUI", self, self.openUI)  
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "spwan_item", self, self.spwan_item)  
        self.ListenForEvent(modConfig.ModName,modConfig.ClientSystemName,  "mergeItem", self, self.mergeItem)  


    def mergeItem(self, args):
        """
        双击物品合堆。
        """
        targetIndex = args['from']
        playerId = args['playerId']
        targetGridType = args['gridType']
        dimension=args["dimension"]
        pos=args["pos"]
        use_way=args["use_way"]
        archives=args["archives"]


        itemsInWorkbench = args.get('itemsInWorkbench')

        itemFlyData = [] 
        itemComp = ServerCompFactory.CreateItem(playerId)
        itemsInInv = itemComp.GetPlayerAllItems(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, True)

        updateInv = [False]
        updateCps = [False]
        # 获取合堆物品信息
        if targetGridType == "inv":
            targetDict = itemsInInv[targetIndex]
        else:
            targetDict = itemsInWorkbench[targetIndex]
        if not  targetDict:
            return
        targetItemName = targetDict['newItemName']
        targetItemAux = targetDict['newAuxValue']
        targetItemMaxStack = LevelItemComp.GetItemBasicInfo(targetItemName, targetItemAux)['maxStackSize']
        def merge(fromIndex, fromGridType):
            """
            合堆函数。

            :param fromIndex: 合堆来源槽位
            :param fromGridType: 合堆来源槽位的类型
            """
            if fromGridType == "inv":
                updateInv[0] = True
            else:
                updateCps[0] = True
            fromAllItems = itemsInInv if fromGridType == "inv" else itemsInWorkbench
            fromDict = fromAllItems[fromIndex]
            # 如果合堆来源物品的数量已经达到最大堆叠数，则跳过该物品
            if fromDict['count'] == targetItemMaxStack:
                return
            # 设置合堆目标槽位和来源槽位的物品数量
            targetDict['count'] += fromDict['count']
            if targetDict['count'] > targetItemMaxStack:
                fromDict['count'] = targetDict['count'] - targetItemMaxStack
                targetDict['count'] = targetItemMaxStack
            else:
                fromAllItems[fromIndex] = None
            # 记录数据用于物品飞行动画
            itemFlyData.append({
                'itemDict': fromDict,
                'from': fromIndex,
                'to': targetIndex,
                'fromType': fromGridType,
                'toType': targetGridType
            })
        # 搜索背包是否有可合堆物品
        if targetGridType == "inv":
            for i in range(36):
                if i == targetIndex:
                    continue
                if not is_empty_item(itemsInInv[i]) and is_same_item(itemsInInv[i], targetDict):
                    merge(i, "inv")
        # 搜索合成栏是否有可合堆物品
        if targetGridType == "composite":
            for i in itemsInWorkbench:

                if  i == targetIndex:
                    continue
                if not is_empty_item(itemsInWorkbench[i]) and is_same_item(itemsInWorkbench[i], targetDict):
                    merge(i, "composite")
        # 刷新客户端显示
        for i in range(0,36):
            if itemsInInv[i]:
                item=itemsInInv[i]
            else:
                item={}
            itemComp.SpawnItemToPlayerInv(item, playerId,i)
        
        blockEntityData=None
        if archives:
            if use_way=="item":
                comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                extraId=item["extraId"]
                blockEntityData=json.loads(extraId)
            else:
                blockEntityComp = compFactory.CreateBlockEntityData(serverApi.GetLevelId())
                blockEntityData = blockEntityComp.GetBlockEntityData(dimension, pos)

        if blockEntityData:
            for i,data in itemsInWorkbench.items():
                blockEntityData[i]=data
        if use_way=="item":
            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            data1=json.dumps(blockEntityData)
            comp.ChangePlayerItemTipsAndExtraId(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, "", data1)

        eventData = self.CreateEventData()    
        eventData[1]={}
        eventData[2]=itemsInWorkbench

       
        for i in xrange(0,36):
            eventData[1][i] = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, i, True)

    

        self.NotifyToClient(playerId,"OnBagChangedEvent", eventData,1)


        self.NotifyToClient(playerId, "setMultipleItemFlyAnimation", {
            'data': itemFlyData
        })


    def spwan_item(self,args):
        '''给玩家物品'''
        data = args['data']
        playerId = args['playerId']
        order = args['order']
        use_way=args["use_way"]   #$打开是物品还是方块
        archives=args["archives"]  
        dimension=args["dimension"]  
        pos=args["pos"]  

        itemComp = compFactory.CreateItem(playerId)
        if order==False:
            for i in data:
                itemComp.SpawnItemToPlayerInv(i, playerId)
        else:
            for index,val in data.items():
                if  type(index)==int:
                    itemComp.SpawnItemToPlayerInv(val, playerId,index)
                else:
                    if archives:
                        if use_way=="item":
                            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                            item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                            extraId=item["extraId"]
                            blockEntityData=json.loads(extraId)
                        else:
                            blockEntityComp = compFactory.CreateBlockEntityData(serverApi.GetLevelId())
                            blockEntityData = blockEntityComp.GetBlockEntityData(dimension, pos)
                        blockEntityData[index]=val

                        if use_way=="item":
                            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                            data1=json.dumps(blockEntityData)
                            comp.ChangePlayerItemTipsAndExtraId(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, "", data1)


    
    def ServerPlayerTryDestroyBlockEvent(self,args):
        fullName = args['fullName']
        dimensionId = args['dimensionId']
        playerId = args['playerId']
        pos=(args['x'],args['y'],args['z'])

        if fullName in  modConfig.blockNamesUI.keys() and fullName not in modConfig.not_archives:
            data=self.GetCustomContainerItems(dimensionId, None, pos,"block",playerId)
            for i in data.values():
                if i!=None:
                    itemComp = compFactory.CreateItem(levelId)
                    itemComp.SpawnItemToLevel(i, dimensionId, pos)

        self.NotifyToClient(playerId,"die_ui_pet",None)

        

    def ServerItemUseOnEvent(self,args):
        blockName = args['blockName']
        if blockName in  modConfig.blockNamesUI.keys() :
            args['ret'] = True

    def PlayerRespawnFinishServerEvent(self,args):
        id=args['playerId']
        self.NotifyToClient(id,"die_ui_pet",None)


    def openUI(self,args):
        playerId=args["playerId"]
        dimension=args["dimension"]
        pos=args["pos"]
        use_way=args["use_way"]


        def UpdateBagUI():
            eventData = self.CreateEventData()    
            eventData[1]={}
            eventData[2]={}
            items=self.GetCustomContainerItems(dimension,None,pos,use_way,playerId)
            itemComp = compFactory.CreateItem(playerId)          
            for i in xrange(0,36):
                eventData[1][i] = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, i, True)
            for i,data in items.items():
                eventData[2][i]=data
            self.NotifyToClient(playerId,"OnBagChangedEvent", eventData,1)

        gameComp = compFactory.CreateGame(serverApi.GetLevelId())
        gameComp.AddTimer(0.0, UpdateBagUI)


    


    def OnItemSwap(self,args):  #交换人物背包
        # @param playerId 玩家Id
        # @param fromSlot 第一次点击的槽位
        # @param fromItem 第一次点击槽位的itemDict
        # @param toSlot 第二次点击的槽位
        # @param toItem 第二次点击槽位的itemDict
        try:
            use_way=args["use_way"]   #$打开是物品还是方块
            archives=args.get("archives",True)  #$是否存档
            entityId=args["entityId"]
            blockPos=args["blockPos"]
            dimension=args["dimension"]
            playerId=args["PlayerId"]
            fromSlot=args["fromSlot"]
            fromItem=args["fromItem"]
            toSlot=args["toSlot"]
            toItem=args["toItem"]
            
        
        except:
            pass
        
        try:
            if "zd" in toSlot:   
                toSlot=int(toSlot[2:])
            elif "itemBth"in toSlot:
                toSlot=int(toSlot[10:])
        except:
            pass

        try:
            if "zd" in fromSlot:  
                fromSlot=int(fromSlot[2:])
            elif "itemBth"in fromSlot:
                fromSlot=int(fromSlot[10:])
        except:
            pass
        itemComp = compFactory.CreateItem(playerId)

        blockEntityData=None
        if archives:
            if use_way=="item":
                comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
                extraId=item["extraId"]
                blockEntityData=json.loads(extraId)
            else:
                blockEntityComp = compFactory.CreateBlockEntityData(serverApi.GetLevelId())
                blockEntityData = blockEntityComp.GetBlockEntityData(dimension, blockPos)


        if args["key"]=="beibao":  #背包内部交换
            itemComp.SetInvItemNum(fromSlot, 0)
            itemComp.SetInvItemNum(toSlot, 0)
            if toItem:
                itemComp.SpawnItemToPlayerInv(toItem, playerId, fromSlot)
            if fromItem:
                itemComp.SpawnItemToPlayerInv(fromItem, playerId, toSlot)
            
        elif args["key"]=="b_z":   #背包和自定义容器交换
            if blockEntityData:
                blockEntityData[toSlot]=fromItem

            if toItem:
                itemComp.SpawnItemToPlayerInv(toItem, playerId, fromSlot)
            else:
                itemComp.SetInvItemNum(fromSlot, 0)
            
        elif args["key"]=="z_b":   #自定义容器交换和背包
            if blockEntityData:
                blockEntityData[fromSlot]=toItem
            itemComp.SpawnItemToPlayerInv(fromItem, playerId, toSlot)


        elif args["key"]=="beibao_drop":   #背包丢东西
            drop=args["drop"]
            if   fromItem :
                itemComp = compFactory.CreateItem(playerId)
                itemComp.SetInvItemNum(fromSlot, fromItem["count"])
            else:
                itemComp.SetInvItemNum(fromSlot, 0)
            itemComp = compFactory.CreateItem(levelId)

            itemComp.SpawnItemToLevel(drop, dimension, blockPos)

        elif args["key"]=="ziding":   #自定义容器内部交换
            if blockEntityData:
                blockEntityData[fromSlot]=toItem
                blockEntityData[toSlot]=fromItem

        elif args["key"]=="ziding_drop":   #自定义容器丢东西
            if blockEntityData:
                blockEntityData[fromSlot]=fromItem

            drop=args["drop"]
            itemComp = compFactory.CreateItem(levelId)
            itemComp.SpawnItemToLevel(drop, dimension, blockPos)

        if use_way=="item":
            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            data1=json.dumps(blockEntityData)
            comp.ChangePlayerItemTipsAndExtraId(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, "", data1)


    def GetCustomContainerItems(self, dimension, blockName, blockPos,use_way,playerId):  #获取对应箱子数据
        # 覆写基类方法，获取自定义熔炉中blockEntityData中的数据
        items = {}
        if use_way!="item":
            blockEntityComp = compFactory.CreateBlockEntityData(serverApi.GetLevelId())
            blockEntityData = blockEntityComp.GetBlockEntityData(dimension, blockPos)
        else:
            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
            extraId=item["extraId"]
            data={}
            if extraId=='':
                for i in range(0, 109):
                    data["itemBtn"+str(i)]=None
                extraId=data
                data1=json.dumps(extraId)
                comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                comp.ChangePlayerItemTipsAndExtraId(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, "", data1)
            else:

                data=json.loads(extraId)
            blockEntityData=data
        
            

        if blockEntityData:
            try:
                for i in range(0, 109):
                    key = "itemBtn"+str(i)
                    items[key] = blockEntityData[key]
            except:
                pass
        return items


    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        # 调用上面的反监听函数来销毁
        pass


    