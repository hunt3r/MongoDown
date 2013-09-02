#!/usr/bin/env python
from datetime import datetime
import markdown, codecs, argparse, os
from lib import parse, utils
import settings_local
from dateutil import parser
from lib.models import ContentItem
from lib.gallery import Gallery
import pprint, logging, sys
from lib.parse.service import ParseService 

#Argparse
argParser = argparse.ArgumentParser()
argParser.add_argument('--contentfolder', help='Path to your content folder', required=True)
args = argParser.parse_args()

#Load environment
settings = settings_local.development
touchfile = "%s%s%s" % (args.contentfolder, os.sep, ".mongodown")

#Markdown parser
md = markdown.Markdown(extensions = ['meta', 'codehilite(linenums=True)', 'footnotes'])
parseService = ParseService(settings)

def defaultKey(dict, key, defaultVal):
	if dict.has_key(key):
		return dict[key]
	return defaultVal

def createItemGallery(meta):
	if meta.has_key("gallery"):
		gallery = Gallery(settings, meta)
		gallery.generate()
		return {"photos" : gallery.photos,
				"name" : gallery.gallery_name}
	else:
		return None
	

def parseMDFile(filePath):
	"""Parse the MD File to a dictionary"""
	inputFile = codecs.open(filePath, mode="r", encoding="utf-8")
	text = inputFile.read()
	html = md.convert(text)
	meta = adaptMetaDataTypes(md.Meta)
	return ContentItem(
			# Can be used to promote certain items to the homepage
			homepage=defaultKey(meta, "homepage", False),
			# Filter by content "type"
			type=defaultKey(meta, "type", "item"),
			# Item title
			title=defaultKey(meta, "title", ""),
			# Used to filter by date on items
			created=parser.parse(defaultKey(meta, "created", str(datetime.now()))),
			# All Metadata as a map
			meta=meta, 
			# The HTML body
			html=html, 
			# Can be used for SEO style URLs if desired
			slug=utils.createSlug(meta),
			# A gallery to pull content from
			gallery=createItemGallery(meta),
			# Markdown file that generated this
			filePath=filePath,
			# Explicitly mark some items as unpublished
			published=defaultKey(meta, "published", True),
			#a list of tags
			tag=defaultKey(meta, "tag", [])
			)

def adaptMetaDataTypes(metaData):
	"""Adapts string values to a proper type"""
	# These types will not be flattened
	reservedArrayTypes = ["tag"]
	
	for key in metaData.keys():
		if type(metaData[key]) == list:
			for i in range(len(metaData[key])):
				if len(metaData[key]) == 1 and key not in reservedArrayTypes:
					metaData[key] = adaptValue(metaData[key][i])
					#flatten it if we have length 1
				else:
					metaData[key][i] = adaptValue(metaData[key][i])

	return metaData

def adaptValue(value):
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
	
def getContentDeltas(allFiles):
	deltas = []
	try:
		for file in allFiles:
			if utils.getFileModifiedTime(file) > utils.getFileModifiedTime(touchfile):
				deltas.append(file)
		return deltas
	except:
		return allFiles

def main():
	files = utils.getFiles(args.contentfolder, settings["content_md_extension"])

	if not settings["drop"]:
		files = getContentDeltas(files)

	if len(files) == 0:
		print "Nothing to do, no changes have been made. Start writing..."
		return

	contentObjects = []
	for file in files:
		try:
	 		contentObjects.append(parseMDFile(file))
	 	except:
	 		logging.error("Print error parsing file: %s" % file)
	 		logging.error(sys.exc_info()[0])

	parseService.upsertContent(contentObjects)

	utils.touch(touchfile)

# Go
if __name__ == "__main__":
    main()

