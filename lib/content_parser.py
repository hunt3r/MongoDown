from lib.models import Base, LogMixin
from datetime import datetime
import markdown, codecs, os
from lib import parse, utils
from dateutil import parser
from lib.models import ContentItem
from lib.gallery import Gallery
import pprint, sys
from lib.parse.service import ParseService 

class ContentParser(Base, LogMixin):

    def __init__(self, settings, args):
        #Load environment
        self.settings = settings
        self.contentFolder = getattr(args, "contentfolder", settings["contentfolder"])
        self.logger.info("Starting process on folder: %s" % self.contentFolder)

        self.touchfile = "%s%s%s" % (self.contentFolder, os.sep, ".mongodown")

        #Markdown parser
        self.md = markdown.Markdown(extensions = ['meta', 'codehilite(linenums=True)', 'footnotes'])
        self.parseService = ParseService(self.settings)
        
    def createItemGallery(self, meta):
        if meta.has_key("gallery"):
            gallery = Gallery(self.settings, meta)
            gallery.generate()
            return {"photos" : gallery.photos,
                    "name" : gallery.gallery_name}
        else:
            return None
        

    def parseMDFile(self, filePath):
        """Parse the MD File to a dictionary"""
        inputFile = codecs.open(filePath, mode="r", encoding="utf-8")
        text = inputFile.read()
        html = self.md.convert(text)
        meta = self.adaptMetaDataTypes(self.md.Meta)
        return ContentItem(
                # Can be used to promote certain items to the homepage
                homepage=getattr(meta, "homepage", False),
                # Filter by content "type"
                type=getattr(meta, "type", "item"),
                # Item title
                title=getattr(meta, "title", ""),
                # Used to filter by date on items
                created=parser.parse(getattr(meta, "created", str(datetime.now()))),
                # All Metadata as a map
                meta=meta, 
                # The HTML body
                html=html, 
                # Can be used for SEO style URLs if desired
                slug=utils.createSlug(meta),
                # A gallery to pull content from
                gallery=self.createItemGallery(meta),
                # Markdown file that generated this
                filePath=filePath,
                # Explicitly mark some items as unpublished
                published=getattr(meta, "published", True),
                #a list of tags
                tag=getattr(meta, "tag", [])
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
        deltas = []
        try:
            for file in allFiles:
                if utils.getFileModifiedTime(file) > utils.getFileModifiedTime(self.touchfile):
                    deltas.append(file)
            return deltas
        except:
            return allFiles

    def generate(self):
        files = utils.getFiles(self.contentFolder, self.settings["content_md_extension"])

        if not self.settings["drop"]:
            files = self.getContentDeltas(files)

        if len(files) == 0:
            self.logger.info("Nothing to do, no changes have been made. Start writing...")
            return

        contentObjects = []
        for file in files:
            try:
                contentObjects.append(self.parseMDFile(file))
            except:
                self.logger.error("Print error parsing file: %s" % file)
                self.logger.error(sys.exc_info()[0])

        self.parseService.upsertContent(contentObjects)

        utils.touch(self.touchfile)