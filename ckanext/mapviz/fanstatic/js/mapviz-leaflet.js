/*
*
*
*/
"use strict";

ckan.module('mapviz-leaflet',function(jQuery) {

	return{
		initialize: function(){
			var self = this;
			this.el.empty();
			this.el.append($("<div></div>").attr({
				"id":"map",
				"style":"width:100%; min-height:650px"
			}));
			var map = L.map('map').setView([51.505, -0.09], 13);
			L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
			    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
			    maxZoom: 18,
			    id: 'mapbox.dark',
			    accessToken: 'pk.eyJ1IjoiamNoZXVuZyIsImEiOiJjajh0M2FwMncwZ290MnFxdTY3enB6cXlnIn0.e26zB-gpmMOt6SjHbJ68vg'
			}).addTo(map);

			var resource_format = this.options.resource_format
			//if osm
			if(resource_format == 'osm'){
				console.log("osm")

			}
			//if geojson
			else if(resource_format == 'geojson'){
				console.log("geojson")
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
			}	
		},

		},

		plotGeoJSON: function(map, geojsonData) {
			L.geoJSON(geojsonData).addTo(map);
			map.fitBounds(geojsonData.getBounds());

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