from parse_rest.connection import register
from parse_rest.connection import ParseBatcher
from parse_rest.query import QueryResourceDoesNotExist
from lib.models import ContentItem
import pprint


class ParseService(object):

    def __init__(self, settings):
        self.settings = settings
        self.fileRestClient = ParseFileRestClient(settings)
        self.galleryService = GalleryService(settings)

        register(self.settings["parse"]["application_id"], self.settings["parse"]["rest_api_key"])
        self.batcher = ParseBatcher()

    def getByFilePath(self, filePath):
        return ContentItem.Query.get(filePath=filePath)

    def post(self, item):
        return item.save()

    # def upsertContent(self, contentObjects):

    #     self.setup()
        
    #     for item in contentObjects:
    #         try:
    #             oldItem = ContentItem.Query.get(filePath=item.filePath)
    #             print "Updating item: '%s'" % oldItem.filePath
                
    #             if(oldItem.gallery != None):
    #                 print "has gallery"
    #                 self.galleryService.cleanupOldPhotos(oldItem.gallery["photos"])

    #             oldItem.delete()
    #             item.save()

    #         except QueryResourceDoesNotExist:
    #             print "Creating new item: '%s'" % item.filePath 
    #             item.save()
                
    def setup(self):
        # There is no truncate on parse, so we iterate and delete all...
        if(self.settings["drop"]):
            items = ContentItem.Query.all()
            print "Truncating items... %s" % items.count()
            if items.count() > 0:
                self.batcher.batch_delete(items)
            print "Done."
