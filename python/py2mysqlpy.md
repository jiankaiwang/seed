# py2mysql.py



### Dependency
---

* mysql.connector [PyPi](https://pypi.python.org/pypi/mysql-connector)

### Constructor
---

```python
# 
# desc : constructor
# inpt :
# |- host : host IP or URI
# |- port : mysql port
# |- user : service user
# |- pwd : login password
# |- dbname : default database name
#

def __init__(self, host, port, user, pwd, dbname):
```

### API
---

```python
#
# desc : get conection status
# inpt : none
# retn : { "state" : [success|failure|warning], "info" : "message", "data" : []}
#
def checkConnectionValid()

#
# desc : execute sql command
# inpt :
# |- sqlCmd : "SELECT first_name, hire_date FROM employees WHERE hire_date BETWEEN %s AND %s"
# |- parameterInSeq (tuple) : (datetime.date(1999, 1, 1), datetime.date(1999, 12, 31))
# |- isQueryFlag : {True|False}
# |- asdict (return as dictionary) : {True|False}
#
def execsql(sqlCmd, parameterInSeq, isQueryFlag, asdict=True)
```

### Example
---

```python
# desc : connect to the mysql server
py2my = py2mysql("127.0.0.1", "3306", "user", "password", "database_name")        
print py2my.checkConnectionValid()  

# desc : query data
queryData = py2my.execsql("select * from table where year = %s limit 10;", (2000,), True, True)
dictRes(queryData)

# desc : insert data
insertData = py2my.execsql("insert into table (year, week, value) values (%s, %s, %s);", (2000, 1, 'value'), False, False)    
print insertData

# desc : update data
updateData = py2my.execsql("update table set value = %s where year = %s and week = %s;", ('new_value', 2000, 1), False, False)    
print updateData

# desc : delete data
deleteData = py2my.execsql("delete from table where year = %s and week = %s;", (2000, 1), False, False)    
print deleteData
```