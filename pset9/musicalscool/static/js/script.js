$(document).ready(function() {
  // Logs when page is loaded
  console.log("Document ready");
  
  // Hides flashed messages
  $("#flash").delay(100).fadeOut(100);
    
  // Switches to login form on login route
  $(".loginFormLink").click(function(e)
  {
    console.log("Login form link clicked");
    $("#loginForm").delay(100).fadeIn(100);
    $("#registerForm").delay(100).fadeOut(100);
    $(".registerFormLink").removeClass("active");
    $(".loginFormLink").addClass("active");
    e.preventDefault();
  });
  
  // Switches to register form on login route
  $(".registerFormLink").click(function(e)
  {
    console.log("Register form link clicked");
    $("#registerForm").delay(100).fadeIn(100);
    $("#loginForm").delay(100).fadeOut(100);
    $(".loginFormLink").removeClass("active");
    $(".registerFormLink").addClass("active");
    e.preventDefault();
  });

  // Functions to show and hide the new student popup
  $("#newStudentBtn").click(function()
  {
    $("#newStudentPopup").show();
  
    // Calculate today for birthdate datepicker
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate(); 
  
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();
    if(dd<10){
          dd='0'+dd
      } 
      if(mm<10){
          mm='0'+mm
      } 
    today = yyyy+'-'+mm+'-'+dd;
    document.getElementById("birthDatePicker").setAttribute("max", today);  
  });
  
  $("#newStudentBlocker").click(function()
  {
    $("#newStudentPopup").hide();
  });

});