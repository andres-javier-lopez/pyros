#coding: utf-8

'''
Created on 20/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 
'''

class URL(object):
    '''Objeto para la construcción de las URL de los nodos del API'''
    def __init__(self):
        '''Inicializa el mapa de rutas como vacío'''
        self.routemap = ()
        
    def add(self, route, handler):
        '''Agrega un nuevo par ruta/manejador al mapa de rutas'''
        self.routemap = self.routemap + (route + '(/\d*)?', handler)
    
    def getMap(self):
        '''Devuelve el mapa de rutas'''
        return self.routemap
        