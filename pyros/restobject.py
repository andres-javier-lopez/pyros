#coding: utf-8

u"""Objeto base para la creación de apliaciones REST."""
## @copyright: TuApp.net - GNU Lesser General Public License
## @author: Andrés Javier López <ajavier.lopez@gmail.com>

import web
import json
import traceback
import auth
from decorations import base_decorator
import inspect

debug_info = False

@base_decorator
def get(f):
    assert(inspect.isfunction(f))
    def func(*args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'get'
    func.type = '_default'
    return func

def getlist(type):
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        assert(inspect.isfunction(f))
        def func(*args, **kwargs):
            return f(*args, **kwargs)
        func.method = 'get'
        func.type = type
        return func
    return sub

@base_decorator
def getall(f):
    assert(inspect.isfunction(f))
    def func(element, *args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'get'
    func.type = '_all'
    return func

@base_decorator
def post(f):
    assert(inspect.isfunction(f))
    def func(element, *args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'post'
    func.type = '_all'
    return func

def post_into(type='_default'):
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        def func(*args, **kwargs):
            return f(*args, **kwargs)
        func.method = 'post'
        func.type = type
        return func
    return sub

class RestObject(object):
    u"""Prototipo de un objeto REST para construir un nodo en el API, se deben de implementar sus procesos"""
    def __init__(self):
        self.get_functions = {}
        self.post_functions = {}
        self.put_functions = {}
        self.delete_functions = {}
        for func in inspect.getmembers(self, inspect.ismethod):
            try:
                assert(inspect.isfunction(func[1]))
                if func[1].method == 'get':
                    self.get_functions[func[1].type] = func[1]
                if func[1].method == 'post':
                    self.post_functions[func[1].type] = func[1]
                if func[1].method == 'put':
                    self.put_functions[func[1].type] = func[1]
                if func[1].method == 'delete':
                    self.delete_functions[func[1].type] = func[1]
            except AttributeError:
                pass 
    
    def GET(self, element=None, type=None):
        u"""Devuelve la respuesta al método GET del protocolo HTTP"""
        if(type is None or type == '/'):
            if(element is None or element == '/'):
                func = self.get_functions['_all']
            else:
                func = self.get_functions['_default']
        else:
            try:
                func = self.get_functions[self._prepare_id(type)]
            except KeyError:
                return # Aquí debe haber un error 404
        return self._response(func(self._prepare_id(element)))
    
    def POST(self, element=None, type=None):
        u"""Devuelve la respuesta al método POST del protocolo HTTP"""
        if(type is None or type == '/'):
            if(element is None or element == '/'):
                func = self.post_functions['_all']
            else:
                func = self.post_functions['_default']
        else:
            try:
                func = self.post_functions[self._prepare_id(type)]
            except KeyError:
                return # Aquí debe haber un error 404
        return self._response(func(self._prepare_id(element)))
    
    def PUT(self, element=None):
        u"""Devuelve la respuesta al método PUT del protocolo HTTP"""
        try:
            self.authenticate('PUT')
            if(element is None or element == '/'):
                return self._response(self.replace())
            else:
                return self._response(self.update_element(self._prepare_id(element)))
        except auth.AuthError as e:
            web.webapi.unauthorized()
            return self._response(self._resp_error(e.__str__(), str(type(e))))
        except Exception as e:
            return self._response(self._resp_error(e.__str__(), str(type(e))))
    
    def DELETE(self, element=None):
        u"""Devuelve la respuesta al método DELETE del protocolo HTTP"""
        try:
            self.authenticate('DELETE')
            if(element is None or element == '/'):
                return self._response(self.delete())
            else:
                return self._response(self.delete_element(self._prepare_id(element)))
        except auth.AuthError as e:
            web.webapi.unauthorized()
            return self._response(self._resp_error(e.__str__(), str(type(e))))
        except Exception as e:
            return self._response(self._resp_error(e.__str__(), str(type(e))))
    
    def _response(self, data):
        u"""Convierte el diccionario proporcionado en una respuesta del tipo JSON"""
        web.header('Content-Type', 'application/json')
        return json.dumps(data)
    
    def _prepare_id(self, string):
        u"""Procesa el parametro opcional obtenido para que se utilice como id"""
        if string is not None:
            return string.replace('/', '')
        else:
            return string
    
    def _resp(self, tag, data):
        u"""Le da el formato adecuado a la respuesta que devuelven los métodos"""
        return {tag: data}
    
    def _resp_success(self, result):
        u"""Respuesta estándar para casos de éxito o fallo de un proceso"""
        return self._resp('success', result)
    
    def _resp_error(self, error_str, debug = ''):
        u"""Error en caso de excepción"""
        resp = self._resp_success(False)
        resp['error'] = error_str
        if(debug_info):
            resp['debug'] = debug
            traceback.print_exc()
        return resp
    
    def read(self):
        u"""Devuelve una lista de elementos en el nodo actual"""
        pass
    
    def insert(self):
        u"""Ingresa un nuevo elemento al nodo actual"""
        pass
    
    def replace(self):
        u"""Reemplaza completamente el nodo actual"""
        pass
    
    def delete(self):
        u"""Elimina completamente el nodo actual"""
        pass
    
    def get_element(self, id_element):
        u"""Devuelve el elemento específicado perteneciente al nodo actual"""
        pass
    
    def insert_into(self, id_element):
        u"""Ingresa un subelemento al elemento especificado dentro del nodo"""
        pass
    
    def update_element(self, id_element):
        u"""Actualiza el elemento específicado en el nodo actual"""
        pass
    
    def delete_element(self, id_element):
        u"""Elimina el elemento específicado dentro del nodo"""
        pass
