<?php
error_reporting(0);
session_start();
function userProfile($returnAsJson){

$heartHtml=($_SESSION['status']=='human')?"<span id='user_profile-hearts' data-val=".$_SESSION['hearts']."></span><span id='user_profile-nextHeart' data-val=".$_SESSION['nextHeart']."></span>":'';

$firstName = explode(' ',$_SESSION['username']);
$firstName = $firstName[0];



$userProfileHtml = <<<END
<div id="user_profile">
<h4 id="user_profile-username">
<img src="images/{$_SESSION['status']}.png" width="48px" height="48px" id="user_profile-icon">
{$firstName}</h4>
<span id="user_profile-userID">Your secret code: <span>{$_SESSION['userID']}</span></span>
<span id="user_profile-humanScore">Human score: <span>{$_SESSION['humanScore']} pts</span></span>
<span id="user_profile-zombieScore">Zombie score: <span>{$_SESSION['zombieScore']} pts</span></span>
{$heartHtml}
<input id="code_box" type="text" placeholder="Enter code here" name="code" maxlength="10"><button id="send_code">GO</button>
<a id="logout" href="index.php?logout=1">Log out</a>
</div>
END;
if($returnAsJson){

return json_encode(array("success"=>true,"html"=>$userProfileHtml));
}else{
    return $userProfileHtml;
}
}

// if(isset($_SESSION['studentNumber']) ){
//         var_dump($_POST);
//   		echo userProfile(false);
//  		die();
// }
