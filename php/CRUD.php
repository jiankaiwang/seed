<?php
class CRUD {
    # ----------------------------------
    # private
    # ----------------------------------
    private $serviceUrl; 
    private $method;
    private $header;
    private $data;
    private $response;    

    #
    # desc : return status
    # 
    private function retStatus($getStatus, $getInfo, $getData) {
        return array("state" => $getStatus, "info" => $getInfo, "data" => $getData);
    }

    #
    # desc : prepare url
    #
    private function preUsrQuery() {
        $queryStr = "";
        foreach(array_keys($this -> data) as $key) {
            if(strlen($queryStr) < 1) {
                $queryStr = "$key=".$this -> data[$key];
            } else {
                $queryStr = $queryStr."&$key=".$this -> data[$key];
            }
        }
        return $queryStr;
    }

    #
    # desc : prepare header
    #
    private function preHeader() {
        $retStr = array();
        foreach(array_keys($this -> header) as $key) {
            $headerStr = "$key:".$this -> header[$key];
            array_push($retStr, $headerStr);
        }
        return $retStr;
    }
     
    #
    # desc : get() operation
    #
    private function GET() {
        $execRes = "";

        try {

            # start the connection session
            $ch = curl_init();

            # set the connection option
            $options = array(
                CURLOPT_URL => $this -> serviceUrl."?".($this -> preUsrQuery()),
                CURLOPT_HTTPHEADER => $this -> preHeader(),
                CURLOPT_HEADER => 1,
                CURLOPT_VERBOSE => 0,
                CURLOPT_RETURNTRANSFER => 1,
                CURLOPT_HTTPGET => true,
                CURLOPT_POST => false
            );

            # the curl option
            curl_setopt_array($ch, $options);

            # execute to fetch the web content
            $execRes = curl_exec($ch);

            # close the connection session
            curl_close($ch);        

            $this -> response = $this -> retStatus("success", "GET complete.", $execRes);

        } catch (Exception $e) {

            $execRes = $e -> getMessage();
            $this -> response = $this -> retStatus("failure", "GET is error.", $execRes);

        }
    }

    #
    # desc : POST() operation
    #
    private function POST() {

        $execRes = "";
    
        try {

            # start the curl functino
            $ch = curl_init();

            # the context body
            $options = array(
                CURLOPT_URL => $this -> serviceUrl,
                CURLOPT_HTTPHEADER => $this -> preHeader(),
                CURLOPT_HEADER => 1,
                CURLOPT_VERBOSE => 0,
                CURLOPT_RETURNTRANSFER => 1,
                CURLOPT_HTTPGET => false,
                CURLOPT_POST => true,
                CURLOPT_POSTFIELDS => http_build_query($this -> data),
            );

            # the curl option
            curl_setopt_array($ch, $options);

            # get curl result
            $execRes = curl_exec($ch);

            # end and close session
            curl_close($ch);

            $this -> response = $this -> retStatus("success", "POST complete.", $execRes);

        } catch (Exception $e) {
            
            $execRes = $e -> getMessage();
            $this -> response = $this -> retStatus("failure", "POST is error.", $execRes);

        }

    }

    # 
    # desc : PUT() or DELETE() function
    # inpt :
    # |- $option : { PUT | DELETE }
    # 
    private function PUTorDEL($option) {
        
        $execRes = "";

        try {

            # start the curl functino
            $ch = curl_init();

            # the context body
            $options = array(
                CURLOPT_URL => $this -> serviceUrl,
                CURLOPT_HTTPHEADER => $this -> preHeader(),
                CURLOPT_CUSTOMREQUEST => $option,
                CURLOPT_HEADER => 1,
                CURLOPT_VERBOSE => 0,
                CURLOPT_RETURNTRANSFER => 1,
                CURLOPT_HTTPGET => false,
                CURLOPT_POST => false,
                CURLOPT_POSTFIELDS => http_build_query($this -> data)
            );

            # the curl option
            curl_setopt_array($ch, $options);

            # get curl result
            $execRes = curl_exec($ch);

            # end and close session
            curl_close($ch);

            $this -> response = $this -> retStatus("success", "$option complete.", $execRes);

        } catch (Exception $e) {

            $execRes = $e -> getMessage();
            $this -> response = $this -> retStatus("failure", "$option is error.", $execRes);

        }

    }

    #
    # desc : constructor
    # inpt : 
    # |- sendUrl : server url, e.g. http://test.php
    # |- getMethod : { GET|POST|PUT|DELETE }
    # |- getHeader : array("auth" => "authVal")
    # |- getData : array("opt" => "val")
    #
    public function __construct($sendUrl, $getMethod, $getHeader, $getData)
    {
        if(!
            (is_string($sendUrl) 
            and is_string($getMethod) 
            and is_array($getHeader) 
            and is_array($getData))
        ) {
            $this -> response("failure", "Input parameters are not correct.", "");    
            
        } else {

            $this -> serviceUrl = $sendUrl;
            $this -> method = strtoupper($getMethod);
            $this -> header = $getHeader;
            $this -> data = $getData;      
  
            # beginning passing request
            switch($this -> method) {
                default:
                case "GET":
                    $this -> GET();
                    break;
                case "POST":
	            $this -> POST();
                    break;
                case "PUT":
                    $this -> PUTorDEL("PUT");
                    break;
                case "DELETE":
                    $this -> PUTorDEL("DELETE");
                    break;
            }
        }
    }

    #
    # desc : destruct
    #
    public function __destruct() {
        $this -> serverInfo = "";
        $this -> method = "";
        $this -> response = "";
    }

    #
    # desc : get response in json
    #
    public function response($format) {
        switch(strtolower($format)) {
            case "json":
            case "js":
            default:
                return json_encode($this -> response);
        }
    }

}

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

# eg.1 GET method
$getObj = new CRUD("http://localhost/REQUESTMETHOD.php", "GET", array("auth" => "keyVal"), array("opt" => 1, "val" => 1));
echo $getObj->response("json");

# eg.2 POST method
$postObj = new CRUD("http://localhost/REQUESTMETHOD.php", "POST", array("auth" => "keyVal"), array("opt" => 1, "val" => 2));
echo $postObj->response("json");

# eg.3 PUT method
$putObj = new CRUD("http://localhost/REQUESTMETHOD.php", "PUT", array("auth" => "keyVal"), array("opt" => 1, "val" => 3));
echo $putObj->response("json");

# eg.4 DELETE method
$delObj = new CRUD("http://localhost/REQUESTMETHOD.php", "DELETE", array("auth" => "keyVal"), array("opt" => 1, "val" => 4));
echo $delObj->response("json");
?>
