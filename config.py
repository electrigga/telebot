# -*- coding: utf-8 -*-

# Hier den API Schlüssel eintragen, den man vom Botfather erhalten hat
apikey = ""

# ACL für die Steuerung User ID here
grant = [,]

# ID des Botowner / der Botowner (die bekommen Nachrichten über Statusänderungen)
owner = []

# Rufzeichen/Name des Repeaters, auf dem der Bot läuft
botcall = ""

# Liste mit zu prüfenden Prozessen
prozesse=["","",""]

# ID des Repeaters
dmrid = ""

# folder which contains mmdvm-logs
mmdvmlogs = "/var/log/mmdvm"

# define pathes to 1-wire sensor data 
sensors = [
  ["/sys/bus/w1/devices/28-03b429126461/w1_slave","Sender"],
  ["/sys/bus/w1/devices/28-559d29126461/w1_slave","Empfänger"],
  ["/sys/bus/w1/devices/28-a4ad29126461/w1_slave","Netzteil"]
]
