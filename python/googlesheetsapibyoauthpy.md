# Access to Google Sheets Api By OAuth (GoogleSheetsApiByOAuth.py)



### Dependency
---

* google sheets api v4
* OAuth 2.0 Client ID

### Constructor
---

```python
#
# desc : constructor
# inpt : 
# |- scope : https://developers.google.com/sheets/api/guides/authorizing
# |- client secret file : absoulted path downloaded from google api console
# |- app name : self-defined    
#

def __init__(self, getScope, getClientSecretFile, getAppName)
```

### API 
---

* Fetch Data

```python
#
# desc : fetch data from google sheets api v4
# inpt : 
# |- getSheetId : https://docs.google.com/spreadsheets/d/{sheet is}/edit#gid=0
# |- getRange : query range, e.g. A:L, A2:L100, ... etc.
# |- retType : 
#   |- 0: returned data as dictionary format in json, 
#       e.g. [ {col1 : data1-col1, col2 : data1-col2}, ... ]
#   |- 1: returned data as list format in json, 
#       e.g. [ [col1, col2, col3, ...], [data1-col1, col2-data1], ... ]
#   |- 99: the original response from google
#
def fetchData(self, getSheetId, getRange, retType=0)
```

* Append a new row

```python
#
# desc : writing data into the sheet
# inpt :
# |- getSheetId : https://docs.google.com/spreadsheets/d/{sheet is}/edit#gid=0
# |- getData : input values, 
#   e.g. [["d2-1", "d2-2", "d2-3", "d2-4","d2-5"], [ another raw values ... ]]
# |- getValueInputOptions : the type of values 
#   {u'INPUT_VALUE_OPTION_UNSPECIFIED' | u'RAW' | u'USER_ENTERED'}
# |- getRange : the range for data to appned
#   e.g. A:E
#                
def appendData(self, getSheetId, getData, getValueInputOptions, getRange)
```

### Example
---

* Fetch Data by auth "spreadsheets.readonly"

```python
#
# example.1 : spreadsheets.readonly
# note : the credential must be regenerated
#   |- linux : default /home/(user)/.credentials/sheets.googleapis.com-python-quickstart.json
#   |- windows : default C:\Users\(user)\.credentials\sheets.googleapis.com-python-quickstart.json
#
fetchDataObj = GoogleSheetsApiByOAuth(\
               "spreadsheets.readonly",\
               "D:\\example\\client_secret.json",\
               "example.1"\
               )
getStatus = fetchDataObj.fetchData("sheetid", "A:E", 0)
```

* Append Data by auth "spreadsheets"

```python
#
# example.2 : spreadsheets (append a new entity as a new raw)
# note : the credential must be regenerated
#
addDataObj = GoogleSheetsApiByOAuth(\
             "spreadsheets",\
             "D:\\example\\client_secret.json",\
             "example.2"\
             )

getAppendStatus = addDataObj.appendData(\
                  "sheetid", \
                  [["d2-1", "d2-2", "d2-3", "d2-4","d2-5"]], \
                  'RAW', \
                  "A:E" \
                  )

```