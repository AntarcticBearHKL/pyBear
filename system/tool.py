import pyBear.bear as bear

import os
import ctypes

def clearScreen():
    os.system('clear')

def loadCLib(libname):
    return ctypes.CDLL(libname)

def judge(conditionList):
    if conditionList.count(False) == 0:
        return True
    return False
