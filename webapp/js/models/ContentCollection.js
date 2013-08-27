define([
  'underscore',
  'backbone',
  'models/ContentItem',
], function(_, Backbone, ContentItem) {

    var ContentCollection =  Parse.Collection.extend({
        model: ContentItem
    })

  return ContentCollection;

});