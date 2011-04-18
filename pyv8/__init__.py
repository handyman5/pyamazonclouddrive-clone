import platform

if 'Windows'==platform.system():
  from windows.PyV8 import *
elif 'Linux'==platform.system():
  import commands
  if '64'==commands.getoutput('getconf LONG_BIT'):
    from linux_x64.PyV8 import *
  else:
    from linux_x86.PyV8 import *
else:
  raise ImportError('Unsupported platform')

