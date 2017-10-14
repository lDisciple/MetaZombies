<?php
    require_once("functions.php");
    $L = getLeaderboard();
    
    foreach($L['sections'] as $section){
        echo "<div class='leaderboard_post'>".$section['SECTIONNAME']."<div class='leaderboard_score'>".$section['SCORE']."</div></div>";        
    }
