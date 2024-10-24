# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode
import mod.client.extraClientApi as clientApi
import Zb_Script_chest.modCommon.modConfig as modConfig

from Zb_Script_chest.modClient.ui.ScreenNode import LYJScreenNode


ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
playerId=clientApi.GetLocalPlayerId()
import copy

# 获取组件工厂，用来创建组件
compFactory = clientApi.GetEngineCompFactory()
client=clientApi.GetSystem(modConfig.ModName,modConfig.ClientSystemName)

ClientCompFactory = clientApi.GetEngineCompFactory()
PlayerItemComp = ClientCompFactory.CreateItem(playerId)
PlayerGameComp = ClientCompFactory.CreateGame(playerId)
# 所有的UI类需要继承自引擎的ScreenNode类
ITEM_CATEGORY_CHINESE = {
    'construction': "建筑",
    'equipment': "装备",
    'items': "物品",
    'nature': "自然"
}
UI_PATH_FLY_ITEM_1 = "/item_fly_panel/item_renderer1"
UI_PATH_FLY_ITEM_2 = "/item_fly_panel/item_renderer2"


duanzaopeifang={
    ("zaibian:infernal_forge","zaibian:void_core"):{"itemName":"zaibian:void_forge",'count': 1,'newItemName': 'zaibian:void_forge','durability':0},
    ("zaibian:ignitium_chestplate","minecraft:elytra"):{"itemName":"zaibian:ignitium_elytra_chestplate",'count': 1,'newItemName': 'zaibian:ignitium_elytra_chestplate','durability':0},
    ("zaibian:wither_assault_shoulder_weapon","zaibian:void_core"):{"itemName":"zaibian:void_assault_shoulder_weapon",'count': 1,'newItemName': 'zaibian:void_assault_shoulder_weapon'},
    ("zaibian:gauntlet_of_guard","zaibian:shield"):{"itemName":"zaibian:gauntlet_of_bulwark",'count': 1,'newItemName': 'zaibian:gauntlet_of_bulwark'},

}

