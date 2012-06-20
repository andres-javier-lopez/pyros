#coding: utf-8

'''
Created on 13/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''
import web
import json

def check_connection():
    if(Database.main is None):
        return False
    else:
        return True

class DatabaseError(Exception):
    pass

class DatasetError(DatabaseError):
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
        if(Database.main is not None):
            self.db = Database.main.get_connection()
        else:
            raise DatabaseError(u'No esta definida una conexión con la base de datos')
        self.table = table
        self.fields = fields
        self._test = _test
        
    def list_all(self, where = None, order = None):
        if(self.table is None):
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
    
    def get(self, id_data):
        if(self.table is None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []):
            fields = '*'
        else:
            fields = web.db.sqllist(self.fields)
        where = 'id_' + self.table + ' = ' + id_data
        result = self.db.select(self.table, what = fields, where = where, _test = self._test )
        return result[0]        
    
    def insert(self, values):
        vals = []
        for key  in values.keys():
            vals.append( '$'+key )
        query = 'INSERT INTO ' + self.table + ' (' + web.db.sqllist(values.keys()) + ') VALUES (' + web.db.sqllist(vals) + ')'
        self.db.query(query, vars=values, _test = self._test)
    
    def update(self, id_data, values):
        vals = []
        for key  in values.keys():
            vals.append( key +' = $'+key )
        query = 'UPDATE ' + self.table + ' SET ' + web.db.sqllist(vals) + ' WHERE `id_' + self.table + '` = ' + id_data
        self.db.query(query, vars=values, _test = self._test)
    
    def delete(self, id_data):
        pass
    

class Dataset(object):
    def __init__(self, fields, json_data=None, index=None):
        self.fields = fields
        self.values = {}
                
        if(json_data is not None):
            self._loadJSON(json_data, index)
        else:
            self.json_data = {}
    
    def _loadJSON(self, json_data, index=None, strict=True):
        try:
            self.json_data = json.loads(json_data)
        except ValueError:
            self.json_data = {}
            raise DatasetError(u'No se pudo decodificar el JSON')
            
        if(index is None):
            self._loadData(self.json_data, strict)
        else:
            self._loadData(self.json_data[index], strict)
    
    def _loadData(self, data, strict=True):
        for field in self.fields:
            try:
                self.values[field] = data[field]
            except KeyError:
                if(strict is True):
                    raise DatasetError(u'El campo ' + field + ' no fue proporcionado')
            
    def _readData(self):
        return self.values
            
    def getFrom(self, table, id_data):
        model = Model(table, self.fields)
        data = model.get(id_data)
        self._loadData(data)
        return self._readData()
        
    def insertTo(self, table):
        if(len(self.values) == 0):
            raise DatasetError(u'Dataset vacío')
        
        model = Model(table, self.fields)
        model.insert(self.values)
        return True
    
    def updateIn(self, table, id_data, data):
        if(len(self.values) == 0):
            self.getFrom(table, id_data)
        self._loadJSON(data, strict=False)
        model = Model(table, self.fields)
        model.update(id_data, self.values)
        return True
        
class Datamap(object):
    def __init__(self, table, fields=[], where=None):
        self.table = table
        self.where = where
        self.joins = []
        self.fields = fields
        self.model = Model(self.table, self.fields)
        
    def add_join(self, datamap, join_field = None, tag = None):
        if(not isinstance(datamap, Datamap)):
            raise DatabaseError(u'Se agregó un objeto diferente de Datamap al join')
        if(tag is None):
            tag = datamap.table
        self.joins.append({'datamap': datamap, 'tag': tag, 'join_field': join_field})
    
    def add_where(self, where):
        self.where = where
       
    def read(self):
        main_list = self.model.list_all(where=self.where)
        for element in main_list:
            for sub in self.joins:
                submap = sub['datamap']
                where = sub['join_field'] + ' = ' + getattr(element, sub['join_field']).__str__()
                submap.add_where(where)
                setattr(element, sub['tag'], submap.read())
        return main_list
    
    def getElement(self, id_element):
        data = self.model.get(id_element)
        for sub in self.joins:
            submap = sub['datamap']
            where = sub['join_field'] + ' = ' + getattr(data, sub['join_field']).__str__()
            submap.add_where(where)
            setattr(data, sub['tag'], submap.read())
        return data
        