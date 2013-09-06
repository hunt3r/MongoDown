MongoDown
=========
The goal of this project is make an easy interface for people to write content in Markdown and push that content into an object store such as MongoDB, Parse.com, Cassandra, et al.  

Currently, the project works w/ Parse.com, but I'd like to make more adapters and service objects to abstract other data sources as well.

The idea is that you would use these object stores as an API to your content rather than generating static files.  This way you can create single page applications that load content via API.

## Installation

Install the following using pip into your virtualenv

```
pip install requests 
pip install git+https://github.com/dgrtwo/ParsePy.git
```

## Plugins

TODO: Explain plugin interface here

### Gallery

```
brew install pil
pip install PIL
```

- Add gallery to plugins list in your settings file


### Python
- https://github.com/lullis/parse_rest

##Sample webapp

I provide a sample web app, which is very rudimentary, but demonstrates the advantages to this approach over traditional static site generators.  Check out the router.js for an example of how to create adhoc queries and inflate your views.

### Javascript
- https://www.parse.com/docs/js_guide

#### PushState
- https://developer.mozilla.org/en-US/docs/Web/Guide/DOM/Manipulating_the_browser_history
- http://backbonejs.org/#History

