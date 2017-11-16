#!/usr/bin/env python


import sys
import urllib.parse
from http.client import HTTPConnection, HTTPSConnection


if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = [sys.stdin]

for filepath in files:
    if isinstance(filepath, str):
        file = open(filepath)
    else:
        file = filepath

    for url in file:
        url = url.strip()
        purl = urllib.parse.urlsplit(url)
        if purl.scheme == "http":
            connection = HTTPConnection(purl.netloc)
        elif purl.scheme == "https":
            connection = HTTPSConnection(purl.netloc)
        else:
            sys.stderr.write("Error: the {scheme} scheme in {url} is not supported, skipping.\n".format(scheme=purl.scheme, url=url))
            continue
        try:
            connection.request("HEAD", url)
            response = connection.getresponse()
        except Exception as e:
            sys.stderr.write("Unexpected error when checking {url}: {errtype}: "
                             "{errmsg}; skipping.\n"
                             .format(url=url, errtype=type(e).__name__, errmsg=e))
            continue
        print(url, response.status, sep="\t")

    if isinstance(filepath, str):
        file.close()
