# Google Sheets API by api key (googlesheetsapikey.cs)



### Dependency
---

* Google Sheets API v4

### Constructor
---

```csharp
/*
* desc : constructor
* inpt : 
* |- getSheetId/getrange/getApiKey : refer to
* |- https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
* |- getRetDataFormat : {0 | 1 | 99}
* |- 0 : [ [column name], [data.1], [data.2], [data.3], ... ]
* |- 1 : [ { colname.1 : data-1.column.1, colname.2 : data-1.column.2 }, { colname.1 : data-2.column.1 }, ... ]
* |- 99 : original google api response
*/
public googlesheetsapikey(string getSheetId, string getRange, string getApiKey, int getRetDataFormat)
```

### API
---

```csharp
/*
* desc : fetch data from google sheets
*/
public HttpResponseMessage fetchData()
```

### Example
---

* Used in ASPX.NET / C# and pass data by the json format

```chsrap
public HttpResponseMessage exampleResponse() {
    string sheetid = "example-id";
    string range = "A:L";
    string apikey = "exmaple-key";
    int retFormat = 0;
    
    var gsbyapikey = new googlesheetsapikey(sheetid, range, apikey, retFormat);
    return gsbyapikey.fetchData();
}
```


