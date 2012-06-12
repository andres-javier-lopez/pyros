#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''

import web

class App(object):
    '''Proceso principal de PyROS'''
    
    def __init__(self, urls):
        self.urls = urls
        if(self.urls == ()):
            self.urls = ('/', 'Welcome')
            
        self.app = web.application(self.urls, globals())
    
    def run(self):
        '''Corre la aplicación web'''
        self.app.run()
        
    def load(self):
        '''Devuelve la aplicacion para wsgi'''
        return self.app.wsgifunc()
    
class Welcome(object):
    '''Se carga por defecto cuando no hay configuración'''
    
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        return 'Bienvenido a PyROS'

