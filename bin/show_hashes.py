#!/usr/bin/env python
import os
import sys
import re

sys.path.insert(0, '/opt/duo')
from ocd_backend.utils.misc import make_hash_filename

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def main():
    file_names = sys.stdin.readlines()
    for file_name in file_names:
        file_name_clean = file_name.replace('"', '').strip()
        hashed_filename = make_hash_filename(file_name_clean)
        full_path = os.path.join('/opt/duo/downloads', hashed_filename)
        if os.path.exists(full_path):
            prefix = "*"
        else:
            prefix = " "
        l = file_len(full_path)
        print "%s%s,%s,%s" % (prefix,file_name_clean, hashed_filename,l,)

if __name__ == '__main__':
    main()
