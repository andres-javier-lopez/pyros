#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
from pyros import restobject, auth

class Start(object):
    def GET(self,a,b):
        return "Pruebas de funcionamiento de PyROS"

class Basic(restobject.RestObject):
    @restobject.get_all
    def listar(self):
        return self._resp("mensaje", "lista de elementos")
    
    @restobject.get
    def element(self, elemento):
        return self._resp("mensaje", "elemento: " + elemento)
    
    @restobject.get_list("valores")
    def valores(self, elemento):
        return self._resp("mensaje", "valores de " + elemento)
    
    @restobject.post
    def prueba_post(self):
        return self._resp("mensaje", "insertando elemento")
    
    @restobject.post_into
    def prueba_post_general(self, elemento):
        return self._resp("mensaje", "insertando en " + elemento)
    
    @restobject.post_list("valores")
    def prueba_post_valores(self, elemento):
        return self._resp("mensaje", "insertando valores de " + elemento)
    
    @restobject.put_all
    def prueba_put(self):
        return self._resp("mensaje", "reemplazando todo")
    
    @restobject.put
    def prueba_put_element(self, elemento):
        return self._resp("mensaje", "reemplazando " + elemento)
    
    @restobject.put_list("valores")
    def prueba_put_valores(self, elemento):
        return self._resp("mensaje", "reemplazando valores de " + elemento)
    
    @restobject.delete_all
    def prueba_delete(self):
        return self._resp("mensaje", "borrando todo")
    
    @restobject.delete
    def prueba_delete_element(self, elemento):
        return self._resp("mensaje", "borrando elemento " + elemento)
    
    @restobject.delete_list("valores")
    def prueba_delete_valores(self, elemento):
        return self._resp("mensaje", "borrando los valores de " + elemento)

class SimpleAuth1(auth.Auth):
    def __init__(self):
        self.key = "1234"
        
class SimpleAuth2(auth.Auth):
    def __init__(self):
        super(SimpleAuth2, self).__init__("1234")

class SimpleAuth3(auth.Auth):
    def __init__(self):
        self.key = "1234"
        self.algorithm = self.DEFAULT_ALGORITHM
        
class SimpleAuth4(auth.Auth):
    def __init__(self):
        self.key = "1234"
        self.algorithm = auth.Auth.DEFAULT_ALGORITHM

class Authenticated(restobject.RestObject):
    @auth.auth(SimpleAuth1)
    @restobject.get_all
    def prueba_autenticacion(self):
        return self._resp("mensaje", "autorizado GET")
    
    @auth.auth(SimpleAuth2)
    @restobject.post
    def prueba_auth_post(self):
        return self._resp("mensaje", "autorizado POST")
    
    @auth.auth(SimpleAuth3)
    @restobject.put_all
    def prueba_auth_put(self):
        return self._resp("mensaje", "autorizado PUT")
    
    @auth.auth(SimpleAuth4)
    @restobject.delete_all
    def prueba_auth_del(self):
        return self._resp("mensaje", "autorizado DELETE")
    
credentials = {'username': 'hola', 'password': 'mundo'}
class HTTPAuth(restobject.RestObject):
    @auth.http_auth(credentials)
    @restobject.get_all
    def prueba_autenticacion_get(self):
        return self._resp("mensaje", "autorizado GET por HTTP")
    
    @auth.http_auth(credentials)
    @restobject.post
    def prueba_autenticacion_post(self):
        return self._resp("mensaje", "autorizado POST por HTTP")
    
    @auth.http_auth(credentials)
    @restobject.put_all
    def prueba_autenticacion_put(self):
        return self._resp("mensaje", "autorizado PUT por HTTP")
    
    @auth.http_auth(credentials)
    @restobject.delete_all
    def prueba_autenticacion_delete(self):
        return self._resp("mensaje", "autorizado DELETE por HTTP")
