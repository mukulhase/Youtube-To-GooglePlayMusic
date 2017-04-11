#!/usr/bin/env python
from gmusicapi import Musicmanager
import sys, os

from audiojack import AudioJack
link = sys.argv[1]
##os.system("wget -O temp.mp3 http://www.youtubeinmp3.com/fetch/?video=" + link)
print link
aj = AudioJack()
name = aj.select(aj.get_results(link)[0],'./Downloaded_Youtube_Songs')

mm = Musicmanager()
mm.login(oauth_credentials=u'./oauth.cred')

mm.upload(name)
