#!/usr/bin/python
import filey, urlz, string, song, os, urlparse, random
from bs4 import BeautifulSoup
from time import sleep

DATA_PATH = "data"
SONG_EXT  = ".txt"

def read_in_urls(url_filename):
    """Reads in urls from a file of urls, one on each line."""
    if len(url_filename) == 0:
        raise Exception("File name is length 0")

    return filey.read_from_file("", url_filename)

def find_songlist_tag(soup):
    """
    In the page source code, there exists a variable called songlist.
    songlist is an array of objects containing the song name and URL.
    This subroutine finds the songlist tag and returns the text associated with it.
    """
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

    if len(properties) > 1:
        song_title = properties[0].lstrip("s: \"").rstrip("\"")
        song_url   = properties[1]
        if song_url.startswith("h:\""):
            song_url = properties[1][3:]
        song_url = song_url.rstrip("\"")

        return song.Song(song_title, song_url)
    else:
        raise Exception("This shit don't exist.")

def decode_json(json_string):
    """
    Removes braces, calls split_json_elem on the contents.
    Returns a list of parsed Song objects.
    """
    elems     = json_string.lstrip("\r {").rstrip("}").split("}, {")
    song_list = []

    for elem in elems:
        song_list.append(split_json_elem(elem))

    return song_list

def print_song_list(song_list):
    """Pretty-prints the list of song objects."""
    for song in song_list:
        print "Song Name: %-*s URL: %s"  % (40, song.name, song.url)

def get_name_from_url(url):
    """Gets artist or song name from the URL."""
    return url.split("/")[-1][0:-5]

def get_song_lyrics(parsed_url, url):
    """
    Takes in two urls--sometimes, with artist collaborations, the second url is
    not a relative URL, but a complete one. I use urlparse to join the two urls
    such that they are baseURL invariant.

    Returns the song lyrics, and prints "Success!" if successful.
    """
    if url.startswith(".."):
        url = urlparse.urljoin(parsed_url.geturl(), url)
    print "Parsing %s..." % (url)

    page      = urlz.open_and_read(url)
    soup      = BeautifulSoup(page, "lxml")
    page_text = soup.get_text()
    lyrics    = page_text[(page_text.index("Print") + 5):page_text.index("if  ( /Android")].strip("\n")

    if type(lyrics) == None:
        print "Nothing returned."
    elif len(lyrics) > 0:
        print "Success!"
    else:
        print "Lyrics are empty."

    return lyrics

def write_songs(artist, song_list, parsed_url):
    length = len(song_list)
    count = 0
    selected_indices = []
    while count < length:
        # Find a random index from the song_list and ensure it is new.
        rand_idx = random.randint(0, length - 1)
        while rand_idx in selected_indices:
            rand_idx = random.randint(0, length - 1)

        song           = song_list[rand_idx]
        song_path      = os.path.join(DATA_PATH, artist)
        song_file_name = filey.scrub_file_name(song.name + SONG_EXT)

        if filey.already_exists(song_path, song_file_name):
            print "%s already exists. Continuing." % (song_file_name)
        else:
            # Be like human.
            sleep(random.triangular(4.8, 7.23, 12.4))
            rand_int = random.randint(0, 10)
            if rand_int == 9:
                sleep(random.triangular(2.6, 10, 7))
            song_data = get_song_lyrics(parsed_url, song.url)
            filey.write_to_file(song_path, song_file_name, song_data)

        selected_indices.append(rand_idx)
        count += 1

def scrape_artist_for_song_urls(url):
    """
    Take in a url, opens it, and parses the page for song URLs and names.
    """
    try:
        parsed_url   = urlparse.urlparse(url)
        artist       = get_name_from_url(url)
        page         = urlz.open_and_read(url)
        soup         = BeautifulSoup(page, "lxml")

        songlist_tag = string.join(find_songlist_tag(soup).split("}];")[0].split("\n")[1:]).strip()
        json_arg     = "{%s}" % (songlist_tag.split("[", 1)[1].rsplit("]", 1)[0].lstrip(" "))
        song_list    = decode_json(json_arg)

        write_songs(artist, song_list, parsed_url)
    except:
        print "Skipping %s" % (url)
