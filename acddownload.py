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
administrator@Tualatin ~/svn/pyacd $ ./acddownload.py --help
Usage: acddownload.py -e EMAIL -p PASSWORD [-q] [-v] [-d PATH] file1 file2 ...

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e EMAIL, --email=EMAIL
                        email address for Amazon
  -p PASSWORD, --password=PASSWORD
                        password for Amazon
  -v, --verbose         show debug infomation
  -q, --quiet           quiet mode
  -d PATH, --destination=PATH
                        download path [default: /]

"""

import sys
import os
from optparse import OptionParser

import pyacd

parser=OptionParser(epilog="This command download file(s) from your Amazon Cloud Drive. "+
                            "If there is same named file, downloading is aborted "+
                            "automatically. (or use --force option)",
                    usage="%prog -e EMAIL -p PASSWORD [-q] [-v] [-d PATH] file1 file2 ...",version="%prog 0.1")

parser.add_option("-e","--email",dest="email",action="store",default=None,
                  help="email address for Amazon")
parser.add_option("-p","--password",dest="password",action="store",default=None,
                  help="password for Amazon")
parser.add_option("-v","--verbose",dest="verbose",action="store_true",default=False,
                  help="show debug infomation")
parser.add_option("-q","--quiet",dest="quiet",action="store_true",default=False,
                  help="quiet mode")
parser.add_option("-d","--destination",dest="path",action="store",default="./",
                  help="upload path [default: %default]")
parser.add_option("-f","--force",dest="force",action="store_true",default=False,
                  help="override local file if it has same name [default: %default]")

def main():
  opts,args=parser.parse_args(sys.argv[1:])

  # Check options
  if not opts.email or not opts.password:
    sys.stderr.write("!! email and password are required !!\n")
    parser.print_help()
    sys.exit(2)
  elif 0==len(args):
    sys.stderr.write("!! no file selected !!\n")
    parser.print_help()
    sys.exit(2)
  else:
    pass
    
  # Check destination
  path=opts.path
  #if path[0]!='/':path='/'+path
  if path[-1]!='/':path=path+'/'
  if not os.path.exists(path) or not os.path.isdir(path):
    sys.stderr.write('"%s" is invalid path\n'%path)
    sys.exit(2)

  # Login to Amazon.com
  session=None
  try:
    if not opts.quiet:
      sys.stderr.write("Logining to Amazon.com ... ")
    session=pyacd.login(opts.email,opts.password)
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
    
  

  for file in args:
    filename = os.path.basename(file)

    if not opts.quiet:
      sys.stderr.write("Downloading %s to %s ... "%(filename,path))

    if os.path.exists(path+filename) and not opts.force:
      sys.stderr.write("Aborted. ('%s' exists.)"%path+filename)
      continue

    # get file
    if opts.verbose:
      sys.stderr.write("get ")
    fileobj = pyacd.api.get_info_by_path(path+filename)
    if opts.verbose:
      sys.stderr.write("-> ")

    if fileobj.Type!= pyacd.types.FILE:
      sys.stderr.write("Aborted. ('%s' s not file.)"%file)
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
