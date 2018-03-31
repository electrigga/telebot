#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess, re, csv, requests, json, telepot, sys, os, time, datetime, psutil, RPi.GPIO as GPIO
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.loop import MessageLoop
from pprint import pprint

reload(sys)
sys.setdefaultencoding('utf8')

import gettext

# Variablen aus der Config holen
from config import (apikey, grant, owner, botcall, prozesse, dmrid, mmdvmlogs, sensors, gwlogs, mmprefix, logfile, userfile, \
		    mmdvmaufruf, dmrgwaufruf, ysfgw, ircdbbgw, dmrgwaktiv, ysfgwaktiv, ircdbbgwaktiv, gpioports, gpioactive, \
		    svxactive, language)

trans = gettext.translation("telebot", "locale", [language])
trans.install()

# Include SVX-Logic
if svxactive == 1:
    from config import (svxlogic)
    from svxlink import (svxcommands,rep_logic,SVXOff,SVXOn,svx_log,svxlh)

grantfehler = _("granterror")
befehlsliste_usr = ['/lh'],['/status'],['/tg'],['/help']
befehlsliste_syop = "/gpio /sw /svx"
query_data = ''
chatcount = 0

# Initial Keyboard
def initialkb(chat_id,id):
    if chatcount == 0:
	if id in grant:
	    #### Keyboard with init functions
    	    markup = ReplyKeyboardMarkup(keyboard=[
            	    ['/lh', '/status'],
                    ['/tg', '/help'],
		    ['/gpio', '/sw', '/svx']
                 ])
    	    bot.sendMessage(chat_id, _('basic_commands'), reply_markup=markup)
    	else:
	    #### Keyboard with init functions
            markup = ReplyKeyboardMarkup(keyboard=[
                    ['/lh', '/status'],
                    ['/tg', '/help']
                 ])
            bot.sendMessage(chat_id, _('basic_commands'), reply_markup=markup)
	# global chatcount
	# chatcount = chatcount + 1
	globals().update(chatcount=1)

# GPIO Settings
if gpioactive == 1:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for gio in gpioports:
    	GPIO.setup(gio[0], GPIO.OUT)

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


# Timemanipulation
def formdate(datum):
    dat = datetime.datetime.fromtimestamp(datum).strftime('%d.%m.%Y')
    return dat
def formtime(zeit):
    tim = datetime.datetime.fromtimestamp(zeit).strftime('%H:%M')
    return tim

# Funktion zur Information des/der Botowner
def ownerinfo(msg,owner):
    for x in owner:
	bot.sendMessage(x,msg)
	#print(_("owner_msg_fails"))

# Lastheardfunktion (DMR im log)
def lastheard(suchstring):
    if suchstring == '':
	suchstring = "received RF voice header"
    else:
        suchstring = "received RF voice header from " +suchstring
    heard = []
    dateiname = mmdvmlogs + "/" + mmprefix + "-" +(time.strftime("%Y-%m-%d"))+".log"
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
	print(heard)
	found = heard[-1][2] + " " + heard[-1][4] + " " + heard[-1][5] + " " + heard[-1][11] + " " + heard[-1][13] + " "
	if len(heard[-1]) > 14:
	    found = found + heard[-1][14]
        return found

