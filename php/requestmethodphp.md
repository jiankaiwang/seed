# REQUESTMETHOD.php



* The class implements receiving requests from clients and also sending the passed json data back to the clients in dictionary format.

### Collaboration
---

* Refer to Python REQUESTMETHOD.py (class REQUESTMETHOD)

### Constructor
---

* Parameters
  1. $getServer : passing global **$_SERVER**

```php
#
# desc : constructor
#
public function __construct($getServer)
```

### API
---

* Handling GET/POST/PUT/DELETE requests automatically at beginning constructor, and all methods are private functions

```php
public function __construct($getServer) {

  # ...
  
  $this -> method = $getServer['REQUEST_METHOD'];
  
  # ...
  
  # beginning passing request
  switch($this -> method) {
      default:
      case "GET":
          $this -> GET();
          break;
      case "POST":
          $this -> POST();
          break;
      case "PUT":
      case "DELETE":
          $this -> PUTOrDelete();
          break;
  }
}
```


* Sending GET/POST/PUT/DELETE responses to client

```python
#
# desc : get response in json
#
public function response($format)
```

### Example
---

* Construct a object and also wait requests to response client with the json data

```php
$obj = new REQUESTMETHOD($_SERVER);
echo $obj->response("json");
```

