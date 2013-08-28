"""Use this file to configure the content repository and how data is stored"""

development = { 
	"content_path": "default-path-to-your-markdown",
	"repository" : "parse",
	"mongo": {
		"host": "localhost",
		"port" : 27017,
		"db" : "devMySite",
		"collection": "content"
	},
	"parse": {
		"application_id" : "your-app-key",
		"rest_api_key" : "your-rest-api-key",
		"master_key" : "your-master-key",
	},
	"drop" : True,
}

staging = development
production = development