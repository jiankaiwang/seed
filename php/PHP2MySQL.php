<?php
class PHP2MySQL {
    
    # --------------------------
    # private
    # param@url : host, e.g. 192.168.1.2
    # param@port : e.g. 3306
    # param@db : e.g. testDB
    # param@table : e.g. dbTable
    # param@user : e.g. dbUser
    # param@pwd : e.g. pwd_EG
    # param@data : ( "col" => "value" ) as dictionary in set command
    # param@selItem : ( "col1", "col2" ) as list in select command
    # param@condition : ( "col" => "value" ) as dictionary in where command
    # param@status : ( "state" => "success", "info" => "complete", "data" +> "sql execution" ) as returning
    # --------------------------
    private $url;
    private $port;
    private $db;
    private $table;
    private $user;
    private $pwd;
    private $data;
    private $selItem;
    private $condition;
    private $status;

    #
    # desc : prepare returned status 
    #
    private function retStatus($getState, $getInfo, $getData) {
        $this -> status["state"] = $getState;
        $this -> status["info"] = $getInfo;
        $this -> status["data"] = $getData;
    }

    #
    # desc : select item commands
    # 
    private function selItemCmds() {
        $selCmd = "";
        if(count($this -> selItem) > 0) {
            $selCmd = join(',', $this -> selItem);
        } else {
            $selCmd = "*";
        }
        return $selCmd;
    }

    #
    # desc : where commands
    #
    private function whereCmds() {
        $wheCmd = array("cmd" => "", "data" => array());
        if(count(array_keys($this -> condition)) > 0) {
            $wheCmd["cmd"] = "where";
            # represents variable count
            $index = 1;
            # contain all conditions
            $tmpCond = array();
            foreach($this -> condition as $key => $value) {
                array_push($tmpCond, $key." = :s".$index);
                $wheCmd["data"][":s".$index] = $value;
                $index += 1;
            } 
            # complete the where commands
            $wheCmd["cmd"] = $wheCmd["cmd"]." ".join(' and ', $tmpCond);
        }
        return $wheCmd;
    }

    # 
    # desc : insert sql cmds 
    #
    private function insertCmds($getData) {
        # $retData["cmd"] = "col1, col2, col3"
        # $retData["paraCmd"] = ":i1, :i2, :i3"
        # $retData["data"] = array(":i1" => value1, ":i2" => value2, ":i3" => value3)
        $retData = array("cmd" => "", "paraCmd" => "", "data" => array());
        # tmpCols : conserve keys
        $tmpCols = array();
        # tmpParams : conserve parameters standing for keys
        $tmpParams = array();
        # tmpIndex : for unique parameter usage
        $tmpIndex = 1;
        foreach($getData as $key => $value) {
            array_push($tmpCols, $key);
            array_push($tmpParams, ":i".$tmpIndex);
            $retData["data"][":i".$tmpIndex] = $value;
            $tmpIndex += 1;
        }
        # complete parameter-based sql command
        $retData["cmd"] = join(' , ', $tmpCols);
        $retData["paraCmd"] = join(' , ', $tmpParams);
        return $retData;
    }

    #
    # desc : set sql cmds
    # 
    private function setCmds($getData) {
        # $retData["paraCmd"] = "col1 = :i1, col2 = :i2, col3 = :i3"
        # $retData["data"] = array(":i1" => value1, ":i2" => value2, ":i3" => value3)
        $retData = array("paraCmd" => "", "data" => array());
        # tmpParams : conserves pairs of each sets, e.g. col1 = :i1
        $tmpParams = array();
        # tmpIndex : for unique parameter usage
        $tmpIndex = 1;
        foreach($getData as $key => $value) {
            array_push($tmpParams, $key." = :u".$tmpIndex);
            $retData["data"][":u".$tmpIndex] = $value;
            $tmpIndex += 1;
        }
        $retData["paraCmd"] = join(' , ', $tmpParams);
        return $retData;
    }

    # --------------------------
    # public
    # --------------------------

    #
    # desc : select body
    # param@$getSelItem : array("name", "country") as list for selected columns showed
    # param@$getConds : array("col" => "value") as dictionary for selected conditions
    #
    public function select($getSelItem, $getConds) {
        $this -> selItem = $getSelItem;
        $this -> condition = $getConds;

        try {
            $dbh = new PDO(
                'mysql:dbname='.$this -> db.';host='.$this -> url.';port='.$this -> port,
                $this -> user,
                $this -> pwd,
                array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES \'UTF8\'')
            );    

            $cmd = "SELECT ".$this -> selItemCmds()." FROM ".$this -> table;

            $bindParams = array();
            if(count(array_keys($this -> condition)) > 0) {
                $wheCmd = $this -> whereCmds();
                $cmd = $cmd." ".$wheCmd["cmd"].";";
                $bindParams = $wheCmd["data"];
            }
                
            $sth = $dbh -> prepare($cmd);

            if($sth->execute($bindParams)) {
               $this -> retStatus("success", "complete", $sth -> fetchAll(PDO::FETCH_ASSOC));
            } else {
               $this -> retStatus("failure", "execution error", array());
            }
            
        } catch (Exception $e) {
            $this -> retStatus("failure", $e -> getMessage(), array());
        }

