#coding: utf-8

u"""Objeto base para la creación de apliaciones REST."""
## @copyright: TuApp.net - GNU Lesser General Public License
## @author: Andrés Javier López <ajavier.lopez@gmail.com>

import web
import json
import traceback
import auth

debug_info = False

class RestObject(object):
    u"""Prototipo de un objeto REST para construir un nodo en el API, se deben de implementar sus procesos"""
    def authenticate(self, method):
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        authobj = auth.Auth(self.get_auth_key(method))
        
        datastring = method + ' ' + web.ctx.path
        sep = '?'
        for key in sorted(data.iterkeys()):
            if(key != 'signature'):
                datastring +=  sep + key + '=' + data[key]
                if(sep == '?'):
                    sep = '&'
        
        if(not authobj.is_valid(datastring, signature, timestamp)):
            raise auth.AuthError()
    
    def get_auth_key(self, method):
        return ''
    
    def GET(self, element=None):
        u"""Devuelve la respuesta al método GET del protocolo HTTP"""
        try:
            self.authenticate('GET')
            if(element is None or element == '/'):
                return self._response(self.read())
            else:
                return self._response(self.get_element(self._prepare_id(element)))
        except auth.AuthError as e:
            web.webapi.unauthorized()
            return self._response(self._resp_error(e.__str__(), str(type(e))))
        except Exception as e:
            return self._response(self._resp_error(e.__str__(), str(type(e))))
    
    def POST(self, element=None):
        u"""Devuelve la respuesta al método POST del protocolo HTTP"""
        try:
            self.authenticate('POST')
            if(element is None or element == '/'):
                return self._response(self.insert())
            else:
                return self._response(self.insert_into(self._prepare_id(element)))
        except auth.AuthError as e:
            web.webapi.unauthorized()
            return self._response(self._resp_error(e.__str__(), str(type(e))))
        except Exception as e:
            return self._response(self._resp_error(e.__str__(), str(type(e))))
    
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
        return string.replace('/', '')
    
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
