#coding: utf-8

u"""Operaciones de base de datos."""
## @copyright: Klan Estudio - www.klanestudio.com 2013
## @author: Andrés Javier López <ajavier.lopez@gmail.com>

class BaseDecorator(object):
    def __init__(self, f):
        super().__init__()
        self.f = f

    def __call__(self):
        self.before_f()
        self.f()
        self.after_f()
        
    def before_f(self):
        pass
    
    def after_f(self):
        pass
