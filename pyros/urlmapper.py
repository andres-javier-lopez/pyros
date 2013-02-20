#coding: utf-8

u"""Sistema de mapeo de URLs"""
## @copyright: TuApp.net - GNU Lesser General Public License
## @author: Andrés Javier López <ajavier.lopez@gmail.com>

class URL(object):
    u"""Objeto para la construcción de las URL de los nodos del API"""
    def __init__(self):
        u"""Inicializa el mapa de rutas como vacío"""
        self.routemap = ()
        
    def add(self, route, handler):
        u"""Agrega un nuevo par ruta/manejador al mapa de rutas"""
        self.routemap = self.routemap + (route + '(/\w*)?(/\w*)?', handler)
    
    def get_map(self):
        u"""Devuelve el mapa de rutas"""
        return self.routemap
        