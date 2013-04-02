#coding: utf-8

u"""Operaciones de base de datos.
copyright: Klan Estudio 2013 - klanestudio.com 
license: GNU Lesser General Public License
author: Andrés Javier López <ajavier.lopez@gmail.com>
"""

def base_decorator(decorator):
    u"""Decorador base que sirve para guardar correctamente los nombres, documentación y atributos.
    Sacado de http://wiki.python.org/moin/PythonDecoratorLibrary"""
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator
        
