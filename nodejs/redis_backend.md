# redis_backend.js



### Dependencies
---

* querystring : ^0.2.0
* redis : "^2.7.1"
* request : "^2.81.0" 
* url : "^0.11.0"
* seed/javascript/Common.js : [https://github.com/jiankaiwang/seed/blob/master/javascript/Common.js](https://github.com/jiankaiwang/seed/blob/master/javascript/Common.js)

### API
---

```javascript
// set the redis configuration
setRedisConf({ "host" : "127.0.0.1", "port" : "6379", "pwd" : "exampleRedisPWD" });

// operation 1-1 : set key-value pair
setRedisPair("key-1", "val-1", function(data) { console.log(data); });

// operation 1-2 : get value by key
getRedisPair("key-1", function(data) { console.log(data); });

// operation 1-3 : delete value by key
delRedisPair("key-1", function(data) { console.log(data); });

// operation 2 : auto process API
// GET example : 
// |- https://api.com/?s=service1&v=api1
// |- https://api.com/?s=service1&v=api2
// |- https://api.com/?s=service2&v=api1
autoProcessAPI(
  {
    "apiUrl" : "https://api.com/", 
    "apiService" : {
      "service1" : ["api1", "api2"],
      "service2" : ["api1"]
    } 
  }
);
```