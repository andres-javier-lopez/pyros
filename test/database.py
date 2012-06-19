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
        
    def read(self):
        test3 = pyros.database.Datamap('test3')
        
        test2 = pyros.database.Datamap('test2')
        test2.add_join(test3, 'id_test2', 'internos')
        
        datamap = pyros.database.Datamap('test', ['id_test', 'valor1_test AS valor1'])
        datamap.add_join(test2, 'id_test', 'subtest')
        
        return datamap.read()
    
    def insert(self):
        data = pyros.database.Dataset(web.data(), ['valor1_test', 'valor2_test'])
        result = data.insertTo('test')
        return {'success': result}