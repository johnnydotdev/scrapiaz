#!/usr/bin/python
import os, sys, errno, string

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

# Tries to make path and only catches exceptions not relating to directory
# already existing.
def make_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def write_to_file(path, filename, data):
    # Recursively create path passed as arg.
    make_path(path)
    filename = "".join(c for c in filename if c in valid_chars).encode('utf-8')
    data     = data.encode('utf-8')

    with open(os.path.join(path, filename), "wb") as file_target:
        if type(data) is list:
            for line in data:
                file_target.write(line + "\n")
        else:
            file_target.write(data)

def read_from_file(path, filename):
    with open(os.path.join(path, filename), "r") as file_source:
        data = [line.rstrip("\n") for line in file_source]

    return data
