#coding: utf-8

u"""Sistema de mapeo de URLs.
copyright: Klan Estudio 2013 - klanestudio.com 
license: GNU Lesser General Public License
author: Andrés Javier López <ajavier.lopez@gmail.com>
"""

class URL(object):
    u"""Construye las URL de los nodos del API"""
    def __init__(self):
        u"""Inicializa el mapa de rutas como vacío"""
        self.routemap = ()
        
    def add(self, route, handler):
        u"""Agrega un nuevo par ruta/manejador al mapa de rutas"""
        self.routemap = self.routemap + (route + '(/\w*)?(/\w*/?)?', handler)
    
    def get_map(self):
        u"""Devuelve el mapa de rutas como una tupla"""
        return self.routemap
        