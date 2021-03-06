#!/usr/bin/env python
import sys
import os
import urllib2
import time
import random
import json
import ConfigParser

from twython import Twython
# arquivo com as configuralcoes de acesso do twitter
from raspTweetConf import *

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 
fileDefaults = '/home/raspbot/raspLab/tweetBot/defaults.cfg'

config = ConfigParser.ConfigParser()
config.readfp(open(fileDefaults))

# variaveis uteis.
hora = time.strftime("%d/%m/%Y - %H:%M:%S")
print '['+hora+'] Rodou.'

#inicio MESMO
if sys.argv[1] == 'listen':
    print '---> Listen <---'
    if config.get('Enviroment','LAST_DM_ID'):
        # pedir somente os itens maiores que o id existente...
        current_val = config.get('Enviroment','LAST_DM_ID')
        print '--> variavel atual: '+str(current_val)+' <--'
        #print 'Valor atual = '+current_val
    else:
        # variavel nao existe.
        config.set('Enviroment','LAST_DM_ID',0)
        config.write(open(fileDefaults,'w'))
        #abort script.
        print '--> Nao existe variavel! <--'
        exit()
    #pegando pacote com as mensagens enviadas
    #print 'seguindo...'
    pkgReturnDM = api.get_direct_messages(since_id=current_val)
    print '--> Tamanho do pacote: '+str(len(pkgReturnDM))+' <--'
    for returnDM in pkgReturnDM:
        senderData = returnDM['sender']
        entities = returnDM['entities']
        print 'Sender ---->' + config.get('Enviroment','allow_sender')
        print 'senderData:' + str(senderData['id'])
        if str(senderData['id']) == config.get('Enviroment','allow_sender'):
            print returnDM['created_at']
            print '--> Usuario OK! <--'
            command =  returnDM['entities']['hashtags'][0]['text']
            print '-> comando recebido: '+command+' <-'
            #Executar o comando da hashtag
            full_path = '/home/raspbot/raspLab/tweetBot/'
            cmd = 'python '+full_path+'raspTweet.py '+command
            print '[ '+cmd+' ]'
            #print 'comando enviado...'
            if os.popen(cmd):
                print '!!! Comando enviado !!!'
            else:
                print ' -- erro ao enviar comando -- '
            # atualiza id
            config.set('Enviroment','LAST_DM_ID',returnDM['id'])
            config.write(open(fileDefaults,'w'))
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
    api.update_status(status='hora: ['+hora+']')
else:
    pass
    #print '--- nothing here ---'
