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

      		console.log(this);
		    console.log(this.options);
		    console.log(this.options.proxy_service_url);

			var counties = $.ajax({
	          url:this.options.proxy_service_url,
	          dataType: "json",
	          success: function(data) {
	          	console.log(data)
	          },
	          error: function (xhr) {
	            alert(xhr.statusText)
	          }
	        })

	        console.log(counties)

      		jQuery.getJSON(this.options.proxy_service_url).done(
		        function(data){
					console.log(data);
		        })
		    .fail(
		        function(jqXHR, textStatus, errorThrown) {
          			self.showError(jqXHR, textStatus, errorThrown);
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