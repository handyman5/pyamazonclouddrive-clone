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
import time
import urllib
try:
  import json
except ImportError,e:
  import simplejson as json

import pyacd
from apiresponse import *


def _error_check(resp_json):
  if resp_json.get("Error"):
    print end_point
    raise pyacd.PyAmazonCloudDriveApiException(resp_json.get("Error"))
    
    
    
def list_by_id(objectId,ordering=None,next_token=0,max_items=None,filter=None):
  """
  ordering examles.
    keyName
    type,keyName,creationDate
  filter examles.
    type = "FOLDER" and hidden = false
    type != "RECYCLE" and status != "PENDING" and hidden = false
  """
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="listById"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "query":query
  }
  
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")
  return Metadata(result)


def select_metadata(query):
  """
  query examles.
    select count(*) from object where hidden != true and parentObjectId="xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" and status != "PENDING" and type != "RECYCLE" and type = "FOLDER"
    select count(*) from object where hidden != true and parentObjectId="xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" and status != "PENDING" and type != "RECYCLE"
    select distinct parentObjectId from object where parent.parentObjectId="xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" and type != "RECYCLE" and hidden = false and status != "PENDING"
    select distinct parentObjectId from object where parent.parentObjectId="xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" and type = "FOLDER" and hidden = false
  """
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="selectMetadata"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "query":query
  }
  
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")
  return Metadata(result)

def get_info_by_path(path):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="getInfoByPath"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "path":path,
    "populatePath":"true"
  }

  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")
  return Info(result)

def get_info_by_id(object_id):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="getInfoById"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "objectId":object_id,
    "populatePath":"true"
  }

  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")
  return Info(result)


def get_user_storage():
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="getUserStorage"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON"
  }

  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")

  return UserStorage(result)




def get_subscription_problem():
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="getSubscriptionProblem"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON"
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")

  return SubscriptionProblem(result)






