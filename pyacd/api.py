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
"""API wrappers

* can_device_download: Check whether downloading is allowed.
* complete_file_upload_by_id: Finalize uploading file.
* copy_bulk_by_id: Copy file"s" or folder"s".
* create_by_id: Create file or folder into somewhere(specified id).
* create_by_path: Create file or folder into somewhere(specified absolute path).
* download_by_id: Download file after can_device_download
* empty_recycle_bin: Empty out "/RecycleBin".
* get_info_by_id: Get informations of file or folder(specified id).
* get_info_by_path: Get informations of file or folder(specified absolute path).
* get_subscription_problem: Get information of xxx(I don't know)
* get_upload_url_by_id: Get uploading URL to S3 after create_by_xxx.
* get_user_storage: Get informations of user storage.
* list_by_id: List entities in somewhere.
* move_bulk_by_id: Move file"s" or folder"s" to to somewhere.
* move_by_id: Move file or folder to to somewhere.
* recycle_bulk_by_id: Move file"s" or folder"s" to to "/RecycleBin".
* remove_bulk_by_id: Remove file"s" or folder"s".
* select_metadata: Query metadata like SQL.
* upload: Upload file's data to S3. (There is NOT such api but utility function)

Naming rules is following.
+-------------------------+----------------------------+
|pyacd.api's function name|Cloud Drive's operation name|
+-------------------------+----------------------------+
|snake case               |lower camel case            |
|(e.g. get_info_by_id)    |(e.g. getInfoById)          |
+-------------------------+----------------------------+

+-------------------------+----------------------------+
|pyacd.api's key name     |Cloud Drive's key name      |
+-------------------------+----------------------------+
|snake case               |lower camel case            |
|(e.g. object_id)         |(e.g. objectId)             |
+------------------------------------------------------+
|                    [Exceptions]                      |
+-------------------------+----------------------------+
|Type                     |type                        |
|modified                 |lastUpdatedDate             |
|created                  |creationDate                |
+------------------------------------------------------+
"""

import sys
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
  """Upload file's data to S3. (There is NOT such api but utility function)

  :type end_point: string
  :param end_point: uploading URL of S3

  :type parameters: dict
  :param parameters: uploading params of S3

  :type filename: string
  :param filename: file name stored in Amazon Cloud Drive

  :type filedata: binary
  :param filedata: like open("/path/to/file","rb").read()
  """
  params=parameters.copy()
  params["Filename"]=filename
  pyacd.post_multipart(end_point,params,{filename:filedata})

def complete_file_upload_by_id(object_id,storage_key):
  """Finalize uploading file.

  :type object_id: string
  :param object_id: upload_url.object_id

  :type storage_key: string
  :param storage_key: upload_url.storage_key
  """
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

def can_device_download():
  """Check whether downloading is allowed.

  :rtype: bool
  :return: whether downloading is allowed.
  """
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  operation="canDeviceDownload"
  params={
    "_":int(time.time()),
    "Operation":operation,
    "customerId":session.customer_id,
    "ContentType":"JSON",
    "deviceId.deviceType":"ubid",
    "deviceId.deviceSerialNumber":session.cookies["ubid-main"]
  }
  end_point=pyacd.api_root+"?"+urllib.urlencode(params)
  resp_json=json.loads(pyacd.conn.do_get(end_point))
  _error_check(resp_json)

  result=resp_json.get(operation+"Response").get(operation+"Result")
  return result["canDownload"]

def get_upload_url_by_id(object_id,size,method="POST"):
  """Get uploading URL to S3 after create_by_xxx.

  :type object_id: string
  :param object_id: 

  :type size: int
  :param size: like len(data)

  :type method: string
  :param method: I know only "POST".

  :rtype: :class:`pyacd.apiresponse.UploadUrl`
  :return: informations of uploading.
  """
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
  """Download file after can_device_download.

  :type object_id: string
  :param object_id: 

  :type attachment: (?)int
  :param attachment: (?)header of "Content-disposition: attachment"

  :rtype: binary
  :return: data stored in S3
  """
  session = pyacd.get_session()
  if not session.is_logined():
    raise pyacd.PyAmazonCloudDriveError("Not logined %s"%session)

  if not can_device_download():
    sys.stderr.write(
      "\n\n"+
      "You have exceeded the maximum number of devices allowed. "+
      "Downloading is disabled for this browser.\n\n"+
      "SEE ALSO http://www.amazon.com/gp/help/customer/display.html/?ie=UTF8&nodeId=200557340\n"+
      "Frequently Asked Questions\n"+
      "How many devices can I use to access the files I've stored in my Cloud Drive?\n"+
      "\n\n"
    )
    raise pyacd.PyAmazonCloudDriveError("device limit (up to eight devices.) can be reached.")

  params={
    "downloadById":object_id,
    "attachment":attachment
  }
  end_point=pyacd.api_root[:-1*len("/api/")]+"?"+urllib.urlencode(params)
  #print end_point
  return pyacd.conn.do_get(end_point)

