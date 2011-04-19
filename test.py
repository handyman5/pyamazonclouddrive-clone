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
from ConfigParser import SafeConfigParser
import time

import pysugarsync
pysugarsync.debug_level=2

config_file="../pysugarsync.ini"

parser=SafeConfigParser()
parser.read(config_file)
credentials=dict(parser.items("Credentials"))

username=credentials.get("username",None)
password=credentials.get("password",None)
access_key=credentials.get("accesskey",None)
private_access_key=credentials.get("privateaccesskey",None)

user=None
token=None

class ActionTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testFileAction(self):
    base_folder = pysugarsync.get_base_folder(user.magic_briefcase)
    sys.stderr.write("%s->"%base_folder.name)

    subfolder="dir_%d"%int(time.time())
    base_folder.create_subfolder(subfolder)

    for folder in base_folder.subfolders():
      if folder.name==subfolder:
        sys.stderr.write("%s->"%folder.name)
        folder.upload_file("README")

  def testFolderAction(self):
    base_folder = pysugarsync.get_base_folder(user.magic_briefcase)
    sys.stderr.write("%s->"%base_folder.name)

    subfolder="dir_%d"%int(time.time())
    base_folder.create_subfolder(subfolder)

    for folder in base_folder.subfolders():
      if folder.name==subfolder:
        sys.stderr.write("%s->"%folder.name)
        #folder.upload_file("README")
        folder.rename("dir_renamed")
        sys.stderr.write("%s->"%folder.name)
        folder.delete()
        #print f.get_folders()
        #print f.get_files()
        
class UserTest(unittest.TestCase):
  def setUp(self):
    pass
    
  def tearDown(self):
    pass

  def testUserRepresentation(self):
    global user
    user = pysugarsync.get_user()
    self.assertEqual(user.username,username,"username is invalid. %s"%user.username)
    self.assertNotEqual(user.nickname,None,"nickname is None")
    self.assertNotEqual(user.usage,None,"usage is None")
    self.assertNotEqual(user.limit,None,"limit is None")


class AuthTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testRetrieveToken(self):
    global token
    token=pysugarsync.retrieve_token(
        username=username,
        password=password,
        access_key=access_key,
        private_access_key=private_access_key
    )
    self.assertTrue(pysugarsync.is_valid_token(token,"",""),"invalid url %s"%token)

  def testSetToken(self):
    pysugarsync.set_token(token)

    

def main():
  suites=[]
  
  suites.append(unittest.TestLoader().loadTestsFromTestCase(AuthTest))
  suites.append(unittest.TestLoader().loadTestsFromTestCase(UserTest))
  suites.append(unittest.TestLoader().loadTestsFromTestCase(ActionTest))

  runner = unittest.TextTestRunner(verbosity=2)

  for s in suites:
    runner.run(s)

#  suite=unittest.TestSuite(suites)
#  runner.run(suite)


if __name__=="__main__":
  main()
    
    
