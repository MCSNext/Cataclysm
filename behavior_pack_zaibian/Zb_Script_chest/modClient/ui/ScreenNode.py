# -*- coding: utf-8 -*-


import mod.client.extraClientApi as _clientApi


ScreenNode = _clientApi.GetScreenNodeCls()
ViewBinder = _clientApi.GetViewBinderCls()
ViewRequest = _clientApi.GetViewViewRequestCls()
ClientSystem = _clientApi.GetClientSystemCls()
ClientCompFactory = _clientApi.GetEngineCompFactory()
PLAYER_ID = _clientApi.GetLocalPlayerId()
PlayerActorRenderComp = ClientCompFactory.CreateActorRender(PLAYER_ID)
PlayerQueryVariableComp = ClientCompFactory.CreateQueryVariable(PLAYER_ID)
PlayerItemComp = ClientCompFactory.CreateItem(PLAYER_ID)
PlayerGameComp = ClientCompFactory.CreateGame(PLAYER_ID)
PlayerCameraComp = ClientCompFactory.CreateCamera(PLAYER_ID)
PlayerTextNotifyClientComp = ClientCompFactory.CreateTextNotifyClient(PLAYER_ID)
PlayerViewComp = ClientCompFactory.CreatePlayerView(PLAYER_ID)
PlayerSkyRenderComp = ClientCompFactory.CreateSkyRender(PLAYER_ID)
PlayerFogComp = ClientCompFactory.CreateFog(PLAYER_ID)
PlayerPosComp = ClientCompFactory.CreatePos(PLAYER_ID)
PlayerActorMotionComp = ClientCompFactory.CreateActorMotion(PLAYER_ID)
PlayerBlockInfoComp = ClientCompFactory.CreateBlockInfo(PLAYER_ID)
PlayerPlayerComp = ClientCompFactory.CreatePlayer(PLAYER_ID)
PlayerRotComp = ClientCompFactory.CreateRot(PLAYER_ID)
PlayerDeviceComp = ClientCompFactory.CreateDevice(PLAYER_ID)


