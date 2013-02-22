#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
from pyros import restobject 


class Test(restobject.RestObject):
    @restobject.get_all
    def listar(self):
        return "lista de elementos"
    
    @restobject.get
    def element(self, elemento):
        return "elemento: " + elemento
    
    @restobject.get_list("valores")
    def valores(self, elemento):
        return "valores de " + elemento
    
    @restobject.post
    def prueba_post(self):
        return "insertando elemento"
    
    @restobject.post_into
    def prueba_post_general(self, elemento):
        return "insertando en " + elemento
    
    @restobject.post_list("valores")
    def prueba_post_valores(self, elemento):
        return "insertando valores de " + elemento
    
    @restobject.put_all
    def prueba_put(self):
        return "reemplazando todo"
    
    @restobject.put
    def prueba_put_element(self, elemento):
        return "reemplazando " + elemento
    
    @restobject.put_list("valores")
    def prueba_put_valores(self, elemento):
        return "reemplazando valores de " + elemento
    
    @restobject.delete_all
    def prueba_delete(self):
        return "borrando todo"
    
    @restobject.delete
    def prueba_delete_element(self, elemento):
        return "borrando elemento " + elemento
    
    @restobject.delete_list("valores")
    def prueba_delete_valores(self, elemento):
        return "borrando los valores de " + elemento
    
