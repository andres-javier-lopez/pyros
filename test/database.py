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

class Test(pyros.restobject.RestObject):
    def __init__(self):
        config.check_database()
        test3 = pyros.database.Datamap('test3')
        
        test2 = pyros.database.Datamap('test2')
        test2.add_join(test3, 'id_test2', 'internos')
        
        self.datamap = pyros.database.Datamap('test', ['id_test', 'valor1_test AS valor1', 'valor2_test'])
        self.datamap.add_join(test2, 'id_test', 'subtest')
        
        self.fields_test = ['valor1_test', 'valor2_test']
        
    def read(self):
        return {'elementos': self.datamap.read()}
    
    def insert(self):
        data = pyros.database.Dataset(self.fields_test, json_data=web.data())
        result = data.insertTo('test')
        return {'success': result}
    
    def getElement(self, id_element):
        return {'elemento': self.datamap.getElement(id_element)}
    
    def updateElement(self, id_element):
        data = pyros.database.Dataset(self.fields_test)
        result = data.updateIn('test', id_element, web.data())
        return {'success': result}
    
    def deleteElement(self, id_element):
        pyros.database.Model('test').delete(id_element)
        return {'success': True}
        