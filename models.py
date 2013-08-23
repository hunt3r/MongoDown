

class ContentItem(object):
	"""This is a standard piece of content that will be serialized for mongo"""
	def __init__(self, meta, html):
		self.meta = meta 
		self.html = html 
