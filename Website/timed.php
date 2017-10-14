<?php
error_reporting(0);
die();#comment this line to switch on the health countdown functions
#in order to prevent users from running this script simply by requesting the page,
#the chronjob will run it with a password
require_once("config.php");
require_once("functions.php");

$password = $argv[1] or die();

if ($password!=$timedPassword){
    die();
}

try {
        $conn = new PDO("mysql:host=".$GLOBALS["DBservername"].";dbname=".$GLOBALS["DBname"], $GLOBALS["DBusername"], $GLOBALS['DBpassword']);
        #set PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        #assuming the user db will be called "Users"
        #still need to finalize DB structure, until then I'll just select all fields
        $statement = $conn->prepare("UPDATE Users SET nextHeart= nextHeart - 60 WHERE nextHeart>0");
    	$statement->execute();
        $statement = $conn->prepare("UPDATE Users SET hearts=hearts-1,nextHeart=10800 WHERE nextHeart < 1 AND status='human'");
        $statement->execute();
        $statement= $conn->prepare("UPDATE Users SET status='zombie' where hearts<1");
        $statement->execute();

    }
	catch(PDOException $e)
    {
    	return error_obj('SQL Error '.$e);
    }
#decrease hearts if time is past nextHeart
#die if hearts drop to zero --> starve
#increment timeSurvived

