#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
import pyros.restobject


class Test(pyros.restobject.RestObject):
    def GET(self):
        return "esta es una prueba"
    
    def POST(self):
        return 'probando post'
    
    def PUT(self):
        return 'probando put'
    
    def DELETE(self):
        return 'probando delete'
    
