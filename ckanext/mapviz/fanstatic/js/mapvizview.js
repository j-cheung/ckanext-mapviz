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

			var file = jQuery.get({
				url: this.options.proxy_service_url,
				dataType: "json"
			});

			console.log(file)

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