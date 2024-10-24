# -*- coding:utf-8 -*-

class Singleton():
    def __init__(self):
        self.mServerSystem = None
        self.totalMgrDict = {}
        pass

    def get_server_system(self):
        return self.mServerSystem

    def set_server_system(self, value):
        self.mServerSystem = value

    def set_assign_system(self,key,val):
        self.totalMgrDict[key] = val

    def get_assign_system(self,key):
        return self.totalMgrDict[key]