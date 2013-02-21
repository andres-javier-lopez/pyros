#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
from pyros.restobject import RestObject, get, getall, getlist, post, post_into


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
    
    @post
    def prueba_post(self):
        return 'probando post'
    
    @post_into()
    def prueba_post_general(self, elemento):
        return 'insertando en ' + elemento
    
    @post_into('valores')
    def prueba_post_valores(self, elemento):
        return 'insertando valores de ' + elemento
    
    def PUT(self, element=None):
        return 'probando put'
    
    def DELETE(self, element=None):
        return 'probando delete'
    
