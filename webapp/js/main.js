
require.config({
  paths: {
    jquery: 'lib/jquery-min',
    underscore: 'lib/underscore-amd-min',
    backbone: 'lib/backbone-amd-min',
    bootstrap: 'lib/bootstrap-min',
    parse: 'lib/parse-min',
    templates: '../templates',
    utils: 'utils',
    parse: 'lib/parse-min'
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