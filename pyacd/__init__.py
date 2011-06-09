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

"""Library to access Amazon Cloud Drive

Amazon Cloud Drive is based on...

 * Authentication: cookie based
 * RequestFormat: query strings (e.g. https://....?operation=foo&param=bar)
 * ResponseFormat: JSON
 * Entity's data: stored S3
 * Entity's metadata: probably stored like following
+-----------+------------------------------------------------------
|primary key|foreign keys               |
+-----------+---------------+-----------+------+-----+--------+----
|objectId   |parentObjectId |customerId | path |name |version |....
+-----------+---------------+-----------+------+-----+--------+----
|...        |...            |...        |...   |...  |...     +....
+-----------+---------------+-----------+------+-----+--------+----

You may use following functions and classes...

 * pyacd.login()
 * pyacd.api.*
 * pyacd.types.*
 * pyacd.status.*
 * pyacd.PyAmazonCloudDriveApiException
 * pyacd.PyAmazonCloudDriveError

Sample code(Downloading)
----
import pyacd
session = pyacd.login("someone@example.com","foobar")
if session and session.is_logined():
  fileobj = pyacd.api.get_info_by_path("/path/to/file")
  data=pyacd.api.download_by_id(fileobj.object_id)
----

Sample code(Uploading)
----
import pyacd
session = pyacd.login("someone@example.com","foobar")
if session and session.is_logined():
  fileobj = pyacd.api.create_by_path("/path/to/upload","filename")
  data = open("/path/to/file","rb").read()
  upload_url = pyacd.api.get_upload_url_by_id(fileobj.object_id,len(data))
  pyacd.api.upload(upload_url.http_request.end_point,
                   upload_url.http_request.parameters,
                   "filename",data)
  pyacd.api.complete_file_upload_by_id(upload_url.object_id,
                                       upload_url.storage_key)
----
"""

__author__ = "sakurai_youhei"
__copyright__ = "Copyright (c) 2011 anatanokeitai.com(sakurai_youhei)"
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "sakurai_youhei"
__status__ = "Prototype"


from pyacd.exception import *
from pyacd.connection import Connection
from pyacd.multipart import post_multipart

from pyacd.auth import login

import types
import status

import api


debug_level=0
conn=Connection()
api_root="https://www.amazon.com/clouddrive/api/"

def get_session():
  """ Get current session having login status and tokens.
  :rtype: :class:`pyacd.session.Session`
  :return: Inclues cookies, username and customer_id.
  """
  return conn.session
