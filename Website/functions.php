<?php
    require_once("config.php");
function getSQLResult($sql,$exec = array()){
    try {
        $conn = new PDO("mysql:host=".$GLOBALS["DBservername"].";dbname=".$GLOBALS["DBname"], $GLOBALS["DBusername"], $GLOBALS['DBpassword']);
        #set PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        #assuming the user db will be called "Users"
        #still need to finalize DB structure, until then I'll just select all fields
        $statement = $conn->prepare($sql);
        $statement->execute($exec);
        $result = $statement->fetchAll(PDO::FETCH_ASSOC);
        $out = $result;
    	$out['success'] = True;
		$conn = null;
		return $out;
    }
	catch(PDOException $e)
    {
    	return error_obj('SQL Error '.$e);
    }
}
function executeSQL($sql,$exec = array()){
     try {
    	$conn = new PDO("mysql:host=".$GLOBALS["DBservername"].";dbname=".$GLOBALS["DBname"], $GLOBALS["DBusername"], $GLOBALS['DBpassword']);
    	#set PDO error mode to exception
    	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    	#assuming the user db will be called "Users"
    	#still need to finalize DB structure, until then I'll just select all fields
		$statement = $conn->prepare($sql);
		$statement->execute($exec);
		$out['success'] = True;
		$conn = null;
		return $out;
    }
	catch(PDOException $e)
    {
    	return error_obj('SQL Error '.$e);
    }
}

function addUpdate($command){
	executeSQL("INSERT INTO `Updates`(`command`) VALUES (:command)",$exec = array(':command' => $command));
}
/**
 * once-off function to transfer the userID|Number|Name|StudentNum to the Whatsapp server
 */
function getUserData(){
	return getSQLResult("SELECT USERID,USERNAME,STUDENTNUMBER,CELLNUMBER FROM Users");
}

/**
 * return all the useful user info
 */
function getUserStatus($userID){
	$user = getUserByID($userID);
	if(!$user['success']){
		return $error_obj($user['error']);
	}
	return $user;
}

/**
 * All manner of claims:  chests,revives etc
 */
function claim($userID,$dropCode){

	$result = getSQLResult("SELECT * FROM Claims WHERE ID = :ID",array(':ID' => $dropCode));
	$claimHistory = getSQLResult("SELECT * FROM ClaimHistory WHERE claimID = :claimid AND userID = :userid",array(':claimid' => $dropCode, ':userid' => $userID));
	$userdata = getSQLResult("SELECT HEARTS,STATUS FROM Users WHERE USERID=:userid",array(':userid' => $userID));

	if(count($userdata) > 1){//Is there a result?
		if(array_key_exists("0",$result)){//Is there a result?
			if ($claimHistory['success'] != 0 and count($claimHistory) <= 1){//Has this been claimed by the user?

				//collect data of claim
				$usesrem = ($result['0']['usesRemaining']-1);
				$claimtype = $result['0']['type'];
				$claimvalue = $result['0']['claimValue'];
				if($usesrem >= 0){//Uses left?
					//Handle Types
					$userHearts = $userdata['0']['HEARTS'];
					if($userdata['0']['STATUS'] == 'zombie'){
						switch ($claimtype) {
							case 888://Revive
								executeSQL("UPDATE `Users` SET `status` = 'human' WHERE `Users`.`userID` = :userID",array(':userID' => $userID));
								getSQLResult("UPDATE `Users` SET `hearts` = 3 WHERE `Users`.`userID` = :userID",array(':userID' => $userID));
								addUpdate("revive~~$userID");
								addHumanScore($userID,$claimvalue);
							case 0:
								break;
							default:
								return array("success" => False,'reason' => " you don't look very human-like. Claim failed.");
						}
					}else{
						switch ($claimtype) {
							case 0:
								break;
							case 1://1 Heart addition
								addHearts($userID,$dropCode,min(5,$userHearts+1));
								addHumanScore($userID,100);
								break;
							case 2://2 Heart addition
								addHearts($userID,$dropCode,min(5,$userHearts+2));
								addHumanScore($userID,100);
								break;
							case 3://3 Heart addition
								addHearts($userID,$dropCode,min(5,$userHearts+3));
								addHumanScore($userID,100);
								break;
							case 4://4 Heart addition
								addHearts($userID,$dropCode,min(5,$userHearts+4));
								addHumanScore($userID,100);
								break;
							case 5://5 Heart addition
								addHearts($userID,$dropCode,min(5,$userHearts+5));
								addHumanScore($userID,100);
								break;
							default:
								return array("success" => False,'reason' => " you don't look very zombie-like. Revive failed.");
						}
					}

					//Remove use from claim and update player score
					executeSQL("UPDATE `Claims` SET `usesRemaining`=:uses WHERE ID=:ID",array(':ID' => $dropCode, ':uses' => $usesrem));
					executeSQL("INSERT INTO `ClaimHistory` ( `claimID`, `userID`) VALUES (:claimid, :userid);",array(':claimid' => $dropCode, ':userid' => $userID));
					return array("success" => True);
				}else{
					return array("success" => False,'reason' => 'there are no uses left.');
				}
			}else{
				return array("success" => False,'reason' => 'you have already claimed this code.');
			}
		}else{
			return array("success" => False,'reason' => 'the code was not found');
		}
	}else{
		return array("success" => False,'reason' => 'Your user code could not be found.');
	}
}

function addHearts($userID,$dropCode,$hearts){
    executeSQL("UPDATE `Users` SET `hearts` = :hearts WHERE `Users`.`userID` = :userID",array(':userID' => $userID,':hearts' => $hearts));
	addUpdate("claim~~$userID~~$dropCode");
}

