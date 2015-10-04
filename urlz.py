import urllib2

def open_and_read(url):
    return urllib2.urlopen(url).read()
