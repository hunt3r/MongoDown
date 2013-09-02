import json, logging
from parse_rest.datatypes import Object
import logging.config
class ContentItem(Object):
    """This is a standard piece of content that will be serialized for parse.com"""
    pass
            
class Base(object):
    def __init__(self):
        pass

class LogMixin(object):
    @property
    def logger(self):
        logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
        logger = logging.getLogger(self.__class__.__name__)
        return logger
