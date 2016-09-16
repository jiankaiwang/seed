#
# author : jiankaiwang (https://welcome-jiankaiwang.rhcloud.com/)
# project : seed (https://github.com/jiankaiwang/seed)
# reference : seed (https://www.gitbook.com/book/jiankaiwang/seed/details)
#

# coding: utf-8

import urllib
import urllib2
import json

#
# desc : request as GET/POST/PUT/DELETE
# retn : the json data passed to the server and returned as json data
#

class SENDREQUEST:

    # -------------------------------
    # private
    # __state : 0 (success) or 1 (failure)
    # -------------------------------
    __url = ""
    __addHeader = ""
    __jsonData = ""
    __response = ""
    __method = ""
    __state = ""

    #
    # desc : add request header
    #
    def __addHeaderBody(self, getRequest):
        retReq = getRequest
        if len(self.__addHeader.keys()) > 0:
            for key, value in self.__addHeader.iteritems():
                retReq.add_header(key, value)
        return retReq

    #
    # desc : GET method
    #
    def __get(self):
        try:
            # prepare get url
            ttlUrl = self.__url

            if len(self.__jsonData) > 0:
                ttlUrl = self.__url + '?'
                allPairs = []
                for key, value in self.__jsonData.iteritems():
                    allPairs.append(str(key) + '=' + str(value))
                ttlUrl = ttlUrl + '&'.join(allPairs)

            # begin get request
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(ttlUrl)
            request.get_method = lambda:"GET"
            # add header
            request = self.__addHeaderBody(request)
            urlReq = opener.open(request)
            self.__response = urlReq.read()
            self.__state = 0
        except urllib2.HTTPError as e:
            self.__response = e
            self.__state = 1
        except:
            self.__response = "uncatchable"
            self.__state = 1
        return

    #
    # desc : POST method
    #
    def __post(self):
        try:
            # begin post request
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            # notice before posting, data must be urlencoded
            request = urllib2.Request(self.__url, urllib.urlencode(self.__jsonData))
            request.get_method = lambda:"POST"
            # add header
            request = self.__addHeaderBody(request)
            urlReq = opener.open(request)
            self.__response = urlReq.read()
            self.__state = 0
        except urllib2.HTTPError as e:
            self.__response = e
            self.__state = 1
        except:
            self.__response = "uncatchable"
            self.__state = 1
        return

    #
    # desc : PUT or Delete method
    # param@jsonUrlecnoding : url encoding or not
    # param@methodPUT : request as PUT or DELETE method
    #
    def __PutOrDelete(self, jsonUrlecnoding=True, methodPUT=True):
        try:
            # begin put request
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            if jsonUrlecnoding:
                # json as encoding
                request = urllib2.Request(self.__url, urllib.urlencode(self.__jsonData))                
            else:
                # json as string 
                request = urllib2.Request(self.__url, data=json.dumps(self.__jsonData))
            if methodPUT:
                # request as PUT
                request.get_method = lambda:"PUT"
            else:
                # request as DELETE
                request.get_method = lambda:"DELETE"
            # add header
            request = self.__addHeaderBody(request)
            urlReq = opener.open(request)
            self.__response = urlReq.read()
            self.__state = 0
        except urllib2.HTTPError as e:
            self.__response = e
            self.__state = 1
        except:
            self.__response = "uncatchable"
            self.__state = 1
        return
    
    # -------------------------------
    # public
    # -------------------------------

    #
    # desc : constructor
    # param@getURL : e.g. 192.168.2.5/test/index.php
    # param@getHeaderSetting : e.g. { "Authorization" : "abcdefg-hijk-lmnop-qrstuv-wxyz" }
    # param@getData : e.g. { "method" : "post" }
    # param@getMtd : one of ["GET", "POST", "PUT", "DELETE"]
    #
    def __init__(self, getURL, getHeaderSetting, getData, getMtd="GET"):
        self.__url = getURL
        self.__addHeader = getHeaderSetting
        self.__jsonData = getData
        self.__response = ""
        self.__method = getMtd.lower()

        if self.__method == "get":
            self.__get()
        elif self.__method == "post":
            self.__post()
        elif self.__method == "put":
            self.__PutOrDelete(True, True)
        elif self.__method == "delete":
            self.__PutOrDelete(True, False)

    #
    # desc : show response
    #
    def response(self):
        return { "state" : self.__state, "response" : self.__response }

# get example
# ret : {
#   u'header': {
#       u'Host': u'192.168.2.5',
#       u'Connection': u'close',
#       u'Accept-Encoding': u'identity',
#       u'User-Agent': u'Python-urllib/2.7'
#   },
#   u'host': u'192.168.2.5',
#   u'response': {u'method': u'get'},
#   u'uri': u'/test/index.php?method=get',
#   u'method': u'GET'
# }
#
a = SENDREQUEST("http://192.168.2.5/test/index.php", {}, {"method" : "get"}, "GET")
a.response()["response"]
print json.loads(a.response()["response"])

# post example
# ret : {
#   u'header': {
#       u'Content-Length': u'11',
#       u'Accept-Encoding': u'identity',
#       u'Connection': u'close',
#       u'User-Agent': u'Python-urllib/2.7',
#       u'Host': u'192.168.2.5', u'Content-Type':
#       u'application/x-www-form-urlencoded',
#       u'Authorization': u'api-key'
#   },
#   u'host': u'192.168.2.5',
#   u'response': {u'method': u'post'},
#   u'uri': u'/test/index.php',
#   u'method': u'POST'
# }
#
a = SENDREQUEST("http://192.168.2.5/test/index.php", {"Authorization" : "api-key"}, {"method" : "post"},"POST")
a.response()["response"]
print json.loads(a.response()["response"])

# put example
# ret : {
#   u'header': {
#       u'Content-Length': u'10',
#       u'Accept-Encoding': u'identity',
#       u'Connection': u'close',
#       u'User-Agent': u'Python-urllib/2.7',
#       u'Host': u'192.168.2.5',
#       u'Content-Type': u'application/x-www-form-urlencoded',
#       u'Authorization': u'api-key'
#   },
#   u'host': u'192.168.2.5',
#   u'response': u'method=put',
#   u'uri': u'/test/index.php',
#   u'method': u'PUT'
# }
#
a = SENDREQUEST("http://192.168.2.5/test/index.php", {"Authorization" : "api-key"}, {"method" : "put"},"PUT")
a.response()["response"]
print json.loads(a.response()["response"])

# delete example
# ret : {
#     u'header': {
#         u'Content-Length': u'13',
#         u'Accept-Encoding': u'identity',
#         u'Host': u'192.168.2.5',
#         u'User-Agent': u'Python-urllib/2.7',
#         u'Connection': u'close',
#         u'Content-Type': u'application/x-www-form-urlencoded'
#     },
#     u'host': u'192.168.2.5',
#     u'response':
#     u'method=delete',
#     u'uri': u'/test/index.php',
#     u'method': u'DELETE'
# }
# 
a = SENDREQUEST("http://192.168.2.5/test/index.php", {}, {"method" : "delete"},"DELETE")
a.response()["response"]
print json.loads(a.response()["response"])






