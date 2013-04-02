#coding: utf-8

'''
@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 
'''
import pyros.database
import pyros.urlmapper

urlmap = pyros.urlmapper.URL()
## Configuradas las rutas de la aplicación
## urlmap.add('/', 'test.simple.Start')
urls = urlmap.get_map()

## Conexión con la base de datos
database = {'dbn': 'mysql', 'user': 'root', 'password': '', 'database': 'test'}

## Depuración desactivada para producción
debug = False

def init_connection():
    pyros.database.Database.initialize(database)
    
def check_database():
    if(pyros.database.check_connection() == False):
        init_connection()
    
init_connection()
