/*
*
*
*/
"use strict";

ckan.module('mapvizview',function(jQuery) {

	return{
		initialize: function(){
			console.log("hello");
      		this.el.append($("<div></div>").attr("id","map"));
      		$("#map").append($("<div>HELLOOOOOOO</div>"));

      		jQuery.get(this.options.proxy_service_url).done(
		        function(data){
		        	console.log(this.options.proxy_service_url)
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