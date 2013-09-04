import logging, json, os, sys, time, Image, requests
from PIL import ImageOps
from lib.parse.file_rest_client import ParseFileRestClient
import logging
from lib.models import Base, LogMixin

"""
Python Gallery

The aim of this code is to make a gallery object which contains a collection of
image objects that represet an image on a server, these collections generally contain multiple image
sizes / prefixes for a given src image.  This will help you with assets that need to be cropped / resized
for different areas of your layout.

"""

class Photo():

    """ Class to represent a Photo, also handles applying presets to itself"""
    def __init__(self, filename, settings, absolute_src_path, output_path, preset):
        self.regenerate = settings["regenerate_existing"]
        self.filename = filename
        self.input_file = "%s%s%s" % (absolute_src_path, os.sep, self.filename)
        self.output_path = output_path
        self.output_file = "%s%s%s" % (output_path, os.sep, self.filename)
        self.preset = preset

        image = Image.open(self.input_file)
        self.process_image(image)
        image = Image.open(self.output_file)

        self.width, self.height = image.size
        self.url = None
        self.parseName = None

    def process_image(self, image):
        """Responsible for applying presets to the Image obj"""
        if not os.path.isfile(self.output_file) or self.regenerate:
            
            # Actions should be processed in order of appearance in actions array
            for i in range(len(self.preset["actions"])):
                a = self.preset["actions"][i]

                if a["type"] == "fit":
                    if not "from" in a:
                        a["from"] = (0.5, 0.5) # crop from middle by default

                    image = ImageOps.fit(image, (a["width"], a["height"],), method=Image.ANTIALIAS, centering=a["from"])
                
                if a["type"] == "greyscale":
                    image = ImageOps.grayscale(image)

                if a["type"] == "resize":
                    image.thumbnail((a["width"], a["height"]), Image.NEAREST)
                
                # TODO: Write other useful transforms here!
            
            image.save(self.output_file)

class Gallery(Base, LogMixin):
    """Represents a Gallery plugin"""
    def __init__(self, settings, contentItem):
        self.contentItem = contentItem
        self.meta = contentItem.meta
        self.settings = settings
        self.gallery_settings = settings["gallery"]
        self.gallery_name = None
        self.photos = []
        self.absolute_src_path = None
        self.absolute_output_path = None
        self.preset_dir = []
        self.service = GalleryService(settings, self.meta)

        if "gallery" in self.meta:
            self.gallery_name = self.meta["gallery"]
            self.absolute_src_path =  "%s%s%s" % (self.gallery_settings["src_path"], 
                                                    os.sep, 
                                                    self.gallery_name)

            self.absolute_output_path = "%s%s%s" % (self.gallery_settings["output_path"], 
                                                    os.sep,
                                                    self.gallery_name)


    def generate(self):
        self.create_preset_folders() 
        self.create_preset_images()
        self.photos = self.service.uploadFiles(self.photos)
        return {"photos" : self.photos, "name" : self.gallery_name}

    def create_preset_images(self):
        """Creates the image assets for each preset and returns a PhotoSet object"""
        for f in self.get_files_from_data():
            photoSets = {}
            for preset in self.gallery_settings["presets"]:
                preset_dir = "%s%s%s" % (self.absolute_output_path,
                                         os.sep, 
                                         preset["name"])
                photoSets[preset["name"]] = Photo(f, self.gallery_settings, self.absolute_src_path, preset_dir, preset).__dict__
                
            self.photos.append(photoSets)
            
    def create_preset_folders(self):
        """Creates the folder structure for a gallery"""

        if not os.path.exists(self.absolute_output_path):
            os.makedirs(self.absolute_output_path)

        # Create gallery preset folders for this gallery
        if "presets" in self.gallery_settings:
            for preset in self.gallery_settings["presets"]:
                preset_dir = "%s%s%s" % (self.absolute_output_path, 
                                        os.sep,
                                        preset["name"])
                self.preset_dir.append(preset_dir)
                if not os.path.exists(preset_dir):
                    os.makedirs(preset_dir)
        else:
            self.logger.error("You have no presets defined, please add gallery_presets array to settings file, with at least one preset defined, see docs.")
    
    def cleanup(self,):
        """Used to cleanup old content items when there are updates, old photos will
            be removed"""
        self.logger.info("Cleaning up old photos")
        self.service.cleanupOldPhotos(self.contentItem.gallery["photos"])

    def get_files_from_data(self):
        from os import listdir
        from os.path import isfile, join
        return [ f for f in listdir(self.absolute_src_path) if isfile(join(self.absolute_src_path,f)) and f != ".DS_Store" ]

class GalleryService(Base, LogMixin):
    """Gallery plugin service functions"""
    def __init__(self, settings, contentItem=None):
        self.settings = settings
        self.client = ParseFileRestClient(settings)

    def uploadFiles(self, photos):
        """Upload all the photos from this gallery to server, and adapt each photo w/ response that includes URL"""
        logging.info("uploading files to parse")
        adapted = []
        for photoSets in photos:
            for key in photoSets.keys():
                self.logger.info("Uploading file: %s" % photoSets[key]["output_file"])
                response = self.client.post(photoSets[key]["output_file"], photoSets[key]["filename"])
                if response.has_key("url"):
                    photoSets[key]["parseName"] = response["name"]
                    photoSets[key]["url"] = response["url"]
            adapted.append(photoSets)

        return adapted

    def cleanupOldPhotos(self, photos):
        """Deletes all the photos from an old revision"""
        for photoset in photos:
            for key in photoset.keys():
                photo = photoset[key]
                if photo.has_key("parseName"):
                    self.logger.info("Deleting old file: %s" % photo["parseName"])
                    try:
                        self.client.delete(photo["parseName"])
                    except ParseError:
                        self.logger.error("Could not delete file: %s" % photo["parseName"])

