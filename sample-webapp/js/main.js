
/**
 *logger
 */
window.log=function(){log.history=log.history||[];log.history.push(arguments);if(this.console){console.log(Array.prototype.slice.call(arguments))}};


require.config({
  paths: {
    jquery: 'lib/jquery-min',
    underscore: 'lib/underscore-amd-min',
    backbone: 'lib/backbone-amd-min',
    bootstrap: 'lib/bootstrap-min',
    parse: 'lib/parse-min',
    templates: '../templates',
    utils: 'utils',
    nprogress: 'lib/nprogress',
  }

});

require([
  // Load our app module and pass it to our definition function
  'app',
], function(App){
  // The "app" dependency is passed in as "App"
  // Again, the other dependencies passed in are not "AMD" therefore don't pass a parameter to this function
  App.initialize();
});