class PyClientScreen(LYJScreenNode):
    def __init__(self, namespace, name, param):
        super(PyClientScreen, self).__init__(namespace, name, param)
  

        self.open="/open"
        self.gbin="/panel/gbbth"

        self.drop="/panel/drop"
        self.mBagInfo={}
        self.mSlotToPath={}
        self.mFlyImgPool = []
        self.mDetailAlpha = 2.0
        self.Time=None
        self.mAlreadyRegisterEvent=False
        # 用于判断点击事件

        self.mClickInterval = 0
        self.mHeldTime = None
        self.mLastTouchButton = None
        self.mIsDoubleClick = False
        self.mTakePercent = 1
        self.image_button = False
        # 管理飞行动画相关数据
        self.flyItem = []
        self.itemFlyData = []


        self.mFlyImgPool = []
        self.mFlyImgIndex = 0
        self.mFlyAnimationTime = 0
        self.entityId=None
        self.tick=0
        self.alphaTick = 0

        self.timer1 = None
        self.timer2 = None
        self.dimension=None
        self.pos=None
        self.show=False  #当前UI是否打开
        self.use_way=None #当前UI的使用状态

        self.type_UI=None   #UI自定义变化 名
        self.historypath=set()  #历史存储注册列表
        self.registerbtn=[]  #注册列表
        self.slotId=None #当前槽 对不是方块UI使用

        self.archives=True  #是否存档

        self.MoveList={} #当前槽 对不是方块UI使用
        self.IsMove=False #当前槽 对不是方块UI使用



        self.UI_PATH_TIPS="/tips_panel"
        self.UI_PATH_TIPS_IMAGE="/tips_panel/image"
        self.UI_PATH_TIPS_LABEL="/tips_panel/image/label"


        self.UI_index=modConfig.UI_index

        self.player_beibao0="/panel/beibao/beibao0"
        self.player_beibao1="/panel/beibao/beibao1"

        self.temporary={}


        self.panel="/panel"


    # Create函数是继承自ScreenNode，会在UI创建完成后被调用
    def Create(self):
        self.entityId=playerId

        self.AddTouchEventHandler(self.open, self.openBth, {"isSwallow": True})
        self.AddTouchEventHandler(self.gbin, self.gbinBth, {"isSwallow": True})

        self.AddTouchEventHandler(self.drop, self.OnButtondrop, {"isSwallow": True})

        self.flyItem.append(self.GetBaseUIControl(UI_PATH_FLY_ITEM_1).asItemRenderer())
        self.flyItem.append(self.GetBaseUIControl(UI_PATH_FLY_ITEM_2).asItemRenderer())

        #文字显示
        self.tipsPanel = self.GetBaseUIControl(self.UI_PATH_TIPS)
        self.tipsPanel.SetVisible(False)
        self.tipsImg = self.GetBaseUIControl(self.UI_PATH_TIPS_IMAGE).asImage()

        self.tipsLabel = self.GetBaseUIControl(self.UI_PATH_TIPS_LABEL).asLabel()

    def RegisterButtonEvents(self):   #注销路径操作
        if self.registerbtn:
            for path in self.registerbtn:
                # self.AddTouchEventHandler(path, self.OnButtonTouch, {"isSwallow": True})
                self.SetButtonDoubleClickCallback(
                path, self.OnItemGridButtonDoubleClick, self.OnButtonTouch
                )
            self.registerbtn=[]


    def show_ui(self,path,key=True):
        baseUIControl = self.GetBaseUIControl(path)
        if baseUIControl:
            baseUIControl.SetVisible(key)

    def openBth(self,args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args.get("TouchEvent")
        # 按钮按下时
        if touchEvent == touchEventEnum.TouchDown or touchEvent==None:
            if touchEvent:
                localPlayerId = clientApi.GetLocalPlayerId()
                rotComp = clientApi.GetEngineCompFactory().CreateRot(localPlayerId)
                rot = rotComp.GetRot()
                x, y, z = clientApi.GetDirFromRot(rot)
                comp = clientApi.GetEngineCompFactory().CreatePos(playerId)
                pos=comp.GetFootPos()
                self.pos = pos[0]+x*3,pos[1],pos[2]+z*3
            
                comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
                self.dimension=comp.GetCurrentDimension()
                self.use_way="item"

                comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
                carriedData = comp.GetCarriedItem()
                self.type_UI=modConfig.itemNamesUI[carriedData["newItemName"]]
                client.before_cls=modConfig.UI_CLS.get(carriedData["newItemName"],"")
                client.itemname=carriedData["newItemName"]
            else:
                self.dimension=args["dimension"]
                self.pos=args["pos"]
                self.use_way=args["use_way"]
                self.type_UI=args.get("type_UI")
            
            self.show=True
            # self.show_ui(self.open,False)
            self.show_ui(self.panel)
            clientApi.HideHudGUI(True)        
            clientApi.SetInputMode(1)        
            clientApi.SetResponse(False)
            client.NotifyToServer("openUI",{"playerId":playerId,"dimension":self.dimension,"pos":self.pos,"use_way":self.use_way})
            self.open_duiyingUI(self.type_UI)

            gameComp = compFactory.CreateGame(clientApi.GetLevelId())
            gameComp.AddTimer(0.2, self.show_ui,self.open,False)

            if client.itemname in  modConfig.not_archives:
                self.archives=False
            else:
                self.archives=True
            


    def open_duiyingUI(self,args):
        '''显示对应UI'''
        for i in self.UI_index.keys():
            if args==i:
                self.show_ui(self.UI_index[i])
            else:
                self.show_ui(self.UI_index[i],False)


    def gbinBth(self,args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args.get("TouchEvent")
        # 按钮按下时
        if touchEvent == touchEventEnum.TouchDown or touchEvent==None:
            self.show=False
            comp = clientApi.GetEngineCompFactory().CreateItem(playerId)
            carriedData = comp.GetCarriedItem()

            if carriedData and carriedData["newItemName"] in modConfig.itemNamesUI:
                self.show_ui(self.open,True)

            self.show_ui(self.panel,False)
            clientApi.HideHudGUI(False)        
            clientApi.SetInputMode(0)        
            clientApi.SetResponse(True)

            ##文字初始化
            self.alphaTick = 0
            self.tipsPanel.SetVisible(False)
            self.tipsImg.SetAlpha(1.0)
            self.tipsLabel.SetAlpha(1.0)
            ###退出初始化
            if self.mLastTouchButton:
                fromSlot=self.mBagInfo[self.mLastTouchButton]["slot"]
                self.SetVisible(self.mLastTouchButton+"/progress_fd" , False)
                fromSlotpath=self.mSlotToPath[fromSlot]
                self.Setimage(fromSlotpath,False)
                self.mLastTouchButton=None
                self.mIsDoubleClick = False
                self.mClickInterval=0
                self.Time=None

            if client.itemname in  modConfig.not_archives:
                data=[]
                for i in self.GetChildrenName(self.UI_index[self.type_UI]):
                    path_d=self.UI_index[self.type_UI]+"/"+i
                    if  self.mBagInfo.get(path_d) and self.mBagInfo[path_d]["slot"]=='itemBtn3' and self.type_UI=='ui':
                        self.mBagInfo['/panel/zhaohuan/itemBtn3']["item"]=None
                        self.SetSlotUI('/panel/zhaohuan/itemBtn3',None)
                        continue
                    if self.mBagInfo.get(path_d) and self.mBagInfo[path_d]["item"]:
                       
                        data.append(self.mBagInfo[path_d]["item"])
                client.NotifyToServer("spwan_item",{"data":data,'playerId':playerId,'order':False,"use_way":self.use_way,
                                                    "archives":self.archives,"dimension":self.dimension,"pos":self.pos})

            self.mBagInfo={}
            self.mSlotToPath={}
                    

    def OnButtondrop(self,args):  #丢弃操作
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        # 点击坐标
        touchPos = args["TouchPosX"], args["TouchPosY"]
        if touchEvent == touchEventEnum.TouchDown:
            if self.mClickInterval==2:
                self.mClickInterval=0
                time=self.Time
                self.Time=None
                self.mHeldTime = None
                self.Setimage(self.mLastTouchButton,False)
                self.SetVisible(self.mLastTouchButton+"/progress_fd" , False)

                fromSlot=self.mBagInfo[self.mLastTouchButton]["slot"]
                fromItem=self.mBagInfo[self.mLastTouchButton]["item"]
                if time>10:
                    give=int(self.mTakePercent*fromItem["count"])
                else:
                    give=fromItem["count"]
        
                self.drop_ui(fromSlot,fromItem,give)

    def drop_ui(self,fromSlot,fromItem,give):
        giveItem=dict(fromItem)
        if type(fromSlot)==int:
            drop="beibao_drop"
        else:
            drop="ziding_drop"
        if give==fromItem["count"]:
            fromItem=None
        else:
            fromItem["count"]-=give
        
        giveItem["count"]=give
        
        localPlayerId = clientApi.GetLocalPlayerId()
        rotComp = clientApi.GetEngineCompFactory().CreateRot(localPlayerId)
        rot = rotComp.GetRot()
        x, y, z = clientApi.GetDirFromRot(rot)

        comp = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId())
        entityFootPos = comp.GetFootPos()
        
        args={
                "PlayerId":clientApi.GetLocalPlayerId(),
                "fromSlot":fromSlot,
                "drop":giveItem,
                "fromItem":fromItem,
                "dimension":self.dimension,
                "entityId":localPlayerId,
                "blockPos":self.pos,

                "key": drop,
            }

        fromSlotpath=self.mSlotToPath[fromSlot]
        self.SetSlotUI(fromSlotpath,fromItem)
        self.mBagInfo[fromSlotpath]["item"]=fromItem

        args["use_way"]=self.use_way
        args["archives"]=self.archives
        client.NotifyToServer("OnItemSwap",args)

    def OnItemSwap(self,PlayerId, fromSlot, fromItem, toSlot, toItem,is_fd=False):   #ui交换操作
        # @param playerId 玩家Id
        # @param fromSlot 第一次点击的槽位
        # @param fromItem 第一次点击槽位的itemDict
        # @param toSlot 第二次点击的槽位
        # @param toItem 第二次点击槽位的itemDict

        print fromSlot, fromItem, toSlot, toItem
        fromSlotpath=self.mSlotToPath[fromSlot]
        toSlotpath=self.mSlotToPath[toSlot]
        comp = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId())
        entityFootPos = comp.GetFootPos()
        localPlayerId = clientApi.GetLocalPlayerId()
        rotComp = clientApi.GetEngineCompFactory().CreateRot(localPlayerId)
        rot = rotComp.GetRot()
        x, y, z = clientApi.GetDirFromRot(rot)
        args={
                "PlayerId":PlayerId,
                "fromSlot":fromSlot,
                "fromItem":fromItem,
                "toSlot":toSlot,
                "toItem":toItem,
                "entityId":PlayerId,
                "dimension":self.dimension,
                "blockPos":self.pos,


                
            }
            # 更新飞行动画
        # self.mFlyAnimationTime = 5
        if type(fromSlot)==int and type(toSlot)==int:   #背包内部交换
            self.SetSlotUI(toSlotpath,fromItem)
            self.SetSlotUI(fromSlotpath,toItem)
            self.mBagInfo[toSlotpath]["item"]=fromItem
            self.mBagInfo[fromSlotpath]["item"]=toItem
        elif type(fromSlot)==str and type(toSlot)==str:#自定义容器内部交换
            self.SetSlotUI(toSlotpath,fromItem)
            self.SetSlotUI(fromSlotpath,toItem)
            self.mBagInfo[toSlotpath]["item"]=fromItem
            self.mBagInfo[fromSlotpath]["item"]=toItem
        elif type(fromSlot)==int and type(toSlot)==str:#背包和自定义容器交换
            self.SetSlotUI(toSlotpath,fromItem)
            self.SetSlotUI(fromSlotpath,toItem)
            self.mBagInfo[toSlotpath]["item"]=fromItem
            self.mBagInfo[fromSlotpath]["item"]=toItem
        elif type(fromSlot)==str and type(toSlot)==int: #自定义容器交换和背包
            self.SetSlotUI(toSlotpath,fromItem)
            self.SetSlotUI(fromSlotpath,toItem)
            self.mBagInfo[toSlotpath]["item"]=fromItem
            self.mBagInfo[fromSlotpath]["item"]=toItem

        if type(fromSlot)==int and type(toSlot)==int:   #背包内部交换
            args["key"]="beibao"
        elif type(fromSlot)==str and type(toSlot)==str:#自定义容器内部交换
            args["key"]="ziding"
        elif type(fromSlot)==int and type(toSlot)==str:#背包和自定义容器交换
            args["key"]="b_z"
        elif type(fromSlot)==str and type(toSlot)==int: #自定义容器交换和背包
            args["key"]="z_b"

        toUiSize = self.GetBaseUIControl(toSlotpath).GetSize()
        fromUiSize = self.GetBaseUIControl(fromSlotpath).GetSize()


        if toItem and toItem['count'] > 0 and not is_fd:
            self.setSingleItemFlyAnimation(
                toItem,
                self.get_ui_position( toSlotpath),
                self.get_ui_position( fromSlotpath),
                toUiSize,
                1
            )
        self.setSingleItemFlyAnimation(
            fromItem,
            self.get_ui_position( fromSlotpath),
            self.get_ui_position( toSlotpath),
            fromUiSize
        )

        args["use_way"]=self.use_way

        args["archives"]=self.archives
        
        client.NotifyToServer("OnItemSwap",args)


    def UpdateBagUI(self,args):  #背包路径存储及item存储

        args1=args[2]
        self.ZBUpdateBagUI(args1)


        args=args[1]
        for path in range(0,36):
            h=path//9
            l=path%9
            if h==0:
                path_=self.player_beibao0
            else:
                path_=self.player_beibao1
            item=args[path]
            path_d=path_+"/"+str(h)+"/itemBtn"+str(l)
            self.mBagInfo[path_d]={"slot": path, "item": item}
            self.SetSlotUI(path_d,item)
            self.mSlotToPath[path] = path_d
            self.id_registerbtn(path_d)
            self.historypath.add(path_d)
   

        self.RegisterButtonEvents()

    def Get_zidingyipath(self,dqpath,higherpath):
        '''自动获取自定义按钮路径'''
        if higherpath=="":
            zzdqpath=dqpath
        else:
            zzdqpath=dqpath+"/"+higherpath
            
        for i in self.GetChildrenName(zzdqpath):
            if 'itemBtn' in i:
                try:
                    k=int(higherpath)
                    val=len(self.GetChildrenName(zzdqpath))*k+int(i.replace("itemBtn","" ))
                    val="itemBtn"+str(val)
                except:
                    val=i
                self.temporary[val]=zzdqpath+"/"+i
            else:
                self.Get_zidingyipath(zzdqpath,i)



    def ZBUpdateBagUI(self,args):  #自定义装备路径存储及item存储
        
        self.Get_zidingyipath(self.UI_index[self.type_UI],"")
        for i,data in  args.items():
            item=data
            index=i
            if self.temporary.get(index):

                path_d=self.temporary.get(index)
                self.mBagInfo[path_d]={"slot": index, "item": item}
                self.SetSlotUI(path_d,item)
                self.mSlotToPath[index] = path_d
                self.id_registerbtn(path_d)
                self.historypath.add(path_d)
        
        self.temporary={}


    def getzdyi(self):
        '''获取自定义物品'''
        self.Get_zidingyipath(self.UI_index[self.type_UI],"")
        itemdict={}
        for i in  range(100):
            index="itemBtn"+str(i)
            if self.temporary.get(index):
                path_d=self.mSlotToPath[index]
                item=self.mBagInfo[path_d]["item"]
                if item:
                    itemdict[index]=item
        return itemdict








