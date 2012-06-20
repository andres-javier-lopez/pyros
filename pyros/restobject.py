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
        if(element is None or element == '/'):
            return self._response(self.read())
        else:
            return self._response(self.getElement(self._prepareId(element)))
    
    def POST(self, element=None):
        if(element is None or element == '/'):
            return self._response(self.insert())
        else:
            return self._response(self.insertInto(self._prepareId(element)))
    
    def PUT(self, element=None):
        if(element is None or element == '/'):
            return self._response(self.replace())
        else:
            return self._response(self.updateElement(self._prepareId(element)))
    
    def DELETE(self, element=None):
        if(element is None or element == '/'):
            return self._response(self.delete())
        else:
            return self._response(self.deleteElement(self._prepareId(element)))
    
    def _response(self, data):
        web.header('Content-Type', 'application/json')
        return json.dumps(data)
    
    def _prepareId(self, string):
        return string.replace('/', '')
    
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
