#!/usr/bin/env python
#coding=utf-8
from distutils.core import setup
import py2exe
import sys

sys.argv.append("py2exe")
# Powered by ***
INCLUDES = ['sip', 'six', 'lxml']

options = {"py2exe":
    {"compressed": 1,
     "optimize": 0,
     "bundle_files": 2,
     "includes": INCLUDES,
     "dll_excludes": [ "MSVCP90.dll", "mswsock.dll", "powrprof.dll","w9xpopen.exe"]
	 }}

setup(
    options=options,
    description="企查查法人查询",
    zipfile=None,
	windows=['qichachaApp.py']
    #console=[{"script": "qichachaApp.py"}],
    )