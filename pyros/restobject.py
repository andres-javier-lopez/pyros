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
                return self._response(self.getElement(self._prepareId(element)))
        except Exception:
            return self._response(self._respError())
    
    def POST(self, element=None):
        '''Devuelve la respuesta al método POST del protocolo HTTP'''
        try:
            if(element is None or element == '/'):
                return self._response(self.insert())
            else:
                return self._response(self.insertInto(self._prepareId(element)))
        except Exception:
            return self._response(self._respError())
    
    def PUT(self, element=None):
        '''Devuelve la respuesta al método PUT del protocolo HTTP'''
        try:
            if(element is None or element == '/'):
                return self._response(self.replace())
            else:
                return self._response(self.updateElement(self._prepareId(element)))
        except Exception:
            return self._response(self._respError())
    
    def DELETE(self, element=None):
        '''Devuelve la respuesta al método DELETE del protocolo HTTP'''
        try:
            if(element is None or element == '/'):
                return self._response(self.delete())
            else:
                return self._response(self.deleteElement(self._prepareId(element)))
        except Exception:
            return self._response(self._respError())
    
    def _response(self, data):
        '''Convierte el diccionario proporcionado en una respuesta del tipo JSON'''
        web.header('Content-Type', 'application/json')
        return json.dumps(data)
    
    def _prepareId(self, string):
        '''Procesa el parametro opcional obtenido para que se utilice como id'''
        return string.replace('/', '')
    
    def _resp(self, tag, data):
        '''Le da el formato adecuado a la respuesta que devuelven los métodos'''
        return {tag: data}
    
    def _respSuccess(self, result):
        '''Respuesta estándar para casos de éxito o fallo de un proceso'''
        return self._resp('success', result)
    
    def _respError(self):
        '''Error en caso de excepción'''
        return self._respSuccess(False)
    
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
    
    def getElement(self, id_element):
        '''Devuelve el elemento específicado perteneciente al nodo actual'''
        pass
    
    def insertInto(self, id_element):
        '''Ingresa un subelemento al elemento especificado dentro del nodo'''
        pass
    
    def updateElement(self, id_element):
        '''Actualiza el elemento específicado en el nodo actual'''
        pass
    
    def deleteElement(self, id_element):
        '''Elimina el elemento específicado dentro del nodo'''
        pass
