import os
import sys
import platform


if 'Windows'==platform.system():
  sys.path.insert(0,os.path.dirname(__file__)+os.sep+"windows")
elif 'Linux'==platform.system():
  import commands
  if '64'==commands.getoutput('getconf LONG_BIT'):
    sys.path.insert(0,os.path.dirname(__file__)+os.sep+"linux_x64")
  else:
    sys.path.insert(0,os.path.dirname(__file__)+os.sep+"linux_x86")
else:
  raise ImportError('Unsupported platform')

try:
  from PyV8 import *
except AttributeError,e:
  pass

sys.path.pop(0)

