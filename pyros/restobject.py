#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 0.5
'''
import web
import json

class RestObject(object):
    '''Prototipo de un objeto REST para construir un nodo en el API, se deben de implementar sus procesos'''
    def GET(self, element=None):
        '''Devuelve la respuesta al método GET del protocolo HTTP'''
        try:
            if(element is None or element == '/'):
                return self._response(self.read())
            else:
                return self._response(self.get_element(self._prepare_id(element)))
        except Exception as e:
            return self._response(self._resp_error(e.__str__()))
            pass
    
    def POST(self, element=None):
        '''Devuelve la respuesta al método POST del protocolo HTTP'''
        try:
            if(element is None or element == '/'):
                return self._response(self.insert())
            else:
                return self._response(self.insert_into(self._prepare_id(element)))
        except Exception as e:
            return self._response(self._resp_error(e.__str__()))
            pass
    
    def PUT(self, element=None):
        '''Devuelve la respuesta al método PUT del protocolo HTTP'''
        try:
            if(element is None or element == '/'):
                return self._response(self.replace())
            else:
                return self._response(self.update_element(self._prepare_id(element)))
        except Exception as e:
            return self._response(self._resp_error(e.__str__()))
            pass
    
    def DELETE(self, element=None):
        '''Devuelve la respuesta al método DELETE del protocolo HTTP'''
        try:
            if(element is None or element == '/'):
                return self._response(self.delete())
            else:
                return self._response(self.delete_element(self._prepare_id(element)))
        except Exception as e:
            return self._response(self._resp_error(e.__str__()))
    
    def _response(self, data):
        '''Convierte el diccionario proporcionado en una respuesta del tipo JSON'''
        web.header('Content-Type', 'application/json')
        return json.dumps(data)
    
    def _prepare_id(self, string):
        '''Procesa el parametro opcional obtenido para que se utilice como id'''
        return string.replace('/', '')
    
    def _resp(self, tag, data):
        '''Le da el formato adecuado a la respuesta que devuelven los métodos'''
        return {tag: data}
    
    def _resp_success(self, result):
        '''Respuesta estándar para casos de éxito o fallo de un proceso'''
        return self._resp('success', result)
    
    def _resp_error(self, error_str):
        '''Error en caso de excepción'''
        resp = self._resp_success(False)
        resp['error'] = error_str
        return resp
    
    def read(self):
        '''Devuelve una lista de elementos en el nodo actual'''
        pass
    
    def insert(self):
        '''Ingresa un nuevo elemento al nodo actual'''
        pass
    
    def replace(self):
        '''Reemplaza completamente el nodo actual'''
        pass
    
    def delete(self):
        '''Elimina completamente el nodo actual'''
        pass
    
    def get_element(self, id_element):
        '''Devuelve el elemento específicado perteneciente al nodo actual'''
        pass
    
    def insert_into(self, id_element):
        '''Ingresa un subelemento al elemento especificado dentro del nodo'''
        pass
    
    def update_element(self, id_element):
        '''Actualiza el elemento específicado en el nodo actual'''
        pass
    
    def delete_element(self, id_element):
        '''Elimina el elemento específicado dentro del nodo'''
        pass
