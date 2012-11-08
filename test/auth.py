#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0 
'''
import pyros.restobject

pyros.restobject.debug_info = True

class AuthTest(pyros.restobject.RestObject):
    
    def get_auth_key(self, method):
        return '1234'
    
    def read(self):
        return self._resp('elementos', 'prueba')


