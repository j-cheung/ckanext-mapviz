/*
*
*
*/
"use strict";

ckan.module('mapvizview',function(jQuery) {

	return{
		initialize: function(){
			var self = this;

      		this.el.append($("<div></div>").attr("id","map"));
      		$("#map").append($("<div>HELLOOOOOOO</div>"));

      		jQuery.getJSON(this.options.proxy_resource_url)
      		.done(
		        function(data){
		        	console.log("success")
					console.log(data);
		        })
		    .fail(
		        function(jqXHR, textStatus, errorThrown) {
		        	console.log("fail")
	           	 	console.log(errorThrown)
		        }
		    );
		},

		showError: function (jqXHR, textStatus, errorThrown) {
	      if (textStatus == 'error' && jqXHR.responseText.length) {
	        this.el.html(jqXHR.responseText);
	      } else {
	        this.el.html(this.i18n('error', {text: textStatus, error: errorThrown}));
	      }
	    },
	};
});