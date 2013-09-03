from lib.models import Base, LogMixin
from datetime import datetime
import markdown, codecs, os, traceback
from lib import parse, utils, plugins
from dateutil import parser
from lib.models import ContentItem
from lib.gallery import Gallery
import pprint, sys
from lib.parse.service import ParseService 
from parse_rest.query import QueryResourceDoesNotExist

class ContentParser(Base, LogMixin):
    """ContentParser is the main process that drives the conversion of markdown -> content objects"""

    def __init__(self, settings, args):
        #Load environment
        self.settings = settings
        self.contentFolder = getattr(args, "contentfolder", settings["contentfolder"])
        self.logger.info("--- Starting process on folder: %s" % self.contentFolder)
        self.contentItems = []
        self.previousRevisions = [] 
        self.touchfile = "%s%s%s" % (self.contentFolder, os.sep, ".mongodown")
        self.md = markdown.Markdown(extensions = ['meta', 'codehilite(linenums=True)', 'footnotes'])
        self.service = ParseService(self.settings)

        # Main process steps
        self.setup()
        self.cleanupRevisions()
        self.decorateContentObjectsWithPlugins()
        self.persist()
        self.complete()

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
        self.logger.info("Starting cleanup of old revisions")
        for i in range(0, len(self.previousRevisions)):
            for metaKey in self.previousRevisions[i].meta.keys():
                if metaKey in self.settings["plugins"]:
                    self.logger.info("Removing %s content for plugin" % metaKey)
                    try:
                        plugin = plugins.getPluginInstance(metaKey, self.settings, self.previousRevisions[i])
                        if(hasattr(plugin, "cleanup")):
                            plugin.cleanup()
                    except:
                        self.logger.error("Plugin cleanup failed: %s " % metaKey)
                        traceback.print_exc(file=sys.stdout)
            
            self.previousRevisions[i].delete()

    def decorateContentObjectsWithPlugins(self):
        """Adds a top level attribute to each content item for each plugin defined in settings"""
        for i in range(0, len(self.contentItems)):
            for metaKey in self.contentItems[i].meta.keys():
                if metaKey in self.settings["plugins"]:
                    self.logger.info("Generating %s content" % (metaKey))
                    try:
                        plugin = plugins.getPluginInstance(metaKey, self.settings, self.contentItems[i])
                        setattr(self.contentItems[i], metaKey, plugin.generate())
                    except:
                        self.logger.error("Plugin failed: %s" % metaKey)
                        traceback.print_exc(file=sys.stdout)

    def stageContentItem(self, filePath):
        """Stages old file for deletion and creates an instance of a new ContentItem to be saved"""
        try:
            oldItem = self.service.getByFilePath(filePath)
            self.logger.info("Updating existing item to new revision: '%s'" % filePath)
            self.previousRevisions.append(oldItem)
        except QueryResourceDoesNotExist:
            self.logger.debug("Creating new item: %s" % filePath)
        except:
            self.logger.error("General content staging error: %s" % sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)

        self.contentItems.append(self.parseMarkdownFile(filePath))

    def persist(self):
        """Iterate over the decorated content items and save each one"""
        for item in self.contentItems:
            item.save()

    def setup(self):
        """Sets up the processor with the correct state and collection of raw content items"""
        files = utils.getFiles(self.contentFolder, self.settings["content_md_extension"])

        if self.settings["drop"]:
            self.service.drop()
        else:
            files = self.getContentDeltas(files)

        if len(files) == 0:
            self.logger.info("Nothing to do, no changes have been made. Start writing...")
            return

        for filePath in files:
            self.stageContentItem(filePath)


    def complete(self):
        utils.touch(self.touchfile)
        self.logger.info("--- Complete!")