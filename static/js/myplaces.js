$(function(){
    
    $(".trace-search-form").submit(function(event){
    	event.preventDefault();
    	var placeOrJournal = $("#place-journal-toggle-btns a.active").text();
    	console.log(placeOrJournal);
    	$("#search-trace-bar").val("");
    	$("#search-trace-cancel").hide();
    	console.log("search for " + placeOrJournal);
    });
	animateTraceSearchBar();
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
