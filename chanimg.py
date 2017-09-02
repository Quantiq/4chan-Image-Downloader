# ChanImg 0.11
#
# Changelog / Fixes:
# - Try to monitor a thread. -Done!
# - Write a timer. -Done!
# - Fix OS Error on Folder exists
#
#
# To Do:
# - Allow user to imput custom amount of time for thread
# - Try to break the script on an input instead of ctrl-X and write a timer. ?
# - Combine the two scripts
# - Fix OS Error on Folder exists
# - Write a functional argument parser and options.
# - - Set the thread update time
# - - quiet mode
# - - return images with original file names.
# - - Monitor Multiple Threads (Be careful for API constraints here)
#
#
# written by Quantiq.

from urllib.request import urlopen
from urllib.request import urlretrieve
from time import sleep

import os
import json
import argparse

def main():

    input_board = 'wg' #input("Input the board: ")
    input_thread = '7007090' #input("Input the thread ID: ")
    original_filename_option = True #input here

    try:
        input_folder = '{} - {} - '.format(input_board, input_thread) + js['posts'][0]['sub'] #broken. js is not defined.
    except:
        input_folder = '{} - {} '.format(input_board, input_thread)

    # try making a folder
    if os.path.exists('output/' + input_folder) == False:
        try:
            os.makedirs('output/' + input_folder)
        except OSError:
            print("OS Error. Not sure what happened. :-(")


    thread_monitor(input_board, input_thread, input_folder, original_filename_option)

#def thread_download
    #my code here

def thread_monitor(board, thread, folder, original_filename_option):

    while True:

        print('Checking thread for updates...')
        dl_num = image_downloader(board, thread, folder, original_filename_option)

        if dl_num == 0:
            print('Nothing to Update. Waiting 60 seconds...')
        elif dl_num == 1:
            print('Downloaded {} image. Waiting 60 seconds...'.format(dl_num))
        else:
            print('Downloaded {} images. Waiting 60 seconds...'.format(dl_num))

        # Sleep timer. Prints to shell dynamically.
        for i in range(15):
            print('Waiting. |', end='\r', flush=True)
            sleep(1)
            print('Waiting. /', end='\r', flush=True)
            sleep(1)
            print('Waiting. -', end='\r', flush=True)
            sleep(1)
            print('Waiting. \\', end='\r', flush=True)
            sleep(1)

def image_downloader(board, thread, folder, original_filename_option):
    dl_num = 0
    pair_list = list_update(board, thread)

    for pair in pair_list:
        orig_name = pair[0]
        dl_name = pair[1]

        # Downloads original filenames if the user selects.
        if original_filename_option == True:
            name_option = orig_name
        else:
            name_option = dl_name

        url_pic = 'https://i.4cdn.org/' + board + '/' + dl_name

        if os.path.exists('output/' + folder + '/' + name_option) == False: # Checks if file exists.
            dl_num += 1
            print("Downloading /{}/{}...".format(board, orig_name))
            urlretrieve(url_pic, 'output/' + folder + '/' + name_option)
            sleep(1)

    return dl_num

def list_update(board, thread):

    pair_list = []

    # Loads json from 4chan API
    json_url = 'https://a.4cdn.org/{}/thread/{}.json'.format(board, thread)
    url = urlopen(json_url)
    js = json.loads(url.read().decode('utf-8'))

    # Dumb hacky way of getting the number of replies in a thread
    count = js['posts'][0]['replies'] + 1

    # Creates a list of picture urls
    ## Note: Should append new to list here? Does it matter if it makes a completely new list each time?
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

main()

#debug
#print(list_update('wg', '6990039'))