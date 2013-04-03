#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
from pyros import __version__

setup(name='pyros',
      version=__version__,
      description='PyROS - Python REST Operation System',
      author='Klan Estudio',
      author_email='javier.lopez@klanestudio.com',
      url='https://github.com/KlanEstudio/pyros/',
      license='Lesser GNU General Public License',
      long_description="A framework for development of RESTful API's based on web.py",
      packages=['pyros'],)
