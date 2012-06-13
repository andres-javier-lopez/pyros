#!/usr/bin/env python
#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''

import sys, os
sys.path.append(os.getcwd())

import web
from app.config import debug, urls

web.config.debug = debug
app = web.application(urls, globals())
application = app.wsgifunc()
