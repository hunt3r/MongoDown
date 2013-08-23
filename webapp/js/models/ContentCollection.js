define([
  'underscore',
  'backbone',
  'models/ContentModel'
], function(_, Backbone, ContentModel) {
  
  var ContentCollection = Backbone.Collection.extend({
  	url: "api/content/",
  	model: ContentModel,
  });

  return ContentCollection;

});