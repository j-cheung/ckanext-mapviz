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
      		this.map.append($("<div>HELLOOOOOOO</div>"));
		}
	};
});