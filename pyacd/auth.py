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


import xml.dom.minidom

import pysugarsync

auth_xml="""
<authRequest>
    <username>username</username>
    <password>password</password>
    <accessKeyId>access_key</accessKeyId>
    <privateAccessKey>private_access_key</privateAccessKey>
</authRequest>
"""

auth_dom=xml.dom.minidom.parseString(auth_xml)

end_point = "https://api.sugarsync.com/authorization"

def retrieve_token(**kwargs):
  access_key=kwargs.get("access_key",None)
  private_access_key=kwargs.get("private_access_key",None)
  username=kwargs.get("username",None)
  password=kwargs.get("password",None)

  auth_dom.getElementsByTagName("accessKeyId")[0].firstChild.data=access_key
  auth_dom.getElementsByTagName("privateAccessKey")[0].firstChild.data=private_access_key
  auth_dom.getElementsByTagName("username")[0].firstChild.data=username
  auth_dom.getElementsByTagName("password")[0].firstChild.data=password

  resp = pysugarsync.conn.do_post(end_point,auth_dom.toxml(),{"content-type":"application/xml; charset=UTF-8"})
  token = resp.info().getheader("Location")
  resp.close()
  return token

def is_valid_token(token,method,url):
  #print token,method,url
  if token:
    return token.startswith(end_point)
  else:
    if method=="POST" and url==pysugarsync.auth.end_point:
      return True
    else:
      return False



end_point = "http://www.amazon.com"



class Session(object):
  def __init__():
    self.username=None
    self.customer_id=None
    self.cookies={}
    self._initializing=True
    self._initializing=False

  def __repr__(self):
    return '<Session: %s>' % ",".join( [ k for k,v in self.cookies.items() ] )

  def __str__(self):
    return '<Session: %s>' % ",".join( [ k for k,v in self.cookies.items() ] )
    
  def is_valid(self):
    if self._initializing:
      return True
    else:
      return True

  def is_logined(self):
    return (self.is_valid() && username && customer_id)

  def update_cookies(self,cookie_str):
    self.cookies={}
    for c in cookie_str.split(", "):
      if c.startswith("session-") or c.startswith("ubid-") or c.startswith("x-") or \
                                                          c.startswith("__")or c.startswith("at-"):
        cookies.update( dict( re.sub(";.*","",c).split("=") ) )