####################复制

    def OnItemGridButtonDoubleClick(self, args):
        """
        双击合堆。
        """
       
        bp = args['ButtonPath']
        data=self.mBagInfo[bp]
        itemDict=data['item']
        if self.is_empty_item(itemDict):
            return
        itemIndex = data['slot']
        if type(itemIndex)==int :
            gridType="inv"
        else:
            gridType="composite"

        maxStack = PlayerItemComp.GetItemBasicInfo(itemDict['newItemName'], itemDict['newAuxValue'])['maxStackSize']
        if 0 < itemDict['count'] < maxStack:
            client.NotifyToServer("mergeItem", {
                'from': itemIndex,
                'playerId': playerId,
                'gridType': gridType,
                'pos': self.pos,
                'dimension': self.dimension,
                'archives': self.archives,
                'itemsInWorkbench': self.getzdyi(),
                'use_way': self.use_way

            })
            fromSlot=self.mBagInfo[self.mLastTouchButton]["slot"]
            fromSlotpath=self.mSlotToPath[fromSlot]
            self.Setimage(fromSlotpath,False)
            self.mLastTouchButton=None
            self.mIsDoubleClick = False
            self.mClickInterval=0
            self.Time=None

    def get_ui_position(self, path):
        """
        获取UI在屏幕上的坐标（而不是相对于父控件的坐标）。

        :param uiCls: UI类实例
        :param path: UI路径
        :return: 坐标元组
        """
        pos = [0, 0]
        splitPath = path.split("/")
        for i in range(len(splitPath)):
            parentPath = "/" + "/".join(splitPath[0: i + 1])
            parentPos = self.GetBaseUIControl(parentPath).GetPosition()
            pos[0] += parentPos[0]
            pos[1] += parentPos[1]
        return tuple(pos)
    

    def id_registerbtn(self,path):
        '''注册按钮'''
        if path not in self.historypath:
            self.registerbtn.append(path)

    def showItemInfoBox(self, itemDict,key=True):
        """
        显示物品信息文本框。
        :param itemDict: 物品信息字典
        """
        def k():
            # 取消正在执行的timer
            if self.timer1:
                PlayerGameComp.CancelTimer(self.timer1)
                self.timer1 = None
            if self.timer2:
                PlayerGameComp.CancelTimer(self.timer2)
                self.timer2 = None
            # 显示文本框
            self.alphaTick = 0
            self.tipsPanel.SetVisible(True)
            self.tipsImg.SetAlpha(1.0)
            self.tipsLabel.SetAlpha(1.0)
            if key:
                self.tipsLabel.SetText(name + itemCategory + customTips)
            else:
                self.tipsLabel.SetText(itemDict)

            # 一秒后执行渐出动画
            def func1():
                self.alphaTick = 30
                self.timer1 = None
            self.timer1 = PlayerGameComp.AddTimer(1, func1)
            # 两秒后隐藏文本框并恢复初始状态
            def func2():
                self.tipsPanel.SetVisible(False)
                self.tipsImg.SetAlpha(1.0)
                self.tipsLabel.SetAlpha(1.0)
                self.timer2 = None
            self.timer2 = PlayerGameComp.AddTimer(2, func2)
        if not key:
            k()
            return
        if itemDict:
            isEnchanted = bool(itemDict.get('enchantData',[]) or itemDict.get('modEnchantData',[]))
            basicInfo = PlayerItemComp.GetItemBasicInfo(
                itemDict['newItemName'], itemDict.get('newAuxValue',0), isEnchanted
            )
            if basicInfo:
                # 获取中文名
                name = basicInfo['itemName']
                # 获取创造栏分类
                itemCategory = ""
                # 获取自定义Tips
                customTips = itemDict.get('customTips', "")
                if customTips:
                    customTips = "\n" + customTips
                k()

    def OnButtonTouch(self,args):   #背包和自定义按钮操作
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        # 点击坐标
        touchPos = args["TouchPosX"], args["TouchPosY"]
        # 触控在按钮范围内弹起时

        if touchEvent == touchEventEnum.TouchUp:
            print "============= touch up  ========="
            if self.mHeldTime:
                self.Time=self.mHeldTime
            if self.mIsDoubleClick:  #按第2个键触发
                if self.mBagInfo[args["ButtonPath"]]["slot"]=='itemBtn3' and self.type_UI=='ui':

                    return
                if self.stop_item():
                    return
                fromSlot=self.mBagInfo[self.mLastTouchButton]["slot"]
                fromItem=self.mBagInfo[self.mLastTouchButton]["item"]

                self.fromItem_ls=copy.deepcopy( fromItem )
                toSlot=self.mBagInfo[args["ButtonPath"]]["slot"]
                toItem=self.mBagInfo[args["ButtonPath"]]["item"]
                self.toItem_ls=copy.deepcopy( toItem )
                if self.type_UI=='ui' and fromSlot=='itemBtn3' and toItem!=None:
                    return
                
                elif  self.type_UI=='ui' and fromSlot=='itemBtn3' and toItem==None:
                    comp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLevelId())
                    musicId = comp.PlayCustomMusic("random.anvil_use", (1,1,1), 1, 1, False, playerId)
                    self.mBagInfo['/panel/zhaohuan/itemBtn1']["item"]=None
                    self.mBagInfo['/panel/zhaohuan/itemBtn2']["item"]=None
                    self.SetSlotUI('/panel/zhaohuan/itemBtn1',None)
                    self.SetSlotUI('/panel/zhaohuan/itemBtn2',None)


                self.mClickInterval=0
                self.mIsDoubleClick = False

                fromSlotpath=self.mSlotToPath[fromSlot]
                self.Setimage(fromSlotpath,False)
    
                if self.Time<10  and toItem and  fromItem["itemName"]==toItem["itemName"] and fromItem["auxValue"] == toItem["auxValue"]:
                    self.HandleCoalesce(clientApi.GetLocalPlayerId(),fromSlot,fromItem,toSlot,toItem)
                    
                elif  self.Time<10 or (self.Time>10 and toItem and fromItem["itemName"]!=toItem["itemName"] ):
                
                    self.OnItemSwap(clientApi.GetLocalPlayerId(),fromSlot,fromItem,toSlot,toItem)
                elif   self.Time>10 and ((toItem and  fromItem["itemName"]==toItem["itemName"] and fromItem["auxValue"] == toItem["auxValue"]) or not toItem):     
                    
                    self.fenduan(clientApi.GetLocalPlayerId(),fromSlot,fromItem,toSlot,toItem)
                self.Time=None
                self.SetVisible(self.mLastTouchButton+"/progress_fd" , False)
            self.mHeldTime=None
 
        # 按钮按下时
        elif touchEvent == touchEventEnum.TouchDown:
            print "============= touch down  =========\n"
            # 释放技能
            # nkkqf:arms1
            if self.slotId==self.mBagInfo[args["ButtonPath"]]["slot"]:
                return
            if self.mClickInterval > 0 and self.mLastTouchButton != args["ButtonPath"]:
                self.mIsDoubleClick = True
                return
            fromItem=self.mBagInfo[args["ButtonPath"]]["item"]
            if fromItem:  #当有物品触发
                self.IsMove=copy.deepcopy(fromItem)

                self.mClickInterval=2
                self.image_button = False
                self.mHeldTime = 0
                self.mLastTouchButton = args["ButtonPath"]
                self.showItemInfoBox(fromItem)
               
                self.Setimage(self.mLastTouchButton,True)
        elif touchEvent == touchEventEnum.TouchCancel:# 按钮按下后移出按钮范围抬起鼠标时触发回调
            if self.mHeldTime:
                self.Time=self.mHeldTime
            self.mHeldTime = None

            self.stop_item()
           
        elif touchEvent == touchEventEnum.TouchMoveOut:# 鼠标按下后移出按钮触发回调
            if self.mHeldTime:
                self.Time=self.mHeldTime
            self.mHeldTime = None
        
        elif touchEvent == touchEventEnum.TouchMoveIn:# 鼠标按下后移出按钮触发回调
            if self.IsMove:
                if not self.MoveList.get(args["ButtonPath"]) and not self.mBagInfo[args["ButtonPath"]]["item"] and args["ButtonPath"]!=self.mLastTouchButton \
                   and  (self.mBagInfo[args["ButtonPath"]]["slot"]!='itemBtn3' and self.type_UI=='ui'):
                    self.setmoveitem(args["ButtonPath"])


    def setmoveitem(self,ButtonPath):
        zcount=self.IsMove["count"]

        if zcount>=len(self.MoveList)+1:
            self.MoveList[ButtonPath]=None
            count=zcount//len(self.MoveList)

            for i in self.MoveList.keys():
                self.MoveList[i]=copy.deepcopy(self.IsMove)
                self.MoveList[i]["count"]=count
            self.start_item()
                
    def start_item(self):
        if self.IsMove:
            if len(self.MoveList.keys())>=2:
                for path,data in  self.MoveList.items():
                    self.mBagInfo[path]["item"]=data
                    self.SetSlotUI(path,data)
                    zcount=self.IsMove["count"]
                    
                    self.SetSlotUI(path,self.mBagInfo[path]["item"])

                scount=zcount%len(self.MoveList)
                if scount:
                    data=copy.deepcopy(self.IsMove)
                    data["count"]=scount
                else:
                    data=None
                self.mBagInfo[self.mLastTouchButton]["item"]=data
                self.SetSlotUI(self.mLastTouchButton,data)


    def stop_item(self):
        print "停止"
        if self.IsMove:
            if len(self.MoveList.keys())>=2:
                data_={}
                for path,data in self.MoveList.items():
                    data_[self.mBagInfo[path]["slot"]]=data

                zcount=self.IsMove["count"]
                scount=zcount%len(self.MoveList)
                if scount:
                    data=copy.deepcopy(self.IsMove)
                    data["count"]=scount
                else:
                    data={}
                data_[self.mBagInfo[self.mLastTouchButton]["slot"]]=data

                client.NotifyToServer("spwan_item",{"data":data_,'playerId':playerId,'order':True,"use_way":self.use_way,
                                                    
                                                    "archives":self.archives,"dimension":self.dimension,"pos":self.pos})

                self.MoveList={}
                self.IsMove=False

                self.Setimage(self.mLastTouchButton,False)
                self.mLastTouchButton=None
                self.mIsDoubleClick = False
                self.mClickInterval=0
                self.Time=None
                return True

            self.MoveList={}
            self.IsMove=False
            

    def is_empty_item(self,itemDict, zeroCountIsEmp=True):
        """
        判断物品是否是空物品。

        :param itemDict: 物品信息字典
        :param zeroCountIsEmp: 是否把数量为0的物品视为空物品
        :return: 是空物品则返回True，否则返回False
        """
        return not itemDict \
            or (zeroCountIsEmp and itemDict.get('count', 1) <= 0) \
            or ('newItemName' not in itemDict and 'itemName' not in itemDict) \
            or (not itemDict.get('newItemName', "") and not itemDict.get('itemName', "")) \
            or itemDict.get('newItemName', "") == "minecraft:air" \
            or itemDict.get('itemName', "") == "minecraft:air"

    def setSingleItemFlyAnimation(self, itemDict, fromPos, toPos, uiSize, num=0):
        """
        设置单个物品飞行动画。

        :param itemDict: 物品信息字典
        :param fromPos: 起点坐标
        :param toPos: 终点坐标
        :param uiSize: 格子尺寸
        :param num: 动画序号
        """
        if self.is_empty_item(itemDict, False):
            return
        itemName = itemDict['newItemName']
        aux = itemDict['newAuxValue']
        isEnchanted = bool(itemDict['enchantData'] or itemDict['modEnchantData'])
        userData = itemDict['userData']
        # ItemRenderer不够用时克隆新的ItemRenderer（初始只有1个ItemRenderer用于物品飞行动画，但同时使用的ItemRenderer可能是多个）
        if num > len(self.flyItem) - 1:
            name = str(num)
            if self.Clone(UI_PATH_FLY_ITEM_1, "/item_fly_panel", name):
                newIR = self.GetBaseUIControl("/item_fly_panel/" + name).asItemRenderer()
                self.flyItem.append(newIR)
        # 配置ItemRenderer
        useItemRenderer = self.flyItem[num]
        useItemRenderer.SetUiItem(itemName, aux, isEnchanted, userData)
        useItemRenderer.SetVisible(True)
        useItemRenderer.SetPosition(fromPos)
        useItemRenderer.SetSize(uiSize, True)
        # 动画持续时间
        dur = 30 * 0.175
        # x轴上每帧的偏移量
        xOff = (toPos[0] - fromPos[0]) / dur
        # y轴上每帧的偏移量
        yOff = (toPos[1] - fromPos[1]) / dur
        # 添加进动画执行队列
        self.itemFlyData.append({
            'xOff': xOff,
            'yOff': yOff,
            'tick': int(dur),
            'uiCtrl': useItemRenderer
        })

    def setMultipleItemFlyAnimation(self, itemAnimDataList):
        """
        设置多个物品飞行动画。动画数据列表中的各个数据均为一个字典，以下是对该字典各个key的说明：
        【itemDict】: 物品信息字典
        【from】: 起点格子对应的槽位
        【to】: 终点格子对应的槽位
        【fromType】: 起点格子类型
        【toType】: 终点格子类型

        :param itemAnimDataList: 动画数据列表
        """
        for i, data in enumerate(itemAnimDataList):
            itemDict = data['itemDict']
            if self.is_empty_item(itemDict, False):
                continue
            fromIndex = data['from']
            toIndex = data['to']
            fromType = data['fromType']
            toType = data['toType']
            # 获取起点格子的坐标

            fromPath=self.mSlotToPath[fromIndex]
           
            fromPos = self.get_ui_position(fromPath)
            uiSize = self.GetBaseUIControl(fromPath).GetSize()
            if fromType == "result":
                uiSize = (uiSize[0] * 0.6, uiSize[1] * 0.6)
            # 获取终点格子的坐标
            toPath=self.mSlotToPath[toIndex]
            toPos = self.get_ui_position( toPath)
            self.setSingleItemFlyAnimation(itemDict, fromPos, toPos, uiSize, i)

    def Update(self):
        """
        node tick function
        """
        super(PyClientScreen, self).Update()
        # tips透明度动画
        if self.alphaTick:
            self.alphaTick -= 1
            alpha = self.alphaTick / 30.0
            self.tipsImg.SetAlpha(alpha)
            self.tipsLabel.SetAlpha(alpha)

        # 更新长按分堆
        self.tick+=1
   
        if self.mHeldTime is not None:
            self.mHeldTime += 1
            if self.mHeldTime >= 10:
                self.SetProgressiveBar()
        if self.mFlyAnimationTime > 0:
            self.mFlyAnimationTime -= 1
            for flyImg in self.mFlyImgPool:
                if flyImg.IsUsing():
                    self.SetPosition(flyImg.GetPath(), flyImg.UpdateCurPosition())
                    if self.mFlyAnimationTime == 0:
                        flyImg.Release()
                        self.SetVisible(flyImg.GetPath(), False)
        
        # 物品飞行动画
        for _, data in enumerate(self.itemFlyData):
            x = data['xOff']
            y = data['yOff']
            uiCtrl = data['uiCtrl']
            pos = uiCtrl.GetPosition()
            uiCtrl.SetPosition((pos[0] + x, pos[1] + y))
            data['tick'] -= 1
            # 动画结束
            if not data['tick']:
                uiCtrl.SetVisible(False)
                self.itemFlyData.remove(data)

    def Setimage(self, path,key):  #显示首先框
        if path:
            self.SetVisible(path+"/selectedImg", key)

    def fenduan(self,PlayerId, fromSlot, fromItem, toSlot, toItem): #分堆
        comp = clientApi.GetEngineCompFactory().CreateItem(clientApi.GetLevelId())
        BasicInfo=comp.GetItemBasicInfo(fromItem["newItemName"])
        BasicInfo=BasicInfo["maxStackSize"]
        if toItem and toItem["count"]==BasicInfo:
            return
        give=int(self.mTakePercent*fromItem["count"])
        if not toItem:
            toItem=dict(fromItem)
            toItem["count"]=0
        fr,to=self.Handle_fd(give,toItem["count"],BasicInfo)

        fromItem["count"]=fromItem["count"]-give+fr

        toItem["count"]=to
        self.OnItemSwap(PlayerId,fromSlot,toItem,toSlot,fromItem,True)

    def Handle_fd(self,give,toItem,BasicInfo):#分堆结果
        
        count_ft=give+toItem
        if count_ft>BasicInfo:
            fromItem=count_ft-BasicInfo
            toItem=BasicInfo
        else:
            fromItem=0
            toItem=count_ft
        
        return fromItem,toItem
    def Handle(self,fromItem,toItem,BasicInfo): #合堆结果
        count_ft=fromItem["count"]+toItem["count"]
        if toItem["count"]==BasicInfo:
            pass
        elif count_ft>BasicInfo:
            fromItem["count"]=BasicInfo
            toItem["count"]=count_ft-BasicInfo
            
        elif count_ft<=BasicInfo:
            fromItem["count"]=count_ft
            toItem=None
        
        return fromItem,toItem

    def HandleCoalesce(self,PlayerId, fromSlot, fromItem, toSlot, toItem):   #合堆
        comp = clientApi.GetEngineCompFactory().CreateItem(clientApi.GetLevelId())
        BasicInfo=comp.GetItemBasicInfo(fromItem["newItemName"])
        BasicInfo=BasicInfo["maxStackSize"]
        if BasicInfo==1:
            self.OnItemSwap(PlayerId,fromSlot,fromItem,toSlot,toItem)
            return
        if toItem["count"]==BasicInfo:
            return
        fromItem,toItem=self.Handle(fromItem,toItem,BasicInfo)
        if not toItem or fromItem["count"] != toItem["count"]:
            self.OnItemSwap(PlayerId,fromSlot,fromItem,toSlot,toItem)

    def bianhua(self):
        '''锻造台变化'''
        
        itemBtn1=copy.deepcopy(self.mBagInfo['/panel/zhaohuan/itemBtn1']["item"])
        itemBtn2=copy.deepcopy(self.mBagInfo['/panel/zhaohuan/itemBtn2']["item"])
        if itemBtn1 and itemBtn2:
            key1=(itemBtn1['itemName'],itemBtn2['itemName'])
            key2=(itemBtn2['itemName'],itemBtn1['itemName']) 
        else:
            self.mBagInfo['/panel/zhaohuan/itemBtn3']["item"]=None
            self.SetSlotUI('/panel/zhaohuan/itemBtn3',None)
            if itemBtn1 or  itemBtn2:
                self.show_ui('/panel/image(0)',True)
            else:
                self.show_ui('/panel/image(0)',False)

            return
        if duanzaopeifang.get(key1):
            if duanzaopeifang.get(key1).get('durability'):
                itemBtn1['durability']=duanzaopeifang.get(key1)['durability']

            itemBtn1['itemName']=duanzaopeifang.get(key1)['itemName']
            itemBtn1['newItemName']=duanzaopeifang.get(key1)['itemName']
            itemBtn1['count']=1


            self.mBagInfo['/panel/zhaohuan/itemBtn3']["item"]=itemBtn1
            self.SetSlotUI('/panel/zhaohuan/itemBtn3',itemBtn1)
            self.show_ui('/panel/image(0)',False)

        elif duanzaopeifang.get(key2):
            if duanzaopeifang.get(key2).get('durability'):
                itemBtn1['durability']=duanzaopeifang.get(key1)['durability']
            itemBtn1['itemName']=duanzaopeifang.get(key2)['itemName']
            itemBtn1['newItemName']=duanzaopeifang.get(key2)['itemName']
            itemBtn1['count']=1

            self.mBagInfo['/panel/zhaohuan/itemBtn3']["item"]=itemBtn1
            self.SetSlotUI('/panel/zhaohuan/itemBtn3',itemBtn1)
            self.show_ui('/panel/image(0)',False)



        else:
            self.mBagInfo['/panel/zhaohuan/itemBtn3']["item"]=None
            self.SetSlotUI('/panel/zhaohuan/itemBtn3',None)
            self.show_ui('/panel/image(0)',True)



        
       


    def SetSlotUI(self, path, item):  #显示渲染等操作
        if path in ['/panel/zhaohuan/itemBtn1','/panel/zhaohuan/itemBtn2']:
            comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
            comp.AddTimer(0.1,self.bianhua)
            
        if item and item.get("count"):
            # 设置耐久
            self.SetDurabilityBar(path, item)
            # 设值附魔
            isEnchant = False
            if item.get("enchantData") or item.get("modEnchantData"):
                isEnchant = True
            userData = item.get("userData")
            self.SetUiItem(path + "/itemImg", item["itemName"], item.get("auxValue",0), isEnchant, userData)
            self.SetVisible(path + "/itemImg", True)
            if item["count"] > 1:
                self.SetText(path + "/itemImg/itemNum", str(item["count"]))
            else:
                self.SetText(path + "/itemImg/itemNum", "")   #数字
        else:
            self.SetVisible(path + "/itemImg", False)  #渲染
            self.SetVisible(path + "/durabilityBar", False)  #耐久
            self.SetText(path + "/itemImg/itemNum", "")

    def SetDurabilityBar(self, path, item):
        """设置目标槽位耐久度UI"""
        durabilityRatio = self.CaculateDurabilityRatio(item)
        
        if durabilityRatio != 1:
            barPath = path + "/durabilityBar"

            progressBarUIControl = self.GetBaseUIControl(barPath).asProgressBar()
            progressBarUIControl.SetValue(durabilityRatio)

            # progressBarUIControl.SetValue(durabilityRatio)
       
            self.SetVisible(barPath, True)
        else:
            self.SetVisible(path + "/durabilityBar", False)


    def CaculateDurabilityRatio(self, itemDict):
        """计算耐久度比例，用于显示耐久度槽"""
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        basicInfo = itemComp.GetItemBasicInfo(itemDict.get("itemName", ""), itemDict.get("auxValue", 0))
        if basicInfo:
            currentDurability = itemDict.get("durability")
            if currentDurability is None:
                return 1
            maxDurability = basicInfo.get("maxDurability", 0)
            if maxDurability != 0:
                return currentDurability * 1.0 / maxDurability
        return 1



    def SetProgressiveBar(self):
        """设置长按分堆进度条"""
        if not self.mLastTouchButton:
            return
        item = self.mBagInfo[self.mLastTouchButton]["item"]
        if not item:
            return
        
        self.CaculateProgressiveRatio(item)
        barPath1 =self.mLastTouchButton + "/progress_fd"

        progressBarUIControl = self.GetBaseUIControl(barPath1).asProgressBar()
        progressBarUIControl.SetValue(self.mTakePercent)

        self.SetVisible(barPath1 , True)


        self.stop_item()



    def CaculateProgressiveRatio(self, itemDict):
        if self.mHeldTime is None:
            return
        heldTime = self.mHeldTime - 10
        if heldTime > 20:
            self.mTakePercent = 1
            return
        totalNum = itemDict.get("count")
        takeNum = heldTime * totalNum / 20
        if takeNum == 0:
            takeNum = 1
            self.mHeldTime = takeNum * 20 / totalNum + 10
        self.mTakePercent = takeNum * 1.0 / totalNum


    # 界面的一些初始化操作
    def Init(self,args):
        pass