        return $this -> status;
    }

    #
    # desc : insert SQL
    # param@$getInsertData : array( "col1" => "val1", "col2" => "val2" )
    #
    public function insert($getInsertData) {

        if(count(array_keys($getInsertData)) > 0) {
            try {
                $dbh = new PDO(
                    'mysql:dbname='.$this -> db.';host='.$this -> url.';port='.$this -> port,
                    $this -> user,
                    $this -> pwd,
                    array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES \'UTF8\'')
                );

                $getInsertedData = $this -> insertCmds($getInsertData);
                
                $cmd = "INSERT INTO ".$this -> table."( ".$getInsertedData["cmd"]." ) value ( ".$getInsertedData["paraCmd"]." );";
                $sth = $dbh -> prepare($cmd);

                if($sth->execute($getInsertedData["data"])) {
                    $this -> retStatus("success", "complete", array());
                } else {
                    $this -> retStatus("failure", "execution error", array());
                }

            } catch (Exception $e) {
                $this -> retStatus("failure", $e -> getMessage(), array());
            }
        } else {
            $this -> retStatus("failure", "Inserted data can not be null.", array());
        }

        return $this -> status;
    }

    #
    # desc : delete SQL 
    # param@$getConds : array( "col1" => "val1", "col2" => "val2" )
    # 
    public function execdelete($getConds) {
        if(count(array_keys($getConds)) > 0) {
            # for where commands usage
            $this -> condition = $getConds;

            try {
                $dbh = new PDO(
                    'mysql:dbname='.$this -> db.';host='.$this -> url.';port='.$this -> port,
                    $this -> user,
                    $this -> pwd,
                    array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES \'UTF8\'')
                );

                $getWhereCmds = $this -> whereCmds();

                $cmd = "DELETE FROM ".$this -> table." ".$getWhereCmds["cmd"].";";
                $sth = $dbh -> prepare($cmd);

                if($sth->execute($getWhereCmds["data"])) {
                    $this -> retStatus("success", "complete", array());
                } else {
                    $this -> retStatus("failure", "execution error", array());
                }

            } catch (Exception $e) {
                $this -> retStatus("failure", $e -> getMessage(), array());
            }

        } else {
            $this -> retStatus("failure", "Condition data can not be null.", array());
        }
        return $this -> status;
    }

    #
    # desc : update SQL
    # param@$getData : array( "col1" => "val1", "col2" => "val2" ) for update value
    # param@$getConds : array( "col1" => "val1", "col2" => "val2" ) for conditional selection
    #
    public function update($getData, $getConds) {
        if(count(array_keys($getData)) > 0 and count(array_keys($getConds)) > 0) {
            # for where commands usage
            $this -> condition = $getConds;

            try {
                $dbh = new PDO(
                    'mysql:dbname='.$this -> db.';host='.$this -> url.';port='.$this -> port,
                    $this -> user,
                    $this -> pwd,
                    array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES \'UTF8\'')
                );

                $setPairs = $this -> setCmds($getData);
                $wherePairs = $this -> whereCmds();

                $cmd = "UPDATE ".$this -> table." set ".$setPairs["paraCmd"]." ".$wherePairs["cmd"].";";
                $sth = $dbh -> prepare($cmd);

                if($sth->execute(array_merge($setPairs["data"], $wherePairs["data"]))) {
                    $this -> retStatus("success", "complete", array());
                } else {
                    $this -> retStatus("failure", "execution error", array());
                }
            } catch (Exception $e) {
                $this -> retStatus("failure", $e -> getMessage(), array());
            }
        } else {
            $this -> retStatus("failure", "Neither updated data nor condition data is null.", array());
        }
        return $this -> status;
    }

    # 
    # desc : constructor
    #
    public function __construct($getUrl, $getPort, $getDB, $getTB, $getUser, $getPwd) {
        # initial
        $this -> data = array();
        $this -> selItem = array();
        $this -> condition = array();
        $this -> status = array("state" => "none", "info" => "none", "data" => array());

        # outer resource
        $this -> url = $getUrl;
        $this -> port = $getPort;
        $this -> db = $getDB;
        $this -> table = $getTB;
        $this -> user = $getUser;
        $this -> pwd = $getPwd;
    }

    #
    # desc : destructor
    #
    public function __destruct() {
        $this -> data = array();
        $this -> selItem = array();
        $this -> condition = array();
        $this -> status = array("state" => "none", "info" => "none", "data" => array());

        # outer resource
        $this -> url = "";
        $this -> port = "";
        $this -> db = "";
        $this -> table = "";
        $this -> user = "";
        $this -> pwd = "";
    }

}

# table example
#+---------+-------------+------+-----+---------+----------------+
#| Field   | Type        | Null | Key | Default | Extra          |
#+---------+-------------+------+-----+---------+----------------+
#| id      | int(11)     | NO   | PRI | NULL    | auto_increment |
#| name    | varchar(75) | YES  |     | NULL    |                |
#| country | varchar(75) | YES  |     | NULL    |                |
#+---------+-------------+------+-----+---------+----------------+

# select example
#$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01"); 
#$getRes = $obj -> select(array("country"), array("name" => "shanghai"));
#echo "select : ".$getRes["state"]." ".$getRes["info"]."<br>";
#foreach($getRes["data"][0] as $key => $value) {
#    echo $key."->".$value."<br>";
#}

# insert example
#$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01");
#$getRes = $obj -> insert(array("name" => "New York", "country" => "U.S.A."));
#echo "insert : ".$getRes["state"]." ".$getRes["info"]."<br>";

# delete example
#$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01");
#$getRes = $obj -> execdelete(array("name" => "New York"));
#echo "delete : ".$getRes["state"]." ".$getRes["info"]."<br>";

# update example
#$obj = new PHP2MySQL("localhost","3306","test","cityData","test01","test01");
#$getRes = $obj -> update(array("country" => "China"), array("name" => "shanghai"));
#echo "update : ".$getRes["state"]." ".$getRes["info"]."<br>";

?>
