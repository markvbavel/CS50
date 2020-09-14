// Logs when page is loaded
$( document ).ready(function() {
    console.log( "Document ready!" );
});

// Hide flashed messages after 6 seconds
$( document ).ready(function() {
    $( "#flash" ).delay(3200).fadeOut(300);
});
