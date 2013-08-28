from parse_rest.connection import register
from parse_rest.connection import ParseBatcher
from models import ContentItem

class ParseService(object):
	def __init__(self, config):
		self.config = config
		register(self.config["parse"]["application_id"], self.config["parse"]["rest_api_key"])
		self.batcher = ParseBatcher()

	def upsertContent(self, contentObjects):
		
		self.setup()

		print "Batch creating all content now... %s items" % len(contentObjects)
		self.batcher.batch_save(contentObjects)

	def setup(self):

		# There is no truncate on parse, so we iterate and delete all...
		if(self.config["drop"]):
			items = ContentItem.Query.all()
			#print dir(items)
			print "Truncating items... %s" % items.count()
			if items.count() > 0:
				self.batcher.batch_delete(items)
			print "Done."