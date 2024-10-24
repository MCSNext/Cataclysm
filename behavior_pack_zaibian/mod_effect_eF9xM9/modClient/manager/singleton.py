# -*- coding:utf-8 -*-

class Singleton():
    def __init__(self):
        self.mClientSystem = None
        self.totalMgrDict = {}
        pass

    def get_client_system(self):
        return self.mClientSystem

    def set_client_system(self, value):
        self.mClientSystem = value

    def set_assign_system(self,key,val):
        self.totalMgrDict[key] = val

    def get_assign_system(self,key):
        return self.totalMgrDict[key]