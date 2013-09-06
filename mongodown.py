#!/usr/bin/env python
import argparse
from lib import content_queue
import settings_local
from datetime import datetime
#Argparse
argParser = argparse.ArgumentParser()
argParser.add_argument('--contentfolder', help='Path to your content folder')
args = argParser.parse_args()

#Load environment
settings = settings_local.production

def main():
    content_queue.ContentQueue(settings, getattr(args, "contentfolder", None))

# Go
if __name__ == "__main__":
    startTime = datetime.now()
    main()
    totalTime = datetime.now() - startTime
    print "Script execution time %s" % totalTime.total_seconds()
