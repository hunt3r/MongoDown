define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/projects/projectList.tpl.html',
    'models/ContentCollection',
    'models/ContentItem'

], function($, _, Backbone, template, ContentCollection, ContentItem){

    var ProjectsListView = Backbone.View.extend({
        el: $("#page"),
        collection: new ContentCollection(),
        initialize: function() {
            var self = this;
            this.query = new Parse.Query(ContentItem);
            this.query.equalTo("type", "project")
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
                $('.menu li a[href="#projects"]').parent().addClass('active');
                var compiledTemplate = _.template( template, { projects: this.collection } );
                this.$el.html(compiledTemplate);
                // var sidebarView = new SidebarView();
                // sidebarView.render();

        }

    });

    return ProjectsListView;
    
});