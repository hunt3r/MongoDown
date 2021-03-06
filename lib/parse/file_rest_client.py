import requests
import exceptions
from lib.models import Base, LogMixin

class ParseFileRestClient(Base, LogMixin):
    
    def __init__(self, settings):
        self.settings = settings
        if not self.settings.has_key("parse"):
            raise ParseError("Missing parse api information")

    def post(self, filepath, filename):
        """Post a new file item to parse.com"""
        url = "%s/%s" % (self.settings["parse"]["rest_file_url"], filename)
        data = open(filepath, 'rb')
        headers = {
            'X-Parse-Application-Id': self.settings["parse"]["application_id"],
            'X-Parse-REST-API-Key': self.settings["parse"]["rest_api_key"],
            'content-type': "image/jpeg"
        }
        r = requests.post(url, data=data, headers=headers)
        return r.json()

    def delete(self, filename):
        """Delete a file from Parse.com"""
        url = "%s/%s" % (self.settings["parse"]["rest_file_url"], filename)

        headers = {
            'X-Parse-Application-Id': self.settings["parse"]["application_id"],
            'X-Parse-Master-Key': self.settings["parse"]["master_key"]
        }

        r = requests.delete(url, headers=headers)

        if r.status_code != 200:
            raise exceptions.ParseError("Delete failed: %s" % r.status_code)
    
