#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
import web

def check_connection():
    if(Database.main == None):
        return False
    else:
        return True

class DatabaseError(Exception):
    pass

class Database(object):
    main = None
        
    def __init__(self, config):
        self.db = web.database(dbn=config['dbn'], user = config['user'], pw = config['password'], db = config['database'])
        
    def get_connection(self):
        return self.db
    
    @staticmethod
    def initialize(config):
        Database.main = Database(config)
    
class Model(object):
    def __init__(self, table, fields = [], _test = False):
        if(Database.main != None):
            self.db = Database.main.get_connection()
        else:
            raise DatabaseError(u'No esta definida una conexión con la base de datos')
        self.table = table
        self.fields = fields
        self._test = _test
        
    def list_all(self, where = None, order = None):
        if(self.table == None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []):
            fields = '*'
        else:
            fields = web.db.sqllist(self.fields)
        result = self.db.select(self.table, what = fields, where = where, order = order, _test = self._test )
        rows = []
        for data in result:
            rows.append(data)
        return rows        
    
    def get(self, id):
        pass
    
    def insert(self, dataset):
        pass
    
    def update(self, dataset):
        pass
    
    def delete(self, id):
        pass
    

class Dataset(object):
    def __init__(self):
        pass
        
class Datamap(object):
    pass