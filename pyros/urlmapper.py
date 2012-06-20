#coding: utf-8

'''
Created on 20/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 
'''

class URL(object):
    def __init__(self):
        self.routemap = ()
        
    def add(self, route, handler):
        self.routemap = self.routemap + (route + '(/\d*)?', handler)
    
    def getMap(self):
        return self.routemap
        