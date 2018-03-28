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
        if id in grant:
            keyboard = []
            buttons = []
            on = _("on")
            off = _("off")
            buttons = [[InlineKeyboardButton(text=gpo[1] + ' ' + on, callback_data=gpo[1] + "_on"),InlineKeyboardButton(text=gpo[1] + ' ' + off, callback_data=gpo[1] + "_off")] for gpo in gpioports]
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            bot.sendMessage(chat_id,_('keyboard_software'), reply_markup=keyboard)
            del keyboard, buttons
        else:
            bot.sendMessage(chat_id,grantfehler)

    elif msg['text'] in ["/testgw"]:
        testgwmc()

    elif msg['text'] in ["/status"]:
        status = ''
        # Eingänge lesen
        for gio in gpioports:
           if GPIO.input(gio[0]) == GPIO.HIGH:
               status += gio[1].upper() + " " + _("is_on") + "\n"
           else:
               status += gio[1].upper() + " " + _("is_off") + "\n"

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

###### Chat-Message-Handler End ######
