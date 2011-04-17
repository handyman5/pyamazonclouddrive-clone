import urllib2
import cookielib

#cj = cookielib.CookieJar()
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#urllib2.install_opener(opener)

end_point="https://www.amazon.com/clouddrive/"
res=urllib2.urlopen(end_point)
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

for key in parser.key_value.keys():
  print "%s=%s"%(key,parser.key_value[key])

url=parser.action
params=parser.key_value.copy()

params["x"]=0
params["y"]=0
params["create"]=0
#params["metadata1"]=""


from ConfigParser import SafeConfigParser
parser=SafeConfigParser()
parser.read("../amazon.ini")
config=dict(parser.items("Credentials"))

params["email"]=config["username"]
params["password"]=config["password"]

import urllib

res=urllib2.urlopen(url,urllib.urlencode(params))
print res.read()


