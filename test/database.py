#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0 
'''
import pyros.restobject
import pyros.database
import config

class TestModel(pyros.database.Model):
    def __init__(self):
        super(TestModel, self).__init__('test', ['valor1_test', 'valor2_test'])
        pass 

class Test(pyros.restobject.RestObject):
    def GET(self):
        model = TestModel()
        results = model.list_all()
        string = ''
        for data in results:
            string += 'valor1: ' + data.valor1_test.__str__() + ' valor2: ' + data.valor2_test
        return string