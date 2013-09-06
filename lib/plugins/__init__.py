from exceptions import PluginException
import pprint
import importlib

def getPluginInstance(pluginName, settings, contentItem):
    """Pass the string name of a class to this and get back and instance of that class"""
    pluginNamespace = "lib.plugins.%s"%pluginName
    module = importlib.import_module(pluginNamespace)
    className = pluginName.encode('utf-8').capitalize()
    class_ = getattr(module, className)
    #Returns the instance, exceptions here should be caught higher up
    return class_(settings, contentItem)


def getFilterInstance(filterName, settings, contentItem):
    pass