<?php

#TODO: test on server
require_once('config.php');
error_reporting(0);
#only allow access from website
#curl -H "207","cellNumber":"1234353453","sectionName":"Easy Company"}' http://localhost/signup.php
function error_json($string){
    return json_encode((array('success' => False,'error' => $string )));
}
#$_POST = json_decode(file_get_contents('php://input'), true);
try {
    #don't forget to sanitize input
	$username = $_POST['username'];
	$password = $_POST['password'];
	$studentNumber = $_POST['studentNumber'];
	$cellNumber = $_POST['cellNumber'];
	$sectionName = $_POST['sectionName'];

	#echo "sectionName: _ $sectionName _";
} catch (Exception $e) {
	echo error_json('GTFO');
	exit();
}

#check if section is valid
$isValidSection = False;
for($i = 0;$i<count($sectionList);$i++){
	if($sectionName == $sectionList[$i]){
			$isValidSection = True;
	}
}

if(strlen($cellNumber)!=10){
	echo error_json('Invalid phone number');
	exit();
}

if(!$isValidSection){
	echo error_json('Invalid section name');
	exit();
}

#check if studentNumber is valid
$stdNums = file('studentNums.txt');
$stdNums = array_map('trim', $stdNums);
$isValidStdNum = in_array($studentNumber, $stdNums);

if(!$isValidStdNum){
	echo error_json('Invalid student number');
	exit();
}

#check if any values in db

try {

    	$conn = new PDO("mysql:host=$DBservername;dbname=$DBname", $DBusername, $DBpassword);
    	#set PDO error mode to exception
    	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    	#assuming the user db will be called "Users"
		$statement = $conn->prepare("SELECT * FROM Users WHERE username=:username OR studentNumber=:studentNumber OR cellNumber=:cellNumber");
		$statement->execute(array(':username' => $username,':studentNumber'=>$studentNumber,':cellNumber'=>$cellNumber));


		$result = $statement->fetchAll();
		if(count($result)>0){
			echo error_json('Invalid details');
			exit();
		}
		$conn = null;
}
catch(PDOException $e){
    	echo error_json('Internal Error '.$e);
    	exit();
}


$userid = substr(md5($studentNumber.$passwordSalt),0,7);#limit to 7 characters
$passwordHash = password_hash($password,PASSWORD_DEFAULT);#TODO
try {
    	$conn = new PDO("mysql:host=$DBservername;dbname=$DBname", $DBusername, $DBpassword);
    	#set PDO error mode to exception
    	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	#removeSymbols
	$statement = $conn->prepare("INSERT INTO Users (userID,username,status,studentNumber,cellNumber,hearts,sectionName,passwordhash) VALUES(:userid,:username,\"human\",:studentNumber,:cellNumber,1,:sectionName,:passwordhash)");#TODO
		$statement->execute(array(':userid' => $userid,':username' => $username,':studentNumber'=>$studentNumber,':cellNumber'=>$cellNumber,':sectionName' => $sectionName,':passwordhash'=>$passwordHash));


		echo json_encode(array('success'=>True));
		exit();
		#$conn = null;
}
catch(PDOException $e){
		print_r($e);
    	echo error_json('Internal Error');
}
