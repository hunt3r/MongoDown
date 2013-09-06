define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/homeView.tpl.html',
    'models/ContentItem'
], function($, _, Backbone, homeTemplate, ContentItem){

    var HomeView = Backbone.View.extend({
        el: $("#page"),
        initialize: function() {
            var self = this;
            this.query = new Parse.Query(ContentItem);
            this.query.equalTo('homepage', true)
            this.query.find({
              success: function(results) {
                self.collection = results;
                self.render();
              }, 
              error: function(error) {
                // error is an instance of Parse.Error.
              }
            });

        },
        render: function(){
            
            $('.menu li').removeClass('active');
            $('.menu li a[href="#"]').parent().addClass('active');
            var compiledTemplate = _.template( homeTemplate, { projects: this.collection } );
            this.$el.html(compiledTemplate);
            // var sidebarView = new SidebarView();
            // sidebarView.render();
 
        }

    });

    return HomeView;
    
});