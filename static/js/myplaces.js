$(function(){
    animateTraceSearchBar();
});
$(".input-group").submit(function(event){
    event.preventDefault();
    var placeOrJournal = $("#place-journal-toggle-btns a.active").text();
    $("#search-trace-bar").val("");
    $("#search-trace-cancel").hide();
    console.log(placeOrJournal);
    console.log("search for " + placeOrJournal); 
});

function animateTraceSearchBar(){
	$("#search-trace-cancel").hide();

    $("#search-trace-bar").focus(function(){
    	$("#search-trace-cancel").show();
    });
    $("#search-trace-cancel").on("click", function(){
    	console.log($("#search-trace-bar").val());
    	$("#search-trace-bar").val("");
    	$("#search-trace-cancel").hide();
    });
}
