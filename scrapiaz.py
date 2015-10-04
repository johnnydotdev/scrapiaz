#!/usr/bin/python
import filey, urlz, string, song
from bs4 import BeautifulSoup

test_url = "http://www.azlyrics.com/j/jayz.html"
DATA_PATH = "data"

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

# Input looks like:
# s:"Young Forever", h:"../lyrics/jayz/youngforever.html", c:"", a:""
def split_json_elem(json_elem):
    """
    Takes in the contents of a json element with curly braces removed.
    Returns a Song data transfer object (see song.py for details).
    """
    properties = json_elem.split("\", ")
    song_title = properties[0].lstrip("s: \"").rstrip("\"")
    song_url = properties[1]
    if song_url.startswith("h:\""):
        song_url = properties[1][3:]
    song_url = song_url.rstrip("\"")

    return song.Song(song_title, song_url)

def decode_json(json_string):
    """
    Removes braces, calls split_json_elem on the contents.
    Returns a list of parsed Song objects.
    """
    elems = json_string.lstrip("\r {").rstrip("}").split("}, {")
    song_list = []
    for elem in elems:
        song_list.append(split_json_elem(elem))

    return song_list

def print_song_list(song_list):
    """Pretty-prints the list of song objects."""
    for song in song_list:
        print "Song Name: %-*s URL: %s"  % (40, song.name, song.url)

def get_name_from_url(url):
    return url.split("/")[-1][0:-5]

def make_song_folder(artist, song_list):
    for song in song_list:
        filey.make_path(DATA_PATH + "/" + artist + "/" + song.name)

def scrape_url(url):
    """
    Take in a url, opens it, and parses the page for song URLs and names.
    """
    artist = get_name_from_url(url)
    page = urlz.open_and_read(url)
    soup = BeautifulSoup(page, "lxml")

    songlist_tag = string.join(find_songlist_tag(soup).split("}];")[0].split("\n")[1:]).strip()
    json_arg = "{%s}" % (songlist_tag.split("[", 1)[1].rsplit("]", 1)[0].lstrip(" "))
    song_list = decode_json(json_arg)
    make_song_folder(artist, song_list)

    print_song_list(song_list)

#print read_in_urls("urls.txt")
scrape_url(test_url)
