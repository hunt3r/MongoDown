#!/usr/bin/env python
import argparse
from lib import content_parser
import settings_local

#Argparse
argParser = argparse.ArgumentParser()
argParser.add_argument('--contentfolder', help='Path to your content folder')
args = argParser.parse_args()

#Load environment
settings = settings_local.development

def main():
	content_parser.ContentParser(settings, getattr(args, "contentfolder", None))

# Go
if __name__ == "__main__":
    main()

