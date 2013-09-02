import json, logging
from parse_rest.datatypes import Object

class ContentItem(Object):
    """This is a standard piece of content that will be serialized for parse.com"""
    pass
            
class Base(object):
    def __init__(self):
        pass

class LogMixin(object):
    @property
    def logger(self):
        #name = '.'.join([__name__, self.__class__.__name__])
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler('output.log')
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger
