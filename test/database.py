#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0 
'''
import pyros.restobject
import pyros.database
import config

class Test(pyros.restobject.RestObject):
    def __init__(self):
        config.check_database()
        
    def read(self):
        datamap = pyros.database.Datamap('test')
        datamap.addJoin('test2', 'id_test')
        return datamap.read()