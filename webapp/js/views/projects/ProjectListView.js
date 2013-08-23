define([
  'jquery',
  'underscore',
  'backbone',
  'text!templates/projects/projectList.tpl.html',
  'models/ContentCollection'

], function($, _, Backbone, template, ContentCollection){


  var ProjectsListView = Backbone.View.extend({
    el: $("#page"),
    collection: new ContentCollection(),
    initialize: function() {
        var self = this;
        this.collection.fetch({ 
            success: function(data, xhr) {
                this.collection.set(xhr.rows);
                self.render();
            }
        });
    },
    render: function(){

        $('.menu li').removeClass('active');
        $('.menu li a[href="#projects"]').parent().addClass('active');
        this.$el.html(template);
        // var sidebarView = new SidebarView();
        // sidebarView.render();

    }

  });

  return ProjectsListView;
  
});