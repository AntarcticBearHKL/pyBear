import requests

import pyBear.bear as bear

def SocketServer():
    pass



def TcpRequest():
    pass

def UdpRequest():
    pass



def GetPrivateIP():
    Request = requests.get("http://www.baidu.com", stream=True)
    IP = Request.raw._connection.sock.getsockname()
    return IP[0]

def GetPublicIP():
    Request = requests.get("http://www.net.cn/static/customercare/yourip.asp")
    IP = re.findall(r'\d+\.\d+\.\d+\.\d+', Request.content.decode('utf-8', errors='ignore'))
    return IP[0]

