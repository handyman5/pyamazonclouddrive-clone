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

# These are respective contributors who gives valuable feedback.
# - Adam Compton (https://github.com/handyman5)
# - Matt Luongo (https://github.com/mhluongo)

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
 * pyacd.set_amazon_domain()
 * pyacd.Session
 * pyacd.api.*
 * pyacd.types.*
 * pyacd.status.*
 * pyacd.PyAmazonCloudDriveApiException
 * pyacd.PyAmazonCloudDriveError

Sample code(Downloading)
----
import pyacd
session = pyacd.login("someone@example.com","foobar")
if session and session.is_logged_in():
  fileobj = pyacd.api.get_info_by_path("/path/to/file")
  data=pyacd.api.download_by_id(fileobj.object_id)
----

Sample code(Uploading)
----
import pyacd
session = pyacd.login("someone@example.com","foobar")
if session and session.is_logged_in() and session.agreed_with_terms:
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

__author__ = "Youhei Sakurai"
__credits__ = ["Adam Compton", "Matt Luongo"]
__copyright__ = "Copyright (c) 2011 anatanokeitai.com(sakurai_youhei)"
__license__ = "MIT"
__version__ = "0.1.2"
__maintainer__ = "Youhei Sakurai"
__status__ = "Prototype"

from pyacd.exception import *
from pyacd.connection import do_get, do_delete, do_post, do_put
from pyacd.multipart import do_post_multipart

from pyacd.auth import login, Session

import types
import status
import api

import urllib2

debug_level=0
amazon_domain="www.amazon.com"
api_root="https://"+amazon_domain+"/clouddrive/api/"


session = None
opener = None

def set_amazon_domain(domain):
  """ Switch Amazon's domain. e.g. from www.amazon.com to www.amazon.co.jp
  :type domain: string
  """
  global amazon_domain,api_root
  amazon_domain=domain
  api_root="https://"+amazon_domain+"/clouddrive/api/"

def get_session():
  """ Get current session having login status and tokens.
  :rtype: :class:`pyacd.session.Session`
  :return: Inclues cookies, username and customer_id.
  """
  return session

def rebuild_opener():
  global opener
  if not session:
    raise PyAmazonCloudDriveError("pyacd.session must not be None.")
  opener = urllib2.build_opener(CustomHTTPCookieProcessor(session.cookies))
  opener.addheaders = [(
    'User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7'
  )]

def get_device_serial_number():
  ubidlist = {
    "www.amazon.com": "ubid-main",
    "www.amazon.co.jp": "ubid-acbjp"
  }
  return session.cookies._cookies[amazon_domain[3:]]["/"][ubidlist[amazon_domain]].value

# Below codes is from http://weboo-returns.com/blog/urllib2-raises-error-by-201-response/
class CustomHTTPCookieProcessor(urllib2.HTTPCookieProcessor):
  def http_error_201(self, request, response, code, msg, hdrs):
    return response
  def http_error_204(self, request, response, code, msg, hdrs):
    return response
  def http_error_206(self, request, response, code, msg, hdrs):
    return response
