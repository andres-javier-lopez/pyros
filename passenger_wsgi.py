#!/usr/bin/env python
#coding: utf-8

'''
Created on 12/06/2012

@author: Andrés Javier López <ajavier.lopez@gmail.com>
@version: 1.0
'''

import sys, os
sys.path.append(os.getcwd())

import pyros.app

urls = ()

app = pyros.app.App(urls)
application = app.load()
