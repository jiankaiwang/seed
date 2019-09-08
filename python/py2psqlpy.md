# py2psql.py



### Dependency
---

* psycopg2 (PostgreSQL + Python)

### Constructor
---

* constructed parameter:
  1. host : URL or IP
  2. port : postgresql server port
  3. db : database name as a string
  4. tb : table name as a string
  5. user : login user as a string
  6. pwd : the password as a string

```python
#
# desc : constructor
# param@getTB : can be null when only using execsql()
#
def __init__(self, getHost, getPort, getDB, getTB, getUser, getPwd):
```

### API
---

* SELECT operation
  1. param@getConds : {}, defined where SQL conditions
  2. param@getParams : [], selected column names, empty : means all
  3. param@asdict : boolean, returned row as dictionary
  4. data as [] type
  5. also support status object, use status()

```python
def select(self, getConds, getParams, asdict=False):
```

* UPDATE operation
  1. param@getParams : {}, set sql parameters  
  2. param@getConds : {}, where sql conditions
  3. retn : 0 : failure, 1 : success
  4. note : also support status object, use status()

```python
def update(self, getParams, getConds)
```

* INSERT operation
  1. param@getParams : {}, value sql parameters    
  2. retn : 0 : failure, 1 : success
  3. note : also support status object, use status()

```python
def insert(self, getParams)
```

* DELETE operation
  1. param@getConds : {}, where sql conditions
  2. retn : 0 : failure, 1 : success
  3. note : also support status object, use status()

```python
def delete(self, getConds)
```

* Custom SQL operation
  1. param@getSQL : parameter-based complex sql command，
     e.g. "select * from public.user where name = %(name)s;"
  2. param@hasRetValue : are there returned values ?
  3. param@getParams : {}
     e.g. {'name' : "test114"}
  4. param@asdict : only works when param@hasRetValue is true, returned value as dictionary data type
  5. retn : return executing status

```python
def execsql(self, getSQL, hasRetValue, getParams, asdict=True)
```

* Get Table schema
  1. param@getTable : get desired table schema
  2. retn : status object
  3. note : when param@getTable == None, **self.__tb** must exist at the beginning of object creation

```python
def getTableSchema(self, getTable=None)
```

* Get the latest operation execution status

```python
def status()
```

* Create table : create table based on schema
  1. param@tableName : name of the table for creation
  2. param@tableSchema : { 'colName' : 'colSchema', '' : '' }
  3. param@dropFirst : whether to drop table first if it exists
  4. retn : None, call status() to get status object

```python
def createTable(self, tableName, tableSchema, dropFirst=False)
```

* Alter table : alter table schema
  1. param@tableName : table for altering
  2. param@tableSchema : { 'colName' : 'new col schema' }
  3. param@createTableFirstIfNotExisted : whether to create table first if table does not exist
  4. param@addColIfNotExisted : whether to add column if it does not exist
  5. param@theSameWithThisSchema : whether to fit the table with the input schema
  6. retn : None, call status() to get status object
  7. note : if addColIfNotExisted == False, the column for altering would be skipped 

```python
def alterTable(self, \
  tableName, \
  tableSchema, \
  createTableFirstIfNotExisted=True, \
  addColIfNotExisted=True,\
  theSameWithThisSchema=True)
```

* Drop table
  1. param@tableName : table for droping
  2. retn : None, call status() to get status object

```python
def dropTable(self, tableName)
```

### Example
---

```python
# link to postgresql database
p2l = py2psql("127.0.0.1","5432","ckan_default","public.user","ckan_default","ckan")

# returned status : call status()
# { "state" : [success|failure|warning], "info" : "message", "data" : []}

# example.1 get table schema
# 1.1
p2l = py2psql("127.0.0.1","5432","ckan_default","public.user","ckan_default","ckan")
p2l.getTableSchema()  # default table, only fetches column name(desc[0])
# 1.2
p2l2 = py2psql("127.0.0.1","5432","ckan_default","","ckan_default","ckan")
p2l2.getTableSchema("public.user",0)  # desired table
p2l2.getTableSchema("public.user",-1)  # fetch all description
p2l.status()

# example.2 query data
# 2.1 select column name, email, 123 (not existing)
data = p2l.select({where},[columns])
data = p2l.select({"name":"test114"},["name","email","123"])
data = p2l.select({"name":"test114"},[])
# 2.2 select column name, email, 123 (not existing) and also returned as dictionary
data = p2l.select({where},[columns],asdict=True)
data = p2l.select({"name":"test114"},["name","email","123"],asdict=True)
data = p2l.select({"name":"test114"},[],asdict=True)

# example.3 update data
# 3.1
p2l.update({set},{where})
p2l.update({"email":"test@tw"},{"name":"test114"})

# example.4 insert data
# 4.1
p2l.insert({ data })
p2l.insert({ "id" : "acbdhcbdh-abchdbch", "name":"123","email":"123@tw" })

# example.5 delete data
# 5.1
p2l.delete({where})
p2l.delete({"name":"test1", "email":"test1@tw"})

# example.6 execsql data
# 6.1 only one function can create object without assigning table
p2l.execsql("sql command", is there returned value, {parameter : value})
p2l.execsql("select * from public.user where name = %(name)s;", True, {'name' : "test114"}, True)
p2l.status()
# 6.2 get table list
p2l.execsql("select * from information_schema.tables where table_name = %(name)s;", True, {'name' : "user"})
p2l.status()

# example.7 create data table
# 7.1 drop first
p2l.createTable("test", {"id" : "serial primary key", "context" : "text not null"}, dropFirst=True)
p2l.status()

# example.8 alter data table
# 8.1 
p2l.alterTable("test", {"context" : "text"}, createTableFirstIfNotExisted=False, addColIfNotExisted=False, theSameWithThisSchema=True)
p2l.status()

# example.9 drop data table
# 9.1
p2l.dropTable("test")
p2l.status()
```




