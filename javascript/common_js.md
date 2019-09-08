# Common.js



### API
---

* get the length of passed dictionary (取得傳入字典物件的長度)

```javascript
var getDictionaryLength(var getDictObj)
```

* get the key list of passed dictionary (取得傳入字典的所有鍵，並以串列回傳)

```javascript
List getDictionaryKeyList(var getDictObj)
```

* get the value list of passed dictionary (取得傳入字典的所有値，並以串列回傳)

```javascript
List getDictionaryValueList(var getDictObj)
```

* sort keys in dictionary by their values (將傳入字典物件依照値進行排序，並以串列回傳排序後的鍵)

```javascript
/*
 * desc : sort keys in dictionary by their values
 * para : 
 *	1. getDictObj : { key : value }
 *	2. sortType : "bubble"(default)
 * 	3. getOrder : desc, asc(default)
 *	4. getListCount : 0-N
 * example :
 * 	var aa = { 'a' : 10, 'b' : 3, "c" : 5 }
 *  var keyList = getKeyBySortOnValue(aa, "bubble", "desc", getDictionaryLength(aa));
*/
List getKeyBySortOnValue = function(getDictObj, sortType, getOrder, getListCount)
```
