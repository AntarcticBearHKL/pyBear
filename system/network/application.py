from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import requests
import os,sys
import json
import ssl
import re

import pyBear.bear as bear
import pyBear.system.file as filebear

def httpServer(pageLocation=None, libraryLocation=None, getHandler=None, postHandler=None, parameterAnalyst=None, port=80):
    Application( [(r".*", getHttpServerListener(pageLocation, libraryLocation, getHandler, postHandler, parameterAnalyst) ),] ).listen(port)
    IOLoop.instance().start()

def httpsServer(certificationLocation=None, pageLocation=None, libraryLocation=None, getHandler=None, postHandler=None, parameterAnalyst=None, port=443):
    if not certificationLocation:
        print('No Certification Assigned!')
        return
    HTTPServer(
        Application(
            [(r".*", getHttpServerListener(pageLocation, libraryLocation, getHandler, postHandler, parameterAnalyst)),], 
            **{
            "static_path" : filebear.join(os.path.dirname(__file__), "static"),
        }),
        ssl_options={
            "certfile": filebear.join(certificationLocation, 'crt'),
            "keyfile": filebear.join(certificationLocation, 'key'),
        }).listen(Port)
    IOLoop.instance().start()

def getHttpServerListener(pageLocation, libraryLocation, getHandler, postHandler, parameterAnalyst):
    class HTTPListener(RequestHandler):
        def get(self):
            if getHandler:
                getHandler(requestHandler(self, pageLocation, libraryLocation, parameterAnalyst))

        def post(self):
            if postHandler:
                postHandler(requestHandler(self, pageLocation, libraryLocation, parameterAnalyst))   
    return HTTPListener


class requestHandler:
    def __init__(self, connection, pageLocation, libraryLocation, parameterAnalyst):
        self.connection = connection

        self.pageLocation = pageLocation
        self.libraryLocation = libraryLocation
        self.method = self.connection.request.method
        self.path = self.connection.request.path.split('/')

        self.request = self.connection.request
        self.argument = {}
        for item in self.connection.request.arguments:
            self.argument[item] = self.connection.request.arguments[item][0].decode(encoding='utf-8')
        self.body = self.connection.request.body

        if parameterAnalyst:
            self.parameter = parameterAnalyst(self.request, self.argument, self.body)
        else:
            self.parameter = {}


    def write(self, content):
        self.connection.write(content)


    def returnPage(self):
        if len(self.path) == 1:
            self.connection.write('URL ERROR')
        if self.path[1] == '':
            self.connection.write('URL ERROR')

        filetype = self.path[1]

        if filetype == 'libcss' or filetype == 'libjs':
            filePath = self.libraryLocation
        else:
            filePath = filebear.join(self.pageLocation, filetype)

        for item in self.Path[2:]:
            filePath = filebear.join(filePath, item)

        retFile = filebear.readB(filePath)

        if filetype == 'html':
            self.connection.set_header('Content-Type', 'text/html')
        elif filetype == 'css' or filetype == 'libcss':
            self.connection.set_header('Content-Type', 'text/css')    
        elif filetype == 'javascript' or filetype == 'libjs':
            self.connection.set_header('Content-Type', 'text/javascript')
        else:
            self.connection.set_header('Content-Type', 'application/octet-stream')

        self.connection.write(retFile)


    def redirect(self, destination):
        self.connection.redirect(destination)


    def GetCookie(self):
        pass

    def SetCookie(self):
        pass


    def printRequest(self):
        print('\n\n')
        print('-------------Information---------------')
        for item in self.request.__dict__:
            print(item, ':', self.request.__dict__[item])
        print('---------------------------------------')
        for item in self.__dict__:
            print(item, ':', self.__dict__[item])
        print('---------------------------------------')



def httpGet(url, parameterData):
    parameter = '?'
    for item in parameterData:
        parameter += str(item) + '=' + parameterData[item] + '&'
    print(url+parameter)
    request = requests.get(url + parameter)
    return [request.status_code, request.text]

def httpPost(url, parameter):
    request = requests.post(url, data=json.dumps(parameter))
    return [request.status_code, request.text]
