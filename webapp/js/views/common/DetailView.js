define([
  'jquery',
  'nprogress',
  'underscore',
  'backbone',
  'models/ContentItem',
  'text!templates/common/detail.tpl.html'
], function($, NProgress, _, Backbone, ContentItem, template){


  var DetailView = Backbone.View.extend({
    el: $("#page"),
    query: new Parse.Query(ContentItem),
    initialize: function(options) {
      NProgress.start();
      var self = this;

      if(_.has(options, "id")) {
        this.id = options.id;
      }

      this.query.get(this.id, {
        success: function(model) {
          self.model = model;
          self.render();
        },
        error: function(object, error) {
          NProgress.done();
        }
      });
    },
    render: function(){
      var self = this;

      var compiledTemplate = _.template(template, {"item": self.model });
      this.$el.html(compiledTemplate);
      NProgress.done();
    }

  });

  return DetailView;
  
});