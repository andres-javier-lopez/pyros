#coding: utf-8

u"""Operaciones de base de datos.
copyright: Klan Estudio 2013 - klanestudio.com 
license: GNU Lesser General Public License
author: Andrés Javier López <ajavier.lopez@gmail.com>
"""

import web
import json

def check_connection():
    u"""Comprueba si la conexión esta activa y devuelve True o False"""
    if(Database.main is None):
        return False
    else:
        return True

class DatabaseError(Exception):
    u"""Error estándar de base de datos"""
    pass

class DatasetError(DatabaseError):
    u"""Error provocado en el Dataset"""
    pass

class Database(object):
    u"""Realiza la conexión con la base de datos"""
    main = None
        
    def __init__(self, config):
        u"""Crea la conexión con la base de datos"""
        self.db = web.database(dbn=config['dbn'], user = config['user'], pw = config['password'], db = config['database'])
        
    def get_connection(self):
        u"""Devuelve un objeto con la conexión a la base de datos"""
        return self.db
    
    @staticmethod
    def initialize(config):
        u"""Inicializa la configuración de la conexión"""
        Database.main = Database(config)
        
    @staticmethod
    def get_static_connection():
        u"""Devuelve el objeto de la conexión a la base de datos de forma estática"""
        return Database.main.get_connection()
        
class Table(object):
    u"""Datos generales de una Tabla"""
    def __init__(self, table="", primary="", fields = None, readfields = None, joined = None, suffix=""):
        u"""Inicializa los datos de la tabla"""
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
        u"""Agrega otra tabla como una relación a la tabla existente."""
        self.relations.append({"data": tabledata, "field": join_field, "key": join_key, "tag": tag})
        
class BaseModel(object):
    u"""Crea modelos derivados y herencia múltiple"""
    def __init__(self, **kwargs):
        u"""Finaliza la herencia de constructores"""
        ## Finaliza el MRO
        pass
    
    def read(self, **kwargs):
        u"""Finaliza la herencia del método read"""
        assert not hasattr(super(BaseModel, self), 'read')
    
    def joined_read(self, **kwargs):
        u"""Finaliza la herencia del método joined_read"""
        assert not hasattr(super(BaseModel, self), 'joined_read')
    
    def get(self, id_data, **kwargs):
        u"""Finaliza la herencia del método get"""
        assert not hasattr(super(BaseModel, self), 'get')
    
    def joined_get(self, id_data, **kwargs):
        u"""Finaliza la herencia del método joined_get"""
        assert not hasattr(super(BaseModel, self), 'joined_get')
    
    def insert(self, values, **kwargs):
        u"""Finaliza la herencia del método insert"""
        assert not hasattr(super(BaseModel, self), 'insert')
    
    def update(self, id_data, values, **kwargs):
        u"""Finaliza la herencia del método update"""
        assert not hasattr(super(BaseModel, self), 'update')
    
    def delete(self, id_data, **kwargs):
        u"""Finaliza la herencia del método delete"""
        assert not hasattr(super(BaseModel, self), 'delete')
    
