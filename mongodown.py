#!/usr/bin/env python

import markdown, codecs, argparse
from lib import mongo
import config
from models import ContentItem

#Argparse
parser = argparse.ArgumentParser()
parser.add_argument('--contentfolder', help='Path to your content folder', default="content")
args = parser.parse_args()

#Markdown parser
md = markdown.Markdown(extensions = ['meta'])
mongoService = mongo.MongoService(config.development)

def parseMDFile(filePath):
	"""Parse the MD File to a dictionary"""
	inputFile = codecs.open(filePath, mode="r", encoding="utf-8")
	text = inputFile.read()
	html = md.convert(text)
	meta = adaptMetaDataTypes(md.Meta)

	return ContentItem(meta,html,filePath)

def getFiles(contentFolder):
	"""Get the mardown files"""
	from os import listdir
	from os.path import isfile, join
	return [ "%s/%s"%(contentFolder, f) for f in listdir(contentFolder) if isfile(join(contentFolder,f)) ]

def adaptMetaDataTypes(metaData):
	"""Adapts string values to a proper type"""
	for key in metaData.keys():
		if type(metaData[key]) == list:
			for i in range(len(metaData[key])):
				metaData[key][i] = adaptValue(metaData[key][i])
		
	return metaData

def adaptValue(value):
	"""Process unicode to string and cast to the appropriate type before storing in mongo"""
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

	mongoService.upsertContent(contentObjects)


# Go
if __name__ == "__main__":
    main()

