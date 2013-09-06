import pykka
from lib.models import Base, LogMixin
from datetime import datetime
import markdown, codecs, os, traceback, time
from lib import parse, utils, plugins
from dateutil import parser
from lib.models import ContentItem
from lib.gallery import Gallery
import pprint, sys
from lib.parse.service import ParseService 
from parse_rest.query import QueryResourceDoesNotExist

class ContentItemActor(pykka.ThreadingActor, LogMixin):
    def __init__(self, settings):
        super(ContentItemActor, self).__init__()
        self.settings = settings
        self.md = markdown.Markdown(extensions = ['meta', 'codehilite(linenums=True)', 'footnotes'])
        self.service = ParseService(self.settings)    
    
    def parse(self, filePath):
        self.filePath = filePath
        self.previousRevision = None
        
        self.stageContentItem()

        if self.previousRevision != None:
            self.cleanupOldRevision()

        self.decorateContentObjectsWithPlugins()
        self.currentRevision.save()

        return self.currentRevision

    def stageContentItem(self):
        try:
            self.previousRevision = self.service.getByFilePath(self.filePath)
            self.logger.info("Updating existing item to new revision: '%s'" % self.filePath)
            
        except QueryResourceDoesNotExist:
            self.logger.info("Creating new item: %s" % self.filePath)
        except:
            self.logger.error("General content staging error: %s" % sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)

        self.currentRevision = self.parseMarkdownFile(self.filePath)

    def cleanupOldRevision(self):        
        """Removes any content from previous revision that might be left behind on the server"""
        for metaKey in self.previousRevision.meta.keys():
            if metaKey in self.settings["plugins"] and self.previousRevision.meta[metaKey] != None:
                self.logger.info("Removing %s content for plugin" % metaKey)
                try:
                    plugin = plugins.getPluginInstance(metaKey, self.settings, self.previousRevision)
                    if(hasattr(plugin, "cleanup")):
                        plugin.cleanup()
                except:
                    self.logger.error("Plugin cleanup failed: %s " % metaKey)
                    traceback.print_exc(file=sys.stdout)

        self.previousRevision.delete()

    def decorateContentObjectsWithPlugins(self):
        """Adds a top level attribute to each content item for each plugin defined in settings"""
        for metaKey in self.currentRevision.meta.keys():
            if metaKey in self.settings["plugins"]:
                self.logger.info("Generating %s content" % (metaKey))
                try:
                    plugin = plugins.getPluginInstance(metaKey, self.settings, self.currentRevision)
                    setattr(self.currentRevision, metaKey, plugin.generate())
                except:
                    self.logger.error("Plugin failed: %s" % metaKey)
                    traceback.print_exc(file=sys.stdout)


    def parseMarkdownFile(self, filePath):
        """Parse the MD File to a dictionary"""
        inputFile = codecs.open(filePath, mode="r", encoding="utf-8")
        text = inputFile.read()
        html = self.md.convert(text)
        meta = self.adaptMetaDataTypes(self.md.Meta)
        return ContentItem(
                # Can be used to promote certain items to the homepage
                homepage=meta.get("homepage", False),
                # Filter by content "type"
                type=meta.get("type", "item"),
                # Item title
                title=meta.get("title", ""),
                # Used to filter by date on items
                created=parser.parse(meta.get("created", str(datetime.now()))),
                # All Metadata as a map
                meta=meta, 
                # The HTML body
                html=html, 
                # Can be used for SEO style URLs if desired
                slug=utils.createSlug(meta),
                # Markdown file that generated this
                filePath=filePath,
                # Explicitly mark some items as unpublished
                published=meta.get("published", True),
                #a list of tags
                tag=meta.get("tag", [])
                )

    def adaptMetaDataTypes(self, metaData):
        """Adapts string values to a proper type"""
        # These types will not be flattened
        reservedArrayTypes = ["tag"]
        
        for key in metaData.keys():
            if type(metaData[key]) == list:
                for i in range(len(metaData[key])):
                    if len(metaData[key]) == 1 and key not in reservedArrayTypes:
                        metaData[key] = self.adaptValue(metaData[key][i])
                        #flatten it if we have length 1
                    else:
                        metaData[key][i] = self.adaptValue(metaData[key][i])

        return metaData

    def adaptValue(self, value):
        """Process unicode to string and cast to the appropriate type before storing in parse"""
        value = value.encode('utf-8')
        if(type(value) == str):
            if value.lower() == "true":
                return True

            if value.lower() == "false":
                return False

            try:
                return int(value)
            except ValueError:
                #Just return the value as a string
                return value