class Model(BaseModel):
    u"""Proporciona las operaciones estándar para la base de datos"""
    def __init__(self, table, primary = 'id', fields = [], suffix = '', _test = False, **kwargs):
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
        super(Model, self).__init__(table = table, primary = primary, fields = fields, suffix = suffix, _test = _test, **kwargs)
        
    def _process_fields(self, fields):
        u"""Reemplaza los sufijos en los campos de la tabla"""
        for field in fields:
            clean = field[:field.find('#s')]
            self.field_keys[clean] = self._suffix(field, False)
            
    def _get_field(self, key):
        u"""Encuentra el nombre correcto de un campo y lo devuelve como cadena de texto"""
        try:
            field = self.field_keys[key]
        except KeyError:
            field = key
        return field
        
    def _suffix(self, str_val, alias=True):
        u"""Aplica el sufijo a una variable y devuelve la cadena de texto de la variable reemplazada"""
        ## No funciona en grupo es necesario aplicarla individualmente a cada campo
        if(str_val is not None):
            if(alias and ' AS ' not in str_val and ' as ' not in str_val):
                aliasstr =  str_val.replace('#s', '').replace(self.table + '.', '')
                replace = self.suffix + ' AS ' + aliasstr
                str_val = str_val.replace('#s', replace)                
            else:
                str_val = str_val.replace('#s', self.suffix)
        return str_val
                
    def read(self, where = None, order = None, **kwargs):
        u"""Consulta los elementos de la tabla en la base de datos y los devuelve como una lista"""
        super(Model, self).read(where=where, order=order, **kwargs)
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
                setattr(data, key, unicode(getattr(data, key)))
            rows.append(data)
        return rows
    
    def joined_read(self, joined, where = None, order = None, **kwargs):
        u"""Consulta los elementos de la tabla leyendo los valores de join y los devuelve como una lista"""
        super(Model, self).joined_read(joined=joined, where=where, order=order, **kwargs)
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
                setattr(data, key, unicode(getattr(data, key)))
            rows.append(data)
        return rows
    
    def get(self, id_data, **kwargs):
        u"""Obtiene un registro específico de una tabla y lo devuelve como un diccionario"""
        super(Model, self).get(id_data, **kwargs)
        if(self.table is None):
            raise DatabaseError(u'No se definió una tabla en el modelo')
        if(self.fields == []):
            fields = '*'
        else:
            fields = map(self._suffix, self.fields)
            fields = web.db.sqllist(fields)
        
        where = unicode(self.primary + ' = ' + web.db.sqlquote(id_data))
        result = self.db.select(self.table, what = fields, where = self._suffix(where, False), _test = self._test )
        if(len(result) == 1):
            data = result[0]
            for key in self.fields:
                key = key.replace('#s', '')
                setattr(data, key, unicode(getattr(data, key)))
            return data
        else:
            return {}
        
    def joined_get(self, id_data, joined, **kwargs):
        u"""Obtiene un registro específico de una tabla junto con sus campos join y lo devuelve como un diccionario"""
        super(Model, self).joined_get(id_data, joined=joined, **kwargs)
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
        sql = "SELECT " + fields + " FROM " + self.table + join_cond + " WHERE " + self.table + '.' + self._suffix(self.primary, False) + " = " + unicode(web.db.sqlquote(id_data))
        result = self.db.query(sql)
        if(len(result) == 1):
            data = result[0]
            for key in self.fields:
                key = key.replace('#s', '')
                setattr(data, key, unicode(getattr(data, key)))
            return data
        else:
            return {}
    
    def insert(self, values, **kwargs):
        u"""Ingresa un registro a la tabla"""
        super(Model, self).insert(values, **kwargs)
        vals = []
        for key  in values.keys():
            vals.append( '$'+key )
        query = 'INSERT INTO ' + self.table + ' (' + web.db.sqllist(map(self._get_field, values.keys())) + ') VALUES (' + web.db.sqllist(vals) + ')'
        self.db.query(query, vars=values, _test = self._test)
        query = 'SELECT last_insert_id() as id;'
        data = self.db.query(query)
        id = data[0].id
        return id
    
    def update(self, id_data, values, **kwargs):
        u"""Actualiza un registro de la tabla"""
        super(Model, self).update(id_data, values, **kwargs)
        vals = []
        for key  in values.keys():
            vals.append( self._get_field(key) +' = $'+key )
        query = 'UPDATE ' + self.table + ' SET ' + web.db.sqllist(vals) + ' WHERE `' + self._suffix(self.primary, False) + '` = ' + unicode(web.db.sqlquote(id_data))
        self.db.query(query, vars=values, _test = self._test)
    
    def delete(self, id_data, **kwargs):
        u"""Elimina un registro en la tabla"""
        super(Model, self).delete(id_data, **kwargs)
        where = self._suffix(self.primary, False) + ' = $id_data'
        self.db.delete(self.table, where=where, vars={'id_data': id_data})
    

