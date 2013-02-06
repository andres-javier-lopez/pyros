#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0 
'''
import pyros.restobject
import pyros.database
import config
import web
import definitions

pyros.restobject.debug_info = True

class Test(pyros.restobject.RestObject):
    def __init__(self):
        config.check_database()
        self.datamap = pyros.database.Datamap(definitions.test1)
        
    def read(self):
        return self._resp('elementos', self.datamap.read())
    
    def insert(self):
        data = pyros.database.Dataset(definitions.test1, json_data=web.data())
        result = data.insert()
        return self._resp_success(result)
    
    def get_element(self, id_element):
        return self._resp('elemento', self.datamap.get_element(id_element))
    
    def insert_into(self, id_element):
        if(self.datamap.get_element(id_element) == {}):
            return self._resp_error(u'No existe la colección en la que se quiere insertar el objeto')
        data = pyros.database.Dataset(definitions.test2, json_data=web.data())
        data.add_field('id_test', id_element)
        result = data.insert()
        return self._resp_success(result)
    
    def update_element(self, id_element):
        data = pyros.database.Dataset(definitions.test1)
        result = data.update(id_element, web.data())
        return self._resp_success(result)
    
    def delete_element(self, id_element):
        pyros.database.Dataset(definitions.test1).delete(id_element)
        return self._resp_success(True)