function addHumanScore($userID,$score){
	getSQLResult("UPDATE `Users` SET `humanScore` = `humanScore`+:claimvalue WHERE `Users`.`userID` = :userID",array(':userID' => $userID,':claimvalue' => $score));
}

function addZombieScore($userID,$score){
	getSQLResult("UPDATE `Users` SET `zombieScore` = `zombieScore`+:claimvalue WHERE `Users`.`userID` = :userID",array(':userID' => $userID,':claimvalue' => $score));
}
/**
 *  kills
 */

function kill($killerID,$victimID){

	$victimData = getSQLResult("SELECT STATUS FROM Users WHERE USERID = :ID",array(':ID' => $victimID));
	$killerData = getSQLResult("SELECT STATUS,ZOMBIESCORE FROM Users WHERE USERID = :ID",array(':ID' => $killerID));
	unset($victimData['success']);
	unset($killerData['success']);
	$killerScore = $killerData[0]['ZOMBIESCORE'];
	if(count($victimData) == 1 and count($killerID) == 1){//Is there a result?
		if($victimData[0]['STATUS'] == 'human'){
			if($killerData[0]['STATUS'] == 'zombie'){
				getSQLResult("UPDATE `Users` SET `ZOMBIESCORE` = :score WHERE `Users`.`userID` = :userID",array(':userID' => $killerID,':score'=>$killerScore+100));
				getSQLResult("UPDATE `Users` SET `STATUS` = 'zombie' WHERE `Users`.`userID` = :userID",array(':userID' => $victimID));
				addUpdate("kill~~$victimID~~$killerID");
				return array("success" => True);
			}else{
				return array("success" => False,'reason' => ' you are not a zombie.');
			}
		}else{
			return array("success" => False,'reason' => ' you cannot kill the undead...');
		}
	}else{
		return array("success" => False,'reason' => ' a user code could not be found.');
	}
}


function getNews($offset,$length){
try {
    	$conn = new PDO("mysql:host=".$GLOBALS["DBservername"].";dbname=".$GLOBALS["DBname"], $GLOBALS["DBusername"], $GLOBALS['DBpassword']);
    	#set PDO error mode to exception
    	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    	#assuming the user db will be called "Users"
    	#still need to finalize DB structure, until then I'll just select all fields
		$conn->query("SET @rank=0;SET @numrows = 0;");
		$conn->query("SELECT @numrows:=COUNT(*) as rows FROM Newsfeed;");
		$state = $conn->query("SELECT @rank:=@rank+1 AS rank, @numrows-@rank as i, message, time
		  FROM Newsfeed
		  WHERE @numrows-@rank >= $offset+1
		  ORDER BY rank DESC
		  LIMIT $length;");
		$out = $state -> fetchAll(PDO::FETCH_ASSOC);
		$conn = null;
		$ret = "";
		foreach ($out as $newspost){
			$ret .= "<div class='news_post'>\n";
			$ret .= "	<p class='post_text'>\n";
			$ret .= "		".$newspost['message']."\n";
			$ret .= "	</p>\n";
			$ret .= "	<p class='post_time'>\n";
			$ret .= "		".$newspost['time']."\n";
			$ret .= "	</p>\n";
			$ret .= "</div>\n";

		}
		echo $ret;
    }
	catch(PDOException $e)
    {
    	return error_obj('SQL Error '.$e);
    }
}

/**
 * does the main long polling, fetches from db, returns upon db change?
 */
function getUpdates(){
	$updates = getSQLResult("SELECT * FROM Updates");
	executeSQL("DELETE FROM Updates");
	if($updates['success'] == true){
		unset($updates['success']);
		return $updates;
	}else{
		return array("sendToAdmin~~Server updates error");
	}
}


/**
 * ???
 */
function getLeaderboard($length = 100){
	$zedscores = getSQLResult("SELECT USERID AS USERNAME,ZOMBIESCORE FROM Users ORDER BY ZOMBIESCORE DESC LIMIT $length");
	$humanscores = getSQLResult("SELECT USERNAME,HUMANSCORE FROM Users ORDER BY HUMANSCORE DESC LIMIT $length");
	$sectionscores = getSQLResult("SELECT SECTIONNAME, SUM(ZOMBIESCORE+HUMANSCORE) as SCORE FROM `Users` GROUP BY SECTIONNAME ORDER BY SCORE DESC");
	if($zedscores['success'] == true and $humanscores['success'] == true and $sectionscores['success'] == true){
		unset( $zedscores['success']);
		unset( $humanscores['success']);
		unset( $sectionscores['success']);
		return 	array("success"=>True,'humans'=>$humanscores,'zombies'=>$zedscores,'sections' => $sectionscores);
	}else{
		return array("success"=>False);
	}

}

function getLiving(){
	$living = getSQLResult("SELECT USERNAME FROM Users WHERE STATUS = 'human' ORDER BY HUMANSCORE DESC");
	unset ($living['success']);
	return $living;
}

/**************************************************************/

function getUserByID($userID){
	#returns a record from the user table + "success: True"
	#or an error object
	$result = getSQLResult("SELECT USERID,USERNAME,STUDENTNUMBER,CELLNUMBER, HUMANSCORE,ZOMBIESCORE,HEARTS,NEXTHEART,STATUS FROM `Users`  WHERE USERID = :userid",array(':userid' => $userID));
	return $result;

}


function error_obj($string){
	return (array('success' => False,'reason' => $string ));
}
