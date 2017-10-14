<?php
// until login is allowed
//die();

error_reporting(0);
require_once("config.php");
require_once("login_functions.php");



#check studentNumber and password

if(!isset($_POST['login_form-studentNumber']) or !isset($_POST['login_form-password'])){
    echo json_encode(array("success"=>false,"error"=>"Invalid login details"));
	die();
}

$studentNum = $_POST['login_form-studentNumber'];
$userpwd = $_POST['login_form-password'];

try {
    	$conn = new PDO("mysql:host=$DBservername;dbname=$DBname", $DBusername, $DBpassword);
    	#set PDO error mode to exception
    	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    	
		$statement = $conn->prepare("SELECT * FROM Users WHERE studentNumber = :studentNumber");
		$statement->execute(array(':studentNumber' => $studentNum));


		$result = $statement->fetchAll(PDO::FETCH_ASSOC);
		if(count($result)>0){
			$userData  = $result[0];
			if(!password_verify($userpwd,$userData['passwordhash'])){
				echo json_encode(array('success'=>false,'error'=>'Incorrect password'));
				die();
			}

			#create the profile div
			$_SESSION['username'] = $userData['username'];
			$_SESSION['studentNumber'] = $studentNum;
			$_SESSION['userID'] = $userData['userID'];
			$_SESSION['status'] = $userData['status'];
			$_SESSION['humanScore'] = $userData['humanScore'];
			$_SESSION['zombieScore'] = $userData['zombieScore'];
			$_SESSION['hearts'] =$userData['hearts'];
			$_SESSION['nextHeart'] = $userData['nextHeart'];

			#temp --> make a function for this
			echo (userProfile(true));
		}else{
			echo json_encode(array('success'=>false,'error'=>'User not found'));
    		die();
    	}
		$conn = null;    	
    }
	catch(PDOException $e)
    {
    	echo json_encode(array('success'=>false,'error'=>'Could not connect to database'));
    	die();
    }


#handles login requests from index.php

