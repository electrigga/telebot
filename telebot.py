#!/usr/bin/python
# -*- coding: utf-8 -*-
import telepot, sys, time, datetime, psutil, RPi.GPIO as GPIO

# Variablen aus der Config holen
from config import apikey
from config import grant
from config import owner
from config import botcall

# GPIO Settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

# Funktion zur Information des/der Botowner
def ownerinfo(msg,owner):
    for x in owner:
        bot.sendMessage(x,msg)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #print(content_type, chat_type, chat_id)

    command = msg['text']
    vorname = msg['from']['first_name']
    username = msg['from']['username']
    id = msg['from']['id']

    print(msg)
    # print 'Kommando erhalten: %s von %s' % (command, username)

    if msg['text'] in ["/start","/start start", "start", "hallo", "Hallo", "Hi", "Start"]:
	bot.sendMessage(chat_id, "Herzlich willkommen bei " + botcall + " " + vorname + "!" + \
				 "\nUm Hilfe zu erhalten, schreib /hilfe. Informationen und Hinweise bitte an @dl2ajb.")

    elif msg['text'] in ["/proc"]:
	for proc in psutil.process_iter():
	    try:
		pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
	    except psutil.NoSuchProcess:
                pass
	    else:
		bot.sendMessage(chat_id,pinfo)

    elif msg['text'] in ["/hilfe"]:
	hilfetext = "Informationen und Kommandos:\n/status Gibt den Status des Repeaters aus\n/hilfe Hilfetext mit der Liste der Kommandos"
        if id in grant:
            hilfetext += "\n/txan Schaltet den Sender an\n/txaus Schaltet den Sender aus\n/rxan Schaltet den RX ein\n/rxaus Schaltet den RX an"
        bot.sendMessage(chat_id,botcall + " " + hilfetext)

    elif msg['text'] in ["/status"]:
	# Eingänge lesen
        if GPIO.input(13) == GPIO.HIGH:
	    gpio13 = "aus"
        else:
            gpio13 = "an"
        if GPIO.input(15) == GPIO.HIGH:
            gpio15 = "aus"
        else:
            gpio15 = "an"

        bot.sendMessage(chat_id, "TX ist " + gpio13 + "\n" + "RX ist " + gpio15)

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
    else:
	bot.sendMessage(chat_id, "Damit kann ich nichts anfangen, " + vorname + "!")

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
