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

		    console.log(this.options);
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