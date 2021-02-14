import sys,os

import pyBear.bear as bear

def writeU(path, content):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    node = open(path, 'w', encoding='utf-8')
    node.write(content)
    node.close()

def readU(path):
    if not os.path.exists(path):
        print('File: ' + path + ' Not Exist')
        return ''
    node = open(path, 'r', encoding='utf-8').read()
    ret = node.read()
    node.close()
    return ret

def writeB(path, content):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    node = open(path, 'wb')
    node.write(content)
    node.close()

def readB(path):
    if not os.path.exists(path):
        print('File: ' + path + ' Not Exist')
        return ''
    node = open(path, 'rb')
    ret = retf.read()
    node.close()
    return ret

def read(path):
    try:
        return readU(path)
    except:
        return readB(path)

write = writeU


def createFile(path):
    Write(path, '')

createDirectory = os.makedirs


def list(path):
    return os.listdir(path)

def listDetail(path):
    ret = {}
    for node in flist(path):
        if os.path.isfile(fjoin(path, node)):
            ret[node] = 'file'
        else:
            ret[node] = 'directory'
    return ret


def removefile(path):
    if fexists(path):
        os.remove(path)
        return True
    else:
        return False

def removeDirectory(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

rename = os.rename

exists = os.path.exists
join = os.path.join

isFile = os.path.isfile
isDirectory = os.path.isdir
