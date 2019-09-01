#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Download complete audio books from knigavuhe.org
"""

import sys, os
import json
import distutils.util
import click
import requests

def GET(url, Referer = 'https://m.knigavuhe.org/', XML=False):
	headers = {}
	headers['User-Agent']='Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60'
	headers['Accept'] = 'text/html, application/xml, application/xhtml+xml, */*'
	headers['Accept-Language'] = 'ru,en;q=0.9'
	headers['Referer'] = Referer
	if XML: headers['x-requested-with'] = 'XMLHttpRequest'
	return requests.get(url, headers=headers).content.decode('utf8')

def normalize_url(url):
	scheme, netloc, path, params, query, fragment = requests.utils.urlparse(url)
	if (path.endswith('/')==True): path=path[:-1]
	if (netloc.startswith('m.')==False): netloc='m.'+ netloc
	return requests.utils.urlunparse((scheme, netloc, path, params, query, fragment))

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def save_byte_data_to_file(full_path_dir, file_name, data):
	open(os.path.join(full_path_dir, file_name), 'wb').write(data)

def get_chapters(url):
	click.echo('====get_chapters====')
	click.echo(url)
	scheme, netloc, path, params, query, fragment = requests.utils.urlparse(url)
	hp=GET(url,requests.utils.urlunparse((scheme, netloc,'','','','')))
#	click.echo(hp)
	if 'book_blocked' in hp: return {'cover':'','blocked':1,'playlist': [{'title': 'Book Blocked.', 'author': 'author', 'duration': 0, 'url':''},]}
	try:cover=mfind(hp,'<img src="','" alt=')
	except: cover=''
	data='[{'+mfind(hp,', [{','],')+']'
	L=eval(data.replace('\\/','/'))
	playlist=[]
	for i in L:
		playlist.append(i)
	LL={'cover': cover,'playlist':playlist,'blocked':0}
	return LL

def download_chapter(url):
    """Download a chapter."""
    return requests.get(url).content

def get_audiobook_name(url):
    """Extract the audiobook name from its URL."""
    # TODO: sanitize the path
    return url.split('/')[-1]

def get_full_dirname(dirname, do_overwrite):
    """
    Return absolute path for dirname, and check for existence.
    
    If dirname exists and is not a directory - raise an exception.
    If not empty - prompt before overwriting unless do_overwrite is True.
    """
    full_path_dir = os.path.abspath(dirname)

    if os.path.exists(full_path_dir):
        if not os.path.isdir(full_path_dir):
            click.echo('\n{} exists, and is not a directory!\n'.format(full_path_dir))
            exit(1)
        if os.listdir(full_path_dir) and not do_overwrite:
            if not click.confirm('\nDirectory "{}" exists. Overwrite?'.format(full_path_dir)):
                sys.exit(1)
            else:
                click.echo('Overwriting files in "{}"\n'.format(full_path_dir))
    else:
        click.echo('\nCreating directory "{}"'.format(full_path_dir))
        # TODO: avoid side effects
        os.makedirs(full_path_dir)
    return full_path_dir


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('audio_book_url')
@click.option(
    '-o', '--output_dir', 'output_dir', default=None,
    help='Directory the audio book will be dowloaded to. Default: <Audio Book Name>'
)
@click.option(
    '-w', '--overwrite', 'do_overwrite', is_flag=True,
    help='Overwrite existing audiobook directory without asking'
)
@click.option(
    '-s', '--skip', 'do_skip_exist', is_flag=True,
    help='Skip exist files.'
)

def downloader_main(output_dir, do_overwrite, audio_book_url,do_skip_exist):

	audio_book_url = normalize_url(audio_book_url)
	if output_dir is None:
		output_dir = get_audiobook_name(audio_book_url)

	full_path_dir = get_full_dirname(output_dir, do_overwrite)

	msg = '\nDownloading audiobook from "{}"\nto "{}"\n'
	click.echo(msg.format(audio_book_url, full_path_dir))

	book_data = get_chapters(audio_book_url)
	if book_data.get('blocked',0)==1: 
		click.echo('Book blocked by copyright holder')
		sys.exit(1)
	save_byte_data_to_file(full_path_dir, '00 - cover.jpg', download_chapter(book_data['cover']))
	playlist=book_data['playlist']
	for s in playlist:
		click.echo(s['url'])
		fname=s['title']
		url=s['url']
		click.echo('Downloading chapter "{}"'.format(fname))
		if do_skip_exist == True and os.path.exists('{}.mp3'.format(os.path.join(full_path_dir, fname))):
			print ('Skipping')
			continue
		save_byte_data_to_file(full_path_dir, fname + '.mp3', download_chapter(url))
	click.echo('All done!\n')

# start the app
if __name__ == '__main__':
	downloader_main()
#https://m.knigavuhe.org/