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

    def upsertContent(self, contentContentItems):

        self.setup()
        
        for item in contentContentItems:
            try:
                oldItem = ContentItem.Query.get(filePath=item.filePath)
                self.logger.info("Found existing file item: '%s'" % oldItem.filePath)
                
                if(oldItem.gallery != None):
                    self.logger.info("Deleting old gallery files...")
                    self.galleryService.cleanupOldPhotos(oldItem.gallery["photos"])

                oldItem.delete()

                item.save()

            except QueryResourceDoesNotExist:
                self.logger.info("Creating new item: '%s'" % item.filePath)
                item.save()
                
    def setup(self):
        # There is no truncate on parse, so we iterate and delete all...
        if(self.settings["drop"]):
            items = ContentItem.Query.all()
            #self.logger.info(dir(items)
            self.logger.info("Truncating items... %s" % items.count())
            if items.count() > 0:
                self.batcher.batch_delete(items)
            self.logger.info("Done.")
