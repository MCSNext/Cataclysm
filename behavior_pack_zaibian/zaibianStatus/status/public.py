# -*- coding: utf-8 -*-

import zaibianStatus.storage as storage
import mod.client.extraClientApi as clientApi


class Public(object):

    def __init__(self,entityId):
 
        self.entityId=entityId
        self.key=False
        self.clientapi=None
        self.serverapi=None


    def init(self,args):
        self.effectDuration=args["effectDuration"]
        self.effectAmplifier=args["effectAmplifier"]


    def status_start(self,cs):
        if cs:
            self.serverapi=storage.serverapi
        else:
            if not self.clientapi:
                self.clientapi=clientApi.GetSystem("zaibianStatus", "TutorialClientSystem")
        
        self.key=True
        pass

    def tick(self,sc=False):
        pass


    def status_end(self):
        self.key=False
        pass