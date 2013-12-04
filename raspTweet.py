#!/usr/bin/env python
import sys
import os
import urllib2
import time
import random
import json

from twython import Twython

# arquivo com as configuralcoes de acesso do twitter
import raspTweetConf

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

hora = time.strftime("%d/%m/%Y - %H:%M:%S")

if sys.argv[1] == 'listen':
    if "LAST_TWEET_ID" in os.environ:
        print " var ok"
    else:
        print " erro"
        print " nova var"
        with open("/home/pi/.bashrc","a") as outfile:
            outfile.write("export LAST_TWEET_ID=1") 
    returnDM = api.get_direct_messages()
    print returnDM[0]['created_at']
    print returnDM[0]['hashtags']
elif sys.argv[1] == 'update':
    api.update_status(status=sys.argv[2])
elif sys.argv[1] == 'temp':
    cmd = '/opt/vc/bin/vcgencmd measure_temp'
    line = os.popen(cmd).readline().strip()
    temp = line.split('=')[1].split("'")[0]
    api.update_status(status='My current CPU temperature is '+temp+' C ['+hora+']')
elif sys.argv[1] == 'addr':
    line = urllib2.urlopen('http://checkip.dyndns.org').readline().strip()
    addr = line.split("<body>")[1].split("</body>")[0]
    addr = addr+' ['+hora+']'
    api.send_direct_message(user='rom232',text=addr)
elif sys.argv[1] == 'fortune':
    cmd = 'fortune'
    line = os.popen(cmd).read().strip()
    if len(line) < 140:
        api.update_status(status=line)
elif sys.argv[1] == 'time':
    api.update_status(status='horao: ['+hora+']')
