var map;
var marker;

google.maps.event.addDomListener(window, 'load', initialize);  

    function initialize() {
      var mapOptions = {
        zoom: 16,
        // center: {lat: 37.8086730, lng:-122.4098210},
        center: new google.maps.LatLng(37.8086730, -122.4098210),
        mapTypeControl: false,
        zoomControl: true,
        zoomControlOptions: {
          style: google.maps.ZoomControlStyle.SMALL
        },
        streetViewControl: false,
      };
      map = new google.maps.Map(document.getElementById('place-map-canvas'),
          mapOptions);
    
      marker = new google.maps.Marker({
                      position: {lat: 37.8086730, lng:-122.4098210},
                      map: map,
                      title:"Pier 39"
                      });

    }
     

    $(function(){
      pickNewPlace();
      updateSharingOptions();
      updateTravelParty();

      removeComment();
      addComment();
      removePlaceImage();
      savePlace();
      updateImgSlider();

	  $(".uploaded-from-camera-roll").hide();
	  // $("#create-self-comment").hide();

      if(parseInt($("span.badge").html()) ==0){
        $("#travel-party-response").hide();
      }
    });

  function pickNewPlace(){
    $("#placemodal-place-tbl li").on("click", function(){
        if(!$(this).has(".icon-check").length){
          //remove check from other place
          $("#placemodal-place-tbl li").children(".icon").remove();
          //add check to this place
          $(this).prepend("<span class='icon icon-check'></span>");
          $("#current-place").html($(this).text());
          marker.setPosition({lat: 37.8081420,lng:-122.4165950 });
          marker.setTitle("New Position");
          map.setCenter({lat: 37.8081420,lng:-122.4165950 });
        }
      });
  } //end function pickNewPlace()

   function updateSharingOptions(){
    $("#public-sharing-notify").hide();
    
    $("#sharing-options li").on("click", function(){
        //remove other option's checkmark
        $("#sharing-options li").children(".icon").remove();

        var curItem = $(this).text();

        //add checkmark to this option
        $(this).prepend('<span class="icon icon-check"></span>');
        //update the share option shown on place detail page
        $(".detail-share-section a").html(curItem);

        if(curItem == "Public"){
          $("#public-sharing-notify").show();
          if(parseInt($("span.badge").html()) !=0){
            $("#travel-party-response").show();
          }
        }
        else{
          $("#public-sharing-notify").hide();
          $("#travel-party-response").hide();
        }
       
    });
     $("#btn-ask-travel-party").on("click", function(){
          
          var count = parseInt($("span.badge").html());
          console.log(count);
          $("span.badge").html(count + 1);
          $("#travel-party-response").show();
        });
  } //end function updateSharingOptions()

  function updateTravelParty(){
    $("#friend-list li").on("click", function(){
         var username = $(this).text();
         var userid = $(this).attr("id");
         userid = userid.slice(userid.lastIndexOf("-")+1, userid.length);
         console.log(userid);
        if(!$(this).has(".icon-check").length){
          $(this).prepend("<span class='icon icon-check'></span>");
          //add the selected user to travel party section
         
          $(".detail-travel-party-section .content-padded").append(
            "<span id='travelparty-" + userid+
            "'><img class='user-profile-pic' src='http://placehold.it/42x42'><span class='user-profile-name'>" + username+ "</span></span>"
            );
        }
        else{
          $(this).children(".icon").remove();
          $("#travelparty-"+userid).remove();
        }
      });
  }// end function updateTravelParty()

function removeComment(){
	$(".del-comment-btn").on("click", function(){
		$(this).parent().remove();
	});
}
function removePlaceImage(){
	$(".detail-img-thumb-section .icon-close").on("click", function(){
		var imgsrc = $(this).prev().attr("src");
        var imgname = imgsrc.slice(imgsrc.lastIndexOf("/")+1, imgsrc.length);
        $(".slide[name='" + imgname + "']").remove();
        $("span[name='" + imgname+ "']").remove();
	});
}
function savePlace(){
	// addComment();
  	$("header a.pull-right").on("click", function(){
  		console.log("boo");
  		var placeId = $("#placemodal-place-tbl li").children(".icon").parent().attr("id");
  		var dateTime = $(".place-detail-datetime").text();
  		var images = $(".uploaded-from-camera-roll img");

  		var travelParty = $(".detail-travel-party-section .content-padded").children("span");
  		var existingComments = $(".self-comment");
  		var newComment = $("#new-comment").val();
  		var shareOption = $(".detail-share-section a").text();

  		createFormInput("placeId", placeId);
  		createFormInput("dateTime", dateTime);
  		createFormInput("shareOption",shareOption);
  		createFormInput("newComment", newComment);

  		travelParty.each(function(){
  			createFormInput($(this).attr("id"), $(this).attr("id"));
  		});

  		existingComments.each(function(){	
			var commentId = $(this).attr("id");
			createFormInput(commentId, $(this).text());
  		});
  	});
  }

  function createFormInput(name, value){
  	var form = $("#form-save-existing-place");
  	
  		var field = document.createElement("input");
  		field.setAttribute("name", name);
  		field.setAttribute("value", value);
  		form.append(field);
  }

  function addComment(){
  	$(".add-comment-btn").on("click", function(){
  		$(".place-comments ul").append("<li class='table-view-cell media'>"+
  			"<img class='media-object pull-left user-profile-pic' src='http://placehold.it/42x42'>"+
                "<div class='media-body'>"+
                  "<input type='textarea' id='new-comment'></input></div>"+
                "<span class='icon icon-close del-comment-btn'></span></li>");
  		removeComment();
  	});
  }

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
