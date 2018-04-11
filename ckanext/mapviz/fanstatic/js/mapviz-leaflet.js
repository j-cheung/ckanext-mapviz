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
			var map = L.map('map').setView([51.505, -0.09], 0);
			// L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
			//     attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
			//     maxZoom: 18,
			//     id: 'mapbox.dark',
			//     accessToken: 'pk.eyJ1IjoiamNoZXVuZyIsImEiOiJjajh0M2FwMncwZ290MnFxdTY3enB6cXlnIn0.e26zB-gpmMOt6SjHbJ68vg'
			// }).addTo(map);

			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				maxZoom: 19,
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
			}).addTo(map);

			var resource_format = this.options.resource_format
			//if osm
			if(resource_format == 'osm'){
				console.log("osm")
				if(this.options.hbase_osm){
					console.log("osm hbase")
					// var parser = new DOMParser();
					var doc = new DOMParser().parseFromString(this.options.hbase_osm, "application/xml");
					console.log(doc)
					self.plotOSM(map,doc)
				}
				else{
					console.log("no hbase")
					jQuery.get(this.options.proxy_resource_url)
					.done(
						function(data){
							console.log(data)
							var parser = new DOMParser();
							var doc = parser.parseFromString(data, "application/xml");
							console.log(doc)
							self.plotOSM(map,doc)
						})
					.fail(
						function(jqXHR, textStatus, errorThrown) {
							console.log("fail")
							console.log(errorThrown)
						}
					);
				}
				
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

		createPopUp: function(feature) {
			var html = '<div class="popup_content">';

			if(feature.hasOwnProperty('type')){
				if(feature.type == "node"){
					html += '<table class="node_popup_table">'
					if(feature.hasOwnProperty('id')){
						// html += '<h2 class="node_id"> id: ' + feature.id + '</h2>'
						html += '<tr>' + '<td>id</td>' + '<td>' + feature.id + '</td>' + '</tr>'
					};
					if(feature.hasOwnProperty('latLng')){
						// html += '<h2 class="node_lat"> lat: ' + feature.latLng.lat + '</h2>'
						// html += '<h2 class="node_lon"> lon: ' + feature.latLng.lng + '</h2>'
						html += '<tr>' + '<td>Latitude</td>' + '<td>' + feature.latLng.lat + '</td>' + '</tr>'
						html += '<tr>' + '<td>Longitude</td>' + '<td>' + feature.latLng.lng + '</td>' + '</tr>'
					};
					if(feature.hasOwnProperty('tags')){
						Object.keys(feature.tags).forEach(function(key){
							// html += '<h2 class="node_tag">' + ' ' + key + ': ' + feature.tags[key] + '</h2>'
							html += '<tr>' + '<td>' + key + '</td>' + '<td>' + feature.tags[key] + '</td>' + '</tr>'
						});
					};
					html += '</table>'
				};
			};

			return html			
		},

		plotOSM: function(map, osmData) {
			var self = this;
			var osmNodeStyle = {
			    "radius": 5,
			    "fillColor": "#ff7800",
			    "color": "#ff7800",
			    "weight": 1,
			    "opacity": 1,
			    "fillOpacity": 0.5
			}

			var osmWayAreaStyle = {		
			    "color": "#ff7800",
			    "weight": 5,
			    "opacity": 0.65
			}

			var osmLayer = new L.OSM.DataLayer(osmData,{
		        styles : {
		        	node: osmNodeStyle,
			        way: osmWayAreaStyle,
			        area: osmWayAreaStyle
		        }
	        }).addTo(map);
			map.fitBounds(osmLayer.getBounds());

			map.eachLayer(function(layer){
				var feature = layer.feature
				if(feature){
			    	layer.bindPopup(self.createPopUp(feature));
				}
			});
		},

		plotGeoJSON: function(map, geojsonData) {

			//styling
			var geojsonMarkerOptions = {
			    "radius": 5,
			    "fillColor": "#ff7800",
			    "color": "#ff7800",
			    "weight": 1,
			    "opacity": 1,
			    "fillOpacity": 0.5
			};

			var geojsonLinePolyStyle = {		
			    "color": "#ff7800",
			    "weight": 5,
			    "opacity": 0.65
			};

			//apply styling, add to map
			var gjLayer = L.geoJSON(geojsonData, {
			    pointToLayer: function (feature, latlng) {
			        return L.circleMarker(latlng, geojsonMarkerOptions);
			    },
			    style : geojsonLinePolyStyle
			}).addTo(map);
			map.fitBounds(gjLayer.getBounds());
			
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