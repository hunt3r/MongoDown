define([
  'jquery',
  'underscore',
  'backbone',
  'text!templates/homeView.tpl.html'
], function($, _, Backbone, homeTemplate){


  var ProjectsListView = Backbone.View.extend({
    el: $("#page"),
    
    render: function(){
      
      $('.menu li').removeClass('active');
      $('.menu li a[href="#projects"]').parent().addClass('active');
      this.$el.html(homeTemplate);

      // var sidebarView = new SidebarView();
      // sidebarView.render();
 
    }

  });

  return ProjectsListView;
  
});