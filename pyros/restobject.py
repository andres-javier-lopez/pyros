#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
import web
import json

class RestObject(object):
    def GET(self):
        return self.response(self.read())
    
    def POST(self):
        return self.response(self.insert())
    
    def PUT(self):
        return self.response(self.replace())
    
    def DELETE(self):
        return self.response(self.delete())
    
    def response(self, data):
        web.header('Content-Type', 'application/json')
        return json.dumps(data)
    
    def read(self):
        pass
    
    def insert(self):
        pass
    
    def replace(self):
        pass
    
    def delete(self):
        pass
