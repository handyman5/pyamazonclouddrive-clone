import httplib
import re
import sys
import urllib
import time

conn=httplib.HTTPConnection("www.amazon.com")
conn.request("GET","/")
res=conn.getresponse()
cookies = []
for c in res.getheader("Set-Cookie").split(", "):
  if c.startswith("session-") or c.startswith("ubid-"):
    cookies.append(re.sub(";.*","",c))
print cookies
print "*"*20
res.read()

headers={"Cookie":"; ".join(cookies)}
conn.request("GET","/",None,headers)
res=conn.getresponse()
cookies = []
for c in res.getheader("Set-Cookie").split(", "):
  if c.startswith("session-") or c.startswith("ubid-"):
    cookies.append(re.sub(";.*","",c))
print cookies
print "*"*20
res.read()

conn.close()

conn=httplib.HTTPSConnection("www.amazon.com")
headers={"Cookie":"; ".join(cookies)}
conn.request("GET","/clouddrive",None,headers)
res=conn.getresponse()
cookies = []
for c in res.getheader("Set-Cookie").split(", "):
  if c.startswith("session-") or c.startswith("ubid-"):
    cookies.append(re.sub(";.*","",c))
print cookies
print "*"*20
res.read()

location = res.getheader("Location")
path = location.split("www.amazon.com",1)[1]
#print path

headers={"Cookie":"; ".join(cookies)}
conn.request("GET",path,None,headers)
res=conn.getresponse()
#cookies = []
#for c in res.getheader("Set-Cookie").split(","):
#  cookies.append(re.sub(";.*","",c))
#print cookies
print "*"*20

begin='<form name="signIn"'
end='</form>'
html=begin + res.read().split(begin)[1].split(end)[0] +end


#conn.close()

#res=urllib2.urlopen("https://www.amazon.com/clouddrive/")
#begin='<form name="signIn"'
#end='</form>'
#html=begin + res.read().split(begin)[1].split(end)[0] +end
#res.close()

#print html.split("action")[1]

from HTMLParser import HTMLParser
class Parser(HTMLParser):
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

parser=Parser()
parser.feed(html)
parser.close()

action=parser.action.split("www.amazon.com",1)[1]
params=parser.key_value.copy()

#params["x"]=0
#params["y"]=0
params["create"]=0
#params["metadata1"]=""


from ConfigParser import SafeConfigParser
parser=SafeConfigParser()
parser.read("../amazon.ini")
config=dict(parser.items("Credentials"))

params["email"]=config["username"]
params["password"]=config["password"]

#print params
#print action
headers["Content-Type"]="application/x-www-form-urlencoded"
body=urllib.urlencode(params)
conn.request("POST",action,body,headers)
res=conn.getresponse()

cookies = []
for c in res.getheader("Set-Cookie").split(", "):
  if c.startswith("session-") or c.startswith("ubid-") or c.startswith("x-") or \
  c.startswith("__")or c.startswith("at-"):
    cookies.append(re.sub(";.*","",c))
print cookies
print "*"*20
res.read()

location = res.getheader("Location")
path = location.split("www.amazon.com",1)[1]
print path

headers={"Cookie":"; ".join(cookies)}
conn.request("GET",path,None,headers)
res=conn.getresponse()

for c in res.getheader("Set-Cookie").split(", "):
  if c.startswith("session-") or c.startswith("ubid-") or c.startswith("x-") or \
  c.startswith("__")or c.startswith("at-"):
    cookies.append(re.sub(";.*","",c))
print cookies
print "*"*20
#res.read()

"""location = res.getheader("Location")
path = location.split("www.amazon.com",1)[1]
print path

headers={"Cookie":"; ".join(cookies)}
conn.request("GET",path,None,headers)
res=conn.getresponse()
"""
html=res.read()

customer_id=html.split("customerId",1)[1]
customer_id=customer_id.split(">",1)[0]
customer_id=re.sub('.*value="','',customer_id)
customer_id=re.sub('".*','',customer_id)
print customer_id

username=html.split("customer_greeting",1)[1]
username=username.split("<",1)[0]
username=username.split(",")[1][1:]
username=re.sub(r'\..*','',username)
print username

print "*"*20

path="/clouddrive/api/?_=%d&Operation=getUserStorage&customerId=%s&ContentType=JSON" \
  %(int(time.time()),customer_id)
