$(document).ready(function() {
  // Logs when page is loaded
  console.log("Document ready");
  
  // Hides flashed messages
  $("#flash").delay(100).fadeOut(100);
    
  // Switches to login form on login route
  $("#loginFormLink").click(function(e)
  {
    console.log("Login form link clicked");
    $("#loginForm").delay(100).fadeIn(100);
    $("#registerForm").delay(100).fadeOut(100);
    $("#registerFormLink").removeClass("active");
    $(this).addClass("active");
    e.preventDefault();
  });
  
  // Switches to register form on login route
  $("#registerFormLink").click(function(e)
  {
    console.log("Register form link clicked");
    $("#registerForm").delay(100).fadeIn(100);
    $("#loginForm").delay(100).fadeOut(100);
    $("#loginFormLink").removeClass("active");
    $(this).addClass("active");
    e.preventDefault();
  });

  // Functions to show and hide the new student popup
  $("#newStudentBtn").click(function()
  {
    $("#newStudentPopup").show();
  });
  
  $("#newStudentBlocker").click(function()
  {
    $("#newStudentPopup").hide();
  });
});