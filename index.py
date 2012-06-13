#!/usr/bin/env python
#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''

import web
from app.config import debug, urls

if __name__ == '__main__':
    web.config.debug = debug
    app = web.application(urls, globals())
    app.run()
