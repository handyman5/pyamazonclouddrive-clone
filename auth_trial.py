import urllib2

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

  def handle_starttag(self, tag, attrs):
    if tag=='input':
      d=dict(attrs)
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





