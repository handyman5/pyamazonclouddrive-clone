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

import pyacd
pyacd.debug_level=2

config_file="../pyacd.ini"

parser=SafeConfigParser()
parser.read(config_file)
credentials=dict(parser.items("Credentials"))

email=credentials.get("email",None)
password=credentials.get("password",None)
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
    sys.stderr.write(str(session))

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
    user_storage = pyacd.get_user_storage()
    self.assertEqual(user_storage.total_space,user_storage.
        used_space+user_storage.free_space,"total /= used+free %s"%user_storage)
    sys.stderr.write(str(user_storage))

  def testSubscriptionProblem(self):
    subscription_problem=pyacd.get_subscription_problem()
    sys.stderr.write(str(subscription_problem))

  def testInfoByPathAndById(self):
    info_by_path=pyacd.get_info_by_path("/")
    sys.stderr.write(str(info_by_path))
    info_by_id=pyacd.get_info_by_id(info_by_path.object_id)
    sys.stderr.write(str(info_by_path))

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
    
    
