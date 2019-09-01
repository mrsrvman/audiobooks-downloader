#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Download complete audio books from audioknigi.club
"""

import argparse
import re
import json
import os
#import urllib
import urllib.request
import distutils.util
from os.path import splitext

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download books from audioknigi.club .')
    parser.add_argument('url', help='Url that contains books player.')
    parser.add_argument('--use_numbers', help='Use only number for output files, like 001.mp3 .',
        default=False, required=False, type=bool)
    parser.add_argument('--skip_exist', help='Skip exist files.',
        default=True, required=False, type=distutils.util.strtobool)

    args = parser.parse_args()

    # get book id
    response = urllib.request.urlopen(args.url)
    #book_id_match = re.search(r'audioPlayer\((\d+),\d+\)', str(response.read()), re.MULTILINE)
    book_id_match = re.search(r'book-circle-progress-(\d+)', str(response.read()), re.MULTILINE)
    if not book_id_match:
        raise Exception('Cannot find book id.')
    book_id = book_id_match.group(1)

    # creade directory for it
    dir = re.search(r'\/((?:.(?!\/))+)$', args.url).group(1)
    if not os.path.exists(dir):
        os.makedirs(dir)

    # download mp3 files
    response = urllib.request.urlopen('https://audioknigi.club/rest/bid/' + book_id).read().decode('utf8')
    titles = json.loads(response)
    index = 0
    for title in titles:
        filename = re.search(r'\/((?:.(?!\/))+)$', title['mp3']).group(1)
        if args.use_numbers:
            filename = str(index).zfill(3) + splitext(filename)[1]
            index = index + 1
        print('Downloading %s' % (filename))
        parsedurl = urllib.parse.urlsplit(title['mp3'])
        parsedurl = parsedurl._replace(path=urllib.parse.quote(parsedurl.path))
        if args.skip_exist == True and os.path.exists(os.path.join(dir, filename)):
            print ('Skipping')
            continue
        urllib.request.urlretrieve(parsedurl.geturl(), os.path.join(dir, filename))
