# REQUESTMETHOD2.py



### Collaboration
---

* Refer to PHP REQUESTMETHOD.php (class REQUESTMETHOD)

### Dependency
---

* urllib2
* requests

### Constructor
---

* Parameters
  1. getURL (string) : e.g. 192.168.2.5/test/index.php
  2. getHeaderSetting (dict) : e.g. { "Authorization" : "abcdefg-hijk-lmnop-qrstuv-wxyz" }
  3. getData (dict) : e.g. { "method" : "post" }
  4. getMtd (string) : one of ["GET", "POST", "PUT", "DELETE"]

```python
#
# desc : constructor
#
def __init__(self, getURL, getHeaderSetting, getData, getMtd="GET")
```

### API
---

* Send GET request by constructor

```python
def __init__(self, getURL, getHeaderSetting, getData, getMtd="GET")
```

* Send POST request by constructor

```python
def __init__(self, getURL, getHeaderSetting, getData, getMtd="POST")
```

* Send PUT request by constructor

```python
def __init__(self, getURL, getHeaderSetting, getData, getMtd="PUT")
```

* Send DELETE request by constructor

```python
def __init__(self, getURL, getHeaderSetting, getData, getMtd="DELETE")
```

* Receive GET/POST/PUT/DELETE responses from Server

```python
def response()
```

### Example
---

* GET Example

```python
# get example
# ret : 
# {\
#    'state': 0, \
#    'response': \
#        u'{\
#        "host":"192.168.2.5", \
#        "uri":"\\/test\\/REQUESTMETHOD.php?1=2&%E4%B8%AD%E6%96%87=%E6%96%B0%E5%A2%9E&method=getData",\
#        "method":"GET",
#        "header":{\
#            "Host":"192.168.2.5",\
#            "Connection":"keep-alive",\
#            "Accept-Encoding":"gzip, deflate",\
#            "Accept":"*\\/*",\
#            "User-Agent":"python-requests\\/2.8.0"},\
#            "response":{"1":"2","\\u4e2d\\u6587":"\\u65b0\\u589e","method":"getData"}
#        }'\
# }
#
a = SENDREQUEST(\
    "http://192.168.2.5/test/REQUESTMETHOD.php", \
    {}, \
    {"method" : "getData", '\xE4\xB8\xAD\xE6\x96\x87' : '\xE6\x96\xB0\xE5\xA2\x9E', 1 : 2}, 
    "GET"\
    )
print a.response()
```

* POST Example

```python
# post example
# ret :
# {
#    'state': 0, \
#    'response': \
#        u'{"\
#            host":"192.168.2.5",\
#            uri":"\\/test\\/REQUESTMETHOD.php",\
#            "method":"POST",\
#            "header":{\
#                "Host":"192.168.2.5",\
#                "Content-Length":"53",\
#                "Accept-Encoding":"gzip, deflate",\
#                "Accept":"*\\/*",\
#                "User-Agent":"python-requests\\/2.8.0",\
#                "Connection":"keep-alive",\
#                "Content-Type":"application\\/x-www-form-urlencoded",\
#                "Authorization":"api-key"},\
#            "response":{"\\u4e2d\\u6587":"\\u65b0\\u589e","method":"postData"}
#        }'
# }
#
b = SENDREQUEST(\
    "http://192.168.2.5/test/REQUESTMETHOD.php", \
    {u'Authorization': u'api-key'}, \
    {"method" : "postData", '\xE4\xB8\xAD\xE6\x96\x87' : '\xE6\x96\xB0\xE5\xA2\x9E'}, \
    "POST"\
    )
print b.response()
```

* PUT Example

```python
# put example
# ret : 
# {\
#    'state': 0, \
#    'response': \
#        u'{\
#            "host":"192.168.2.5",\
#            "uri":"\\/test\\/REQUESTMETHOD.php",\
#            "method":"PUT",\
#            "header":{\
#                "Host":"192.168.2.5",\
#                "Content-Length":"10",\
#                "Accept-Encoding":"gzip, deflate",\
#                "Accept":"*\\/*",\
#                "User-Agent":"python-requests\\/2.8.0",\
#                "Connection":"keep-alive",\
#                "Content-Type":"application\\/x-www-form-urlencoded",\
#                "Authorization":"api-key"},
#            "response":"method=put"
#        }'
# }
#
c = SENDREQUEST(\
    "http://192.168.2.5/test/REQUESTMETHOD.php", \
    {"Authorization" : "api-key"}, \
    {"method" : "put"}, \
    "PUT"\
    )
print c.response()
```

* DELETE Example

```python
# delete example
# ret :
# {\
#    'state': 0, \
#    'response': \
#        u'{\
#            "host":"192.168.2.5",\
#            "uri":"\\/test\\/REQUESTMETHOD.php",\
#            "method":"DELETE",\
#            "header":{
#                "Host":"192.168.2.5",\
#                "Content-Length":"13",\
#                "Accept-Encoding":"gzip, deflate",\
#                "Accept":"*\\/*",\
#                "User-Agent":"python-requests\\/2.8.0",\
#                "Connection":"keep-alive",\
#                "Content-Type":"application\\/x-www-form-urlencoded"},
#            "response":"method=delete"
#        }'
# }
# 
d = SENDREQUEST(\
    "http://192.168.2.5/test/REQUESTMETHOD.php", \
    {}, \
    {"method" : "delete"}, \
    "DELETE"\
    )
print d.response()
```