from lib.models import Base, LogMixin
from datetime import datetime
import markdown, codecs, os, traceback, pykka
from lib import parse, utils, plugins
from dateutil import parser
from lib.models import ContentItem
from lib.gallery import Gallery
import pprint, sys
from lib.parse.service import ParseService 
from parse_rest.query import QueryResourceDoesNotExist
from lib.content_item_actor import ContentItemActor

class ContentQueue(Base, LogMixin):
    """ContentQueue is the main process that drives the conversion of markdown -> content objects"""

    def __init__(self, settings, args):
        #Load environment
        self.settings = settings
        self.contentFolder = getattr(args, "contentfolder", settings["contentfolder"])
        self.queueSize = getattr(args, "queuesize", settings["queue_size"])

        self.logger.info("--- Starting process on folder: %s" % self.contentFolder)
        self.touchfile = "%s%s%s" % (self.contentFolder, os.sep, ".mongodown")
        self.service = ParseService(self.settings)  

        self.files = []
        self.contentObjects = []

        self.setupQueue()

        #Create an item actor queue
        contentItemActors = [ContentItemActor.start(self.settings).proxy() for _ in range(self.queueSize)]

        # Distribute work to contentItemActors (not blocking)
        for i, filePath in enumerate(self.files):
            self.contentObjects.append(contentItemActors[i % len(contentItemActors)].parse(filePath))
        
        results = pykka.get_all(self.contentObjects)
        
        pykka.ActorRegistry.stop_all()

        self.complete()

    def setupQueue(self):
        self.files = utils.getFiles(self.contentFolder, self.settings["content_md_extension"])

        if not self.settings["drop"]:
            self.files = self.getContentDeltas(self.files)

        if len(self.files) == 0:
            self.logger.info("Nothing to do, no changes have been made. Start writing...")
            return

    def getContentDeltas(self, allFiles):
        """Gets all files that have changed since the last successful run of mongodown"""
        deltas = []
        try:
            for filepath in allFiles:
                if utils.getFileModifiedTime(filepath) > utils.getFileModifiedTime(self.touchfile):
                    deltas.append(filepath)
            return deltas
        except:
            # Typically this happens the first time through, with no touchfile
            return allFiles

    def cleanupRevisions(self):        
        """Removes any content from previous revision that might be left behind on the server"""
        for i in range(0, len(self.previousRevisions)):
            for metaKey in self.previousRevisions[i].meta.keys():
                if metaKey in self.settings["plugins"] and self.previousRevisions[i].meta[metaKey] != None:
                    self.logger.info("Removing %s content for plugin" % metaKey)
                    try:
                        plugin = plugins.getPluginInstance(metaKey, self.settings, self.previousRevisions[i])
                        if(hasattr(plugin, "cleanup")):
                            plugin.cleanup()
                    except:
                        self.logger.error("Plugin cleanup failed: %s " % metaKey)
                        traceback.print_exc(file=sys.stdout)

            self.previousRevisions[i].delete()

    def complete(self):
        """The last step run in the process"""
        utils.touch(self.touchfile)
        self.logger.info("--- Complete!")