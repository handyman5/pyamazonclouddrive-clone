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

import os, sys
import urllib2

import pyacd

def do_get(url,headers=None):
  req = urllib2.Request(url)
  if headers:
    for k,v in headers.items():
      req.add_header(k, v)
  return _do_request(req,None)

def do_delete(url,headers=None):
  req = urllib2.Request(url)
  if headers:
    for k,v in headers.items():
      req.add_header(k, v)
  req.get_method = lambda: 'DELETE'
  return _do_request(req,None)

def do_post(url,body,headers=None):
  req = urllib2.Request(url)
  if headers:
    for k,v in headers.items():
      req.add_header(k, v)
  return _do_request(req,body)

def do_put(url,body,headers=None):
  req = urllib2.Request(url)
  if headers:
    for k,v in headers.items():
      req.add_header(k, v)
  req.get_method = lambda: 'PUT'
  return _do_request(req,body)

def _do_request(req,body):
  """
  return response string
  """
  if not pyacd.session:
    raise pyacd.PyAmazonCloudDriveError("session is None.")
  domain = pyacd.amazon_domain[3:]
  if pyacd.session.cookies._cookies.get(domain) and\
     pyacd.session.cookies._cookies[domain].get("/") and\
     pyacd.session.cookies._cookies[domain]["/"].get("session-id"):
    req.add_header(
      "x-amzn-SessionId",
      pyacd.session.cookies._cookies[domain]["/"]["session-id"].value
    )

  try:
    if body:
      res = pyacd.opener.open(req,body)
    else:
      res = pyacd.opener.open(req)
    html = res.read()
    res.close()
    return html
  except urllib2.HTTPError, e:
    raise pyacd.PyAmazonCloudDriveError("%s %s %s:%s"%(
      req.get_full_url(),
      req.headers,
      e.code,
      e.msg
    ))

