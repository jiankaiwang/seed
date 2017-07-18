/*
 * desc : example to process data from the api and save into redis server 
 * author : jiankaiwang
 * project : seed
 * env :
 * |- redis : version 3.2.9
 * |- nodejs : version 6.9.1
 * pkg :
 * |- "querystring": "^0.2.0" 
 * |- "redis": "^2.7.1"
 * |- "request": "^2.81.0" 
 * |- "url": "^0.11.0"
 * |- "seed/javascript/Common.js" : "https://github.com/jiankaiwang/seed/blob/master/javascript/Common.js"
 *   |- * note : remember to exports function, e.g. exports.getDictionaryKeyList = getDictionaryKeyList
 * e.g. :
 
// set the redis configuration
setRedisConf({ "host" : "127.0.0.1", "port" : "6379", "pwd" : "exampleRedisPWD" });

// operation 1-1 : set key-value pair
setRedisPair("key-1","val-1");

// operation 1-2 : get value by key
getRedisPair("key-1", function(data) { console.log("callBack function to get value " + data); });

// operation 1-3 : delete value by key
delRedisPair("key-1");

// operation 2 : auto process API
autoProcessAPI(
  {
	  "apiUrl" : "https://api.com/", 
		"apiService" : {
			"service1" : ["api1", "api2"],
			"service2" : ["api1"]
		}
  }
);

 * ref : 
 * |- https://github.com/NodeRedis/node_redis
 */

var redisHost = '',
    redisPort = 0,
    redisPWD = '',
    apiUrl = "",
    apiService = {};

var redis = require("redis"),
    url = require("url"),
    querystring = require('querystring'),
    request = require('request'),
    common = require('./public/seed/Common.js');

/*
 * desc : response the result 
 */
function responseResult(state, info, data) {
	return(JSON.stringify({ "state" : state, "info" : info, "data" : data }));
}

/*
 * desc : connect to the redis and set the key-value pair 
 */
function setRedisPair(key, value) {
	var client = redis.createClient({ host: redisHost, port: redisPort, password: redisPWD });
	
	// connection error
	client.on("error", function(error) {
	    console.log('info', responseResult("failure","Connecting to the Redis went error.",error));
	});

	// save into the Redis
	client.on('connect', function() {
	    client.set(key, value);
        // close the connection
    	client.quit();
	});
}

/*
 * desc : connect to the redis and get the value by key 
 */
function getRedisPair(key, callBackFunc) {
	var client = redis.createClient({ host: redisHost, port: redisPort, password: redisPWD });
	
	// connection error
	client.on("error", function(error) {
	    console.log('info', responseResult("failure","Connecting to the Redis went error.",error));
	    callBackFunc("error: Connecting to the Redis went error.");
	});

	// save into the Redis
	client.on('connect', function() {
	    client.get(key, function(err, reply) {
	    	if(!err) {
	    		callBackFunc(reply);
	    	} else {
	    		callBackFunc("error: operation get on the redis");
	    	}
	    })
        // close the connection
    	client.quit();
	});
}

/*
 * desc : connect to the redis and delete the value by key 
 */
function delRedisPair(key) {
	var client = redis.createClient({ host: redisHost, port: redisPort, password: redisPWD });
	
	// connection error
	client.on("error", function(error) {
	    console.log('info', responseResult("failure","Connecting to the Redis went error.",error));
	});

	// save into the Redis
	client.on('connect', function() {
	    client.del(key, function(err, reply) {
	    	if(err) { console.log("error: operation delete on the redis"); }
	    })
        // close the connection
    	client.quit();
	});
}

/*
 * desc : access the api and save into the redis
 * oper : set (save)
 */
function __request(apiURI, allQueries) {
  request(
	apiURI + "?s=" + allQueries["s"] + "&v=" + allQueries["v"]
  , function (error, response, body) {
    if (!error) {
    	setRedisPair(allQueries["s"] + allQueries["v"], body);
    } else {
        console.log('info', responseResult("failure","Access the API went error.",""));
    }
  });
}

/*
 * desc : set redis server conf 
 */
function setRedisConf(redis) {
	redisHost = redis["host"];
    redisPort = redis["port"];
    redisPWD = redis["pwd"];	
}

/*
 * desc : query the api and save the data
 * inpt :
 * |- redis : {"host" : "127.0.0.1", "port" : "6379", "pwd" : "exampleRedisPWD" }
 * |- api : {"apiUrl" : "url", "apiService" : { "service1" : ["api1", "api2"], "service2" : ["api1"] }}
 */
function autoProcessAPI(api) {
    apiUrl = api["apiUrl"];
    apiService = api["apiService"];
	
	var allServices = common.getDictionaryKeyList(apiService);
	var eachAPI = [];
	for(var i = 0 ; i < allServices.length ; i++) {
		eachAPI = apiService[allServices[i]];
		for(var j = 0 ; j < eachAPI.length ; j++) {
			__request(apiUrl, {"s" : allServices[i], "v" : eachAPI[j]});
		}
	}   
}

/*
 * desc : entry 
 */

//exports functions
exports.setRedisConf = setRedisConf;
exports.setRedisPair = setRedisPair;
exports.getRedisPair = getRedisPair;
exports.delRedisPair = delRedisPair;
exports.autoProcessAPI = autoProcessAPI;
