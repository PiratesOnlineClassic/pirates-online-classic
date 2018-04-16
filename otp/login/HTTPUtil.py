# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.HTTPUtil
from pandac.PandaModules import *


class HTTPUtilException(Exception):

    def __init__(self, what):
        Exception.__init__(self, what)


class ConnectionError(HTTPUtilException):

    def __init__(self, what, statusCode):
        HTTPUtilException.__init__(self, what)
        self.statusCode = statusCode


class UnexpectedResponse(HTTPUtilException):

    def __init__(self, what):
        HTTPUtilException.__init__(self, what)


def getHTTPResponse(url, http, body=''):
    if body:
        hd = http.postForm(url, body)
    else:
        hd = http.getDocument(url)
    if not hd.isValid():
        raise ConnectionError(
            'Unable to reach %s' %
            url.cStr(), hd.getStatusCode())
    stream = hd.openReadFile(1)
    sr = StreamReader(stream, 1)
    response = sr.readlines()
    for i in xrange(len(response)):
        if response[i][-1] == '\n':
            response[i] = response[i][:-1]

    return response
# okay decompiling .\otp\login\HTTPUtil.pyc
