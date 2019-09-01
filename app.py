"""
    Download complete audio books from audioknigi.ru
"""
import argparse
import distutils.util
from os.path import splitext
import os

import contextlib
import json
import re
import sys

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



AJAX_ON_SUCCESS = '''
    $(document).ajaxSuccess(function(event, xhr, opt) {
        if (opt.url.indexOf('ajax/bid') !== -1) {
            $('body').html($('<div />', {
                id: 'playlist',
                text: JSON.parse(xhr.responseText).aItems
            }))
        }
    });
'''

INIT_PLAYER = '$(document).audioPlayer({}, 0)'


@contextlib.contextmanager
def open_browser(url):
    """Open a web page with Selenium."""
    if getattr(sys, 'frozen', False):
        tmp_path = getattr(sys, '_MEIPASS')
        os.environ['PATH'] += os.pathsep + tmp_path
    browser = webdriver.Chrome()
    browser.get(url)
    yield browser
    browser.close()


def get_book_id(html):
    """Get the internal book ID."""
    player = re.compile(r'audioPlayer\((.*)\,')
    book_id_match=player.search(html)
    if not book_id_match:
        raise Exception('Cannot find book id.')
    return book_id_match.group(1)
#    return player.search(html).group(1)


def get_playist(browser, book_id):
    """Extract the playlist."""
    browser.execute_script(AJAX_ON_SUCCESS)
    browser.execute_script(INIT_PLAYER.format(book_id))
    playlist_loaded = EC.presence_of_element_located((By.ID, 'playlist'))
    element = WebDriverWait(browser, 20).until(playlist_loaded)
    return tuple((track['mp3'], track['title']) for track in json.loads(element.text))


def download_chapter(url):
    """Download a chapter."""
    return requests.get(url).content


# start the app
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download books from audioknigi.club .')
    parser.add_argument('url', help='Url that contains books player.')
    parser.add_argument('--use_numbers', help='Use only number for output files, like 001.mp3 .',
        default=False, required=False, type=bool)
    parser.add_argument('--skip', help='Skip exist files.',
        default=True, required=False, type=distutils.util.strtobool)

    args = parser.parse_args()

    try: 
      with open_browser(args.url) as browser:
        book_id = get_book_id(browser.page_source)
        playlist = get_playist(browser, book_id)
    except Exception as inst:
       print ("Unexpected error:", inst)
       browser.close()
       sys.exit(1)

    dir = re.search(r'\/((?:.(?!\/))+)$', args.url).group(1)
    # create directory for audiobook
    if not os.path.exists(dir):
        os.makedirs(dir)

    for url, fname in playlist:
        print('Downloading chapter "{}"'.format(fname))
        if args.skip == True and os.path.exists(os.path.join(dir,'{}.mp3'.format(fname))):
            print ('Skipping')
            continue
        with open(os.path.join(dir,'{}.mp3'.format(fname)), 'wb') as outfile:
            outfile.write(download_chapter(url))

    print('All done.')