class BaseDataset(object):
    u"""Permite la creación de herencia múltiple de Dataset"""
    def __init__(self, **kwargs):
        u"""Finaliza la herencia del constructor"""
        ## Fin del MRO
        pass
    
    def add_field(self, field, value, **kwargs):
        u"""Finaliza la herencia del método add_field"""
        assert not hasattr(super(BaseDataset, self), 'add_field')
    
    def get_data(self, id_data, **kwargs):
        u"""Finaliza la herencia del método get_data"""
        assert not hasattr(super(BaseDataset, self), 'get_data')
    
    def insert(self, **kwargs):
        u"""Finaliza la herencia del método insert"""
        assert not hasattr(super(BaseDataset, self), 'insert')
    
    def update(self, id_data, **kwargs):
        u"""Finaliza la herencia del método update"""
        assert not hasattr(super(BaseDataset, self), 'update')
    
    def delete(self, id_data, **kwargs):
        u"""Finaliza la herencia del método delete"""
        assert not hasattr(super(BaseDataset, self), 'delete')

class Dataset(BaseDataset):
    u"""Simula un registro en una tabla para poder hacer inserciones y actualizaciones"""
    def __init__(self, tabledata, json_data=None, index=None, **kwargs):
        u"""Construye un registro con los datos proporcionados"""        
        self.table = tabledata.table
        self.primary = tabledata.primary
        self.fields = tabledata.fields
        self.suffix = tabledata.suffix
        self.values = {}
        super(Dataset, self).__init__(tabledata=tabledata, json_data=json_data, index=index, **kwargs)
                
        if(json_data is not None):
            self._load_JSON(json_data, index)
        else:
            self.json_data = {}
            
    def _suffix(self, str_val):
        u"""Reemplaza el sufijo en la variable proporcionada y la devuelve como una cadena de texto"""
        return str_val.replace('#s', '')
    
    def _load_JSON(self, json_data, index=None):
        u"""Carga los datos del registro proporcionados en formato JSON"""
        try:
            self.json_data = json.loads(json_data)
        except ValueError:
            self.json_data = {}
            raise DatasetError(u'No se pudo decodificar el JSON')
            
        if(index is None):
            self._load_data(self.json_data)
        else:
            self._load_data(self.json_data[index])
    
    def _load_data(self, data):
        u"""Carga los datos del registro proporcionados en un diccionario"""
        for field in self.fields:
            try:
                field = self._suffix(field)
                self.values[field] = data[field]
            except KeyError:
                pass # Ignoramos si un campo no está entre los datos
            
    def _read_data(self):
        u"""Devuelve la lista de campos y datos correspondiente al registro en un diccionario"""
        return self.values
    
    def add_field(self, field, value, **kwargs):
        u"""Agrega un nuevo campo al registro"""
        super(Dataset, self).add_field(field, value, **kwargs)
        if(not field in self.fields and not (field + '#s') in self.fields):
            self.fields.append(field)
        self.values[field] = value
            
    def get_data(self, id_data, **kwargs):
        u"""Devuelve la información del registro proporcionado como un diccionario"""
        super(Dataset, self).get_data(id_data, **kwargs)
        model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        data = model.get(id_data)
        if(data == {}):
            raise DatasetError(u'No existe el registro al que se quiere acceder')
        self._load_data(data)
        return self._read_data()
        
    def insert(self, **kwargs):
        u"""Inserta el registro a la tabla proporcionada"""
        super(Dataset, self).insert(**kwargs)
        if(len(self.values) == 0):
            raise DatasetError(u'Dataset vacío')
        
        model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        id = model.insert(self.values)
        return id
    
    def update(self, id_data, data = '', **kwargs):
        u"""Actualiza el registro en la tabla proporcionada"""
        super(Dataset, self).update(id_data, data=data, **kwargs)
        if(len(self.values) == 0):
            self.get_data(id_data)
        if(data != ''):
            self._load_JSON(data)
        model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        model.update(id_data, self.values)
        return True
    
    def delete(self, id_data, **kwargs):
        u'''Elimina el registro de la tabla proporcionada'''
        super(Dataset, self).delete(id_data, **kwargs)
        Model(self.table, self.primary).delete(id_data)

