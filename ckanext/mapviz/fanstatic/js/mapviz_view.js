/*
*
*
*/


ckan.module('mapvizview',function(jQuery,_) {

	return{
		options:{

		},
		initialize: function(){
      		console.log('Ive been called for element: %o', this.el);
			this.el.empty();
			this.el.append($("<div></div>").attr("id","map"))
		}

	}

});