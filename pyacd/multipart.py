# Original code is following URL
# http://stackoverflow.com/questions/1254270/multipart-form-post-to-google-app-engine-not-working


import mimetypes
import urllib2
import httplib
import sys

import pyacd

def do_post_multipart(url, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    #print body

    # Issue 1
    # http://code.google.com/p/pyamazonclouddrive/issues/detail?id=1
    hs={'content-type': content_type,'content-length': str(len(body))}

    return pyacd.do_post(url,body,hs)

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

