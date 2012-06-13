#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
import json

class RestObject(object):
    def GET(self):
        return json.dumps(self.read())
    
    def POST(self):
        return json.dumps(self.insert())
    
    def PUT(self):
        return json.dumps(self.replace())
    
    def DELETE(self):
        return json.dumps(self.delete())
    
    def read(self):
        pass
    
    def insert(self):
        pass
    
    def replace(self):
        pass
    
    def delete(self):
        pass
