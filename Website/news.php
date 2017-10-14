<?php
	// die();
	require_once("functions.php");
	
	$req = $_POST;
	getNews($req['offset'],$req['length']);