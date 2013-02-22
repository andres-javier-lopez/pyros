#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0 
'''
import config
import web
import definitions
from pyros import restobject, database

restobject.debug_info = True

class Test(restobject.RestObject):
    def __init__(self):
        super(Test, self).__init__()
        config.check_database()
        self.datamap = database.Datamap(definitions.test1)
        
    @restobject.get_all
    def read(self):
        return self._resp('elementos', self.datamap.read())
    
    @restobject.post
    def insert(self):
        data = database.Dataset(definitions.test1, json_data=web.data())
        result = data.insert()
        return self._resp_success(result)
    
    @restobject.get
    def get_element(self, id_element):
        return self._resp('elemento', self.datamap.get_element(id_element))
    
    @restobject.post_into
    def insert_into(self, id_element):
        if(self.datamap.get_element(id_element) == {}):
            return self._resp_error(u'No existe la colección en la que se quiere insertar el objeto')
        data = database.Dataset(definitions.test2, json_data=web.data())
        data.add_field('id_test', id_element)
        result = data.insert()
        return self._resp_success(result)
    
    @restobject.put
    def update_element(self, id_element):
        data = database.Dataset(definitions.test1)
        result = data.update(id_element, web.data())
        return self._resp_success(result)
    
    @restobject.delete
    def delete_element(self, id_element):
        database.Dataset(definitions.test1).delete(id_element)
        return self._resp_success(True)

class SubTest(restobject.RestObject):
    @restobject.get
    def get_element(self, id_element):
        self.datamap = database.Datamap(definitions.test2)
        return self._resp('elemento', self.datamap.get_element(id_element))
    
    @restobject.delete
    def delete_element(self, id_element):
        database.Dataset(definitions.test2).delete(id_element)
        return self._resp_success(True)
    
