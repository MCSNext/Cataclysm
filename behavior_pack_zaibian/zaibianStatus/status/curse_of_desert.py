
from zaibianStatus.status.public import Public
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
class curse_of_desert(Public):

    def __init__(self,entityId):
        super(curse_of_desert, self).__init__(entityId)
        self.tick_=0
    def status_start(self,cs):
        super(curse_of_desert,self).status_start(cs)

        if self.clientapi:
            self.disorganized_state = True
            comp = clientApi.GetEngineCompFactory().CreateOperation(self.entityId)
            comp.SetCanMove(False)
        else:
            self.serverapi.ListenForEvent("zaibianStatus", "TutorialClientSystem", "PlayerMotionClientEvent", self, self.PlayerMotionClientEvent)
        

    def PlayerMotionClientEvent(self,args):
        motionComp = serverApi.GetEngineCompFactory().CreateActorMotion(args["playerId"])
        motionComp.SetPlayerMotion(args["motion"])

    def tick(self,sc=False):
        if sc==False :
            comp = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())
            left, up = comp.GetInputVector()
            rot = clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).GetRot()
            if not rot:
                return
            rot = (0,rot[1])
            upMotionVector = clientApi.GetDirFromRot(rot)
            upMotion = (upMotionVector[0]*up,0,upMotionVector[2]*up)
            if left>=0:
                rot = (0,rot[1]-90)
            else:
                rot = (0,rot[1]+90)
            leftMotionVector = clientApi.GetDirFromRot(rot)
            leftMotionVector = (leftMotionVector[0]*left,0,leftMotionVector[2]*left)
            leftMotion = (leftMotionVector[0]*left,0,leftMotionVector[2]*left)
            motion = comp.GetMotion()
            # print motion
            inputMotion = ((upMotion[0] + leftMotion[0]) * -0.2, motion[1]-0.1, (upMotion[2] + leftMotion[2]) * -0.2)
            comp.SetMotion(inputMotion)
            self.clientapi.NotifyToServer("PlayerMotionClientEvent", {"playerId":clientApi.GetLocalPlayerId(),"motion":inputMotion})

    def status_end(self):
        super(curse_of_desert,self).status_end()
        if self.clientapi:
            self.disorganized_state = False
            def f():
                comp = clientApi.GetEngineCompFactory().CreateOperation(self.entityId)
                # 不响应移动
                if not comp.SetCanMove(True) and self.entityId ==clientApi.GetLocalPlayerId(): 
                    comp = clientApi.GetEngineCompFactory().CreateGame(self.entityId)
                    comp.AddTimer(0.5,f)
            comp = clientApi.GetEngineCompFactory().CreateGame(self.entityId)
            comp.AddTimer(0,f)
        else:
            self.serverapi.UnListenForEvent("zaibianStatus", "TutorialClientSystem", "PlayerMotionClientEvent", self, self.PlayerMotionClientEvent)
