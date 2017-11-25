$(document).ready(function(){
    $(".nav a").click(function(){
        alert($(this).attr("href"));
        return false;
    });
});