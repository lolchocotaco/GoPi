#!/usr/bin/env python
import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages
import platform

classifiers = ['Development Status :: 2 - Pre-Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

extra = {}
if platform.python_version().startswith('3'):
    extra['use_2to3'] = True

setup(name             = 'RPi.GPIO',
      version          = '0.1.0',
      packages         = find_packages(),
      author           = 'Ben Croston',
      author_email     = 'ben@croston.org',
      description      = 'A class to control Raspberry Pi GPIO channels',
      long_description = open('README.txt').read() + open('CHANGELOG.txt').read(),
      license          = 'MIT',
      keywords         = 'Raspberry Pi GPIO',
      url              = 'http://code.google.com/p/raspberry-gpio-python/',
      classifiers      = classifiers,
      **extra)
