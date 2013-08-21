#!/usr/bin/env python
import markdown, codecs

md = markdown.Markdown(extensions = ['meta'])

input_file = codecs.open("content/test.md", mode="r", encoding="utf-8")
text = input_file.read()
html = md.convert(text)

obj = {"html" : html,
		"meta" : md.Meta}

print obj
