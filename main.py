#!/usr/bin/python
from scrapiaz import *

artist_urls = read_in_urls("urls.txt")
for main_url in artist_urls:
    scrape_artist_for_song_urls(main_url)
