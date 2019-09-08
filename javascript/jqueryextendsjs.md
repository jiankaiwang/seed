# JqueryExtends.js



### API and Example
---

* Parse URL into array by default operator '?'

```javascript
/* inpt
* |- token : the parameter
* retn : string
* e.g. : http://localhost/?token=example
*/
$.getUrlVar(token)  // return "example"
```

* Show network type

```javascript
/* inpt
* |- operator : e.g. '?' or '#'
* |- token : the parameter
* retn : string
* e.g. : http://localhost/#token=example
*/
$.getUrlVarsByChar(operator,token);  // return "example"
```


