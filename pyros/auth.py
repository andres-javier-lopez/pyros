#coding: utf-8

u"""Procesos de autenticación.
copyright: Klan Estudio 2013 - klanestudio.com 
license: GNU Lesser General Public License
author: Andrés Javier López <ajavier.lopez@gmail.com>
"""

import hashlib, hmac, datetime
import re, base64
import web
from decorations import base_decorator

class AuthError (Exception):
    u"""Error estándar de autenticación"""
    pass

class Auth(object):
    u"""Realiza el proceso de autenticación"""
    
    DEFAULT_ALGORITHM = hashlib.sha256
    
    def __init__(self, key, algorithm = hashlib.sha256):
        u"""Inicializa el objeto"""
        self.key = key
        self.algorithm = algorithm
        
    def check_algorithm(self):
        try:
            self.algorithm
        except AttributeError:
            self.algorithm = Auth.DEFAULT_ALGORITHM
    
    def is_valid(self, data, hashed, timestamp):
        u"""Comprueba si el hash es válido y devuelve True o False"""
        if(self.key == ''):
            return True
        
        diff = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(float(timestamp))
        if(diff < datetime.timedelta() or diff > datetime.timedelta(minutes=5)):
            return False
        
        if(hashed == hmac.new(self.key, data.encode('utf-8'), self.algorithm).hexdigest()):
            return True 
        else:
            return False

def auth(authclass, method=''):
    u"""Activa el proceso de autenticación"""
    @base_decorator
    def fauth(f):
        def func(*args, **kwargs):
            data = web.input()
            try:
                signature = data.signature
                timestamp = data.timestamp
            except AttributeError:
                raise AuthError(u"Falta información de autenticación")
            
            if not issubclass(authclass, Auth):
                raise AuthError(u"Clase de autenticación no válida")
                
            authobj = authclass()
            authobj.check_algorithm()
            
            if(method == ''):
                try:
                    met = f.method
                except AttributeError:
                    raise AuthError(u"No se específico un método")
            else:
                met = method
            
            datastring = met + ' ' + web.ctx.path
            sep = '?'
            for key in sorted(data.iterkeys()):
                if(key != 'signature' and data[key] != ''):
                    datastring = datastring + sep + key + '=' + data[key]
                    if(sep == '?'):
                        sep = '&'
            
            datastring = datastring + ' ' + web.data()
            
            if(not authobj.is_valid(datastring, signature, timestamp)):
                raise AuthError(u"Autenticación no válida")
            return f(*args, **kwargs)
        return func
    return fauth

def http_auth(credentials):
    u"""Realiza la autenticación basada en HTTP"""
    ## Faltan pruebas
    @base_decorator
    def fauth(f):
        def func(*args, **kwargs):
            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            if auth is None:
                raise AuthError(u"No se autenticó")
            auth = re.sub('^Basic ', '', auth)
            username_auth,password_auth = base64.decodestring(auth).split(':')
            if username_auth == credentials['username'] and password_auth == credentials['password']:
                return f(*args,**kwargs)
            else:
                raise AuthError(u"Autenticación no válida")
        return func
    return fauth
