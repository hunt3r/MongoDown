from parse_rest.connection import register
from parse_rest.connection import ParseBatcher
from parse_rest.query import QueryResourceDoesNotExist
from file_rest_client import ParseFileRestClient
from lib.gallery import GalleryService
from lib.models import ContentItem, Base, LogMixin

class ParseService(Base, LogMixin):

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

    def drop(self):
        # There is no truncate on parse, so we iterate and delete all...
        if(self.settings["drop"]):
            items = ContentItem.Query.all()
            #self.logger.info(dir(items)
            self.logger.info("Truncating items... %s" % items.count())
            if items.count() > 0:
                self.batcher.batch_delete(items)
            self.logger.info("Done.")
