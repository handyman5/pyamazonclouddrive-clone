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

import re
import urllib
from HTMLParser import HTMLParser

import pyacd

def login(email=None,password=None,session=None):
  if session:
    pyacd.conn.session=Session(session)
  elif email is None or password is None:
    raise TypeError("invalid args email->%s,password->%s"%(email,password))
  else:
    pyacd.conn.session=Session()
  
  end_point="https://www.amazon.com/clouddrive"
  html=pyacd.conn.do_get(end_point)

  if email and password:
    begin='<form name="signIn"'
    end='</form>'
    html=begin + html.split(begin,1)[1].split(end,1)[0] +end

    parser=CustomHTMLParser()
    parser.feed(html)
    parser.close()

    action=parser.action
    params=parser.key_value.copy()

    params["create"]=0
    #params["x"]=0
    #params["y"]=0
    #params["metadata1"]=""
    params["email"]=email
    params["password"]=password
    body=urllib.urlencode(params)
    html=pyacd.conn.do_post(action,body,{"Content-Type":"application/x-www-form-urlencoded"})

  try:
    customer_id=html.split("customerId",1)[1]
    customer_id=customer_id.split(">",1)[0]
    customer_id=re.sub('.*value="','',customer_id)
    customer_id=re.sub('".*','',customer_id)
    pyacd.conn.session.customer_id=customer_id

    username=html.split("customer_greeting",1)[1]
    username=username.split("<",1)[0]
    username=username.split(",")[1][1:]
    username=re.sub(r'\..*','',username)
    pyacd.conn.session.username=username
  except:
    pass
    
  return pyacd.conn.session




class CustomHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.key_value={}
    self.action=""

  def handle_starttag(self, tag, attrs):
    d=dict(attrs)
    if tag=="form":
      #print d
      self.action=d.get("action","")
    elif tag=='input':
      if d.get('name'):
        self.key_value[d.get('name')]=d.get('value','')
  def handle_endtag(self, tag):
    if tag=='input':
      pass




class Session(object):
  def __init__(self,session=None):
    self.username=None
    self.customer_id=None
    self.cookies={}
    self._initializing=True
    if not session:
      pyacd.conn.session=self
      end_point = "http://www.amazon.com/"
      pyacd.conn.do_get(end_point)
      pyacd.conn.do_get(end_point)
      self._initializing=False
    else:
      self.cookies.update(session.cookies)
      self._initializing=False
     
      
  def __repr__(self):
    return '<Session: %s>' % ",".join( [ k for k,v in self.cookies.items() ] )

  def __str__(self):
    return '<Session: %s>' % ",".join( [ k for k,v in self.cookies.items() ] )
    
  def is_valid(self):
    if self._initializing:
      return True
    else:
      return self.cookies.has_key("session-id") and \
                    self.cookies.has_key("session-id-time") and \
                         self.cookies.has_key("ubid-main")

  def is_logined(self):
    return (self.is_valid() and self.username and self.customer_id)

  def update_cookies(self,cookie_str):
    #self.cookies={}
    for c in cookie_str.split(", "):
      if c.startswith("session-") or c.startswith("ubid-") or c.startswith("x-") or \
                                                          c.startswith("__")or c.startswith("at-"):
        self.cookies.update( dict( [re.sub(";.*","",c).split("=",1),] ) )

  def print_debug(self):
    print "*"*20
    for k,v in self.cookies.items():
      print "%s=%s"%(k,v)
    
