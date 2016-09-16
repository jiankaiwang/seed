<?php
class REQUESTMETHOD {

    # ----------------------------------
    # private
    # ----------------------------------
    private $serverInfo; 
    private $method;
    private $response;


    #
    # desc : get method
    #
    private function GET() {
        global $_GET;
        $getData = array();
        foreach($_GET as $key => $value) {
            $getData[$key] = $value;
        }
        $this -> response["response"] = $getData;
        return;
    }

    #
    # desc : post method
    #
    private function POST() {
        global $_POST;
        $postData = array();
        foreach($_POST as $key => $value) {
            $postData[$key] = $value;
        }
        $this -> response["response"] = $postData;
        return;
    }
  
    #
    # desc : put or delete method
    #
    private function getVars() {
        if (strlen(trim($vars = file_get_contents('php://input'))) === 0) {
            $vars = false;
        }
        return $vars;
    }
    private function PUTOrDelete() {
        $this -> response["response"] = $this -> getVars();
        return;
    }


    # ----------------------------------
    # public
    # ----------------------------------

    #
    # desc : constructor
    #
    public function __construct($getServer)
    {
        $this -> serverInfo = $getServer;
        $this -> method = $getServer['REQUEST_METHOD'];
        $this -> response = array("host" => $getServer['SERVER_NAME'], "uri" => $getServer['REQUEST_URI'], "method" => $getServer['REQUEST_METHOD']);

        # get all headers
        $this -> response['header'] = array();
        foreach (getallheaders() as $name => $value) {
            $this -> response['header'][$name] = $value;
        }
        
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
            case "DELETE":
                $this -> PUTOrDelete();
                break;
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

} // end of class Vegetable

$obj = new REQUESTMETHOD($_SERVER);
echo $obj->response("json");
?>
