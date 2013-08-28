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
                    log(error);
                }
            });
        },
        render: function(){
            var compiledTemplate = _.template( template, { projects: this.collection } );
            this.$el.html(compiledTemplate);
        }

    });

    return ProjectsListView;
        
});