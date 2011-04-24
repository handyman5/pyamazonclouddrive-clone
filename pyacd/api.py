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
    raise pyacd.PyAmazonCloudDriveApiException(resp_json.get("Error"))

def upload(end_point,parameters,filename,filedata):
  params=parameters.copy()
  params["Filename"]="sample.txt"
  pyacd.post_multipart(end_point,params,{filename:filedata})

def complete_file_upload_by_id(object_id,storage_key):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="completeFileUploadById"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "objectId":object_id,
    "storageKey":storage_key,
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)

def get_upload_url_by_id(object_id,size,method="POST"):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="getUploadUrlById"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "objectId":object_id,
    "size":size,
    "method":method
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)

  result=resp_json.get(operation+"Response").get(operation+"Result")
  return UploadUrl(result)

def download_by_id(object_id,attachment=0):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  params={
    "downloadById":object_id,
    "attachment":attachment
  }
  end_point=pyacd.api_root[:-1*"/api/"]+"?"+urllib.urlencode(params)
  print end_point
  return pyacd.conn.do_get(end_point)

def empty_recycle_bin():
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="emptyRecycleBin"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)

def recycle_bulk_by_id(source_inclusion_ids=[]):
  _operate2_bulk_by_id("recycleBulkById",source_inclusion_ids)

def remove_bulk_by_id(source_inclusion_ids=[]):
  _operate2_bulk_by_id("removeBulkById",source_inclusion_ids)

def _operate2_bulk_by_id(operation,source_inclusion_ids):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  if len(source_inclusion_ids)==0:
    raise pyacd.PyAmazonCloudDriveError("No source ids %s"%str(source_inclusion_ids))

  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
  }
  params.update(dict([["inclusionIds.member.%d"%(i+1),source_inclusion_ids[i]] for i in range(len(source_inclusion_ids))]))
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
    
def _operate1_bulk_by_id(operation,destination_parent_id,source_inclusion_ids,conflict_resolution):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  if len(source_inclusion_ids)==0:
    raise pyacd.PyAmazonCloudDriveError("No source ids %s"%str(source_inclusion_ids))

  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "destinationParentId":destination_parent_id,
    "conflictResolution":conflict_resolution,
  }
  params.update(dict([["sourceInclusionIds.member.%d"%(i+1),source_inclusion_ids[i]] for i in range(len(source_inclusion_ids))]))
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)

def move_bulk_by_id(destination_parent_id,source_inclusion_ids=[],conflict_resolution="MERGE"):
  _operate1_bulk_by_id("moveBulkById",destination_parent_id,source_inclusion_ids,"MERGE")

def copy_bulk_by_id(destination_parent_id,source_inclusion_ids=[],conflict_resolution="RENAME"):
  _operate1_bulk_by_id("copyBulkById",destination_parent_id,source_inclusion_ids,"RENAME")

def move_by_id(source_id,destination_parent_id,destination_name,overwrite=False):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="moveById"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "sourceId":source_id,
    "destinationParentId":destination_parent_id,
    "destinationName":destination_name,
    "overwrite":"true" if overwrite else "false"
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)


def create_by_path(path,name,Type=pyacd.types.FILE,conflict_resolution="RENAME",overwrite=False,autoparent=True):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="createByPath"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "path":path,
    "name":name,
    "type":Type,
    "conflictResolution":conflict_resolution,
    "overwrite":"true" if overwrite else "false",
    "autoparent":"true" if autoparent else "false"
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")
  return Info(result.get("info"))

def create_by_id(parent_id,name,Type=pyacd.types.FOLDER,overwrite=False):
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="createById"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "parentId":parent_id,
    "name":name,
    "type":Type,
    "overwrite":"true" if overwrite else "false"
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")
  return Info(result.get("info"))


def list_by_id(object_id,ordering=None,next_token=0,max_items=None,Filter=None):
  """
  ordering examles.
    keyName
    type,keyName,creationDate
  Filter examles.
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
    "objectId":object_id,
    "nextToken":next_token
  }
  if ordering:params["ordering"]=ordering
  if max_items:params["maxItems"]=max_items
  if Filter:params["filter"]=Filter
  
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)
  result=resp_json.get(operation+"Response").get(operation+"Result")
  return List(result)


def select_metadata(query):
  """
  query examles.
    select count(*) from object where hidden != true and parentObjectId='xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' and status != 'PENDING' and type != 'RECYCLE' and type = "FOLDER"
    select count(*) from object where hidden != true and parentObjectId='xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' and status != 'PENDING' and type != 'RECYCLE'
    select distinct parentObjectId from object where parent.parentObjectId='xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' and type != "RECYCLE" and hidden = false and status != "PENDING"
    select distinct parentObjectId from object where parent.parentObjectId='xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' and type = 'FOLDER' and hidden = false
    select creationDate, extension, objectId, keyName, purchaseDate, parentObjectId, status, name, lastModifiedDate, version, type, size, parent.name from object where purchaseDate = null and type='FILE' and hidden=false and status='AVAILABLE' order by creationDate DESC,keyName limit 0, 2
    select creationDate, extension, objectId, keyName, purchaseDate, parentObjectId, status, name, lastModifiedDate, version, type, size, parent.name from object where type='FILE' and hidden=false and status='AVAILABLE' order by creationDate DESC,keyName limit 0, 2
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






