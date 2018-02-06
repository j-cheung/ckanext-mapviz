/*
*
*
*/
"use strict";

ckan.module('mapvizview',function(jQuery) {

	return{
		initialize: function(){
			var self = this;

      		this.el.append($("<div></div>").attr({
      			"id":"map",
      			"style":"width:100%; min-height:650px"
      		}));
      		// $("#map").append($("<div>HELLOOOOOOO</div>"));

      		mapboxgl.accessToken = 'pk.eyJ1IjoiamNoZXVuZyIsImEiOiJjajh0M2FwMncwZ290MnFxdTY3enB6cXlnIn0.e26zB-gpmMOt6SjHbJ68vg';
			var map = new mapboxgl.Map({
			    container: 'map',
			    style: 'mapbox://styles/mapbox/streets-v9'
			});

      		jQuery.getJSON(this.options.proxy_resource_url)
      		.done(
		        function(data){
		        	console.log("success")
					console.log(data);
					//plot on map
					self.plotGeoJSON(map,data)
		        })
		    .fail(
		        function(jqXHR, textStatus, errorThrown) {
		        	console.log("fail")
	           	 	console.log(errorThrown)
		        }
		    );
		},

		plotGeoJSON: function(map,jsonData) {
			map.on('load', function() {
				map.addSource({
					"type": "geojson",
					"data": jsonData
				});


			})
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