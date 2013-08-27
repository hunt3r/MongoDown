from parse_rest.connection import register
from parse_rest.connection import ParseBatcher


class ParseService(object):
	def __init__(self, config):
		self.config = config
		register(self.config["parse"]["application_id"], self.config["parse"]["rest_api_key"])
		
		# self.connection = Connection(config["Parse"]["host"], config["mongo"]["port"])
		# self.db = self.connection[config["mongo"]["db"]]
		# self.collection = self.db[config["mongo"]["collection"]]

	def upsertContent(self, contentObjects):
		
		# if(self.config["drop"]):
		# 	self.collection.drop()

		batcher = ParseBatcher()
		batcher.batch_save(contentObjects)