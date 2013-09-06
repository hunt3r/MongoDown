"""Use this file to configure the content repository and how data is stored"""
development = { 
    "contentfolder": "../content", #Relative to the mongodown folder
    "content_md_extension": "*.markdown",
    "default_author": "Your name",
    "mongo": {
        "host": "localhost",
        "port" : 27017,
        "db" : "dev1",
        "collection": "content"
    },
    "parse": {
        "application_id" : "appid",
        "rest_api_key" : "",
        "master_key" : "",
        "rest_file_url" : "https://api.parse.com/1/files"
    },
    "plugins": ["gallery"], #Add plugins to this list to enable them
    "drop" : False, # If set to yes, all content will be deleted before creating
    "gallery" : {
        "src_path": "../content/galleries", #relative to the current folder
        "output_path": "../.gallery_cache",
        "regenerate_existing": True, #If this is set to true, images will be regenerated in cache
        "presets": [
            {"name": "thumb", "actions": [{"type": "fit", "height": 100, "width": 100, "from": (0.5, 0.5) }]},
            {"name": "slider", "actions": [{"type": "fit", "height": 300, "width": 1024, "from": (0.5, 0.5) }]},
            {"name": "large", "actions": [{"type": "resize", "height": 640, "width": 850, "from": (0.5, 0.5) }]},
        ],
    },
}

production = development

test = {
    "parse": {
        "application_id" : "your-app-key",
        "rest_api_key" : "api-key",
        "master_key" : "master-key",
        "rest_file_url" : "https://api.parse.com/1/files"
    },
    "gallery" : {
        "src_path": "test_data",
        "output_path": "test_data/output",
        "regenerate_existing": True,
        "presets": [
            {
                "name": "thumb_greyscale", 
                "actions": [
                    {"type": "fit", "height": 100, "width": 100, "from": (0.5, 0.5) },
                    {"type": "greyscale"}
                ]
            }
        ],
    }
}