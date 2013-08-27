define(['jquery',
        'underscore',
        'backbone'], 
        function($, _, Backbone) {

    var $document = $(document);

    return {
    	setTitle: function(title) {
            var baseTitle = $document.attr('title');
            $document.attr('title', baseTitle + " - " + title);
    	}
    }

});