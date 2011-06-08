#!/usr/bin/env python
#
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
 
import sys
import unittest
from cStringIO import StringIO
#from ConfigParser import SafeConfigParser
import time
import xml.dom.minidom

import pyacd
pyacd.debug_level=2

"""
config_file="../pyacd.ini"

parser=SafeConfigParser()
parser.read(config_file)
credentials=dict(parser.items("Credentials"))

email=credentials.get("email",None)
password=credentials.get("password",None)
"""
if len(sys.argv)!=3:
  sys.stderr.write("usage: ./test.py email password")
  sys.exit(2)

email=sys.argv[1]
password=sys.argv[2]

print "**Config**"
print "email->",email
print "password->",password
print "*"*20

session=None

class AuthTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testLogin(self):
    global session
    session=pyacd.login(email,password)
    self.assertTrue(session.is_valid(),"invalid session %s"%session)
    self.assertTrue(session.is_logined(),"not logined %s"%session)
    self.assertNotEqual(session.username,None,"username is None %s"%session)
    self.assertNotEqual(session.customer_id,None,"customer_id is None %s"%session)
    #sys.stderr.write(str(session))

"""
  def testLoginWithNoneEmail(self):
    global session
    try:
      session=pyacd.login(None,password)
    except TypeError,e:
      pass

  def testLoginWithNonePassword(self):
    global session
    try:
      session=pyacd.login(email,None)
    except TypeError,e:
      pass

  def testLoginWithNoneArgs(self):
    global session
    try:
      session=pyacd.login(None,None,None)
    except TypeError,e:
      pass

  def testReloginWithSession(self):
    global session
    session=pyacd.login(session=session)
    self.assertTrue(session.is_valid(),"invalid session %s"%session)
    self.assertTrue(session.is_logined(),"not logined %s"%session)
    self.assertNotEqual(session.username,None,"username is None %s"%session)
    self.assertNotEqual(session.customer_id,None,"customer_id is None %s"%session)
"""
    
class ApiTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testUserStorage(self):
    user_storage = pyacd.api.get_user_storage()
    self.assertEqual(user_storage.total_space,user_storage.
        used_space+user_storage.free_space,"total /= used+free %s"%user_storage)
    #sys.stderr.write(str(user_storage))

  def testSubscriptionProblem(self):
    subscription_problem=pyacd.api.get_subscription_problem()
    #sys.stderr.write(str(subscription_problem))

  def testInfoByPathAndById(self):
    info_by_path=pyacd.api.get_info_by_path("/")
    #sys.stderr.write(str(info_by_path))
    info_by_id=pyacd.api.get_info_by_id(info_by_path.object_id)
    #sys.stderr.write(str(info_by_path))
    self.assertEqual(info_by_path.name,info_by_id.name,"different from byPath(%s) and byId(%s)"%
                    (info_by_path,info_by_id))

  def testListById(self):
    info=pyacd.api.get_info_by_path("/")
    pyacd.api.list_by_id(info.object_id)

  def testFolder_Create_Rename_Copy_Recycle_Remove(self):
    root=pyacd.api.get_info_by_path("/")
    old_name="create_%d"%int(time.time())
    new_name=old_name.replace("create","rename")
    
    # folder1 create(old_name) -> rename(new_name)
    folder1=pyacd.api.create_by_id(root.object_id,old_name)
    pyacd.api.move_by_id(folder1.object_id,root.object_id,new_name)

    # folder2 create(old_name) -> copy to new_name/ move to new_name/
    folder2=pyacd.api.create_by_id(root.object_id,old_name)
    pyacd.api.copy_bulk_by_id(folder1.object_id,[folder2.object_id,])
    pyacd.api.move_bulk_by_id(folder1.object_id,[folder2.object_id,])

    # folder1 recycle -> remove
    pyacd.api.recycle_bulk_by_id([folder1.object_id,])
    pyacd.api.remove_bulk_by_id([folder1.object_id,])

  def testEmptyRecycleBin(self):
    pyacd.api.empty_recycle_bin()

  def testFile_Create_Upload_Download(self):
    filename = "test_%d.txt"%int(time.time())
    filedata = "12345"
    
    # file1 create
    file1 = pyacd.api.create_by_path("/",filename)

    # get upload_url
    upload_url = pyacd.api.get_upload_url_by_id(file1.object_id,len(filedata))
    storage_key=upload_url.storage_key
    object_id=upload_url.object_id
    end_point=upload_url.http_request.end_point
    parameters=upload_url.http_request.parameters

    # upload file
    pyacd.api.upload(end_point,parameters,filename,filedata)

    # completeing file
    pyacd.api.complete_file_upload_by_id(object_id,storage_key)

    # download file
    download_data=pyacd.api.download_by_id(object_id)
    
    self.assertEqual(filedata,download_data,"different from upload and download")
    


def main():
  suites=[]
  
  suites.append(unittest.TestLoader().loadTestsFromTestCase(AuthTest))
  suites.append(unittest.TestLoader().loadTestsFromTestCase(ApiTest))

  runner = unittest.TextTestRunner(verbosity=2)

  for s in suites:
    runner.run(s)

#  suite=unittest.TestSuite(suites)
#  runner.run(suite)


if __name__=="__main__":
  main()
    
    
