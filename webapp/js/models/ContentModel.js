define([
  'underscore',
  'backbone'
], function(_, Backbone) {
  
  var ContentModel = Backbone.Model.extend({
  	url: "api/content"
  });

  return ContentModel;

});