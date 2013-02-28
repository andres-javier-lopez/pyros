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
        
class Table(object):
    u"""Datos generales de una Tabla"""
    def __init__(self, table="", primary="", fields = None, readfields = None, joined = None, suffix=""):
        self.table = table
        self.primary = primary
        if fields is not None:
            self.fields = fields
        else:
            self.fields = []
        if readfields is not None:
            self.readfields = readfields
        else:
            self.readfields = []
        self.joined = joined
        self.relations = []
        self.suffix = suffix
        
    def add_relation(self, tabledata, join_field = None, join_key = None, tag = None):
        self.relations.append({"data": tabledata, "field": join_field, "key": join_key, "tag": tag})
    
class Model(object):
    u"""Proporciona las operaciones estándar para la base de datos"""
    def __init__(self, table, primary = 'id', fields = [], suffix = '', _test = False):
        u"""Inicializa la conexión y los valores del modelo"""
        if(Database.main is not None):
            self.db = Database.main.get_connection()
        else:
            raise DatabaseError(u'No esta definida una conexión con la base de datos')
        self.table = table
        self.primary = primary
        self.fields = fields
        self.field_keys = {}
        if(suffix == ''):
            suffix = '_' + table
        self.suffix = suffix
        self._process_fields(fields)        
        self._test = _test
        
    def _process_fields(self, fields):
        for field in fields:
            clean = field[:field.find('#s')]
            self.field_keys[clean] = self._suffix(field, False)
            
    def _get_field(self, key):
        try:
            field = self.field_keys[key]
        except KeyError:
            field = key
        return field
        
    def _suffix(self, str_val, alias=True):
        ## No funciona en grupo es necesario aplicarla individualmente a cada campo
        if(str_val is not None):
            if(alias and ' AS ' not in str_val and ' as ' not in str_val):
                aliasstr =  str_val.replace('#s', '').replace(self.table + '.', '')
                replace = self.suffix + ' AS ' + aliasstr
                str_val = str_val.replace('#s', replace)                
            else:
                str_val = str_val.replace('#s', self.suffix)
        return str_val
                
    def read(self, where = None, order = None):
        u"""Lista de elementos de una tabla"""
        if(self.table is None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []): 
            fields = '*'
        else: # Agregar automaticamente el campo primary
            fields = map(self._suffix, self.fields)
            fields = web.db.sqllist(fields)

        result = self.db.select(self.table, what = fields, where = self._suffix(where, False), order = self._suffix(order, False), _test = self._test )
        rows = []
        for data in result:
            for key in self.fields:
                key = key.replace('#s', '')
                setattr(data, key, str(getattr(data, key)))
            rows.append(data)
        return rows
    
    def joined_read(self, joined, where = None, order = None):
        u"""Read especial que permite hacer joins entre tablas"""
        if(self.table is None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []): 
            table_fields = ['*']
        else: # Agregar automaticamente el campo primary
            table_fields = []
            for field in self.fields:
                table_fields.append(self.table + '.' + field)
        
        join_cond = ''
        for table in joined:
            join_fields = table['fields']
            for field in join_fields:
                table_fields.append(table['table'] + "." + field)
            join_cond += " LEFT JOIN " + table['table'] + " ON " + table["cond"]
        
        table_fields = map(self._suffix, table_fields)
        fields = web.db.sqllist(table_fields)
        sql = "SELECT " + fields + " FROM " + self.table + join_cond
        if(where is not None):
            sql += " WHERE " + self._suffix(where, False)
        if(order is not None):
            sql += " ORDER BY " + self._suffix(order, False)
        result = self.db.query(sql)
        rows = []
        for data in result:
            for key in self.fields:
                key = key.replace('#s', '')
                setattr(data, key, str(getattr(data, key)))
            rows.append(data)
        return rows
    
    def get(self, id_data):
        u"""Obtiene un registro específico de una tabla"""
        if(self.table is None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []):
            fields = '*'
        else:
            fields = map(self._suffix, self.fields)
            fields = web.db.sqllist(fields)
        
        where = self.primary + ' = "' + id_data + '"'
        result = self.db.select(self.table, what = fields, where = self._suffix(where, False), _test = self._test )
        if(len(result) == 1):
            data = result[0]
            for key in self.fields:
                key = key.replace('#s', '')
                setattr(data, key, str(getattr(data, key)))
            return data
        else:
            return {}
        
    def joined_get(self, id_data, joined):
        u"""Read especial que permite hacer joins entre tablas"""
        if(self.table is None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []): 
            table_fields = ['*']
        else: # Agregar automaticamente el campo primary
            table_fields = []
            for field in self.fields:
                table_fields.append(self.table + '.' + field)
        
        join_cond = ''
        for table in joined:
            join_fields = table['fields']
            for field in join_fields:
                table_fields.append(table['table'] + "." + field)
            join_cond += " LEFT JOIN " + table['table'] + " ON " + table["cond"]
        
        table_fields = map(self._suffix, table_fields)
        fields = web.db.sqllist(table_fields)
        sql = "SELECT " + fields + " FROM " + self.table + join_cond + " WHERE " + self.table + '.' + self._suffix(self.primary, False) + " = '" + id_data + "'"
        result = self.db.query(sql)
        if(len(result) == 1):
            data = result[0]
            for key in self.fields:
                key = key.replace('#s', '')
                setattr(data, key, str(getattr(data, key)))
            return data
        else:
            return {}
    
    def insert(self, values):
        u"""Ingresa un registro a la tabla"""
        vals = []
        for key  in values.keys():
            vals.append( '$'+key )
        query = 'INSERT INTO ' + self.table + ' (' + web.db.sqllist(map(self._get_field, values.keys())) + ') VALUES (' + web.db.sqllist(vals) + ')'
        self.db.query(query, vars=values, _test = self._test)
    
    def update(self, id_data, values):
        u"""Actualiza un registro de la tabla"""
        vals = []
        for key  in values.keys():
            vals.append( self._get_field(key) +' = $'+key )
        query = 'UPDATE ' + self.table + ' SET ' + web.db.sqllist(vals) + ' WHERE `' + self._suffix(self.primary, False) + '` = "' + id_data + '"'
        self.db.query(query, vars=values, _test = self._test)
    
    def delete(self, id_data):
        u"""Elimina un registro en la tabla"""
        where = self._suffix(self.primary, False) + ' = $id_data'
        self.db.delete(self.table, where=where, vars={'id_data': id_data})
    

