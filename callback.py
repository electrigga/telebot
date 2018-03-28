###### Callback-Query-Handler Start ######

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

### GPIO switcher ###

    command = query_data.split("_")
    for i in range(len(gpioports)):
        if command[0] in gpioports[i]:
            print(str(gpioports[i][0])+str(gpioports[i][1])+str(gpioports[i][2]))
            if command[1] == "on" and gpioports[i][2] == 0:
                GPIO.output(gpioports[i][0], GPIO.HIGH)
                bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_on"))
            elif command[1] == "on" and gpioports[i][2] == 1:
                GPIO.output(gpioports[i][0], GPIO.LOW)
                bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_off"))
            elif command[1] == "off" and gpioports[i][2] == 0:
                GPIO.output(gpioports[i][0], GPIO.LOW)
                bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_off"))
            elif command[1] == "off" and gpioports[i][2] == 1:
                GPIO.output(gpioports[i][0], GPIO.HIGH)
                bot.answerCallbackQuery(query_id,gpioports[i][1] + " " + _("is_on"))

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
