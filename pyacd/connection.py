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




import sys
import urllib2
import httplib

import pyacd
from pyacd.exception import PyAmazonCloudDriveError


class Connection(object):
  def __init__(self):
    self.session=None

  def do_get(self,url,headers):
    return self._do_request("GET",url,None,headers)

  def do_delete(self,url,headers):
    return self._do_request("DELETE",url,None,headers)

  def do_post(self,url,body,headers):
    return self._do_request("POST",url,body,headers)

  def do_put(self,url,body,headers):
    return self._do_request("PUT",url,body,headers)

  def _do_request(self,method,url,body,headers):
    """
    return response string
    """
    if not (method=="GET" or method=="POST" or method=="PUT" or method=="DELETE"):
      raise PyAmazonCloudDriveError("unsupported method %s"%method)

    if not self.session:
      raise PyAmazonCloudDriveError("session is None.")
    elif not self.session.is_valid():
      raise PyAmazonCloudDriveError("session is invalid. %s"%self.session)

    scheme,host = urllib2.urlparse.urlparse(url)[:1]

    if scheme=='http':
      conn=httplib.HTTPConnection(host)
    elif scheme=='https':
      conn=httplib.HTTPSConnection(host)
    else:
      raise PyAmazonCloudDriveError("unsupported scheme. %s"%scheme)

    hs={"Cookie":"; ".join( ["=".join(i) for i in self.session.cookies.items()] )}
    if self.session.cookies.get("session-id"):
      hs["x-amzn-SessionId"]=self.session.cookies.get("session-id=")

    if headers:
      hs.update(headers)

    path = url.split(host,1)[1]
    conn.request(method,path,None,hs)

    if pysugarsync.debug_level:
      #print method,
      sys.stderr.write(method)

    resp = conn.getresponse()

    if 400< resp.status <599:
      sys.stderr.write(resp.read())
      raise PyAmazonCloudDriveError("response code is %d"%resp.status)

    if pysugarsync.debug_level:
      #print "->",
      sys.stderr.write("->")

    self.session.update_cookies(resp.getheader("Set-Cookie"))

    if resp.getheader("Location"):
      return self.do_get(resp.getheader("Location"))

    resp_body=resp.read()
    conn.close()
    return resp_body


