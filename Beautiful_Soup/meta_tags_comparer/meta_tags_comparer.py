#!/usr/bin/env python3

# The program for parsing meta tag`s data from some urls (from file given as parameter (argv))
# and comparing it with prepared data (from 'meta' module)

# Parsed data are collected in list of dictionaries as well as prepared data, then compared.

import sys
from bs4 import BeautifulSoup
import urllib.request
import meta

if len(sys.argv) > 1:
	files = sys.argv[1:]
else:
	files = [sys.stdin]

# open file if exists, otherwise read from stdin

for filepath in files:
	if isinstance(filepath, str):
		file = open(filepath)
	else:
		file = filepath

# Parse data and form list of dictionaries

items = []
for url in file:
	url = url.strip()
	sauce = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(sauce, 'html.parser')
	items.append({
		'url': url,
		'title': soup.title.string,
		'description': soup.find(attrs={"name":"description"})['content']
	})

# Compare parsed data with prepared and print result

for x in range(len(items)):
	print("\n" + items[x]['url'])
	print("URL: OK" if items[x]['url'] == meta.mt[x]['url'] else 
		"URL: NO\nPrepared url is: " + meta.mt[x]['url'])
	print("Title: OK" if items[x]['title'] == meta.mt[x]['title'] else
		"Title: NO\nParsed title is:\n" + items[x]['title'] +
		"\nPrepared title is:\n" + meta.mt[x]['title'])
	print("Description: OK" if items[x]['description'] == meta.mt[x]['description'] else
		"Description: NO\nParsed description is:\n" + items[x]['description'] +
		"\nPrepared description is:\n" + meta.mt[x]['description'])

if isinstance(filepath, str):
	file.close()

