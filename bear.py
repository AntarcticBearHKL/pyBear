# -*- coding: utf-8 -*-  

#------------------------
#GlobalConfig:
#------------------------
testUnit = False

import time
import datetime
startTime = datetime.datetime.now()
systemTimeZone = int(int(time.strftime('%z'))/100)
defaultTimeZone = 8
def upTime():
    print(datetime.datetime.now() - startTime)


import platform
if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

elif platform.system() == "Linux":
    pass

#------------------------
#GlobalFunction:
#------------------------
def result(code, message):
    print(message)
    return code

class badBear(Exception):
    def __init__(self, solveFunction):
        self.solveFunction = solveFunction
    
    def solve(self):
        return self.solveFunction()

debug = False
def catchBadBear(fn, *args, **kwargs):
    def ret(*args, **kwargs): 
        return fn(*args, **kwargs)
        if debug:
            return fn(*args, **kwargs)
        else:
            try:
                return fn(*args, **kwargs)
            except badBear as error:
                return error.solve()    
            except Exception as otherError:
                print(otherError)
    return ret


serverList = {}
class newServer:
    def __init__(self, serverName, serverCode):
        import pyBear.mathematics.cipher as cipher
        key = input('Input Password For ' + serverName + ': ')
        if cipher.AESDecrypt(serverCode[176:], key) != 'Authenticated':
            print('Key Error')
            return None
        self.ip = cipher.AESDecrypt(serverCode[:44], key)
        self.port = int(cipher.AESDecrypt(serverCode[44:88], key))
        self.username = cipher.AESDecrypt(serverCode[88:132], key)
        self.password = cipher.AESDecrypt(serverCode[132:176], key)
        serverList[serverName] = self

def server(serverName):
    return serverList[serverName]

def generateServerCode(key, ip, port, username, password):
    import pyBear.mathematics.cipher as cipher
    ret = ''
    ret += cipher.AESEncrypt(ip, key)
    ret += cipher.AESEncrypt(port, key)
    ret += cipher.AESEncrypt(username, key)
    ret += cipher.AESEncrypt(password, key)
    ret += cipher.AESEncrypt('Authenticated', key)
    return ret
