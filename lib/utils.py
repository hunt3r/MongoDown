"""This class is used for various little helpers"""
import urllib, re

def createSlug(meta):
	"""Create a human readable slug string that can be used to generate more descriptive URLs"""
	returnVal = ""

	if meta.has_key("title"):
		returnVal = meta["title"]

	if meta.has_key("slug"):
		returnVal = meta["slug"]

	return urllib.quote(re.sub('[^A-Za-z0-9]+', '-', returnVal).lower())