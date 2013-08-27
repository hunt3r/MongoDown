define([
  'jquery',
  'nprogress',
  'underscore',
  'backbone',
  'text!templates/homeView.tpl.html'
], function($, NProgress, _, Backbone, homeTemplate){


  var ProjectsListView = Backbone.View.extend({
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
        },
        error: function(object, error) {

        }
      });
    }
    render: function(){
      var self = this;

      if(_.has(options, "model")) {
        self.model = options.model;
      }

      $('.menu li').removeClass('active');
      $('.menu li a[href="#projects"]').parent().addClass('active');
      this.$el.html(homeTemplate, { pageTitle: "test", item: self.model });
      NProgress.done();
    }

  });

  return ProjectsListView;
  
});