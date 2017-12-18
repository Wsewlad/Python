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

for filepath in files:
	if isinstance(filepath, str):
		file = open(filepath)
	else:
		file = filepath

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
	
for x in range(len(items)):
	print(items[x]['url'])
	print('OK' if items[x] == meta.mt[x] else 'NO')

if isinstance(filepath, str):
	file.close()

