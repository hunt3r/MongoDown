define(['jquery',
        'underscore',
        'backbone',
        'nprogress',
        'text!templates/common/list.tpl.html',
        'models/ContentCollection',
        'models/ContentItem'], 
        function($, _, Backbone, NProgress, template, ContentCollection, ContentItem){


    var ListView = Backbone.View.extend({
        el: $("#page"),
        collection: null,
        progressBar: NProgress,
        query: new Parse.Query(ContentItem),
        initialize: function(options) {
            var self = this;
            NProgress.start();
            if(_.has(options, "query")) {
                this.query = options.query;
            }

            this.query.descending("created");

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
            var compiledTemplate = _.template( template, { items: this.collection } );
            this.$el.html(compiledTemplate);
            NProgress.done();
        }

    });

    return ListView;
        
});