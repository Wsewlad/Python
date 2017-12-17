#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
import urllib.request
import csv
from itertools import product
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
i = 0;
for url in file:
	url = url.strip()
	sauce = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(sauce, 'html.parser')
	items.append({
		'url': url,
		'title': soup.title.string,
		'description': soup.find(attrs={"name":"description"})['content']})
	i = i + 1
for x in items: print(x)

# file_meta =  open('meta.txt', 'r', encoding='utf-8')
# prepared_meta_tags = file_meta.read()

print(meta.mt[0])

# file_meta.close()
if isinstance(filepath, str):
	file.close()