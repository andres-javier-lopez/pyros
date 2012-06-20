#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
import web
import json

class RestObject(object):
    def GET(self, element=None):
        if(element is None):
            return self.response(self.read())
        else:
            return self.response(self.getElement(element))
    
    def POST(self, element=None):
        if(element is None):
            return self.response(self.insert())
        else:
            return self.response(self.insertInto(element))
    
    def PUT(self, element=None):
        if(element is None):
            return self.response(self.replace())
        else:
            return self.response(self.updateElement(element))
    
    def DELETE(self, element=None):
        if(element is None):
            return self.response(self.delete())
        else:
            return self.response(self.deleteElement(element))
    
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
    
    def getElement(self, id_element):
        pass
    
    def insertInto(self, id_element):
        pass
    
    def updateElement(self, id_element):
        pass
    
    def deleteElement(self, id_element):
        pass
