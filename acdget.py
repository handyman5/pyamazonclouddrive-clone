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
administrator@Tualatin ~/svn/pyacd $ ./acdget.py --help
Usage: acdget.py [Options] file1 file2 - ...('-' means STDIN)

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e EMAIL, --email=EMAIL
                        email address for Amazon.com
  -p PASSWORD, --password=PASSWORD
                        password for Amazon.com
  -s FILE, --session=FILE
                        save or load login session to/from FILE
  -d PATH, --destination=PATH
                        download path [default: ./]
  -f, --force           override local file if it has same name [default:
                        False]
  -v, --verbose         show debug infomation
  -q, --quiet           quiet mode

This command download file(s) from your Amazon Cloud Drive. If there is same
named file, downloading is canceled automatically. (or use --force option)

administrator@Tualatin ~/svn/pyacd $ ./acdget.py -s ~/.session README.TXT
Logining to Amazon.com ... Done
Updating /home/administrator/.session ... Done
Downloading /README.TXT to ./ ... Done
"""

import sys
import os
from optparse import OptionParser
import pickle

pyacd_lib_dir=os.path.dirname(os.__file__)+os.sep+"pyacd"
if os.path.exists(pyacd_lib_dir) and os.path.isdir(pyacd_lib_dir):
  sys.path.insert(0, pyacd_lib_dir)

import pyacd

parser=OptionParser(epilog="This command download file(s) from your Amazon Cloud Drive. "+
                            "If there is same named file, downloading is canceled "+
                            "automatically. (or use --force option)",
                    usage="%prog [Options] file1 file2 - ...('-' means STDIN)",version="%prog 0.2")

parser.add_option("-e","--email",dest="email",action="store",default=None,
                  help="email address for Amazon.com")
parser.add_option("-p","--password",dest="password",action="store",default=None,
                  help="password for Amazon.com")
parser.add_option("-s","--session",dest="session",action="store",default=None,
                  metavar="FILE",help="save or load login session to/from FILE")
parser.add_option("-d","--destination",dest="path",action="store",default="."+os.sep,
                  help="download path [default: %default]")
parser.add_option("-f","--force",dest="force",action="store_true",default=False,
                  help="override local file if it has same name [default: %default]")
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
    sys.stderr.write("!! no file selected !!\n")
    parser.print_help()
    sys.exit(2)
  else:
    pass
    
  # Check destination
  path=opts.path
  if path[-1]!=os.sep:path=path+os.sep
  if not os.path.exists(path):
    sys.stderr.write('"%s" does not exist\n'%path)
    sys.exit(2)
  elif not os.path.isdir(path):
    sys.stderr.write('"%s" is not file\n'%path)
    sys.exit(2)

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

  for file in args:
    if file[0]!='/':file='/'+file
    filename = os.path.basename(file)

    if not opts.quiet:
      sys.stderr.write("Downloading %s to %s ... "%(file,path))

    if os.path.exists(path+filename) and not opts.force:
      sys.stderr.write("Aborted. ('%s' exists.)\n"%(path+filename))
      continue

    # get file
    if opts.verbose:
      sys.stderr.write("get ")
    try:
      fileobj = pyacd.api.get_info_by_path(file)
    except pyacd.PyAmazonCloudDriveApiException,e:
      sys.stderr.write("Aborted. ('%s')\n"%e.message)
      continue
    if opts.verbose:
      sys.stderr.write("-> ")

    if fileobj.Type!= pyacd.types.FILE:
      sys.stderr.write("Aborted. ('%s' is not file.)"%file)
      continue

    # download
    data=pyacd.api.download_by_id(fileobj.object_id)
    

    f=open(path+filename,"wb")
    f.truncate()
    f.write(data)
    f.close()

    if not opts.quiet:
      sys.stderr.write("Done\n")


if __name__=="__main__":
  main()
