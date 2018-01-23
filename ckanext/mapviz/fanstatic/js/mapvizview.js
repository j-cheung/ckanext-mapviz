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

      		jQuery.get(resource['url']).done(
		        function(data){
					console.log("done");
		        })
		    .fail(
		        function(jqXHR, textStatus, errorThrown) {
					console.log("fail");
		        }
		    );
		}
	};
});