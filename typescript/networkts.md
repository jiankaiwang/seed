# network.ts



### Constructor
---

```typescript
/*
* desc : constructor
* inpt : 
* |- getIPv4Addr : e.g. 192.168.99.100
* |- getMask : e.g. 255.255.255.0
* |- getSubsetEnabled : whether to allow subnets (all-0 and all-1)
*/
public constructor(getIPv4Addr, getMask, getSubsetEnabled)
```

### API
---

* Show total number of available IPv4 addresses

```typescript
// inpt : [None]
// retn : integer (>=1)
public showAvailIPv4Addr()
```

* Show network type

```typescript
// inpt : [None]
// retn : {string | "Class A", ... , "Class E", "Undefined Class"}
public showNetworkType()
```

* Show wild card

```typescript
// inpt : {showType | string, ""}
// retn
// |- string, e.g. 0.0.0.255
// |- number[], e.g. [0, 0, 0, 255]
public showWildcard(showType) : string | number[]
```

* Show the available IPv4 address list

```typescript
// inpt : None
// retn : a dictionary, 
// |- e.g. {0: Object, 1: Object, 2: Object, 3: {start : 0, end : 255}}
public showIPv4AvailList()
```

* Show all available IPv4 addresses

```typescript
// inpt : None
// retn : a dictionary, 
// |- e.g. {status: 0, info: "Show all available IPv4 addresses.", data: Array[254]}
public showAllIPAddress()
```

### Examples
----

```typescript
var net = new RangeOfIPv4Addr("192.168.99.100","255.255.255.0",true);

// 254
net.showAvailIPv4Addr();

// "Class C"
net.showNetworkType();

// "0.0.0.255"
net.showWildcard("decstr");

// [0, 0, 0, 255]
net.showWildcard("");

// Object {0: Object, 1: Object, 2: Object, 3: {start : 0, end : 255}}
net.showIPv4AvailList();  

// Object {status: 0, info: "Show all available IPv4 addresses.", data: Array[254]}
net.showAllIPAddress();  
```



