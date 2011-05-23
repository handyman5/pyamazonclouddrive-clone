# Original code is following URL
# http://stackoverflow.com/questions/1254270/multipart-form-post-to-google-app-engine-not-working


import mimetypes
import urllib2
import httplib
import sys

import pyacd
from pyacd.exception import PyAmazonCloudDriveError
from pyacd.connection import gen_httplib_conn

def post_multipart(url, fields, files):
    method="POST"
    content_type, body = encode_multipart_formdata(fields, files)
    #print body

    # Issue 1
    # http://code.google.com/p/pyamazonclouddrive/issues/detail?id=1
    hs={'content-type': content_type,'content-length': str(len(body))}

    scheme,host = urllib2.urlparse.urlparse(url)[:2]

    conn=gen_httplib_conn(scheme,host)

    path = url.split(host,1)[1]
    conn.request(method,path,body,hs)

    if pyacd.debug_level:
      sys.stderr.write(method)

    resp = conn.getresponse()
    #print "code->",resp.status
    if 400< resp.status <599:
      sys.stderr.write(resp.read())
      raise PyAmazonCloudDriveError("response code is %d"%resp.status)

    if pyacd.debug_level:
      sys.stderr.write("->")

    #if resp.getheader("Location"):
    #  return pyacd.conn.do_get(resp.getheader("Location"))

    resp_body=resp.read()
    conn.close()
    return resp_body

def encode_multipart_formdata(fields, files):
    """
    fields is a dict of (name, value) elements for regular form fields.
    files is a dict of (filename, filedata) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for key, value in fields.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for filename, filedata in files.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="file"; filename="%s"' % (filename))
        L.append('Content-Type: %s' % 'application/octet-stream')
        L.append('')
        L.append(filedata)
    L.append('--' + BOUNDARY + '--')
    L.append('')

    # Issue 1
    # http://code.google.com/p/pyamazonclouddrive/issues/detail?id=1
    body = CRLF.join([x if type(x)==str else str(x) for x in L])

    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

