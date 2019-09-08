# common.h



### Required libraries
---

```cpp
#include <string>
#include <vector>
```

### API Description
---

* strsplit

```cpp
/*
* namespace : std
* description : string is split by delimit words
* parameter :
* |- getStr@String : "string prepared for being split"
* |- delimit@String : "split char in the string"
* return : vector<string>
* example : 
* vector<string> getVect = strsplit("string name, name2(string), name3(c-string);","(;");
*/
vector<string> strsplit(string getStr, string delimit);
```