class BaseDatamap(object):
    u"""Permite la herencia múltiple de un Datamap"""
    def __init__(self, **kwargs):
        u"""Finaliza la herencia del constructor"""
        ## Fin del MRO
        pass
    
    def add_join(self, **kwargs):
        u"""Finaliza la herencia del método add_join"""
        assert not hasattr(super(BaseDatamap, self), 'add_join')
       
    def add_where(self, **kwargs):
        u"""Finaliza la herencia del método add_where"""
        assert not hasattr(super(BaseDatamap, self), 'add_where')
        
    def read(self, **kwargs):
        u"""Finaliza la herencia del método read"""
        assert not hasattr(super(BaseDatamap, self), 'read')
    
    def get_element(self, id_element, **kwargs):
        u"""Finaliza la herencia del método get_element"""
        assert not hasattr(super(BaseDatamap, self), 'get_element')

class Datamap(BaseDatamap):
    u"""Realiza un mapa de los datos de la base"""
    def __init__(self, tabledata, where=None, **kwargs):
        u"""Crea un mapa de datos de la tabla proporcionada"""        
        self.table = tabledata.table
        self.primary = tabledata.primary
        self.where = where
        self.joins = []
        self.fields = list(tabledata.fields)
        if(tabledata.primary != ''):
            self.fields.append(tabledata.primary)
        self.fields.extend(tabledata.readfields)
        self.joined = tabledata.joined
        self.suffix = tabledata.suffix
        self.model = Model(self.table, self.primary, self.fields, suffix = self.suffix)
        
        for relation in tabledata.relations:
            self.add_join(Datamap(relation["data"]), relation["field"], relation["key"], relation["tag"])
            
        super(Datamap, self).__init__(tabledata=tabledata, where=where, **kwargs)
        
    def add_join(self, datamap, join_field = None, join_key = None, tag = None, **kwargs):
        u"""Agrega un submapa a través de llaves foráneas"""
        super(Datamap, self).add_join(datamap=datamap, join_field=join_field, join_key=join_key, tag=tag, **kwargs)
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
        
    def add_where(self, field, value = None, **kwargs):
        u"""Agrega una condición de búsqueda adicional"""
        super(Datamap, self).add_where(field=field, value=value, **kwargs)
        if(value is None):
            cond = field
        else:
            cond = self.model._get_field(field) + ' = "' + value + '"'
        
        if(self.where is not None):
            assert(isinstance(self.where, basestring))
            self.where += ' AND ' + cond
        else:
            self.where = cond
       
    def read(self, **kwargs):
        u"""Lee los elementos del mapa y los retorna como una lista"""
        super(Datamap, self).read(**kwargs)
        if(self.joined is None):
            main_list = self.model.read(where=self.where)
        else:
            main_list = self.model.joined_read(self.joined, where = self.where)
        for element in main_list:
            for sub in self.joins:
                submap = sub['datamap']
                where = unicode(sub['join_field'] + ' = ' + web.db.sqlquote(getattr(element, sub['join_key']).__str__()))
                submap.set_where(where)
                setattr(element, sub['tag'], submap.read())
        return main_list
    
    def get_element(self, id_element, **kwargs):
        u"""Encuentra un elemento único dentro del mapa con el id proporcionado y lo devuelve como un diccionario"""
        super(Datamap, self).get_element(id_element, **kwargs)
        if(self.joined is None):
            data = self.model.get(id_element)
        else:
            data = self.model.joined_get(id_element, self.joined)
        if(data != {}):
            for sub in self.joins:
                submap = sub['datamap']
                where = unicode(sub['join_field'] + ' = ' + web.db.sqlquote(getattr(data, sub['join_key']).__str__()))
                submap.set_where(where)
                setattr(data, sub['tag'], submap.read())
        return data

