#coding: utf-8

u"""Objeto base para la creación de apliaciones REST.
copyright: Klan Estudio 2013 - klanestudio.com 
license: GNU Lesser General Public License
author: Andrés Javier López <ajavier.lopez@gmail.com>
"""

import web
import json
import traceback
import auth
from decorations import base_decorator
import inspect

debug_info = False

@base_decorator
def get(f):
    u"""Convierte la función en una petición de tipo GET que devuelve un único elemento"""
    assert(inspect.isfunction(f))
    def func(self, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'GET'
    func.type = '_default'
    return func

def get_list(type):
    u"""Convierte la función en una petición de tipo GET que devuelve una lista de subelementos"""
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        assert(inspect.isfunction(f))
        def func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        func.method = 'GET'
        func.type = type
        return func
    return sub

@base_decorator
def get_all(f):
    u"""Convierte la función en una petición de tipo GET que devuelve la lista de todos los elementos"""
    assert(inspect.isfunction(f))
    def func(self, element, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'GET'
    func.type = '_all'
    return func

@base_decorator
def post(f):
    u"""Convierte la función en una petición de tipo POST que inserta un elemento a la lista general"""
    assert(inspect.isfunction(f))
    def func(self, element, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'POST'
    func.type = '_all'
    return func

@base_decorator
def post_into(f):
    u"""Convierte la función en una petición de tipo POST que inserta un subelemento dentro de otro elemento"""
    assert(inspect.isfunction(f))
    def func(self, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'POST'
    func.type = '_default'
    return func

def post_list(type):
    u"""Convierte la función en una petición de tipo POST que inserta un elemento en una lista específica"""
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        def func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        func.method = 'POST'
        func.type = type
        return func
    return sub

@base_decorator
def put_all(f):
    u"""Convierte la función en una petición de tipo PUT que reemplaza una lista completa de elementos"""
    assert(inspect.isfunction(f))
    def func(self, element, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'PUT'
    func.type = '_all'
    return func

@base_decorator
def put(f):
    u"""Convierte la función en una petición de tipo PUT que reemplaza un solo elemento"""
    assert(inspect.isfunction(f))
    def func(self, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'PUT'
    func.type = '_default'
    return func

def put_list(type):
    u"""Convierte la función en una petición de tipo PUT que reemplaza una lista específica de elementos"""
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        assert(inspect.isfunction(f))
        def func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        func.method = 'PUT'
        func.type = type
        return func
    return sub

@base_decorator
def delete_all(f):
    u"""Convierte la función en una petición de tipo DELETE que elimina todos los elementos"""
    assert(inspect.isfunction(f))
    def func(self, element, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'DELETE'
    func.type = '_all'
    return func

@base_decorator
def delete(f):
    u"""Convierte la función en una petición de tipo DELETE que elimina un elemento específico"""
    assert(inspect.isfunction(f))
    def func(self, *args, **kwargs):
        return f(self, *args, **kwargs)
    func.method = 'DELETE'
    func.type = '_default'
    return func

def delete_list(type):
    u"""Convierte la función en una petición de tipo DELETE que elimina una lista específica de elementos"""
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        assert(inspect.isfunction(f))
        def func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        func.method = 'DELETE'
        func.type = type
        return func
    return sub

class BaseRestObject(object):
    u"""Permite la herencia múltiple en objetos REST"""
    def __init__(self, **kwargs):
        u"""Finaliza la herencia del constructor e inicializa un buffer de salida"""
        ## Finaliza la cadena de MRO
        self.buffer = ''
    
    def GET(self, *args):
        u"""Finaliza la herencia del método GET y devuelve la respuesta almacenada en el buffer"""
        assert not hasattr(super(BaseRestObject, self), 'GET')
        response = self.buffer
        self.buffer = ''
        return response
    
    def POST(self, *args):
        u"""Finaliza la herencia del método POST y devuelve la respuesta almacenada en el buffer"""
        assert not hasattr(super(BaseRestObject, self), 'POST')
        response = self.buffer
        self.buffer = ''
        return response
        
    def PUT(self, *args):
        u"""Finaliza la herencia del método PUT y devuelve la respuesta almacenada en el buffer"""
        assert not hasattr(super(BaseRestObject, self), 'PUT')
        response = self.buffer
        self.buffer = ''
        return response
        
    def DELETE(self, *args):
        u"""Finaliza la herencia del método DELETE y devuelve la respuesta almacenada en el buffer"""
        assert not hasattr(super(BaseRestObject, self), 'DELETE')
        response = self.buffer
        self.buffer = ''
        return response

class RestObject(BaseRestObject):
    u"""Prototipo de un objeto REST para construir un nodo en el API a través de decorators"""
    def __init__(self, **kwargs):
        u"""Recorre la lista de métodos del objeto y los ordena en los métodos GET, POST, PUT y DELETE"""
        self.get_functions = {}
        self.post_functions = {}
        self.put_functions = {}
        self.delete_functions = {}
        for func in inspect.getmembers(self, inspect.ismethod):
            try:
                if func[1].method == 'GET':
                    self.get_functions[func[1].type] = func[1]
                if func[1].method == 'POST':
                    self.post_functions[func[1].type] = func[1]
                if func[1].method == 'PUT':
                    self.put_functions[func[1].type] = func[1]
                if func[1].method == 'DELETE':
                    self.delete_functions[func[1].type] = func[1]
            except AttributeError:
                pass 
        super(RestObject, self).__init__(**kwargs)
    
    def GET(self, element=None, type=None, *args):
        u"""Devuelve la respuesta al método GET del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.get_functions['_all']
                else:
                    func = self.get_functions['_default']
            except KeyError:
                return self._404_error()
        else:
            try:
                func = self.get_functions[self._prepare_id(type)]
            except KeyError:
                return self._404_error()
        try:
            self.buffer += self._response(func(self._prepare_id(element)))
        except auth.AuthError:
            return self._401_error()
        except Exception as e:
            return self._resp_error("An exception ocurred", e.__str__())
        return super(RestObject, self).GET(element, type, *args)        
    
    def POST(self, element=None, type=None, *args):
        u"""Devuelve la respuesta al método POST del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.post_functions['_all']
                else:
                    func = self.post_functions['_default']
            except KeyError:
                return self._404_error()
        else:
            try:
                func = self.post_functions[self._prepare_id(type)]
            except KeyError:
                return self._404_error()
        try:
            self.buffer += self._response(func(self._prepare_id(element)))
        except auth.AuthError:
            return self._401_error()
        except Exception as e:
            return self._resp_error("An exception ocurred", e.__str__())
        return super(RestObject, self).POST(element, type, *args)
    
    def PUT(self, element=None, type=None, *args):
        u"""Devuelve la respuesta al método PUT del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.put_functions['_all']
                else:
                    func = self.put_functions['_default']
            except KeyError:
                return self._404_error()
        else:
            try:
                func = self.put_functions[self._prepare_id(type)]
            except KeyError:
                return self._404_error()
        try:
            self.buffer += self._response(func(self._prepare_id(element)))
        except auth.AuthError:
            return self._401_error()
        except Exception as e:
            return self._resp_error("An exception ocurred", e.__str__())
        return super(RestObject, self).PUT(element, type, *args)
    
    def DELETE(self, element=None, type=None, *args):
        u"""Devuelve la respuesta al método DELETE del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.delete_functions['_all']
                else:
                    func = self.delete_functions['_default']
            except KeyError:
                return self._404_error()
        else:
            try:
                func = self.delete_functions[self._prepare_id(type)]
            except KeyError:
                return self._404_error()
        try:
            self.buffer += self._response(func(self._prepare_id(element)))
        except auth.AuthError:
            return self._401_error()
        except Exception as e:
            return self._resp_error("An exception ocurred", e.__str__())
        return super(RestObject, self).DELETE(element, type, *args)
    
    def _response(self, data):
        u"""Convierte el diccionario proporcionado en una cadena formateada como JSON"""
        web.header('Content-Type', 'application/json')
        return json.dumps(data)
    
    def _prepare_id(self, string):
        u"""Procesa el parametro opcional obtenido para que se utilice como id y lo devuelve como cadena de texto"""
        if string is not None:
            return string.replace('/', '')
        else:
            return string
    
    def _resp(self, tag, data):
        u"""Le da el formato adecuado a la respuesta que devuelven los métodos y la devuelve como diccionario"""
        return {tag: data}
    
    def _resp_success(self, result):
        u"""Construye una respuesta estándar para casos de éxito o fallo de un proceso y la devuelve como diccionario"""
        return self._resp('success', result)
    
    def _resp_error(self, error_str, debug = ''):
        u"""Construye una respuesta de error en caso de excepción y la devuelve como diccionario"""
        resp = self._resp_success(False)
        resp['error'] = error_str
        if(debug_info):
            resp['debug'] = debug
            traceback.print_exc()
        return resp
    
    def _404_error(self):
        web.ctx.status = '404 Not Found'
        return 'Error 404 - Page Not Found'
    
    def _401_error(self):
        web.ctx.status = '401 Unauthorized'
        return 'Error 401 - Unauthorized'
        
