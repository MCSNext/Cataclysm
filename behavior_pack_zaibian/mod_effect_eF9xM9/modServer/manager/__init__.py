# -*- coding:utf-8 -*-

from mod_effect_eF9xM9.modServer.manager import singleton
mSingleton = singleton.Singleton()  # 所有的单例管理类


def get_singleton():
    return mSingleton
