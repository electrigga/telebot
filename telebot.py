#!/usr/bin/python
# -*- coding: utf-8 -*-
import telepot, sys, time, datetime, RPi.GPIO as GPIO

# Variablen aus der Config holen
from config import apikey
from config import grant
from config import owner

# GPIO Settings
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

def ownerinfo(msg,owner):
    for x in owner:
        bot.sendMessage(x,msg)

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    vorname = msg['from']['first_name']
    username = msg['from']['username']
    id = msg['from']['id']

    # print(msg)

    print 'Kommando erhalten: %s von %s' % (command, username)

    if command == '/start':
	bot.sendMessage(chat_id, "Herzlich willkommen bei DB0ASE " + vorname + "!")
    elif command == '/status':
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

    elif command == '/txaus':
        if id in grant:
            GPIO.output(13, GPIO.HIGH)
	    bot.sendMessage(chat_id,"Sender ist aus!")
        else:
	    bot.sendMessage(chat_id,"Das darfst du nicht!")
    elif command == '/txan':
        if id in grant:
            GPIO.output(13, GPIO.LOW)
            bot.sendMessage(chat_id,"Sender ist wieder an!")
        else:
            bot.sendMessage(chat_id,"Das darfst du nicht!")


    else:
	bot.sendMessage(chat_id, "Das kenne ich nicht, " + vorname + "!")

bot = telepot.Bot(apikey)
try:
    ownerinfo("Ich bin wieder da",owner)
    bot.message_loop(handle)
except:
    print("Irgendwas stimmt mit dem Bot nicht....")

try:
    while 1:
        time.sleep(10)

except:
    print("Tschüss....")
    GPIO.cleanup()
