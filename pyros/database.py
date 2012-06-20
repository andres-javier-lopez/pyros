#coding: utf-8

u"""Operaciones de base de datos."""
## @copyright: TuApp.net - GNU Lesser General Public License
## @author: Andrés Javier López <ajavier.lopez@gmail.com>

import web
import json

def check_connection():
    u"""Comprueba la conexión activa"""
    if(Database.main is None):
        return False
    else:
        return True

class DatabaseError(Exception):
    u"""Error local de base de datos"""
    pass

class DatasetError(DatabaseError):
    u"""Error provocado en el Dataset"""
    pass

class Database(object):
    u"""Conexión general a la base de datos"""
    main = None
        
    def __init__(self, config):
        u"""Creación de la conexión"""
        self.db = web.database(dbn=config['dbn'], user = config['user'], pw = config['password'], db = config['database'])
        
    def get_connection(self):
        u"""Devuelve la conexión activa"""
        return self.db
    
    @staticmethod
    def initialize(config):
        u"""Inicializa la configuración de la conexión"""
        Database.main = Database(config)
    
class Model(object):
    u"""Proporciona las operaciones estándar para la base de datos"""
    def __init__(self, table, fields = [], _test = False):
        u"""Inicializa la conexión y los valores del modelo"""
        if(Database.main is not None):
            self.db = Database.main.get_connection()
        else:
            raise DatabaseError(u'No esta definida una conexión con la base de datos')
        self.table = table
        self.fields = fields
        self._test = _test
        
    def list_all(self, where = None, order = None):
        u"""Lista de elementos de una tabla"""
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
        u"""Obtiene un registro específico de una tabla"""
        if(self.table is None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []):
            fields = '*'
        else:
            fields = web.db.sqllist(self.fields)
        where = 'id_' + self.table + ' = ' + id_data
        result = self.db.select(self.table, what = fields, where = where, _test = self._test )
        if(len(result) == 1):
            return result[0]
        else:
            return {}
    
    def insert(self, values):
        u"""Ingresa un registro a la tabla"""
        vals = []
        for key  in values.keys():
            vals.append( '$'+key )
        query = 'INSERT INTO ' + self.table + ' (' + web.db.sqllist(values.keys()) + ') VALUES (' + web.db.sqllist(vals) + ')'
        self.db.query(query, vars=values, _test = self._test)
    
    def update(self, id_data, values):
        u"""Actualiza un registro de la tabla"""
        vals = []
        for key  in values.keys():
            vals.append( key +' = $'+key )
        query = 'UPDATE ' + self.table + ' SET ' + web.db.sqllist(vals) + ' WHERE `id_' + self.table + '` = ' + id_data
        self.db.query(query, vars=values, _test = self._test)
    
    def delete(self, id_data):
        u"""Elimina un registro en la tabla"""
        where = 'id_' + self.table + ' = $id_data'
        self.db.delete(self.table, where=where, vars={'id_data': id_data})
    

class Dataset(object):
    u"""Simula un registro en una tabla para poder hacer inserciones y actualizaciones"""
    def __init__(self, fields, json_data=None, index=None):
        u"""Construye un registro con los datos proporcionados"""
        self.fields = fields
        self.values = {}
                
        if(json_data is not None):
            self._load_JSON(json_data, index)
        else:
            self.json_data = {}
    
    def _load_JSON(self, json_data, index=None, strict=True):
        u"""Obtiene datos del registro proporcionados en formato JSON"""
        try:
            self.json_data = json.loads(json_data)
        except ValueError:
            self.json_data = {}
            raise DatasetError(u'No se pudo decodificar el JSON')
            
        if(index is None):
            self._load_data(self.json_data, strict)
        else:
            self._load_data(self.json_data[index], strict)
    
    def _load_data(self, data, strict=True):
        u"""Obtiene datos del registro proporcionados en un diccionario"""
        for field in self.fields:
            try:
                self.values[field] = data[field]
            except KeyError:
                if(strict):
                    raise DatasetError(u'El campo ' + field + ' no fue proporcionado')
            
    def _read_data(self):
        u"""Devuelve la lista de campos y datos correspondiente al registro"""
        return self.values
    
    def add_field(self, field, value):
        u"""Agrega un nuevo campo al registro"""
        self.fields.append(field)
        self.values[field] = value
            
    def get_from(self, table, id_data):
        u"""Carga la información del registro proporcionado"""
        model = Model(table, self.fields)
        data = model.get(id_data)
        self._load_data(data)
        return self._read_data()
        
    def insert_to(self, table):
        u"""Inserta el registro a la tabla proporcionada"""
        if(len(self.values) == 0):
            raise DatasetError(u'Dataset vacío')
        
        model = Model(table, self.fields)
        model.insert(self.values)
        return True
    
    def update_in(self, table, id_data, data):
        u"""Actualiza el registro en la tabla proporcionada"""
        if(len(self.values) == 0):
            self.get_from(table, id_data)
        self._load_JSON(data, strict=False)
        model = Model(table, self.fields)
        model.update(id_data, self.values)
        return True
        
class Datamap(object):
    u"""Objeto para realizar mapeo de datos"""
    def __init__(self, table, fields=[], where=None):
        u"""Crea un mapa de datos de la tabla proporcionada"""
        self.table = table
        self.where = where
        self.joins = []
        self.fields = fields
        self.model = Model(self.table, self.fields)
        
    def add_join(self, datamap, join_field = None, tag = None):
        u"""Agrega un submapa a través de llaves foráneas"""
        if(not isinstance(datamap, Datamap)):
            raise DatabaseError(u'Se agregó un objeto diferente de Datamap al join')
        if(tag is None):
            tag = datamap.table
        self.joins.append({'datamap': datamap, 'tag': tag, 'join_field': join_field})
    
    def add_where(self, where):
        u"""Establece una condición de búsqueda"""
        self.where = where
       
    def read(self):
        u"""Devuelve la lista completa de los elementos del mapa"""
        main_list = self.model.list_all(where=self.where)
        for element in main_list:
            for sub in self.joins:
                submap = sub['datamap']
                where = sub['join_field'] + ' = ' + getattr(element, sub['join_field']).__str__()
                submap.add_where(where)
                setattr(element, sub['tag'], submap.read())
        return main_list
    
    def get_element(self, id_element):
        u"""Devuelve un único elemento en el mapa con el id proporcionado"""
        data = self.model.get(id_element)
        if(data != {}):
            for sub in self.joins:
                submap = sub['datamap']
                where = sub['join_field'] + ' = ' + getattr(data, sub['join_field']).__str__()
                submap.add_where(where)
                setattr(data, sub['tag'], submap.read())
        return data
        