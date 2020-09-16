// Logs when page is loaded
$( document ).ready(function() {
    // Logs when page is loaded
    console.log( "Document ready!" );

    // Hides flashed messages
    $("#flash").delay(500).fadeOut(1000);

    $(function yearselect()
    {
        var yearselect = $("#yearSelect");
        var currentyear = (new Date()).getFullYear();

        for (var i = 2000; i <= currentyear; i++)
        {
            var option = $("<option/>");
            option.html(i);
            option.val(i);
            yearselect.append(option);
        }
        console.log("Yearselect ready")
    })
    
});

function openForm() {
    document.getElementById("newStudentForm").style.display = "block";
}
  
function closeForm() {
    document.getElementById("newStudentForm").style.display = "none";
}

$(".yearselect").ready(function() {
    var minOffset = 18, maxOffset = 100; // Change to whatever you want
    var thisYear = (new Date()).getFullYear();
    var select = $('<select>');

    for (var i = minOffset; i <= maxOffset; i++) {
        var year = thisYear - i;
    $('<option>', {value: year, text: year}).appendTo(select);
}
})