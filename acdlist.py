#!/usr/bin/env python
#
# Copyright (c) 2011 anatanokeitai.com(sakurai_youhei)
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# 
# The Software shall be used for Younger than you, not Older.
# 
"""
administrator@Tualatin ~/svn/pyacd $ ./acdlist.py --help
Usage: acdlist.py [Options] path1 path2 - ...('-' means STDIN)

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e EMAIL, --email=EMAIL
                        email address for Amazon.com
  -p PASSWORD, --password=PASSWORD
                        password for Amazon.com
  -s FILE, --session=FILE
                        save or load login session to/from FILE
  -l                    use a long listing format
  -t TYPE, --type=TYPE  list type (ALL|FILE|FOLDER) [default: ALL]
  -v, --verbose         show debug infomation
  -q, --quiet           quiet mode

This command lists files and directories of your Amazon Cloud Drive.

administrator@Tualatin ~/svn/pyacd $ ./acdlist.py -s ~/.session / -l
Logining to Amazon.com ... Done
Updating /home/administrator/.session ... Done
Listing / ... Done
total 2 (/)
==modified========== ==size/type== ==version== ==name==========
2011-04-24T23:06:00         121266         (5) test.jpg
2011-04-24T23:06:15         116236         (3) test (2).jpg
"""

import sys
import os
from optparse import OptionParser
import pickle
import time,datetime

pyacd_lib_dir=os.path.dirname(os.__file__)+os.sep+"pyacd"
if os.path.exists(pyacd_lib_dir) and os.path.isdir(pyacd_lib_dir):
  sys.path.insert(0, pyacd_lib_dir)

import pyacd

parser=OptionParser(epilog="This command lists files and directories of "
                           "your Amazon Cloud Drive. ",
                    usage="%prog [Options] path1 path2 - ...('-' means STDIN)",version="%prog 0.2")

parser.add_option("-e","--email",dest="email",action="store",default=None,
                  help="email address for Amazon.com")
parser.add_option("-p","--password",dest="password",action="store",default=None,
                  help="password for Amazon.com")
parser.add_option("-s","--session",dest="session",action="store",default=None,
                  metavar="FILE",help="save or load login session to/from FILE")
parser.add_option("-l",dest="long_format",action="store_true",default=False,
                  help="use a long listing format")
parser.add_option("-t","--type",dest="list_type",action="store",default="ALL",
                  metavar="TYPE",help="list type (ALL|FILE|FOLDER) [default: %default]")
parser.add_option("-v","--verbose",dest="verbose",action="store_true",default=False,
                  help="show debug infomation")
parser.add_option("-q","--quiet",dest="quiet",action="store_true",default=False,
                  help="quiet mode")

def main():
  opts,args=parser.parse_args(sys.argv[1:])

  # Check options of authentication
  if opts.session and os.path.exists(opts.session) and not os.path.isdir(opts.session):
    pass
  elif not opts.email or not opts.password:
    sys.stderr.write("!! email and password are required !!\n")
    parser.print_help()
    sys.exit(2)

  args=list(set(args))
  if "-" in args:
    args.remove("-")
    args += [x.strip() for x in sys.stdin.readlines()]

  if 0==len(args):
    args.append("/")
  else:
    pass

  # Login to Amazon.com
  session=None
  try:
    if not opts.quiet:
      sys.stderr.write("Logining to Amazon.com ... ")
    if opts.email and opts.password:
      session=pyacd.login(opts.email,opts.password)
    else:
      fp=open(opts.session,"rb")
      session=pickle.load(fp)
      fp.close()
      session=pyacd.login(session=session)
  except:
    pass

  # Check login status
  if not session:
    sys.stderr.write("Unexpected error occured.\n")
    sys.exit(2)
  elif not session.is_valid():
    sys.stderr.write("Session is invalid.\n%s\n"%session)
    sys.exit(2)
  elif not session.is_logined():
    sys.stderr.write("Login failed.\n%s\n"%session)
    sys.exit(2)

  if not opts.quiet:
    sys.stderr.write("Done\n")

  if opts.session:
    if not opts.quiet:
      sys.stderr.write("Updating %s ... "%opts.session)
    fp=open(opts.session,"wb")
    fp.truncate()
    pickle.dump(session,fp)
    fp.close()
    if not opts.quiet:
      sys.stderr.write("Done\n")

  for path in args:
    if path[0]!='/':path='/'+path

    if not opts.quiet:
      sys.stderr.write("Listing %s ... "%(path))

    # get path
    if opts.verbose:
      sys.stderr.write("get ")
    try:
      pathobj = pyacd.api.get_info_by_path(path)
    except pyacd.PyAmazonCloudDriveApiException,e:
      sys.stderr.write("Aborted. ('%s')\n"%e.message)
      continue
    if opts.verbose:
      sys.stderr.write("-> ")

    obj=[]
    if pathobj.Type== pyacd.types.FILE:
      obj.append(pathobj)
    else:
      if opts.verbose:
        sys.stderr.write("info ")
      info = pyacd.api.list_by_id(pathobj.object_id)
      if opts.verbose:
        sys.stderr.write("-> ")
      obj+=info.objects

    if not opts.quiet:
      sys.stderr.write("Done\n")

    #print obj
    if opts.long_format:
      print "total %s (%s)"%(len(obj),path)
      print "==modified========== ==size/type== ==version== ==name=========="
    for o in obj:
      if opts.list_type!="ALL" and opts.list_type!=o.Type:
        continue
      if opts.long_format:
        print "%s "%datetime.datetime(*time.localtime(o.modified)[:-3]).isoformat(),
        if o.Type == pyacd.types.FILE:
          print "%13s"%(o.size if o.size else -1),
        else:
          print "%13s"%("<"+o.Type+">"),

        print "%11s"%("("+str(o.version)+")"),

      print o.name if o.Type == pyacd.types.FILE else o.name+"/"

    continue

if __name__=="__main__":
  main()
