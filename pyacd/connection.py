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

import os
import sys
import urllib2
import httplib
import socket

import pyacd
from pyacd.exception import PyAmazonCloudDriveError


class Connection(object):
  def __init__(self):
    self.session=None

  def do_get(self,url,headers=None):
    return self._do_request("GET",url,None,headers)

  def do_delete(self,url,headers=None):
    return self._do_request("DELETE",url,None,headers)

  def do_post(self,url,body,headers=None):
    return self._do_request("POST",url,body,headers)

  def do_put(self,url,body,headers=None):
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

    scheme,host = urllib2.urlparse.urlparse(url)[:2]

    conn=gen_httplib_conn(scheme,host)

    hs={"Cookie":"; ".join( ["=".join(i) for i in self.session.cookies.items()] )}
    if self.session.cookies.get("session-id"):
      hs["x-amzn-SessionId"]=self.session.cookies.get("session-id")

    if headers:
      hs.update(headers)

    path = url.split(host,1)[1]
    conn.request(method,path,body,hs)


#    print method
#    print path
#    print body
#    print hs
#    print "*"*20


    if pyacd.debug_level:
      sys.stderr.write(method)

    resp = conn.getresponse()

    if 400< resp.status <599:
      sys.stderr.write(resp.read())
      raise PyAmazonCloudDriveError("response code is %d"%resp.status)

    if pyacd.debug_level:
      sys.stderr.write("->")

    if resp.getheader("Set-Cookie"):
      self.session.update_cookies(resp.getheader("Set-Cookie"))

    if resp.getheader("Location"):
      return self.do_get(resp.getheader("Location"))

    resp_body=resp.read()
    conn.close()
    return resp_body


def gen_httplib_conn(scheme,host,proxy_host=None,proxy_port=None):
  """
    SEE ALSO http://code.activestate.com/recipes/301740-simplest-useful-https-with-basic-proxy-authenticat/
  """
  _port = {'http' : 80, 'https' : 443}
  _conn= {'http' : httplib.HTTPConnection, 'https' : httplib.HTTPSConnection}

  if scheme not in _port.keys():
    raise PyAmazonCloudDriveError("unsupported scheme. %s"%scheme)

  if proxy_host and proxy_port:
    pass
  elif urllib2.getproxies().has_key(scheme):
    proxy = urllib2.getproxies()[scheme]
    if proxy.find("/")!=-1:
      proxy = urllib2.urlparse.urlparse(urllib2.getproxies()[scheme])[1]
    if proxy.find(":")!=-1:
      proxy_host,proxy_port=proxy.split(":")
    else:
      proxy_host=proxy
      proxy_port=_port[scheme]

  else:
    return _conn[scheme](host)

  #print proxy_host,proxy_port

  proxy_connect='CONNECT %s:%s HTTP/1.1\r\n'%(host,_port[scheme])
  proxy_pieces=proxy_connect+'\r\n'

  #print proxy_pieces

  proxy_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  proxy_socket.connect((proxy_host,int(proxy_port)))
  proxy_socket.sendall(proxy_pieces)
  response=proxy_socket.recv(8192) 
  status=response.split()[1]
  if status!=str(200):
    raise PyAmazonCloudDriveError("%s:%s CONNECT returns %s."%
                                   (proxy_host,proxy_port,status))

  if scheme == 'http':
    sock = proxy_socket
  else:
    if sys.version_info[:2] < (2, 6):
      ssl = socket.ssl(proxy_socket, None, None)
      sock = httplib.FakeSocket(proxy_socket, ssl)
    else:
      import ssl
      sock = ssl.wrap_socket(proxy_socket, None, None)

  conn=httplib.HTTPConnection(host)
  conn.sock=sock
  return conn


