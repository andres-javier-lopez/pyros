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
    func.method = 'GET'
    func.type = '_default'
    return func

def get_list(type):
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        assert(inspect.isfunction(f))
        def func(*args, **kwargs):
            return f(*args, **kwargs)
        func.method = 'GET'
        func.type = type
        return func
    return sub

@base_decorator
def get_all(f):
    assert(inspect.isfunction(f))
    def func(element, *args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'GET'
    func.type = '_all'
    return func

@base_decorator
def post(f):
    assert(inspect.isfunction(f))
    def func(element, *args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'POST'
    func.type = '_all'
    return func

@base_decorator
def post_into(f):
    assert(inspect.isfunction(f))
    def func(*args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'POST'
    func.type = '_default'
    return func

def post_list(type):
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        def func(*args, **kwargs):
            return f(*args, **kwargs)
        func.method = 'POST'
        func.type = type
        return func
    return sub

@base_decorator
def put_all(f):
    assert(inspect.isfunction(f))
    def func(element, *args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'PUT'
    func.type = '_all'
    return func

@base_decorator
def put(f):
    assert(inspect.isfunction(f))
    def func(*args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'PUT'
    func.type = '_default'
    return func

def put_list(type):
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        assert(inspect.isfunction(f))
        def func(*args, **kwargs):
            return f(*args, **kwargs)
        func.method = 'PUT'
        func.type = type
        return func
    return sub

@base_decorator
def delete_all(f):
    assert(inspect.isfunction(f))
    def func(element, *args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'DELETE'
    func.type = '_all'
    return func

@base_decorator
def delete(f):
    assert(inspect.isfunction(f))
    def func(*args, **kwargs):
        return f(*args, **kwargs)
    func.method = 'DELETE'
    func.type = '_default'
    return func

def delete_list(type):
    assert(not inspect.isfunction(type))
    @base_decorator
    def sub(f):
        assert(inspect.isfunction(f))
        def func(*args, **kwargs):
            return f(*args, **kwargs)
        func.method = 'DELETE'
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
    
    def GET(self, element=None, type=None):
        u"""Devuelve la respuesta al método GET del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.get_functions['_all']
                else:
                    func = self.get_functions['_default']
            except KeyError:
                return # 404
        else:
            try:
                func = self.get_functions[self._prepare_id(type)]
            except KeyError:
                return # Aquí debe haber un error 404
        return self._response(func(self._prepare_id(element)))
    
    def POST(self, element=None, type=None):
        u"""Devuelve la respuesta al método POST del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.post_functions['_all']
                else:
                    func = self.post_functions['_default']
            except KeyError:
                return # 404
        else:
            try:
                func = self.post_functions[self._prepare_id(type)]
            except KeyError:
                return # Aquí debe haber un error 404
        return self._response(func(self._prepare_id(element)))
    
    def PUT(self, element=None, type=None):
        u"""Devuelve la respuesta al método PUT del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.put_functions['_all']
                else:
                    func = self.put_functions['_default']
            except KeyError:
                return # 404
        else:
            try:
                func = self.put_functions[self._prepare_id(type)]
            except KeyError:
                return # Aquí debe haber un error 404
        return self._response(func(self._prepare_id(element)))
    
    def DELETE(self, element=None, type=None):
        u"""Devuelve la respuesta al método DELETE del protocolo HTTP"""
        if(type is None or type == '/'):
            try:
                if(element is None or element == '/'):
                    func = self.delete_functions['_all']
                else:
                    func = self.delete_functions['_default']
            except KeyError:
                return # 404
        else:
            try:
                func = self.delete_functions[self._prepare_id(type)]
            except KeyError:
                return # Aquí debe haber un error 404
        return self._response(func(self._prepare_id(element)))
    
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
