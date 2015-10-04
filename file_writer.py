#!/usr/bin/python

import os, sys, errno

def make_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def write_to_file(path, filename, data):
    # Recursively create path passed in
    make_path(path)

    with open(os.path.join(path, filename), "wb") as file_target:
        file_target.write(data)
