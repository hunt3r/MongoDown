// Filename: router.js
define([
    'jquery',
    'underscore',
    'backbone',
    'utils',
    'models/ContentItem',
    'views/HomeView',
    'views/projects/ProjectDetailView',
    'views/common/ListView',
], function($, _, Backbone, Utils, ContentItem, HomeView, ProjectDetailView, ListView) {

    var AppRouter = Backbone.Router.extend({
        
        routes: {
            // Define some URL routes
            'projects': 'Projects',
            'thoughts': 'Thoughts',
            "item/:id": "getItem",
            'home': 'Home',
            // Default
            '*actions': '404'
        }
    });
    
    var initialize = function(){

        var app_router = new AppRouter;

        /**
         * Global event for route change
         */
        app_router.on("route",function(route, router) {
            log(route);
            Utils.setTitle(route);
        });

        /**
         * Projects Page
         */
        app_router.on('route:Projects', function(){
     
                var query = new Parse.Query(ContentItem);
                query.equalTo("type", "project");
                var view = new ListView({"query": query});

        });
        
        /**
         * My thoughts blog
         */
        app_router.on('route:Thoughts', function(){
            var query = new Parse.Query(ContentItem);
            query.equalTo("type", "thought");
            var view = new ListView({"query": query});
        });
        
        /**
         * Item detail view
         */
        app_router.on('route:Item', function(id){
            var view = new DetailView({"id": id});
        });


        /**
         * Homepage
         */
        app_router.on('route:Home', function (actions) {
            // We have no matching route, lets display the home page 
            var query = new Parse.Query(ContentItem);
            query.equalTo("homepage", true);
            var view = new ListView({"query": query});
        });

        /**
         * 404 page
         */
        app_router.on('route:404', function (actions) {
            // We have no matching route, lets display the home page 
            var query = new Parse.Query(ContentItem);
            query.equalTo("homepage", true);
            var view = new ListView({"query": query});
        });

        // Unlike the above, we don't call render on this view as it will handle
        // the render call internally after it loads data. Further more we load it
        // outside of an on-route function to have it loaded no matter which page is
        // loaded initially.
        // var footerView = new FooterView();

        Backbone.history.start({pushState: true});
    };
    return { 
        initialize: initialize
    };
});