#!/usr/bin/python
import filey, urlz
from bs4 import BeautifulSoup

test_url = "http://www.azlyrics.com/j/jayz.html"

def read_in_urls(url_filename):
    """Reads in urls from a file of urls, one on each line."""
    if len(url_filename) == 0:
        raise Exception("File name is length 0")

    return filey.read_from_file("", url_filename)

def find_songlist_tag(soup):
    songlist_tag = ""
    for tag in soup.findAll("script"):
        tag_text = tag.text
        if "var songlist" in tag_text:
            songlist_tag = tag_text
            break

    return songlist_tag

def scrape_url(url):
    page = urlz.open_and_read(url)
    soup = BeautifulSoup(page, "lxml")

    songlist_tag = find_songlist_tag(soup)

    print songlist_tag

#print read_in_urls("urls.txt")
scrape_url(test_url)
