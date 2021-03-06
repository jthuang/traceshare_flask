 var map;
 var marker;
 var lat;
 var lng;


    $(function(){
      navigator.geolocation.getCurrentPosition(foundLocation, noLocation);
      google.maps.event.addDomListener(window, 'load', initialize);  
      pickNewPlace();
      updateSharingOptions();
      updateTravelParty();
      savePlace();
      if(parseInt($("span.badge").html()) ==0){
        $("#travel-party-response").hide();
      }
    });

    function initialize() {
      var mapOptions = {
        zoom: 16,
        center: new google.maps.LatLng(lat, lng),
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
                      position: {lat: lat, lng: lng},
                      map: map,
                      title:"Pier 39"
                      });

    }

  function foundLocation(position) {
     lat = position.coords.latitude;
     lng = position.coords.longitude;
     console.log(lat, lng);
     getPlaceName();
     initialize();
  }
  function noLocation() {}

  function getPlaceName() {
     $.get("/getplacename", {lat: lat, lng: lng}, function (place_info) {
        $("#current-place").html(place_info.name);
     }, "json");
  }

  function pickNewPlace(){
    $("#placemodal-place-tbl li").on("click", function(){
        if(!$(this).has(".icon-check").length){
          //remove check from other place
          $("#placemodal-place-tbl li").children(".icon").remove();
          //add check to this place
          $(this).prepend("<span class='icon icon-check'></span>");
          $("#current-place").html($(this).text());

          var lat = parseFloat($(this).attr("lat"));
          var lng = parseFloat($(this).attr("lng"));
          marker.setPosition({lat: lat, lng: lng });
          marker.setTitle($(this).text());
          map.setCenter({lat: lat, lng: lng });
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
          console.log("ask");
          var count = parseInt($("span.badge").html());
          $("span.badge").html(count + 1);
          $("#travel-party-response").show();
        });
  } //end function updateSharingOptions()

  function updateTravelParty(){
    $("#friend-list li").on("click", function(){
         var username = $(this).text();
         var userid = $(this).attr("id");
         userid = userid.slice(userid.lastIndexOf("-")+1, userid.length);
         
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

  function savePlace(){
  	$("header a.pull-right").on("click", function(){

  		var placeId = $("#placemodal-place-tbl li").children(".icon").parent().attr("id");
  		var dateTime = $(".place-datetime").text();
  		var images = $(".uploaded-from-camera-roll img");
  		var travelParty = $(".detail-travel-party-section .content-padded").children("span");
  		var picUrl = $(".uploaded-from-camera-roll").children("span").children("img");
  		var comments = $(".place-comments input").val();
  		var shareOption = $(".detail-share-section a").text();

  		createFormInput("placeId", placeId);
  		createFormInput("dateTime", dateTime);
  		createFormInput("selfComment", comments);
  		createFormInput("shareOption",shareOption);

                travel_party = new Array();
  		travelParty.each(function(){
  		   travel_party.push($(this).attr("id"));
  		});
  	        createFormInput("travelParty", travel_party.toString());

  	        pic_url = new Array();
  		picUrl.each(function(){
  		   pic_url.push($(this).attr("src"));
  		});
  	        createFormInput("picUrl", pic_url.toString());


  		form = $("#form-save-new-place");
  		form.submit();

  	});

  }

  function createFormInput(name, value){
  	var form = $("#form-save-new-place");
  	
  		var field = document.createElement("input");
  		field.setAttribute("name", name);
  		field.setAttribute("value", value);
  		form.append(field);

  }

