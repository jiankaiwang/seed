# PHP2MySQL.php



### Example table
---

```mysql
# table example
+---------+-------------+------+-----+---------+----------------+
| Field   | Type        | Null | Key | Default | Extra          |
+---------+-------------+------+-----+---------+----------------+
| id      | int(11)     | NO   | PRI | NULL    | auto_increment |
| name    | varchar(75) | YES  |     | NULL    |                |
| country | varchar(75) | YES  |     | NULL    |                |
+---------+-------------+------+-----+---------+----------------+
```

### Constructor
---

* Parameters
  1. $getUrl : MySQL Server URL or IP
  2. $getPort : MySQL Service Port
  3. $getDB : used database
  4. $getTB : used table
  5. $getUser : access user
  6. $getPwd : user password

```php
# 
# desc : constructor
#
public function __construct($getUrl, $getPort, $getDB, $getTB, $getUser, $getPwd)
```

### API
---

* Select SQL

```php
#
# desc : select body
# param@$getSelItem : array("name", "country") as list for selected columns showed
# param@$getConds : array("col" => "value") as dictionary for selected conditions
#
public function select($getSelItem, $getConds)
```

* insert SQL

```php
#
# desc : insert SQL
# param@$getInsertData : array( "col1" => "val1", "col2" => "val2" )
#
public function insert($getInsertData)
```

* delete SQL

```php
#
# desc : delete SQL 
# param@$getConds : array( "col1" => "val1", "col2" => "val2" )
# 
public function execdelete($getConds)
```

* update SQL

```php
#
# desc : update SQL
# param@$getData : array( "col1" => "val1", "col2" => "val2" ) for update value
# param@$getConds : array( "col1" => "val1", "col2" => "val2" ) for conditional selection
#
public function update($getData, $getConds)
```

* advanced SQL : support complex sql command

```php
#
# desc : advanced and combined sql command
# param@sqlCmd : sql command, e.g. 
# select dm.*, dp.dept_name 
#   from dept_manager as dm left 
#     outer join departments as dp on dm.dept_no = dp.dept_no 
#   where dm.from_date > '1990-01-01'
#   order by dm.from_date asc;
# param@existRetData ( is there returned data ? ) : true (yes, select), false (no, insert, delete, update)
# param@paramDataArray ( parameter-based array for sql ) : e.g. '1990-01-01' is replaced by :from_date, array(':from_date' => $_POST['fd'])
#
public function execsql($sqlCmd, $existRetData, $paramDataArray)
```

### Example
---

* Select SQL

```php
$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01"); 
$getRes = $obj -> select(array("country"), array("name" => "shanghai"));
echo "select : ".$getRes["state"]." ".$getRes["info"]."<br>";
foreach($getRes["data"] as $key => $value) {
    echo $key."->".$value."<br>";
}
```

* insert SQL

```php
$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01");
$getRes = $obj -> insert(array("name" => "New York", "country" => "U.S.A."));
echo "insert : ".$getRes["state"]." ".$getRes["info"]."<br>";
```

* delete SQL

```php
$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01");
$getRes = $obj -> execdelete(array("name" => "New York"));
echo "delete : ".$getRes["state"]." ".$getRes["info"]."<br>";
```

* update SQL

```php
$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01");
$getRes = $obj -> update(array("country" => "China"), array("name" => "shanghai"));
echo "update : ".$getRes["state"]." ".$getRes["info"]."<br>";
```

* execsql example (complicated SQL)

```php
# only this function execsql() can not passe table names at the beginning of object created
$obj = new PHP2MySQL("localhost","3306","employees","","test01","test01");
$getRes = $obj -> execsql(
  "select dm.*, dp.dept_name from dept_manager as dm left outer join departments as dp on dm.dept_no = dp.dept_no where dm.from_date > :from_date order by dm.from_date asc;",
  True,
  array(':from_date' => '1990-01-01')
);
echo "select : ".$getRes["state"]." ".$getRes["info"]."<br>";
foreach($getRes["data"][0] as $key => $value) {
    echo $key."->".$value."<br>";
}
```
