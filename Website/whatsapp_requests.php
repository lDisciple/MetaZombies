<?php
    require_once("config.php");
    require_once("functions.php");
    #make it fail if the request doesn't use a chosen password?

    /*
        This script accepts a POST request from the whatsapp server

    	Commands:
			getUserData ()-> returns line for each user: userID~~username~~Human|Zombie status
			getUserStatus (userID)-> {Username, hearts , human|zombie status,time till next heart loss, other stuff}
			claim (code)-> True or False (packages,kills,revives)
			getUpdates ()-> long polling ... return command~~param1~~param2
			getLeaderboard ()-> return leaderboard?

			ADMIN COMMANDS?


	*/

	//error_reporting(0);
		#TODO: sanitize???

		#$request = json_decode($_POST['json']);#php input stream?
		$request = json_decode(file_get_contents('php://input'), true);#php input stream?
		if($request['password'] == $WhatsappPassword){

			try{
				$command = $request["command"];//FORMAT
				switch ($command) {
					case 'getUserData':
						$output = getUserData();
						break;
					case 'getUserStatus':
						$output = getUserStatus($request["userID"]);
						break;
					case 'claim':
						$output = claim($request["userID"],$request["code"]);
						break;
					case 'kill':
						$output = kill($request["killerID"],$request["victimID"]);
						break;
					case 'getUpdates':
						$output	= getUpdates();
						break;
					case 'getLeaderboard':
						$output = getLeaderboard(15);
						break;
    				case 'getLiving':
						$output = getLiving();
						break;
					default:
						$output = error_obj("Invalid command");
						break;
				}
			}catch (Exception $e){
					//just as a precaution
					$output = error_obj("Invalid request");
			}
			echo json_encode($output);


		}else{
			echo json_encode(array('success'=>False,'reason' => 'Wrong password'.$request['password'].$WhatsappPassword));
		}

