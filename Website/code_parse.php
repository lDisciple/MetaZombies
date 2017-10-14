<?php

//die();
session_start();
require_once("functions.php");
if(isset($_POST["code"]) && isset($_SESSION['userID'])){
    if(strlen($_POST["code"])==intval($killStringLength)){
        $outputArr = kill($_SESSION['userID'],$_POST['code']);
    }else{
		$outputArr = claim($_SESSION['userID'],$_POST['code']);
	}
	echo json_encode($outputArr);
}else{
	echo json_encode(array("success"=>false,"reason"=>"Refresh and try again"));
}