class LYJScreenNode(ScreenNode):
    """
    自定义ScreenNode。
    新增方法：
    OnGameTick：频率与游戏实时帧率同步的Tick事件（客户端调用一次SetGameTickEnabled后生效）
    SetButtonDoubleClickCallback：设置按钮双击监听
    SetButtonMovable：设置按钮可拖动
    CancelButtonMovable：取消按钮可拖动
    SetButtonLongClickCallback：设置按钮长按监听
    RemoveButtonLongClickCallback：移除按钮长按监听
    SetLongClickVibrateTime：设置长按后震动反馈的时长
    HasLongClicked：获取按钮按下后是否触发了长按
    """
    def __init__(self, namespace, name, param):
        super(LYJScreenNode, self).__init__(namespace, name, param)
        # self.clientSystem = param['cs'] # type
        self._doubleClickTick = 0
        self._btnDoubleClickData = {}
        self._doubleClickBtnPath = ""
        self._doubleClickArgs = None
        self._fingerPos = None
        self._isMoving = False
        self._screenSize = PlayerGameComp.GetScreenSize()
        self._vibrateTime = 100
        self._btnLongClickData = {}
        self._btnTouchData = {}
        self._touchingButtonPath = ""
        self._touchingButtonArgs = {}
        self._tick = 0
        self._btnMovableData = {}
        self._btnTouchUpCallbackData = {}

    def Create(self):
        pass

    def Destroy(self):
        pass

    def OnDeactive(self):
        pass

    def OnActive(self):
        pass

    def Update(self):
        # 双击触发逻辑
        if self._doubleClickTick:
            self._doubleClickTick += 1
            if self._doubleClickTick == 11:
                self._doubleClickTick = 0
        # 长按触发逻辑
        if 1 <= self._tick <= 10:
            self._tick += 1
            if self._tick == 11 and self._touchingButtonPath in self._btnLongClickData:
                btnData = self._btnLongClickData[self._touchingButtonPath]
                btnData['longClickFunc'](self._touchingButtonArgs)
                btnData['hasLongClicked'] = True
                self._vibrate()

    def OnGameTick(self, args):
        """
        频率与游戏实时帧率同步的Tick事件（客户端调用一次SetGameTickEnabled后生效）。
        """
        pass

    def _runTouchUpList(self, args):
        touchEventEnum = _clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        # 点击坐标
        touchPos = args["TouchPosX"], args["TouchPosY"]
        # 触控在按钮范围内弹起时
        if touchEvent == touchEventEnum.TouchUp:
            bp = args['ButtonPath']
            if bp in self._btnTouchUpCallbackData:
                for func in self._btnTouchUpCallbackData[bp]:
                    func(args)
        else:
            bp = args['ButtonPath']
            if bp in self._btnTouchUpCallbackData:
                if len(self._btnTouchUpCallbackData[bp])==2:
                    self._btnTouchUpCallbackData[bp][0](args)



    # todo:=========================================== 双击逻辑 =========================================================

    def _onBtnTouchUp(self, args):
        bp = args['ButtonPath']
        if bp in self._btnDoubleClickData:
            if self._doubleClickTick and bp == self._doubleClickBtnPath:
                self._btnDoubleClickData[bp]['doubleClickCallback'](args)
                self._doubleClickTick = 0
                self._doubleClickBtnPath = ""
                self._doubleClickArgs = None
            else:
                self._doubleClickTick = 1
                self._doubleClickBtnPath = bp
                self._doubleClickArgs = args

    # noinspection PyUnresolvedReferences
    def SetButtonDoubleClickCallback(self, buttonPath, doubleClickCallback, touchUpCallback=None):
        # type: (str, function, function) -> None
        """
        设置按钮双击监听。

        :param buttonPath: 按钮路径
        :param doubleClickCallback: 按钮双击回调函数
        :param touchUpCallback: 按钮抬起回调函数
        :return: None
        """
        self._btnDoubleClickData[buttonPath] = {
            'doubleClickCallback': doubleClickCallback,
            'touchUpCallback': touchUpCallback
        }
        # btnCtrl = self.GetBaseUIControl(buttonPath).asButton()
        # btnCtrl.AddTouchEventParams()
        # btnCtrl.SetButtonTouchUpCallback(self._runTouchUpList)

        self.AddTouchEventHandler(buttonPath, self._runTouchUpList, {"isSwallow": True})

        if buttonPath not in self._btnTouchUpCallbackData:
            self._btnTouchUpCallbackData[buttonPath] = []
        if touchUpCallback and touchUpCallback not in self._btnTouchUpCallbackData[buttonPath]:
            self._btnTouchUpCallbackData[buttonPath].append(touchUpCallback)
        self._btnTouchUpCallbackData[buttonPath].append(self._onBtnTouchUp)

    # todo:=========================================== 拖动逻辑 =========================================================

    def _testPosIsOut(self, pos, buttonSize):
        if pos[1] < 0:
            pos[1] = 0
        if pos[0] < 0:
            pos[0] = 0
        if pos[1] + buttonSize[1] > self._screenSize[1]:
            pos[1] = self._screenSize[1] - buttonSize[1]
        if pos[0] + buttonSize[0] > self._screenSize[0]:
            pos[0] = self._screenSize[0] - buttonSize[0]

    def _setWidgetPosition(self, widgetControl, offset, widgetSize):
        origPos = widgetControl.GetPosition()
        newPos = [origPos[0] + offset[0], origPos[1] + offset[1]]
        self._testPosIsOut(newPos, widgetSize)
        widgetControl.SetPosition(tuple(newPos))

    def _onMove(self, args):
        touchX = args['TouchPosX']
        touchY = args['TouchPosY']
        buttonPath = args['ButtonPath']
        if buttonPath not in self._btnMovableData:
            return
        moveParent = self._btnMovableData[buttonPath]['moveParent']
        associatedWidgetPath = self._btnMovableData[buttonPath]['associatedWidgetPath']
        touchMoveCallback = self._btnMovableData[buttonPath]['touchMoveCallback']
        self._isMoving = True
        if not self._fingerPos:
            self._fingerPos = (touchX, touchY)
        offset = (touchX - self._fingerPos[0], touchY - self._fingerPos[1])
        self._fingerPos = (touchX, touchY)
        if not moveParent:
            buttonControl = self.GetBaseUIControl(buttonPath)
            buttonSize = buttonControl.GetSize()
            self._setWidgetPosition(buttonControl, offset, buttonSize)
        else:
            buttonName = buttonPath.split("/")[-1]
            parentPath = buttonPath.split("/" + buttonName)[0]
            parentControl = self.GetBaseUIControl(parentPath)
            parentSize = parentControl.GetSize()
            self._setWidgetPosition(parentControl, offset, parentSize)
        for path in associatedWidgetPath:
            associatedWidgetControl = self.GetBaseUIControl(path)
            associatedWidgetSize = associatedWidgetControl.GetSize()
            self._setWidgetPosition(associatedWidgetControl, offset, associatedWidgetSize)
        if touchMoveCallback:
            touchMoveCallback(args)

    def SetButtonMovable(self, btnPath, moveParent, associatedWidgetPath=(), touchMoveCallback=None):
        # type: (ButtonUIControl, bool, tuple, function) -> None
        """
        设置按钮可拖动。

        :param btnPath: 按钮路径
        :param moveParent: 是否同时拖动父控件
        :param associatedWidgetPath: 关联拖动的其他控件的路径，多个控件请使用元组
        :param touchMoveCallback: 按钮的TouchMoveCallback
        :return: None
        """
        self._isMoving = False
        self._fingerPos = None
        if not isinstance(associatedWidgetPath, tuple):
            associatedWidgetPath = (associatedWidgetPath,)
        self._btnMovableData[btnPath] = {
            'moveParent': moveParent,
            'associatedWidgetPath': associatedWidgetPath,
            'touchMoveCallback': touchMoveCallback
        }
        btn = self.GetBaseUIControl(btnPath).asButton()
        btn.AddTouchEventParams()
        btn.SetButtonTouchMoveCallback(self._onMove)

    def CancelButtonMovable(self, buttonControl):
        # type: (ButtonUIControl) -> None
        """
        取消按钮可拖动。

        :param buttonControl: 按钮的ButtonUIControl实例
        :return: None
        """
        buttonControl.SetButtonTouchMoveCallback(None)

    # todo:=========================================== 长按逻辑 =========================================================

    def _onTouchUp(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._tick = 0

    def _onTouchCancel(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._tick = 0
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchCancelFunc']:
                touchData['touchCancelFunc'](args)

    def _onTouchMoveOut(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._tick = 0
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchMoveOutFunc']:
                touchData['touchMoveOutFunc'](args)

    def _onTouchDown(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._touchingButtonArgs = args
            self._touchingButtonPath = btnPath
            self._tick = 1
            self._btnLongClickData[btnPath]['hasLongClicked'] = False
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchDownFunc']:
                touchData['touchDownFunc'](args)

    def _vibrate(self):
        PlayerDeviceComp.SetDeviceVibrate(self._vibrateTime)

    def SetButtonLongClickCallback(self, btnPath, longClickFunc, touchUpFunc=None, touchMoveOutFunc=None,
                                   touchDownFunc=None, touchCancelFunc=None):
        # type: (str, function, function, function, function, function) -> None
        """
        设置按钮长按监听。

        :param btnPath: 按钮路径
        :param longClickFunc: LongClick回调函数
        :param touchCancelFunc: TouchCancel回调函数
        :param touchDownFunc: TouchDown回调函数
        :param touchMoveOutFunc: TouchMoveOut回调函数
        :param touchUpFunc: TouchUp回调函数
        :return: None
        """
        self._btnLongClickData[btnPath] = {
            'longClickFunc': longClickFunc,
            'hasLongClicked': False
        }
        self._btnTouchData[btnPath] = {
            'touchMoveOutFunc': touchMoveOutFunc,
            'touchDownFunc': touchDownFunc,
            'touchCancelFunc': touchCancelFunc
        }
        btn = self.GetBaseUIControl(btnPath).asButton()
        btn.AddTouchEventParams()
        btn.SetButtonTouchMoveOutCallback(self._onTouchCancel)
        btn.SetButtonTouchDownCallback(self._onTouchDown)
        btn.SetButtonTouchCancelCallback(self._onTouchMoveOut)
        btn.SetButtonTouchUpCallback(self._runTouchUpList)
        if btnPath not in self._btnTouchUpCallbackData:
            self._btnTouchUpCallbackData[btnPath] = []
        self._btnTouchUpCallbackData[btnPath].append(self._onTouchUp)
        if touchUpFunc and touchUpFunc not in self._btnTouchUpCallbackData[btnPath]:
            self._btnTouchUpCallbackData[btnPath].append(touchUpFunc)

    def RemoveButtonLongClickCallback(self, btnPath):
        # type: (str) -> None
        """
        移除按钮长按监听。

        :param btnPath: 按钮路径
        :return: None
        """
        if btnPath in self._btnLongClickData:
            del self._btnLongClickData[btnPath]

    def SetLongClickVibrateTime(self, time):
        # type: (int) -> None
        """
        设置长按后震动反馈的时长。

        :param time: 毫秒
        :return: None
        """
        self._vibrateTime = time

    def HasLongClicked(self, bp):
        # type: (str) -> bool
        """
        获取按钮按下后是否触发了长按。

        :param bp: 按钮路径
        :return: 若按钮已经触发长按则返回True，否则返回False
        """
        if bp in self._btnLongClickData:
            return self._btnLongClickData[bp]['hasLongClicked']
        else:
            return False