# function to test master connection in gw
def testgw():
    gwerror = []
    suchstring = "Connection to the master has timed out"
    dateiname = gwlogs + "/" + gwprefix + "-" + (time.strftime("%Y-%m-%d"))+".log"
    file = open(dateiname, "r")
    for line in file:
        if line.find(suchstring) > 1:
            string = (line.rstrip())
            # string = string.split(" ")
            gwerror.append(string)
    file.close()
    print(gwerror)
    return _("gw_error")

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
    data = r.json()
    pprint(data)
    tgs = 'Talkgroups:'
    for tg in data['staticSubscriptions']:
        tgs += "\n" + str(tg['talkgroup']) + " im TS" + str(tg['slot'])
    for tg in data['clusters']:
        tgs += "\n" + str(tg['talkgroup']) + " im TS" + str(tg['slot']) + " (" + str(tg['extTalkgroup']) + ")"
    lang = (len(data['timedSubscriptions']))
    i = 0
    while i < lang:
	tgs += "\n"
    	tgs += str(data['timedSubscriptions'][i]['talkgroup']) + " " + _("im") + " TS" + \
               str(data['timedSubscriptions'][i]['slot']) + " " + _("every") + " "
    	if data['timedSubscriptions'][i]['data']['monday'] == 1:
            tgs += _("monday") + " "
    	elif data['timedSubscriptions'][i]['data']['tuesday'] == 1:
            tgs += _("tuesday") + " "
    	elif data['timedSubscriptions'][i]['data']['wednesday'] == 1:
            tgs += _("wednesday") + " "
    	elif data['timedSubscriptions'][i]['data']['thursday'] == 1:
            tgs += _("thursday") + " "
    	elif data['timedSubscriptions'][i]['data']['friday'] == 1:
            tgs += _("friday") + " "
    	elif data['timedSubscriptions'][i]['data']['saturday'] == 1:
            tgs += _("saturday") + " "
    	elif data['timedSubscriptions'][i]['data']['sunday'] == 1:
            tgs += _("sunday") + " "
        tgs += _("subscribtion_starttime") + " " + str(formtime(data['timedSubscriptions'][i]['data']['start'])) + " UTC "
        tgs += _("subscribtion_stoptime") + " " + str(formtime(data['timedSubscriptions'][i]['data']['stop'])) + " UTC "
    	tgs += _("subscribtion_startdate") + " " + formdate(data['timedSubscriptions'][i]['data']['startDate'])
    	tgs += " " + _("subscribtion_enddate") + " " + formdate(data['timedSubscriptions'][i]['data']['endDate'])
    	i = i+1

    if tgs == 'Talkgroups:':
        tgs = _("no_static_tg")
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

###### Callback-Query-Handler Start ######

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    command = query_data.split("_")

### GPIO switcher ###
    if gpioactive == 1:
        for i in range(len(gpioports)):
            if command[0] in gpioports[i]:
                print(str(gpioports[i][0])+" "+str(gpioports[i][1])+" "+str(gpioports[i][2]))
                if command[1] == "on" and gpioports[i][2] == 0:
            	    GPIO.output(gpioports[i][0], GPIO.HIGH)
            	    bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_on"))
                elif command[1] == "on" and gpioports[i][2] == 1:
                    GPIO.output(gpioports[i][0], GPIO.LOW)
		    bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_on"))
                elif command[1] == "off" and gpioports[i][2] == 0:
                    GPIO.output(gpioports[i][0], GPIO.LOW)
		    bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_off"))
                elif command[1] == "off" and gpioports[i][2] == 1:
                    GPIO.output(gpioports[i][0], GPIO.HIGH)
		    bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_off"))

### SVX Handler ####
    if svxactive == 1:
	if query_data == "/killsvx":
	    os.system(SVXOff)
	    bot.answerCallbackQuery(query_id,'SVX' + " " + _("is_off"))
	elif query_data == "/startsvx":
	    os.system(SVXOn)
            bot.answerCallbackQuery(query_id,'SVX' + " " + _("is_on"))
	elif query_data == "/lhecho":
            lhecho = subprocess.check_output('grep "EchoLink QSO state changed to CONNECTED" ' + svx_log + ' | tail -1 | cut -d: -f4', shell=True)
            bot.answerCallbackQuery(query_id,_("last_in_echolink") + ":" + lhecho)
	    bot.sendMessage(from_id,_("last_in_echolink") + ": " + lhecho)

	for i in range(len(svxcommands)):
	    if command[0] in svxcommands[i]:
	    	#print("CMD"+svxcommands[i][0])
	      	svxcmd = "echo " + svxcommands[i][1] + " > " + rep_logic
		print(svxcmd)
		try:
		    os.system(svxcmd)
		    bot.answerCallbackQuery(query_id,svxcommands[i][1] + " " + _('done'))
		except:
		    bot.answerCallbackQuery(query_id,svxcommands[i][1] + " " + _('svx_failure'))
	for i in range(len(svxlh)):
	    if query_data in svxlh[i]:
		string = "grep" + " \"" + svxlh[i][0] + ": Talker" + "\" " + svx_log + '| tail -1 | cut -d: -f6'
		lh = subprocess.check_output(string, shell=True)
		bot.answerCallbackQuery(query_id, _("last_heard") + " " + _("im") + svxlh[i][0] + " " + lh)
		bot.sendMessage(from_id, _("last_heard") + " " + _("im") + " " + svxlh[i][0] + " " + lh)

