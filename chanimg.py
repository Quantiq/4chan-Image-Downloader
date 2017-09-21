#!/usr/bin/env python3

from time import sleep

import os
import argparse
import json
import urllib.request

'''Global Argument Parsing'''
parser = argparse.ArgumentParser(prog='chanimg', usage='%(prog)s url [optional arguments]', description='ChanImg is a simple command-line 4chan image downloader written in Python.')

parser.add_argument('url', type=str, help='Downloads images from a given input URL.')
parser.add_argument('-m', '--monitor', action='store_true', help='Monitors a specified thread.')
parser.add_argument('-u', '--update', metavar='', default=60, type=int, help='Specifies the amount of time in seconds to update a thread. (Default: 60)')
parser.add_argument('-o', '--original', action='store_true', help='Saves images as original filenames.')
parser.add_argument('-f', '--foldername', type=str, default=None, help='Save images to a specified folder name.')

args = parser.parse_args()

def link_parse(url):
    '''Converts thread URL to JSON URL'''
    url = url.replace('boards', 'a')
    url = url.replace('4chan', '4cdn')

    return url + '.json'

def board_parse(url):
    '''4chan doesn't include the board name in its API, so here is some weird string parsing that grabs it from the URL.'''
    x = url.find('.org') + 5
    y = url.find('thread') - 1

    return url[x:y]

def load_json(url):
    '''Returns JSON upon call.'''
    try:
        response = urllib.request.urlopen(url)
        js = json.loads(response.read().decode('utf-8'))
        return js

    except urllib.error.HTTPError as err:
        print("{} Error.".format(err.code))

    except urllib.error.URLError:
        print("URL Error. Are you sure you have the correct link?")

def make_folder(thread_json, board):
    '''Make a directory to put images in.'''
    if args.foldername == None:
        '''If thread title exists, then write that to the folder name.'''
        try:
            input_folder = board + ' - ' + str(thread_json['posts'][0]['no']) + ' - ' + str(thread_json['posts'][0]['sub'])
        except:
            input_folder = board + ' - ' + str(thread_json['posts'][0]['no'])
    else:
        input_folder = args.foldername

    '''replaces '/' in foldername string'''
    if '/' in input_folder:
        input_folder = input_folder.replace('/', '')

    '''Try making a folder'''
    if os.path.exists('output/' + input_folder) == False:
        try:
            os.makedirs('output/' + input_folder)
        except OSError:
            print('Something went wrong while trying to make your folder.')

    return input_folder

def list_maker(js):
    '''Makes a list if image urls based on the input JSON.'''
    pair_list = []

    '''Dumb way of getting the number of replies in a thread'''
    count = js['posts'][0]['replies'] + 1

    for i in range(count):
        try:
            js_filename = js['posts'][i]['filename']
            js_tim = js['posts'][i]['tim']
            js_extension = js['posts'][i]['ext']

            dl_imagename = str(js_tim) + js_extension
            original_imagename = str(js_filename) + js_extension

            image_pair = [original_imagename, dl_imagename]

            pair_list.append(image_pair)
        except:
            pass

    return pair_list

def image_downloader(folder, pair_list, board):
    '''Main image downloading program.'''
    dl_num = 0

    for pair in pair_list:
        orig_name = pair[0]
        dl_name = pair[1]

        '''Downloads original filenames if the user has selected'''
        if args.original == True:
            name_option = orig_name
        else:
            name_option = dl_name

        url_pic = 'https://i.4cdn.org/' + board + '/' + dl_name

        '''Checks if file exists'''
        if os.path.exists('output/' + folder + '/' + name_option) == False:
            dl_num += 1
            print("Downloading {}...".format(orig_name))
            urllib.request.urlretrieve(url_pic, 'output/' + folder + '/' + name_option)
            sleep(1)
    return dl_num

def dl_status(dl_num):
    '''Return status of how many images downloaded in a session.'''
    if args.monitor == True:
        if dl_num == 0:
            print('No images to download. Waiting {} seconds to update.'.format(args.update))
        elif dl_num == 1:
            print('Downloaded {} image. Waiting {} seconds to update.'.format(dl_num, args.update))
        else:
            print('Downloaded {} images. Waiting {} seconds to update.'.format(dl_num, args.update))

    else:
        if dl_num == 0:
            print('No images to download.')
        elif dl_num == 1:
            print('Downloaded {} image.'.format(dl_num))
        else:
            print('Downloaded {} images.'.format(dl_num))

    print('')
    return

def timer(time):
    '''Sleeps for specified amount of time.'''
    for i in range(time):
        try:
            print('Waiting... Press Ctrl + C to exit.', end='\r', flush=True)
            sleep(1)
        except KeyboardInterrupt:
            print('')
            print('Exiting program.')
            exit()
    return

def thread_download(folder, js, board):
    '''Single instance downloader'''
    print("Checking thread for images to download...")

    pairlist = list_maker(js)
    dl_num = image_downloader(folder, pairlist, board)
    dl_status(dl_num)

    exit()

def thread_monitor(folder, js, board):
    '''Main Thread monitoring'''

    '''Checks to make sure JSON is not loaded on first call.'''
    do_not_load_json = True

    while True:

        if do_not_load_json == False:
            js = load_json(url)

        print("Checking thread for images to download...")

        pairlist = list_maker(js)
        dl_num = image_downloader(folder, pairlist, board)

        dl_status(dl_num)
        timer(args.update)
        do_not_load_json = False

if __name__ == '__main__':
    if args.update < 10:
        print('Update value must be set to 10 seconds or higher.')
        exit()

    url = link_parse(args.url)
    board = board_parse(args.url)
    thread_json = load_json(url)

    foldername = make_folder(thread_json, board)

    if args.monitor == True:
        thread_monitor(foldername, thread_json, board)
    else:
        thread_download(foldername, thread_json, board)