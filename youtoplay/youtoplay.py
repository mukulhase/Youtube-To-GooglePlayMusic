#!/usr/bin/env python
from __future__ import unicode_literals
from gmusicapi import Musicmanager
import sys, os
import youtube_dl
import glob


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

def init():
    mm = Musicmanager()
    try:
        script_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_path = os.getcwd()
    mm.login(oauth_credentials=os.path.join(script_path, "oauth.cred"))
    return mm

def upload_last():
    mm = init()
    newest = max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime)
    name = newest
    mm.upload(name)

def youtube_download(link):
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                }],
            'logger': MyLogger(),
            }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        name=ydl.download([link])
        upload_last()
#try:
#	name = aj.select(aj.get_results(link)[0],'./Downloaded_Youtube_Songs')
#except:
#	name = "temp.mp3"
#	os.system("wget -O temp.mp3 http://www.youtubeinmp3.com/fetch/?video=" + link)

if __name__ == "__main__":
    link = sys.argv[1]
    print(link)
    youtube_download(link)

