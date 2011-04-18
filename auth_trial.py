import urllib2
import cookielib


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

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#urllib2.install_opener(opener)

#res=opener.open("http://www.amazon.com/")

end_point="https://www.amazon.com/clouddrive/"
req=urllib2.Request(end_point,None,{'Cookie':'ubid-main=002-8989859-9917520; session-id-time=2082787201l;session-id=189-6539933-5925661;'})

res=opener.open(req)
#res.headers.headers.append('Set-Cookie: ubid-main=002-8989859-9917520; path=/; domain=.amazon.com; expires=Tue Jan 01 08:00:01 2036 GMT')
#res.headers.headers.append('Set-Cookie: session-id-time=2082787201l; path=/; domain=.amazon.com; expires=Tue Jan 01 08:00:01 2036 GMT')
#res.headers.headers.append('Set-Cookie: session-id=189-6539933-5925661; path=/; domain=.amazon.com; expires=Tue Jan 01 08:00:01 2036 GMT')
for cookie in cj.make_cookies(res,req):
  cj.set_cookie(cookie)

print cj 
print "*"*10

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
req=urllib2.Request(end_point)
print cj._cookies_for_request(req)
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


