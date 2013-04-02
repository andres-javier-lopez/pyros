#coding: utf-8

u"""Procesos de autenticacion."""
## @copyright: TuApp.net - GNU Lesser General Public License
## @author: Andrés Javier López <ajavier.lopez@gmail.com>

import hashlib, hmac, datetime
import web
from decorations import base_decorator

class AuthError (Exception):
    u"""Error estándar de autenticación"""
    pass

def auth(secret_key, method='', algorithm = hashlib.sha256):
    @base_decorator
    def fauth(f):
        def func(*args, **kwargs):
            data = web.input()
            try:
                signature = data.signature
                timestamp = data.timestamp
            except AttributeError:
                raise AuthError(u"Falta información de autenticación")
                
            authobj = Auth(secret_key, algorithm)
            
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

class Auth(object):
    u"""Sistema de autenticación"""
    
    def __init__(self, key, algorithm = hashlib.sha256):
        self.key = key
        self.algorithm = algorithm
    
    def is_valid(self, data, hashed, timestamp):
        if(self.key == ''):
            return True
        
        diff = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(float(timestamp))
        if(diff < datetime.timedelta() or diff > datetime.timedelta(minutes=5)):
            return False
        
        if(hashed == hmac.new(self.key, data.encode('utf-8'), self.algorithm).hexdigest()):
            return True 
        else:
            return False
