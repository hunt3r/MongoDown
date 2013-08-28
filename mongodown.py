#!/usr/bin/env python
from datetime import datetime
import markdown, codecs, argparse
from lib import parse, utils
import settings_local
from dateutil import parser
from lib.models import ContentItem

#Argparse
argParser = argparse.ArgumentParser()
argParser.add_argument('--contentfolder', help='Path to your content folder', required=True)
args = argParser.parse_args()

#Markdown parser
md = markdown.Markdown(extensions = ['meta'])
parseService = parse.ParseService(settings_local.development)

def defaultKey(dict, key, defaultVal):
	if dict.has_key(key):
		return dict[key]
	return defaultVal

def parseMDFile(filePath):
	"""Parse the MD File to a dictionary"""
	inputFile = codecs.open(filePath, mode="r", encoding="utf-8")
	print filePath
	text = inputFile.read()
	html = md.convert(text)
	meta = adaptMetaDataTypes(md.Meta)

	return ContentItem(homepage=defaultKey(meta, "homepage", False), 
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
						# Markdown that generated this
						filePath=filePath)

def getFiles(contentFolder):
	"""Get the mardown files"""
	from os import listdir
	from os.path import isfile, join
	return [ "%s/%s"%(contentFolder, f) for f in listdir(contentFolder) if isfile(join(contentFolder,f)) and f.endswith("md") or f.endswith("markdown") ]

def adaptMetaDataTypes(metaData):
	"""Adapts string values to a proper type"""
	for key in metaData.keys():
		if type(metaData[key]) == list:
			for i in range(len(metaData[key])):
				if len(metaData[key]) == 1:
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
	


def main():

	mdFiles = getFiles(args.contentfolder)
	
	contentObjects = []
	for file in mdFiles:
	 	contentObjects.append(parseMDFile(file))

	parseService.upsertContent(contentObjects)


# Go
if __name__ == "__main__":
    main()

