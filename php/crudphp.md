# CRUD.php



### Constructor
---

```php
#
# desc : constructor
# inpt : 
# |- sendUrl : server url, e.g. http://test.php
# |- getMethod : request type, e.g. { GET|POST|PUT|DELETE }
# |- getHeader : header info, e.g. array("auth" => "authVal")
# |- getData : data content, e.g. array("opt" => "val")
#
public function __construct($sendUrl, $getMethod, $getHeader, $getData)
```

### API and Examples
---

* GET Request

```php
# eg.1 GET method
$getObj = new CRUD(
    "http://localhost/REQUESTMETHOD.php", 
    "GET", 
    array("auth" => "keyVal"), 
    array("opt" => 1, "val" => 1)
);
echo $getObj->response("json");
```

* GET Request

```php
# eg.2 POST method
$postObj = new CRUD(
    "http://localhost/REQUESTMETHOD.php", 
    "POST", 
    array("auth" => "keyVal"), 
    array("opt" => 1, "val" => 2)
);
echo $postObj->response("json");
```

* PUT Request

```php
# eg.3 PUT method
$putObj = new CRUD(
    "http://localhost/REQUESTMETHOD.php", 
    "PUT", 
    array("auth" => "keyVal"), 
    array("opt" => 1, "val" => 3)
);
echo $putObj->response("json");
```

* DELETE Request

```php
# eg.4 DELETE method
$delObj = new CRUD(
    "http://localhost/REQUESTMETHOD.php", 
    "DELETE", 
    array("auth" => "keyVal"), 
    array("opt" => 1, "val" => 4)
);
echo $delObj->response("json");
?>
```

