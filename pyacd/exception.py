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


class PyAmazonCloudDriveError(StandardError):
  """General error"""

  def __init__(self, reason):
    StandardError.__init__(self)
    self.reason = reason

  def __repr__(self):
    return 'PyAmazonCloudDriveError: %s' % self.reason

  def __str__(self):
    return 'PyAmazonCloudDriveError: %s' % self.reason

class PyAmazonCloudDriveApiException(PyAmazonCloudDriveError):
  """server returns error code and message"""

  def __init__(self,error_obj):
      if not isinstance(error_obj,dict):
        PyAmazonCloudDriveError.__init__(self,error_obj)
      else:
        self.message=error_obj.get("Message")
        self.code=error_obj.get("Code")
        self._type=error_obj.get("Type")
        PyAmazonCloudDriveError.__init__(self,"%s:%s"%(self.code,self.message))
