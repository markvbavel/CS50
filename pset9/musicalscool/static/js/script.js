$(document).ready(function() {
    
  // Switches to login form on login route
  $(".loginFormLink").click(function(e)
  {
    $("#loginForm").delay(50).fadeIn(200);
    $("#registerForm").fadeOut(0);
    $(".registerFormLink").removeClass("active");
    $(".loginFormLink").addClass("active");
    e.preventDefault();
  });
  
  // Switches to register form on login route
  $(".registerFormLink").click(function(e)
  {
    $("#registerForm").delay(50).fadeIn(200);
    $("#loginForm").fadeOut(0);
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