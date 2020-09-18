// Logs when page is loaded
$(document).ready(function() 
{
    // Logs when page is loaded
    console.log( "Document ready!" );

    // Hides flashed messages
    $("#flash").delay(500).fadeOut(1000);
});
  
const cardContainer = document.querySelector('.cardContainer');
function showForm() {
  cardContainer.classList.add('open');
}
function hideForm() {
  cardContainer.classList.remove('open');
}