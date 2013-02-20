#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
from pyros.restobject import RestObject, get, getall, getlist


class Test(RestObject):
    @getall
    def listar(self):
        return "lista de elementos"
    
    @get
    def element(self, elemento):
        return "elemento: " + elemento
    
    @getlist('valores')
    def valores(self, elemento):
        return "valores de " + elemento
    
    def POST(self, element=None):
        return 'probando post'
    
    def PUT(self, element=None):
        return 'probando put'
    
    def DELETE(self, element=None):
        return 'probando delete'
    
