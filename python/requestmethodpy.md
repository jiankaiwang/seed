# REQUESTMETHOD.py



### Collaboration
---

* Refer to PHP REQUESTMETHOD.php (class REQUESTMETHOD)

### Dependency
---

* urllib
* urllib2
* json

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
```

* POST Example

```python
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
```

* PUT Example

```python
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
```

* DELETE Example

```python
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
```

