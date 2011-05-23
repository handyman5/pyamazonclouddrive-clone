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


class UploadUrl(object):
  def __init__(self,result_json):
    self.object_id=result_json.get("objectId")
    self.path=result_json.get("path")
    self.storage_key=result_json.get("storageKey")
    self.http_request=HttpRequest(result_json.get("httpRequest"))
    
  def __repr__(self):
    return '<UploadUrl: %s>' % (self.object_id)

  def __str__(self):
    return '<UploadUrl: %s>' % (self.object_id)

class HttpRequest(object):
  def __init__(self,result_json):
    self.headers=result_json.get("headers")
    self.end_point=result_json.get("endpoint")
    self.method=result_json.get("methodName")
    self.resource_path=result_json.get("resourcePath")
    self.parameters=result_json.get("parameters")
    #print self.parameters.keys()
    
    
  def __repr__(self):
    return '<HttpRequest: %s,%s>' % (self.method,self.end_point)

  def __str__(self):
    return '<HttpRequest: %s,%s>' % (self.method,self.end_point)


class List(object):
  def __init__(self,result_json):
    self.next_token=result_json.get("nextToken")
    self.parent_modified=result_json.get("parentLastUpdated")
    self.objects=[]
    for obj in result_json.get("objects"):
      self.objects.append(Info(obj))

  def __repr__(self):
    return '<List: includes %d objects)>' % (len(self.objects))

  def __str__(self):
    return '<List: includes %d objects)>' % (len(self.objects))

class Metadata(object):
  def __init__(self,result_json):
    self.items=result_json.get("items")

  def __repr__(self):
    return '<Metadata: includes %d items)>' % (len(self.items))

  def __str__(self):
    return '<Metadata: includes %d items)>' % (len(self.items))
 
class Info(object):
  def __init__(self,result_json):
    self.parent_object_id=result_json.get("parentObjectId")
    self.status=result_json.get("status")
    self.purchased=result_json.get("purchaseDate")
    self.size=result_json.get("size")
    self.object_id=result_json.get("objectId")
    self.storage_system=result_json.get("storageSystem")
    self.version=result_json.get("version")
    self.hidden=result_json.get("hidden")
    self.md5=result_json.get("md5")
    self.Type=result_json.get("type")
    self.name=result_json.get("name")
    self.path=result_json.get("path")
    if len(self.name) and self.path:
      self.path=self.path[:-1*len(self.name)]
    self.created=result_json.get("creationDate")
    self.parent_path_before_recycle=result_json.get("parentPathBeforeRecycle")
    self.modified=result_json.get("lastUpdatedDate")
    # Unknown usage
    # keyName,asin,metadata,orderId,permissions,extension,localFilePath

    if self.storage_system:
      self.storage_system=StorageSystem(self.storage_system)
    #if self.purchased:
    #  time.asctime(time.localtime(self.purchased))
    #if self.created:
    #  time.asctime(time.localtime(self.purchased))
    #if self.modified:
    #  time.asctime(time.localtime(self.purchased))

  def __repr__(self):
    return '<Info: %s%s (type=%s,status=%s,version=%d)>' % (self.path,self.name,self.Type,self.status,self.version)

  def __str__(self):
    return '<Info: %s%s (type=%s,status=%s,version=%d)>' % (self.path,self.name,self.Type,self.status,self.version)

class StorageSystem(object):
  def __init__(self,result_json):
     self.encrypted=result_json.get("encrypted")
     self.storage_key=result_json.get("storageKey")
     self.payer_id=result_json.get("payerId") 
     self.Type=result_json.get("type") 
    
  def __repr__(self):
    return '<StrageSystem: (encrypted=%s,player_id=%s,type=%d)>' % (self.encrypted,self.payer_id,self.Type)

  def __str__(self):
    return '<StrageSystem: (encrypted=%s,player_id=%s,type=%d)>' % (self.encrypted,self.payer_id,self.Type)
    
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

class SubscriptionProblem(object):
  def __init__(self,result_json):
    self.previous_plan_detail = result_json.get("previousPlanDetail")
    self.problem_code = result_json.get("problemCode")
    self.target_plan_id = result_json.get("targetPlanId")
    self.transaction_type = result_json.get("transactionType")

  def __repr__(self):
    return '<SubscriptionProblem: %s,%s,%s,%s>' % (
        self.previous_plan_detail,self.problem_code,
        self.target_plan_id,self.transaction_type)

  def __str__(self):
    return '<SubscriptionProblem: %s,%s,%s,%s>' % (
        self.previous_plan_detail,self.problem_code,
        self.target_plan_id,self.transaction_type)
