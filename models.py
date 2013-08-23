import json
from bson.objectid import ObjectId
class ContentItem(object):
	"""This is a standard piece of content that will be serialized for mongo"""
	def __init__(self, meta, html, filePath=None):
		self.meta = meta
		self.html = html 
		self.filePath = filePath
		
		self.id = None
		self.setId()

	def setId(self):
		if "id" not in self.meta:
			print "no id, creating a new one"
			self.id = ObjectId()
			