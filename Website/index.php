<?php
    $pageTitle = "Metazombies 2017";
    require_once('config.php');
    require_once("header.php");
    require_once('login_functions.php');
?>

<div id="panel_left">
    <div id="userArea">
    <?php
        //var_dump($_SESSION);
        if(isset($_GET['logout'])){
            $_SESSION = array();
        }
    	if (isset($_SESSION['username'])) {
			#if user is logged in : show profile

		try {
    	$conn = new PDO("mysql:host=$DBservername;dbname=$DBname", $DBusername, $DBpassword);
    	#set PDO error mode to exception
    	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

		$statement = $conn->prepare("SELECT * FROM Users WHERE studentNumber = :studentNumber");
		$statement->execute(array(':studentNumber' => $_SESSION['studentNumber']));


		$result = $statement->fetchAll(PDO::FETCH_ASSOC);
		if(count($result)>0){
			$userData  = $result[0];


			#create the profile div
			$_SESSION['status'] = $userData['status'];
			$_SESSION['humanScore'] = $userData['humanScore'];
			$_SESSION['zombieScore'] = $userData['zombieScore'];
			$_SESSION['hearts'] =$userData['hearts'];
			$_SESSION['nextHeart'] = $userData['nextHeart'];

			#temp --> make a function for this
		}
		$conn = null;
		$userAreaString = userProfile(false);
    }
	catch(PDOException $e)
    {
    	$userAreaString=<<<END
<form id="login_form" action="login.php" method="POST">
	<input name="login_form-studentNumber" placeholder="Student Number e.g. 20653145" maxlength="8" type="text">
	<input name="login_form-password" type="password" placeholder="Password e.g. 1234567">
	<div id="userArea_buttons" style="padding:0;min-width:100%;">
		<input type="submit" value="Log in" id="login_form-submit" style="margin-left:5%">
		<button type="button" id="login_form-register" onclick="document.location.href='register.php';">Register</button>
	</div>
	<span style="background-color:#191919;" id="login_errors"></span>
</form>

END;
    }

			// $userAreaString = $userAreaString["html"];
		}else{
			#else: show login bar with register button
$userAreaString=<<<END
<form id="login_form" action="login.php" method="POST">
	<input name="login_form-studentNumber" placeholder="Student Number e.g. 20653145" maxlength="8" type="text">
	<input name="login_form-password" type="password" placeholder="Password e.g. 1234567">
	<div id="userArea_buttons" style="padding:0;min-width:100%;">
		<input type="submit" value="Log in" id="login_form-submit" style="margin-left:5%">
		<button type="button" id="login_form-register" onclick="document.location.href='register.php';">Register</button>
	</div>
	<span style="background-color:#191919;" id="login_errors"></span>
</form>

END;
		}

		echo $userAreaString;
	?>
	</div>

	<div id="panel_left-buttons">
		<button class="nav_button" id="leaderboard_button" data-tab="leaderboard">Leaderboard<span class="nav_button-arrow">&gt;</span></button>
		<button class="nav_button" id="rules_button" data-tab="rules">Rules<span class="nav_button-arrow">&gt;</span></button>
		<button class="nav_button nav_button-active" id="news_button" data-tab="news">News<span class="nav_button-arrow">&gt;</span></button>
	</div>
</div>
<div id="panel_right">
	<div id="leaderboard" class="panel_right-section">
		<h4 class="panelSection-header">Leaderboard</h4>
		<div class="panel_content">
            <?php
            require_once("config.php");
            require_once("functions.php");
            $out = "";
            $leaderboardObj = getLeaderboard();

            foreach($leaderboardObj["humans"] as $human){
                if($human['HUMANSCORE']>0){


                    $out.="<div class='leaderboard_post'>".$human['USERNAME']."<div class='leaderboard_score'>Human score: ".$human['HUMANSCORE']."</div></div>";
                }
            }

            $out.="<hr>";

            foreach($leaderboardObj['sections'] as $section){
                $out.= "<div class='leaderboard_post'><b>".$section['SECTIONNAME']."</b><div class='leaderboard_score'>Total score: ".$section['SCORE']."</div></div>";
            }

            echo $out;

            ?>
		</div>
	</div>
	<div id="rules" class="panel_right-section">
		<h4 class="panelSection-header">Rules</h4>
		<div class="panel_content">
			<?php require_once("rules.php");?>
			<!--<div id="comingSoon" style='text-align:center;'><h3>Coming Soon<h3></div>-->
		</div>
	</div>
	<div id="news" class="panel_right-section current">
		<h4 class="panelSection-header">News</h4>
		<div class="panel_content" ss-container>
			<!-- <div id="comingSoon" style='text-align:center;'><h3>Coming Soon<h3></div> -->

			<div id="news_content" ss-container></div>
		<button id="newsShowMore" onclick="fetchNews()">Show more...</button>
		</div>

	</div>
</div>
<script type="text/javascript" src="main.js"></script>
<?php require_once("footer.php"); ?>
