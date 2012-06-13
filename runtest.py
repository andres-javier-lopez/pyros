#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 
'''

import web
from test.config import debug, urls

if __name__ == '__main__':
    web.config.debug = debug
    app = web.application(urls, globals())
    app.run()
