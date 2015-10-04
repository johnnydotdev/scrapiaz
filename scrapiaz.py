#!/usr/bin/python
import filey, urlz
from bs4 import BeautifulSoup

test_url = "http://www.azlyrics.com/g/ghostfacekillah.html"

def read_in_urls(url_filename):
"""Reads in urls from a file of urls, one on each line."""
    if len(url_filename) == 0:
        raise Exception("File name is length 0")

    return filey.read_from_file("", url_filename)

#print read_in_urls("urls.txt")