print path
headers={"Cookie":"; ".join(cookies)}
for c in cookies:
  if c.startswith("session-id="):
    headers["x-amzn-SessionId"]=c.replace("session-id=","")
conn.request("GET",path,None,headers)
res=conn.getresponse()

json=res.read()

print json
sys.exit(0)








import cookielib

amazon_cookies="""
.amazon.com	TRUE	/	FALSE	2082787201	ubid-main	192-3822733-3278467
.amazon.com	TRUE	/	FALSE	2082787201	session-id	192-9309567-1619917
.amazon.com	TRUE	/	FALSE	2082787201	session-id-time	2082787201l
"""


#redirect_handler = urllib2.HTTPRedirectHandler() 
#class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler): 
#    def http_error_302(self, req, fp, code, msg, headers): 
#        print headers 
#        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers) 
#    http_error_301 = http_error_303 = http_error_307 = http_error_302 
#cookieprocessor = urllib2.HTTPCookieProcessor() 
#opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor) 
#urllib2.install_opener(opener) 
#response =urllib2.urlopen("WHEREEVER") 
#print response.read() 

class MyCookiePolicy(cookielib.DefaultCookiePolicy):
    """Cookie Policy for live.com

    With python 2.6, cookie.DefaultCookiePolicy works. But with python 2.4,
    cookie.DefaultCookiePolicy won't accept cookies whose version > 0 unless
    rfc2965 is set to true. The domain ".login.live.com" isn't accepted also.
    """
    def set_ok(self, cookie, request):
        # Note: Fixed for python 2.4
        cookie.version = 0
        if not cookielib.DefaultCookiePolicy.set_ok(self, cookie, request):
            return False

        return True

policy = MyCookiePolicy(rfc2965 = True)

#cj = cookielib.FileCookieJar("cookie.txt")
#cj = cookielib.MozillaCookieJar(policy=policy)
cj = cookielib.MozillaCookieJar()
cj.load("cookie.txt",True)
print cj
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#urllib2.install_opener(opener)

#res=opener.open("http://www.amazon.com/")
print "*"*10

end_point="https://www.amazon.com/clouddrive/"
req=urllib2.Request(end_point)
#print cj._cookies_for_request(req)
print "*"*10

res=opener.open(end_point)
#res.headers.headers.append('Set-Cookie: ubid-main=002-8989859-9917520; path=/; domain=.amazon.com; expires=Tue Jan 01 08:00:01 2036 GMT')
#res.headers.headers.append('Set-Cookie: session-id-time=2082787201l; path=/; domain=.amazon.com; expires=Tue Jan 01 08:00:01 2036 GMT')
#res.headers.headers.append('Set-Cookie: session-id=189-6539933-5925661; path=/; domain=.amazon.com; expires=Tue Jan 01 08:00:01 2036 GMT')
#for cookie in cj.make_cookies(res,req):
#  cj.set_cookie(cookie)

print cj 
#cj.save("_cookie.txt",True)
print "*"*10

#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
req=urllib2.Request(end_point)
res=opener.open(req)
print cj
print "*"*10

begin='<form name="signIn"'
end='</form>'
html=begin + res.read().split(begin)[1].split(end)[0] +end

from HTMLParser import HTMLParser

class Parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.key_value={}
    self.action=""

  def handle_starttag(self, tag, attrs):
    d=dict(attrs)
    if tag=="form":
      self.action=d.get("action","")
    elif tag=='input':
      if d.get('name'):
        self.key_value[d.get('name')]=d.get('value','')
  def handle_endtag(self, tag):
    if tag=='input':
      pass

parser=Parser()
parser.feed(html)
parser.close()

#for key in parser.key_value.keys():
#  print "%s=%s"%(key,parser.key_value[key])

url=parser.action
params=parser.key_value.copy()

#params["x"]=0
#params["y"]=0
params["create"]=0
#params["metadata1"]=""


from ConfigParser import SafeConfigParser
parser=SafeConfigParser()
parser.read("../amazon.ini")
config=dict(parser.items("Credentials"))

params["email"]=config["username"]
params["password"]=config["password"]

import urllib

res=opener.open(url,urllib.urlencode(params))
#print res.read()
print cj

