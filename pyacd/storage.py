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


class UserStorage(object):
  def __init__(self,result_json):
    self.total_space=result_json.get("totalSpace")
    self.used_space=result_json.get("usedSpace")
    self.free_space=result_json.get("freeSpace")
    if not self.total_space or not self.used_space or not self.free_space:
      raise pyacd.PyAmazonCloudDriveError("unexpected response %s"%str(result_json))
  
  def __repr__(self):
    return '<Storage: (total)%d = (used)%d + (free)%d>' % (
        self.total_space,self.used_space,self.free_space)

  def __str__(self):
    return '<Storage: (total)%d = (used)%d + (free)%d>' % (
        self.total_space,self.used_space,self.free_space)
