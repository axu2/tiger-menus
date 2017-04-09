// for feedback form
var submitted=false;
function feedbackFormSubmitted() {
  submitted = false;
  $('.form').slideToggle();
  $('#feedback-button').text("Thank you!");

  // resets to tell us what you think by fading in and out
  setTimeout(function(){
    $('#feedback-button').animate({opacity:0})
    .queue(function(){
      $('#feedback-button').text("Tell us what you think.").dequeue()
    }).animate({opacity:1});  
  }, 2000);

  // resets all input fields and renables submit button
  $('.ss-q-long').val("")
  $("#ss-submit").show();
  $("#ss-submit-disabled").hide();
}

$(document).ready(function() {
  // adding a nice delay
  setTimeout(function(){
    $('#feedback-form').slideDown(750);
  }, 250);
  
  // animation for moving it up
  $("#feedback-button").click(function(){
    $('.form').slideToggle();       
  });

  // hack needed to disable submit (prevents multiple submissions)
  $("#ss-submit").click(function(){
    $("#ss-submit").hide();
    $("#ss-submit-disabled").show();
  });
});