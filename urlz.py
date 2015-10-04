import urllib2, string
from httplib import BadStatusLine

def open_and_read(url):
    try:
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403157 Safari/537.36")
        req.add_header("Referer", "https://www.google.com/?gws_rd=ssl#q=azlyrics")
        resp = urllib2.urlopen(req).read()

        return resp
    except BadStatusLine:
        print "URL %s got owned." % (url)