class Dataset(object):
    u"""Simula un registro en una tabla para poder hacer inserciones y actualizaciones"""
    def __init__(self, tabledata, json_data=None, index=None):
        u"""Construye un registro con los datos proporcionados"""        
        self.table = tabledata.table
        self.primary = tabledata.primary
        self.fields = tabledata.fields
        self.suffix = tabledata.suffix
        self.values = {}
                
        if(json_data is not None):
            self._load_JSON(json_data, index)
        else:
            self.json_data = {}
            
    def _suffix(self, str_val):
        return str_val.replace('#s', '')
    
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
                field = self._suffix(field)
                self.values[field] = data[field]
            except KeyError:
                if(strict):
                    raise DatasetError(u'El campo ' + field + ' no fue proporcionado')
            
    def _read_data(self):
        u"""Devuelve la lista de campos y datos correspondiente al registro"""
        return self.values
    
    def add_field(self, field, value):
        u"""Agrega un nuevo campo al registro"""
        if(not field in self.fields and not (field + '#s') in self.fields):
            self.fields.append(field)
        self.values[field] = value
            
    def get_data(self, id_data):
        u"""Carga la información del registro proporcionado"""
        model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        data = model.get(id_data)
        if(data == {}):
            raise DatasetError(u'No existe el registro al que se quiere acceder')
        self._load_data(data)
        return self._read_data()
        
    def insert(self):
        u"""Inserta el registro a la tabla proporcionada"""
        if(len(self.values) == 0):
            raise DatasetError(u'Dataset vacío')
        
        model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        model.insert(self.values)
        return True
    
    def update(self, id_data, data = ''):
        u"""Actualiza el registro en la tabla proporcionada"""
        if(len(self.values) == 0):
            self.get_data(id_data)
        if(data != ''):
            self._load_JSON(data, strict=False)
        model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        model.update(id_data, self.values)
        return True
    
    def delete(self, id_data):
        Model(self.table, self.primary).delete(id_data)

class Datamap(object):
    u"""Objeto para realizar mapeo de datos"""
    def __init__(self, tabledata, where=None):
        u"""Crea un mapa de datos de la tabla proporcionada"""        
        self.table = tabledata.table
        self.primary = tabledata.primary
        self.where = where
        self.joins = []
        self.fields = list(tabledata.fields)
        self.fields.append(tabledata.primary)
        self.fields.extend(tabledata.readfields)
        self.joined = tabledata.joined
        self.suffix = tabledata.suffix
        self.model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        
        for relation in tabledata.relations:
            self.add_join(Datamap(relation["data"]), relation["field"], relation["key"], relation["tag"])
        
    def add_join(self, datamap, join_field = None, join_key = None, tag = None):
        u"""Agrega un submapa a través de llaves foráneas"""
        if(not isinstance(datamap, Datamap)):
            raise DatabaseError(u'Se agregó un objeto diferente de Datamap al join')
        if(tag is None):
            tag = datamap.table
        if(join_field is None):
            join_field = self.primary
        if(join_key is None):
            join_key = join_field
            
        self.joins.append({'datamap': datamap, 'tag': tag, 'join_field': join_field, 'join_key': join_key})
    
    def set_where(self, where):
        u"""Establece una condición de búsqueda"""
        self.where = where
        
    def add_where(self, field, value = None):
        u"""Agrega una condición de búsqueda adicional"""
        if(value is None):
            cond = field
        else:
            cond = self.model._get_field(field) + ' = "' + value + '"'
        
        if(self.where is not None):
            assert(isinstance(self.where, basestring))
            self.where += ' AND ' + cond
        else:
            self.where = cond
       
    def read(self):
        u"""Devuelve la lista completa de los elementos del mapa"""
        if(self.joined is None):
            main_list = self.model.read(where=self.where)
        else:
            main_list = self.model.joined_read(self.joined, where = self.where)
        for element in main_list:
            for sub in self.joins:
                submap = sub['datamap']
                where = sub['join_field'] + ' = "' + getattr(element, sub['join_key']).__str__() + '"'
                submap.set_where(where)
                setattr(element, sub['tag'], submap.read())
        return main_list
    
    def get_element(self, id_element):
        u"""Devuelve un único elemento en el mapa con el id proporcionado"""
        if(self.joined is None):
            data = self.model.get(id_element)
        else:
            data = self.model.joined_get(id_element, self.joined)
        if(data != {}):
            for sub in self.joins:
                submap = sub['datamap']
                where = sub['join_field'] + ' = "' + getattr(data, sub['join_key']).__str__() + '"'
                submap.set_where(where)
                setattr(data, sub['tag'], submap.read())
        return data

