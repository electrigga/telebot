#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, csv, requests, json, telepot, sys, os, time, datetime, psutil, RPi.GPIO as GPIO
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
from pprint import pprint

reload(sys)
sys.setdefaultencoding('utf8')

import gettext

trans = gettext.translation("telebot", "locale", ["sl"])
trans.install()

# Variablen aus der Config holen
from config import apikey
from config import grant
from config import owner
from config import botcall
from config import prozesse
from config import dmrid
from config import mmdvmlogs
from config import sensors

logfile = "botlog.txt"
userfile = "users.csv"
grantfehler = _("granterror")
mmdvmaufruf = "/usr/bin/screen /home/pi/MMDVMHost/MMDVMHost /home/pi/MMDVMHost/MMDVM-DB0ASE.ini"
dmrgwaufruf = "/usr/bin/screen /home/pi/DMRGateway/DMRGateway /home/pi/DMRGateway/DMRGateway-DB0ASE.ini"

befehlsliste_usr = "/lh /status /tg /help\n"
befehlsliste_syop = "/gpio /sw /svx"

# GPIO Settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

# Loggingfunktion
def botlog(logtext):
    file = open(logfile, "a+")
    file.write(time.strftime("%d.%m. %H:%M:%S") + ": " + logtext + '\n')
    file.close()

# function to read temp-sensors
def read_sensor(path):
  value = "U"
  try:
      f = open(path[0], "r")
      line = f.readline()
      if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
          line = f.readline()
          m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
      if m:
          value = str(round(float(m.group(2)) / 1000.0,1)) + "°C"
      f.close()
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return path[1] + ": " + value

# Funktion zur Information des/der Botowner
def ownerinfo(msg,owner):
    for x in owner:
	try:
            bot.sendMessage(x,msg)
	except:
	    print_(("owner_msg_fails"))

# Lastheardfunktion
def lastheard(suchstring):
    if suchstring == '':
	suchstring = "received RF voice header"
    else:
        suchstring = "received RF voice header from " +suchstring
    heard = []
    dateiname = mmdvmlogs + "/mmdvm-"+(time.strftime("%Y-%m-%d"))+".log"
    file = open(dateiname, "r")
    for line in file:
        if line.find(suchstring) > 1:
	    string = (line.rstrip())
	    string = string.split(" ")
	    heard.append(string)
    file.close()
    if not heard:
	return _("not_seen_today")
    else:
        return heard[-1][2] + " " + heard[-1][4] + " " + heard[-1][5] + " " + heard[-1][11] + " " + heard[-1][13] + " " + heard[-1][14]

# Prozesskiller
def prockiller(prozess):
    os.system('pkill '+prozess)

# Funktion Ausgabe Befehle
def befehlsliste(id):
    if id in grant:
	return "\n" + befehlsliste_usr + befehlsliste_syop
    else:
	return "\n" + befehlsliste_usr

# Funktion zum Abruf der Abbonierten TG
def talkgroups():
    r = requests.get("http://api.brandmeister.network/v1.0/repeater/?action=profile&q=" + dmrid)
    try:
        data = r.json()
        pprint(data)
        tgs = 'Talkgroups:'
        for tg in data['staticSubscriptions']:
            tgs += "\n" + str(tg['talkgroup']) + " im TS" + str(tg['slot'])
        for tg in data['clusters']:
            tgs += "\n" + str(tg['talkgroup']) + " im TS" + str(tg['slot']) + " (" + str(tg['extTalkgroup']) + ")"
        for tg in data['timedSubscriptions']:
	    tgs += "\n" + str(tg['talkgroup']) + " im TS" + str(tg['slot'])
        if tgs == 'Talkgroups:':
            tgs = _("no_static_tg")
    except:
        print_(("read_tg_fails"))
    r.close()
    return tgs

