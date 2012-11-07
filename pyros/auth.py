#coding: utf-8

u"""Procesos de autenticacion."""
## @copyright: TuApp.net - GNU Lesser General Public License
## @author: Andrés Javier López <ajavier.lopez@gmail.com>

import hashlib, hmac, datetime

class AuthError (Exception):
    u"""Error estándar de autenticación"""
    pass

class Auth:
    u"""Sistema de autenticación"""
    
    def __init__(self, key, algorithm = hashlib.sha256()):
        self.key = key
        self.algorithm = algorithm
    
    def is_valid(self, data, hashed, timestamp):
        diff = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(timestamp)
        if(diff > datetime.timedelta(minutes=5)):
            return False
        
        if(hashed == hmac.new(self.key, data, self.algorithm).hexdigest()):
            return True 
        else:
            return False
