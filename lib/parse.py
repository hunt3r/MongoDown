from parse_rest.connection import register
from parse_rest.connection import ParseBatcher
from models import ContentItem

class ParseService(object):
	def __init__(self, config):
		self.config = config
		register(self.config["parse"]["application_id"], self.config["parse"]["rest_api_key"])
	
	def upsertContent(self, contentObjects):
		batcher = ParseBatcher()

		# There is no truncate on parse, so we iterate and delete all...
		if(self.config["drop"]):
			print "Truncating content..."
			batcher.batch_delete(ContentItem.Query.all())
			print "Done."

		print "Batch creating all content now..."
		batcher.batch_save(contentObjects)