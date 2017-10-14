<?php
        error_reporting(0);
    $pageTitle = "Register for Metazombies 2017";
	require_once("config.php");
	require_once("header.php");
?>
	<form name="main" id="signup_form" action="signup.php" method="POST">
		<input type="text" name="username" placeholder="Name and surname" maxlength="60">
		<input type="text" name="studentNumber" placeholder="Student number e.g. 19132456" maxlength="8">
		<select name="sectionName">
			<option disabled selected value>-- select section name --</option>
			<?php
				$str = "";
				#create an option for each value name in $sectionList
				foreach ($sectionList as $sectionName) {
					$sectionName2 = $sectionName;
					if($sectionName=="Easy Company"){
						$sectionName2.= ' &#128002; ?';
					}
					if($sectionName == "Kushi Square"){
						$sectionName2.=' &hearts;';
					}
			 		$str .= '<option value="'.$sectionName.'">'.$sectionName2.'</option>';
			 	}
			 	echo $str;
			?>
		</select>
		<input type="text" name="cellNumber" placeholder="cell number e.g. 082XXXXXXX" maxlength="10">
		<input type="password" name="password" placeholder="Password (Min 7 Characters)">
		<input id="confirm_password" type="password" placeholder="Confirm password">
		<input id="submit" type="submit" value="submit">
	</form>
	<span id="formWarnings"></span>
	<script type="text/javascript">
		$('#signup_form').submit(function(event){
			event.preventDefault();
			var $form = $(this);


				if($('input[name=\"studentNumber\"]').val().length < 8){
					$("#formWarnings").html("Invalid student number");
					return false;
				}
				if (!$('select[name=\"sectionName\"]').val()){
					$("#formWarnings").html("Choose a section name");
					return false;
				}
				if($('input[name=\"cellNumber\"]').val().length<10){
					$("#formWarnings").html("Invalid cellphone number");
					return false;
				}
				if($('input[name=\"password\"]').val().length < 6){
					$("#formWarnings").html("Password must be at least 6 characters long");
					return false;
				}
				if($('#confirm_password').val() != $('input[name=\"password\"]').val()){
					$("#formWarnings").html("Passwords do not match");
					return false;
				}

                $.ajax({
                    type:'POST',
                    url:'signup.php',
                    data:$('#signup_form').serialize(),
                    success:function(response)
                    {
                    	var responseObj = JSON.parse(response);
                    	if(!responseObj.success){
                        	$("#formWarnings").html(responseObj.error);
                        	$("#formWarnings").addClass("showFormWarnings");

                    	}else{
                    		$form.remove();
                    		$('#formWarnings').remove();
                    		$('body').append(
                    			"<div id=\"register_success\"><h4> Success! </h4>"+
                    			"<p> You are now registered for Metazombies 2017. </p>"+
                    			"<button id='success_return' class='nav_button' onclick=\"document.location.href=\'index.php\'\">Return to home page</a></div>");
                    	}
                    }
                });

		});

	</script>
<?php
	require_once("footer.php");
?>
