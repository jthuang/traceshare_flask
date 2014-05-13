 var map;
 var marker;
 var lat;
 var lng;
 var tmp_cids = new Array();


    $(function(){
      saveJournal();
    });

  function saveJournal(){
  	$("header a.pull-right").on("click", function(){

  		var title = $('input[name="title"]').val();
  		var desp = $('input[name="desp"]').val();
  		var shareOption = $(".detail-share-section a").text();

                console.log($(".checkin-detail").length);
                var cids = new Array();
  		$(".checkin-detail").each(function(){
  		   if (this.checked) {
     		     cids.push($(this).attr("id"));
                   }
  		});
  		console.log(cids.toString());
  		console.log(tmp_cids.toString());


  		createFormInput("title", title);
  		createFormInput("desp", desp);
  		createFormInput("shareOption",shareOption);
  		createFormInput("cids", cids.toString());
  		createFormInput("tmp_cids", tmp_cids.toString());


  		form = $("#form-preview-journal");
  		form.submit();
  	});

  }

  function createFormInput(name, value){
  	var form = $("#form-preview-journal");
  	
  		var field = document.createElement("input");
  		field.setAttribute("name", name);
  		field.setAttribute("value", value);
  		form.append(field);

  }

