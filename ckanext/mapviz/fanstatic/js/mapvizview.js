/*
*
*
*/
"use strict";

ckan.module('mapvizview',function(jQuery) {

	return{
		initialize: function(){
      		this.el.append($("<div></div>").attr("id","map"));
      		$("#map").append($("<div>HELLOOOOOOO</div>"));

      		console.log(this);
		    console.log(this.options);
		    console.log(this.options.proxy_service_url);

			var counties = $.ajax({
	          url:this.options.proxy_service_url,
	          dataType: "json",
	          success: console.log(data),
	          error: function (xhr) {
	            alert(xhr.statusText)
	          }
	        })

	        console.log(counties)

      		jQuery.get(this.options.proxy_service_url).done(
		        function(data){
					console.log(data);
		        })
		    .fail(
		        function(jqXHR, textStatus, errorThrown) {
					console.log("fail");
		        }
		    );
		}
	};
});