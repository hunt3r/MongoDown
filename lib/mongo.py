
from pymongo.connection import Connection
from pymongo import MongoClient

class MongoService(object):
	def __init__(self, config):
		self.config = config
		self.connection = Connection(config["mongo"]["host"], config["mongo"]["port"])
		self.db = self.connection[config["mongo"]["db"]]
		self.collection = self.db[config["mongo"]["collection"]]

	def upsertContent(self, contentObjects):
		
		if(self.config["drop"]):
			self.collection.drop()

		for obj in contentObjects:
			self.collection.insert(obj.__dict__)
			#print obj.__dict__
