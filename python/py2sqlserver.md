# py2sqlserver.py



### Dependency
---

* pyodbc (based on SQL Server Driver)

### Constructor
---

```python
server = 'localhost'
port = 1433
database = 'Example'
username = 'ExampleUser'
password = 'exampleuser'

py2sqlserver = py2SQLServer(server, port, username, password, database)
```

### API
---

* validate whether the connection is existing

```python
# params : None
# return
# |- state : success or failure
# |- info : connection message
# |- data : ""
def validateConnection()
```

* Query by SQL Command

```python
# params : the parameter-based sql command
# |- sqlCmd (string) : e.g. SELECT * from dbo.example;
# |- SqlParas (tuple) : e.g. ()
def queryBySQLcmd(sqlCmd, SqlParas)
```

* Get Column Names From the SQL Query

```python
# params : the parameter-based sql command
# |- sqlCmd (string) : e.g. SELECT * from dbo.example;
# |- SqlParas (tuple) : e.g. ()
def getColumnNames(self, sqlCmd, SqlParas)
```

* Non-Query by SQL Command : Insert, Update, Delete

```python
# params : the parameter-based sql command
# |- sqlCmd (string) : e.g. insert into dbo.example("attr1", "attr2", "attr3") values(?, ?, ?);
# |- SqlParas (tuple) : e.g. ('data3', 789, '2017-09-15 11:24:00')
def nonQueryBySQLCmd(sqlCmd, SqlParas)
```

### Example
---

```python
server = 'localhost'
port = 1433
database = 'Example'
username = 'ExampleUser'
password = 'exampleuser'

py2sqlserver = py2SQLServer(server, port, username, password, database)
if py2sqlserver.validateConnection()['state'] == "success":
    print(py2sqlserver.nonQueryBySQLCmd(\
        'insert into dbo.example("attr1", "attr2", "attr3") values(?, ?, ?);', \
        ('data3', 789, '2017-09-15 11:24:00')\
    ))
    print(py2sqlserver.nonQueryBySQLCmd(\
        'delete from dbo.example where attr2 = ?;', \
        (234,)\
    ))
    print(py2sqlserver.nonQueryBySQLCmd(\
        'update dbo.example set attr2 = ? where attr1 = ?;', \
        (100, "data1")\
    ))
    print(py2sqlserver.nonQueryBySQLCmd(\
        'delete from dbo.example where attr1 = ?;', \
        ("data1",)\
    ))
    print(py2sqlserver.queryBySQLcmd("SELECT * from dbo.example;", ()))
    print(py2sqlserver.getColumnNames("SELECT * from dbo.example;", ()))
```








