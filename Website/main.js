var newsIndex = 0;
var newsFetchLength = 15;
var loggedIn = false;
function fetchNews(){
    //request with ajax --> newsIndex,newsFetchLength
	$.ajax({
                    type:'POST',
                    url:'news.php',
                    data:{"offset":newsIndex,"length":15},
                    success:function(response)
                    {
                    	if(response.length==0){
                    		$("#newsShowMore").remove();
                    	}
                    		$('#news_content').append(response);
                    		newsIndex+=newsFetchLength;
                    }
                });
}


$(document).ready(function(){
    $heartsHtml = '';
    $numHearts = Number($('#user_profile-hearts').attr('data-val'));
    for (var i = 0; i < 5; i++) {
                   if(i<$numHearts){
                      $heartsHtml+="<img class='heartImg' src='images/heart.png'>";
                   }else{
                      $heartsHtml+="<img class='heartImg' src='images/heart-grey.png'>";
                   }
    }
    $('#user_profile-hearts').html($heartsHtml);


    setInterval(function(){
        var time = Number($("#user_profile-nextHeart").attr('data-val'));
        $("#user_profile-nextHeart").attr('data-val',time-1);

        if(time<0){
          time=0;
        }
        var hours = Math.floor(time / 3600);
        time -= hours * 3600;

        var minutes = Math.floor(time / 60);
        time -= minutes * 60;

        var seconds = parseInt(time % 60, 10);



    $("#user_profile-nextHeart").html(hours + ':' + (minutes < 10 ? '0' + minutes : minutes) + ':' + (seconds < 10 ? '0' + seconds : seconds) +" until next heart expires");
}, 1000);


      $("#login_errors").hide();
      $('#login_form').submit(function(event){
          event.preventDefault();
          var $form= $(this);

          $.ajax({
                    type:'POST',
                    url:'login.php',
                    data:$('#login_form').serialize(),
                    success:function(response)
                    {
                         responseObj = JSON.parse(response);
                         if(responseObj.success){

                              $('#login_form').remove();
                              $("#userArea").append(responseObj.html);
                              loggedIn = true;

                              $heartsHtml = '';

                              $numHearts = Number($('#user_profile-hearts').attr('data-val'));
                              for (var i = 0; i < 5; i++) {
                                             if(i<$numHearts){
                                                $heartsHtml+="<img class='heartImg' src='images/heart.png'>";
                                             }else{
                                                $heartsHtml+="<img class='heartImg' src='images/heart-grey.png'>";

                                             }
                              }
                              $('#user_profile-hearts').html($heartsHtml);



     $("#send_code").on('click',function(){

        $.ajax({
                    type:'POST',
                    url:'code_parse.php',
                    data:{'code':$('#code_box').val()},
                    success:function(response)
                    {
                         r = JSON.parse(response);
                         if(r.success){
                            $("#code_box").val("");
                            $("#code_box").attr("placeholder","Success!");
                         }else{
                            $("#code_box").val("");
                            $("#code_box").attr("placeholder","Oops, "+r.reason);
                         }
                          }
                });
     });
                         }else{

                              $("#login_errors").show().text(responseObj.error);

                         }
                    }
                });

      });



     $('.panel_right-section').css('height',$(window).height() - $('#page_header').height() -60);
     fetchNews();

     $('.nav_button').click(function(){
          var tab_id = $(this).attr('data-tab');

          $('.nav_button').removeClass('nav_button-active');
          $('.panel_right-section').removeClass('current');

          $(this).addClass('nav_button-active');
          $("#"+tab_id).addClass('current');
  });


});