### Software Handler ####
    if query_data == "/killmmdvm":
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

###### Callback-Query-Handler End ######

###### Chat-Message-Handler Start ######

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    vorname = msg['from']['first_name']
    username = msg['from']['username']
    id = msg['from']['id']
    msg['text'] = msg['text'].lower()

    keyboard = ""

    # print(msg['text'])
    print(msg)

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

    ### SVX Handle ###
    elif msg['text'] in ["/svx"]:
	    if svxactive == 1:
		svxkey = InlineKeyboardMarkup(inline_keyboard=[
			   [
				InlineKeyboardButton(text=_('btn_start_svxlink'), callback_data='/startsvx'),
				InlineKeyboardButton(text=_('btn_stop_svxlink'), callback_data='/killsvx')
			   ],
			   [
				InlineKeyboardButton(text=_('lh_echolink'), callback_data='/lhecho')
			   ]
			])
		bot.sendMessage(chat_id,_('keyboard_svxlink'), reply_markup=svxkey)
		# dynamic section for logics
		btnlogic = [[InlineKeyboardButton(text=logic[0], callback_data=logic[0])] for logic in svxlh]
		keyboard = InlineKeyboardMarkup(inline_keyboard=btnlogic)
		bot.sendMessage(chat_id,_('keyboard_svxlink'), reply_markup=keyboard)
		# dynamic section for DTMF-List
		buttons = [[InlineKeyboardButton(text=cmd[0], callback_data=cmd[1])] for cmd in svxcommands]
		keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            	bot.sendMessage(chat_id,_('keyboard_svxlink'), reply_markup=keyboard)
	    else:
	        bot.sendMessage(chat_id,_("not_activ"))

    ### SW Handle ###
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
                                InlineKeyboardButton(text=_('btn_start_ysfgw'), callback_data='/startysfgw'),
                                InlineKeyboardButton(text=_('btn_stop_ysfgw'), callback_data='/killysfgw')
                        ],
                        [
                                InlineKeyboardButton(text=_('btn_reboot'), callback_data='/reboot')
                        ]
		    ])
	    bot.sendMessage(chat_id,_('keyboard_software'), reply_markup=keyboard)
	else:
	    bot.sendMessage(chat_id,grantfehler)

    #### GPIO handle ####
    elif msg['text'] in ["/gpio"]:
	if gpioactive == 1:
	    if id in grant:
	        keyboard = []
	        buttons = []
	        on = _("on")
	        off = _("off")
	        buttons = [[InlineKeyboardButton(text=gpo[1] + ' ' + on, callback_data=gpo[1] + "_on"),InlineKeyboardButton(text=gpo[1] + ' ' + off, callback_data=gpo[1] + "_off")] for gpo in gpioports]
	        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
	        bot.sendMessage(chat_id,_('gpio'), reply_markup=keyboard)
	        del keyboard, buttons
	    else:
                bot.sendMessage(chat_id,grantfehler)
	else:
	    	bot.sendMessage(chat_id,_("not_activ"))

    elif msg['text'] in ["/testgw"]:
	testgwmc()

    elif msg['text'] in ["/status"]:
	status = ''
	# Eingänge lesen
	if gpioactive == 1:
	    i = 0
            for gio in gpioports:
	  	if gpioports[i][2] == 0:
               	    if GPIO.input(gio[0]) == GPIO.HIGH:
	               status += gio[1].upper() + " " + _("is_on") + "\n"
               	    else:
	           	status += gio[1].upper() + " " + _("is_off") + "\n"
		    i = i + 1
		elif gpioports[i][2] == 1:
                    if GPIO.input(gio[0]) == GPIO.HIGH:
                       status += gio[1].upper() + " " + _("is_off") + "\n"
                    else:
                        status += gio[1].upper() + " " + _("is_on") + "\n"
                    i = i + 1

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

    # bot.sendMessage(chat_id, befehlsliste(id))
    initialkb(chat_id,id)

###### Chat-Message-Handler End ######

bot = telepot.Bot(apikey)

try:
    ownerinfo(_("start_msg_owner"),owner)
    MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
except:
    print(_("bot_is_wrong"))

try:
    while 1:
	# testgwmc()
        time.sleep(10)
except:
    print(_("bot_shutdown"))
    ownerinfo(_("bye_msg_owner"),owner)
    # GPIO.cleanup()
