$(function(){
    removeComment();
    $(".uploaded-from-camera-roll").hide();
    $("#create-self-comment").hide();

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

function removeComment(){
	$(".del-comment-btn").on("click", function(){
		$(".self-comment .slider").remove();
		$("#create-self-comment").show();
	});
}

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

function removePlaceImage(){
	$(".detail-img-thumb-section .icon-close").on("click", function(){
		
	});
}