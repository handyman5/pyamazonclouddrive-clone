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
administrator@Tualatin ~/svn/pyacd $ ./acdupload.py --help
Usage: acdupload.py [Options] file1 file2 ...

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e EMAIL, --email=EMAIL
                        email address for Amazon
  -p PASSWORD, --password=PASSWORD
                        password for Amazon
  -v, --verbose         show debug infomation
  -q, --quiet           quiet mode

This command upload files to root(/) of your Amazon Cloud Drive. If you have
same named file in root(/), uploading file is renamed automatically. (e.g.
'test.mp3' -> 'test (2).mp3')

administrator@Tualatin ~/svn/pyacd $ ./acdupload.py -e someone@example.com -p xxxx ~/test.jpg 
Logining to Amazon.com ... Done
Uploading test.jpg ... Done
"""

import sys
import os
from optparse import OptionParser

import pyacd

parser=OptionParser(epilog="This command upload files to root(/) of your Amazon Cloud Drive. "+
                            "If you have same named file in root(/), "+
                            "uploading file is renamed automatically. (e.g. 'test.mp3' -> 'test (2).mp3')",
                    usage="%prog [Options] file1 file2 ...",version="%prog 0.1")

parser.add_option("-e","--email",dest="email",action="store",default=None,
                  help="email address for Amazon")
parser.add_option("-p","--password",dest="password",action="store",default=None,
                  help="password for Amazon")
parser.add_option("-v","--verbose",dest="verbose",action="store_true",default=False,
                  help="show debug infomation")
parser.add_option("-q","--quiet",dest="quiet",action="store_true",default=False,
                  help="quiet mode")

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
    for file in args:
      if not os.path.exists(file):
        sys.stderr.write('Not found "%s"\n'%file)
        sys.exit(2)
      elif os.path.isdir(file):
        sys.stderr.write('"%s" is not file\n'%file)
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
    sys.stderr.write("Session is invalid.\n%s"%session)
    sys.exit(2)
  elif not session.is_logined():
    sys.stderr.write("Login failed.\n%s"%session)
    sys.exit(2)

  if not opts.quiet:
    sys.stderr.write("Done\n")

  for file in args:
    filename = os.path.basename(file)
    f=open(file,"rb")
    filedata = f.read()
    f.close()

    if not opts.quiet:
      sys.stderr.write("Uploading %s ... "%filename)

    # create file
    if opts.verbose:
      sys.stderr.write("create ")
    fileobj = pyacd.api.create_by_path("/",filename)
    if opts.verbose:
      sys.stderr.write("-> ")

    # get upload_url
    if opts.verbose:
      sys.stderr.write("url ")
    upload_url = pyacd.api.get_upload_url_by_id(fileobj.object_id,len(filedata))
    if opts.verbose:
      sys.stderr.write("-> ")

    end_point=upload_url.http_request.end_point
    parameters=upload_url.http_request.parameters

    storage_key=upload_url.storage_key
    object_id=upload_url.object_id

    # upload file
    if opts.verbose:
      sys.stderr.write("send ")
    pyacd.api.upload(end_point,parameters,filename,filedata)
    if opts.verbose:
      sys.stderr.write("-> ")

    # completeing file
    if opts.verbose:
      sys.stderr.write("finish ")
    pyacd.api.complete_file_upload_by_id(object_id,storage_key)
    if opts.verbose:
      sys.stderr.write("-> ")

  if not opts.quiet:
    sys.stderr.write("Done\n")





if __name__=="__main__":
  main()
