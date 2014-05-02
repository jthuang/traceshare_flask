$(function(){
    
    $(".public-img-thumb-section").hide();
    $("#btn-view-more-thumb").on("click", function(){
    	if($(this).html() == "Show Thumbnails"){
    		$(".public-img-thumb-section").show();
    		$(this).html("Hide Thumbnails");
    	}
    	else{
    		$(".public-img-thumb-section").hide();
    		$(this).html("Show Thumbnails");
    	}
    });

    $(".like-info").on("click", function(){
    	var liked = $(this).children(".icon");
    	if(liked.hasClass("icon-star")){
    		liked.remove();
    		var numLikes = parseInt($(this).text()) + 1;
    		$(this).html("<span class='icon icon-star-filled'></span>" + numLikes);

    		//push the change to server
    		// data should include photo id, user id, number of likes
   //  		$.ajax({
			//   type: "POST",
			//   url: url,
			//   data: data,
			//   success: success,
			//   dataType: dataType
			// });
    	}
    });

    $("#btn-add-favorite").on("click", function(){
        console.log("add to favorite");
        //add place to favorite, push the change to server
        // data should include place id, user id
    //       $.ajax({
        //   type: "POST",
        //   url: url,
        //   data: data,
        //   success: success,
        //   dataType: dataType
        // });
    });

    updateImgSlider();
});

function updateImgSlider(){
    $(".detail-thumb-img").on("click", function(){
        var src = $(this).attr("src");
        //find out the position of this img in the slider group
        var listOfImg = $("#detail-large-img-slider").find(".slide");

        var index = 0;
        $.each(listOfImg, function(i, v){
            if ($(v).children("img").attr("src") == src){
                index = i;
            }
        });

        var sliderWidth = document.querySelector(".slide").offsetWidth;
        var offsetX = -(index * sliderWidth);
        
        $("#detail-large-img-slider").children(".slide-group").css('-webkit-transition-duration', '.2s');
        $("#detail-large-img-slider").children(".slide-group").css('webkitTransform', 'translate3d(' + offsetX + 'px,0,0)');
    });
}