"""This class is used for various little helpers"""
import urllib, re, os, datetime, fnmatch, inspect

def createSlug(meta):
    """Create a human readable slug string that can be used to generate more descriptive URLs"""
    returnVal = ""

    if meta.has_key("title"):
        returnVal = meta["title"]

    if meta.has_key("slug"):
        returnVal = meta["slug"]

    return urllib.quote(re.sub('[^A-Za-z0-9]+', '-', returnVal).lower())

def getFiles(basePath, extension):
    """Recursive file search function"""
    matches = []
    for root, dirnames, filenames in os.walk(basePath):
        for filename in fnmatch.filter(filenames, extension):
            matches.append(os.path.join(root, filename))
    return matches

def getFileModifiedTime(fileName):
    """Get the last modified date of a file"""
    t = os.path.getmtime(fileName)
    return datetime.datetime.fromtimestamp(t)

def touch(filePath):
    """basic touch implementation"""
    if os.path.exists(filePath):
        os.utime(filePath, None)
    else:
        open(filePath, 'w').close()
