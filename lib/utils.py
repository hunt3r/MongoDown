"""This class is used for various little helpers"""
import urllib

def createSlug(meta):
	"""Create a human readable slug string that can be used to generate more descriptive URLs"""
	returnVal = ""

	if meta.has_key("title"):
		returnVal = meta["title"].replace(" ", "-")

	if meta.has_key("slug"):
		returnVal = meta["slug"].replace(" ", "-")

	return urllib.quote(returnVal).lower()