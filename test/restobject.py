#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
import pyros.restobject


class Test(pyros.restobject.RestObject):
    def GET(self, element=None):
        return "esta es una prueba"
    
    def POST(self, element=None):
        return 'probando post'
    
    def PUT(self, element=None):
        return 'probando put'
    
    def DELETE(self, element=None):
        return 'probando delete'
    