# Funktion zum Testen, ob ein Prozess läuft
def prozesschecker(prozess):
    proc = ([p.info for p in psutil.process_iter(attrs=['pid','name']) if prozess in p.info['name']])
    if proc != []:
	status = _("runs")
    else:
	status = _("runs_not")
    return status

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    if query_data == "/txon":
	if from_id in grant:
            GPIO.output(13, GPIO.LOW)
            bot.answerCallbackQuery(query_id,_("tx_is_on"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

    elif query_data == "/txoff":
        if from_id in grant:
            GPIO.output(13, GPIO.HIGH)
            bot.answerCallbackQuery(query_id,_("tx_is_off"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

    elif query_data == "/rxon":
        if from_id in grant:
            GPIO.output(15, GPIO.LOW)
            bot.answerCallbackQuery(query_id,_("rx_is_on"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

    elif query_data == "/rxoff":
        if from_id in grant:
            GPIO.output(15, GPIO.HIGH)
            bot.answerCallbackQuery(query_id,_("rx_is_off"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

    elif query_data == "/killmmdvm":
        if from_id in grant:
            prockiller("MMDVMHost")
            bot.answerCallbackQuery(query_id,_("stop_mmdvm"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

    elif query_data == "/startmmdvm":
        if from_id in grant:
            os.system(mmdvmaufruf)
            bot.answerCallbackQuery(query_id,_("start_mmdvm"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

    elif query_data == "/killdmrgw":
        if from_id in grant:
            prockiller("DMRGateway")
            bot.answerCallbackQuery(query_id,_("stop_dmrgw"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

    elif query_data == "/startdmrgw":
        if from_id in grant:
            os.system(dmrgwaufruf)
            bot.answerCallbackQuery(query_id,_("start_dmrgw"))
        else:
            bot.answerCallbackQuery(query_id,grantfehler)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    vorname = msg['from']['first_name']
    username = msg['from']['username']
    id = msg['from']['id']
    msg['text'] = msg['text'].lower()

    keyboard = ""

    # print(msg['text'])
    # print(msg)

    if msg['text'] in ["/start","/start start", "start", "hallo", "Hallo", "Hi", "Start"]:
	bot.sendMessage(chat_id, _("welcome") + " " + botcall + " " + vorname + "!" + \
				 "\n" + _("toget_help_write_/help"))

    elif msg['text'] in ["/help", "hilfe", "help", "/hilfe"]:
	hilfetext = _("info_commands") + "\n" + "/status " + _("status_help") + "\n" + "/help " + _("help_help") + "\n" + \
		    "/tg " + _("tg_help") + "\n" + "/lh " + _("lh_help") + "\n" + "/lh CALL " + _("lh_CALL_help")
        if id in grant:
            hilfetext += "\n\n" + "/gpio " + _("gpio_help") + "\n" + "/sw " + _("sw_help") + "\n" + "/svx " + _("svx_help")
        bot.sendMessage(chat_id,botcall + " " + hilfetext)

    elif msg['text'] in ["/tg"]:
	bot.sendMessage(chat_id, talkgroups())

    elif "/lh" in msg['text']:
	if msg['text'] == "/lh":
            heard = lastheard('')
            bot.sendMessage(chat_id,heard)
	else:
	    suche = msg['text'].split(" ")
	    heard = lastheard(suche[1].upper())
	    bot.sendMessage(chat_id,heard)

    elif msg['text'] in ["/svx"]:
	    bot.sendMessage(chat_id,_("not_yet_implemented"))

    elif msg['text'] in ["/sw"]:
	if id in grant:
	    keyboard = InlineKeyboardMarkup(inline_keyboard=[
			[
                                InlineKeyboardButton(text=_('btn_start_mmdvm'), callback_data='/startmmdvm'),
				InlineKeyboardButton(text=_('btn_stop_mmdvm'), callback_data='/killmmdvm')
			],
                        [
                                InlineKeyboardButton(text=_('btn_start_dmrgw'), callback_data='/startdmrgw'),
                                InlineKeyboardButton(text=_('btn_stop_dmrgw'), callback_data='/killdmrgw')
                        ],
                        [
                                InlineKeyboardButton(text=_('btn_reboot'), callback_data='/reboot')
                        ]
		    ])
	    bot.sendMessage(chat_id,_('keyboard_software'), reply_markup=keyboard)
	else:
	    bot.sendMessage(chat_id,grantfehler)

    elif msg['text'] in ["/gpio"]:
	if id in grant:
	    keyboard = InlineKeyboardMarkup(inline_keyboard=[
			   [
				InlineKeyboardButton(text=_('btn_tx_on'), callback_data='/txon'),
				InlineKeyboardButton(text=_('btn_tx_off'), callback_data='/txoff')
			   ],
			   [
				InlineKeyboardButton(text=_('btn_rx_on'), callback_data='/rxon'),
				InlineKeyboardButton(text=_('btn_rx_off'), callback_data='/rxoff')
			   ]
			])
	    bot.sendMessage(chat_id,_('keyboard_gpio'), reply_markup=keyboard)
	else:
            bot.sendMessage(chat_id,grantfehler)

    elif msg['text'] in ["/status"]:
	status = ''
	# Eingänge lesen
        if GPIO.input(13) == GPIO.HIGH:
	    status += _("tx_is_off") + "\n"
        else:
            status += _("tx_is_on") + "\n"
        if GPIO.input(15) == GPIO.HIGH:
            status += _("rx_is_off")
        else:
            status += _("rx_is_on")
	# Laufende Prozesse testen
	for proc in prozesse:
	    status += "\n" + proc + " " + prozesschecker(proc)

	## Temperaturen
	# CPU-Temperaturen auslesen
	tFile = open('/sys/class/thermal/thermal_zone0/temp')
	temp = float(tFile.read())
	tempC = temp/1000
	status += "\n" + _("cpu_temp") + " " + str(round(tempC,1)) + "°C"

	# read the sensors
	i = 0
	for row in sensors:
    	    status += '\n'
    	    status += read_sensor(sensors[i])
    	    i = i + 1

        bot.sendMessage(chat_id, status)

    elif msg['text'] in ["/reboot"]:
	if id in grant:
	    bot.sendMessage(chat_id,_("rebooting_system"))
    	    os.system('sudo shutdown -r now')
	else:
            bot.sendMessage(chat_id,grantfehler)
    else:
	bot.sendMessage(chat_id, _("no_idea_command") + msg['text'] + " "  + vorname + "!\n" + _("cmd_list_with /help."))

    bot.sendMessage(chat_id, befehlsliste(id))

bot = telepot.Bot(apikey)

try:
    ownerinfo(_("start_msg_owner"),owner)
    # MessageLoop(bot,handle).run_as_thread()
    MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
except:
    print(_("bot_is_wrong"))

try:
    while 1:
        time.sleep(10)

except:
    print(_("bot_shutdown"))
    ownerinfo(_("bye_msg_owner"),owner)
    # GPIO.cleanup()