def empty_recycle_bin():
  """Empty out "/RecycleBin".
  """
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
  """Move file"s" or folder"s" to to "/RecycleBin".

  :type source_inclusion_ids: list
  :param source_inclusion_ids: list of object_id
  """
  _operate2_bulk_by_id("recycleBulkById",source_inclusion_ids)

def remove_bulk_by_id(source_inclusion_ids=[]):
  """Remove file"s" or folder"s".

  :type source_inclusion_ids: list
  :param source_inclusion_ids: list of object_id
  """
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
  """Move file"s" or folder"s" to to somewhere.

  :type destination_parent_id: string
  :param destination_parent_id: folder's object_id

  :type source_inclusion_ids: list
  :param source_inclusion_ids: list of object_id

  :type conflict_resolution: string
  :param conflict_resolution: "RENAME" | "MERGE"
  """
  _operate1_bulk_by_id("moveBulkById",destination_parent_id,source_inclusion_ids,"MERGE")

def copy_bulk_by_id(destination_parent_id,source_inclusion_ids=[],conflict_resolution="RENAME"):
  """Copy file"s" or folder"s".
  :type destination_parent_id: string
  :param destination_parent_id: folder's object_id

  :type source_inclusion_ids: list
  :param source_inclusion_ids: list of object_id

  :type conflict_resolution: string
  :param conflict_resolution: "RENAME" | "MERGE"
  """
  _operate1_bulk_by_id("copyBulkById",destination_parent_id,source_inclusion_ids,"RENAME")

def move_by_id(source_id,destination_parent_id,destination_name,overwrite=False):
  """Move file or folder to to somewhere.

  :type source_id: string
  :param source_id: 

  :type destination_parent_id: string
  :param destination_parent_id: 

  :type destination_name: new name
  :param destination_name: 

  :type overwrite: bool
  :param overwrite: whether override or not.
  """
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
  """Create file or folder into somewhere(specified absolute path).

  :type path: string
  :param path: 

  :type name: string
  :param name: 

  :type Type: string
  :param Type: pyacd.types.FILE | pyacd.types.FOLDER

  :type conflict_resolution: string
  :param conflict_resolution: "RENAME" | "MERGE"

  :type overwrite: bool
  :param overwrite: whether override or not.

  :type autoparent: bool
  :param autoparent: (?)

  :rtype: :class:`pyacd.apiresponse.Info`
  :return: information of created one.
  """
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
  """Create file or folder into somewhere(specified id).

  :type parent_id: string
  :param parent_id: 

  :type name: string
  :param name: 

  :type Type: string
  :param Type: pyacd.types.FILE | pyacd.types.FOLDER

  :type overwrite: bool
  :param overwrite: whether override or not.

  :rtype: :class:`pyacd.apiresponse.Info`
  :return: information of created one.
  """
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
  """List entities in somewhere.

  :type object_id: string
  :param object_id: 

  :type ordering: string
  :param ordering: comma separated and like "order by" in SQL
                   e.g. keyName
                        type,keyName,creationDate

  :type next_token: (?)int
  :param next_token: (?)

  :type max_items: int
  :param max_items: None means unlimited

  :type Filter: string
  :param Filter: like "where" in SQL
                 e.g. type = "FOLDER" and hidden = false
                      type != "RECYCLE" and status != "PENDING" and hidden = false

  :rtype: :class:`pyacd.apiresponse.List`
  :return: informations listed.
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
  """Query metadata like SQL.

  :type query: string
  :param query: like SQL
                e.g. select count(*) from object where hidden != true and parentObjectId='xxx' and status != 'PENDING' and type != 'RECYCLE' and type = "FOLDER"
                     select count(*) from object where hidden != true and parentObjectId='xxx' and status != 'PENDING' and type != 'RECYCLE'
                     select distinct parentObjectId from object where parent.parentObjectId='xxx' and type != "RECYCLE" and hidden = false and status != "PENDING"
                     select distinct parentObjectId from object where parent.parentObjectId='xxx' and type = 'FOLDER' and hidden = false
                     select creationDate, extension, objectId, keyName, purchaseDate, parentObjectId, status, name, lastModifiedDate, version, type, size, parent.name from object where purchaseDate = null and type='FILE' and hidden=false and status='AVAILABLE' order by creationDate DESC,keyName limit 0, 2
                     select creationDate, extension, objectId, keyName, purchaseDate, parentObjectId, status, name, lastModifiedDate, version, type, size, parent.name from object where type='FILE' and hidden=false and status='AVAILABLE' order by creationDate DESC,keyName limit 0, 2

  :rtype: :class:`pyacd.apiresponse.Metadata`
  :return: informations selected.
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
  """Get informations of file or folder(specified absolute path).

  :type path: string
  :param path: 

  :rtype: :class:`pyacd.apiresponse.Info`
  :return: information.
  """
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
  """Get informations of file or folder(specified id).

  :type object_id: string
  :param object_id: 

  :rtype: :class:`pyacd.apiresponse.Info`
  :return: information.
  """
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
  """Get informations of user storage.

  :rtype: :class:`pyacd.apiresponse.UserStorage`
  :return: information.
  """
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
  """Get information of xxx. (I don't know)

  :rtype: :class:`pyacd.apiresponse.SubscriptionProblem`
  :return: (?)
  """
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






