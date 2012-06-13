#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0 
'''
import pyros.restobject
import pyros.database
import config

config.check_database()

class TestModel(pyros.database.Model):
    def __init__(self):
        super(TestModel, self).__init__('test', ['valor1_test', 'valor2_test']) 

class Test(pyros.restobject.RestObject):
    def read(self):
        model = TestModel()
        results = model.list_all()
        return results