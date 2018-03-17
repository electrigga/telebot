#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, json, telepot, sys, os, time, datetime, psutil, RPi.GPIO as GPIO

# Variablen aus der Config holen
from config import apikey
from config import grant
from config import owner
from config import botcall
from config import prozesse
from config import dmrid

# GPIO Settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

# Funktion zur Information des/der Botowner
def ownerinfo(msg,owner):
    for x in owner:
        bot.sendMessage(x,msg)

# Funktion zum Abruf der Abbonierten TG
def talkgroups():
    r = requests.get("http://api.brandmeister.network/v1.0/repeater/?action=profile&q=" + dmrid)
    try:
        data = r.json()
        tgs = 'Talkgroups:'
        for tg in data['staticSubscriptions']:
            tgs += "\n" + str(tg['talkgroup']) + " im TS" + str(tg['slot'])
        for tg in data['clusters']:
            tgs += "\n" + str(tg['talkgroup']) + " im TS" + str(tg['slot']) + " (" + str(tg['extTalkgroup']) + ")"
        if tgs == 'Talkgroups:':
            tgs = "Keine Talkgroups statisch geschaltet."
    except:
        print("Abruf der Talkgroups ging schief....")
    r.close()
    return tgs

# Funktion zum Testen, ob ein Prozess läuft
def prozesschecker(prozess):
    proc = ([p.info for p in psutil.process_iter(attrs=['pid','name']) if prozess in p.info['name']])
    if proc != []:
	status = "Läuft"
    else:
	status = "Läuft nicht"
    return status

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #print(content_type, chat_type, chat_id)

    command = msg['text']
    vorname = msg['from']['first_name']
    username = msg['from']['username']
    id = msg['from']['id']

    # print(msg)

    if msg['text'] in ["/start","/start start", "start", "hallo", "Hallo", "Hi", "Start"]:
	bot.sendMessage(chat_id, "Herzlich willkommen bei " + botcall + " " + vorname + "!" + \
				 "\nUm Hilfe zu erhalten, schreib /hilfe. Informationen und Hinweise bitte an @dl2ajb.")

    elif msg['text'] in ["/hilfe"]:
	hilfetext = "Informationen und Kommandos:\n/status Gibt den Status des Repeaters aus\n/hilfe Hilfetext mit der" \
                    " Liste der Kommandos\n/tg Listet die in DMR geschalteten TG auf"
        if id in grant:
            hilfetext += "\n/txan Schaltet den Sender an\n/txaus Schaltet den Sender aus\n/rxan Schaltet den RX ein" \
			"\n/rxaus Schaltet den RX an\n/reboot start den Rechner neu"
        bot.sendMessage(chat_id,botcall + " " + hilfetext)

    elif msg['text'] in ["/tg"]:
	bot.sendMessage(chat_id, talkgroups())

    elif msg['text'] in ["/status"]:
	status = ''
	# Eingänge lesen
        if GPIO.input(13) == GPIO.HIGH:
	    status += "TX ist aus\n"
        else:
            status += "TX is an\n"
        if GPIO.input(15) == GPIO.HIGH:
            status += "RX ist aus"
        else:
            status += "RX ist an"
	# Laufende Prozesse testen
	for proc in prozesse:
	    status += "\n" + proc + " " + prozesschecker(proc)

	## Temperaturen
	# CPU-Temperaturen auslesen
	tFile = open('/sys/class/thermal/thermal_zone0/temp')
	temp = float(tFile.read())
	tempC = temp/1000
	status += "\nCPU Temperatur " + str(tempC)

        bot.sendMessage(chat_id, status)

    elif msg['text'] in ["/txaus"]:
        if id in grant:
            GPIO.output(13, GPIO.HIGH)
	    bot.sendMessage(chat_id,"Sender ist aus!")
        else:
	    bot.sendMessage(chat_id,"Das darfst du nicht!")
    elif msg['text'] in ["/txan"]:
        if id in grant:
            GPIO.output(13, GPIO.LOW)
            bot.sendMessage(chat_id,"Sender ist wieder an!")
        else:
            bot.sendMessage(chat_id,"Das darfst du nicht!")

    elif msg['text'] in ["/rxaus"]:
        if id in grant:
            GPIO.output(15, GPIO.HIGH)
            bot.sendMessage(chat_id,"Empfang ist aus!")
        else:
            bot.sendMessage(chat_id,"Das darfst du nicht!")
    elif msg['text'] in ["/rxan"]:
        if id in grant:
            GPIO.output(15, GPIO.LOW)
            bot.sendMessage(chat_id,"Empfang ist wieder an!")
        else:
            bot.sendMessage(chat_id,"Das darfst du nicht!")

    elif msg['text'] in ["/reboot"]:
	if id in grant:
	    bot.sendMessage(chat_id,"Starte das System neu.")
	    os.system('sudo shutdown -r now')
	else:
            bot.sendMessage(chat_id,"Das darfst du nicht!")
    else:
	bot.sendMessage(chat_id, 'Mit "' + msg['text'] + '" kann ich nichts anfangen, '+ vorname + "!\nEine Liste der Befehle bekommst du mit /hilfe.")

bot = telepot.Bot(apikey)
try:
    ownerinfo("Ich bin wieder da...",owner)
    bot.message_loop(handle)
except:
    print("Irgendwas stimmt mit dem Bot nicht....")

try:
    while 1:
        time.sleep(10)

except:
    print("Tschüss....")
    ownerinfo("Der Bot wird beendet...",owner)
    # GPIO.cleanup()
