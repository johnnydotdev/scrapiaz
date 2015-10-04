#!/usr/bin/python
import filey

def read_urls(url_filename):
    if len(url_filename) == 0:
        raise Exception("File name is length 0")

    return filey.read_from_file("", url_filename)

print read_urls("urls.txt")
