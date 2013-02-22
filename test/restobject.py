#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
from pyros import restobject 


class Test(restobject.RestObject):
    @restobject.getall
    def listar(self):
        return "lista de elementos"
    
    @restobject.get
    def element(self, elemento):
        return "elemento: " + elemento
    
    @restobject.getlist('valores')
    def valores(self, elemento):
        return "valores de " + elemento
    
    @restobject.post
    def prueba_post(self):
        return 'probando post'
    
    @restobject.post_into()
    def prueba_post_general(self, elemento):
        return 'insertando en ' + elemento
    
    @restobject.post_into('valores')
    def prueba_post_valores(self, elemento):
        return 'insertando valores de ' + elemento
    
    @restobject.put
    def prueba_put(self):
        return "prueba put completo"
    
    @restobject.put_element
    def prueba_put_element(self, elemento):
        return "reemplaznado " + elemento
    
    @restobject.put_list('valores')
    def prueba_put_valores(self, elemento):
        return "reemplazando valores de " + elemento
    
    @restobject.delete
    def prueba_delete(self):
        return "borrando todo"
    
    @restobject.delete_element
    def prueba_delete_element(self, elemento):
        return "borrando elemento " + elemento
    
    @restobject.delete_list("valores")
    def prueba_delete_valores(self, elemento):
        return "borrando los valores de " + elemento
    
