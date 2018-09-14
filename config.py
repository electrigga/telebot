# -*- coding: utf-8 -*-

# prefered language
# translations available
# de = deutsch, en = english, sv = svenska, da = dansk, sl = Slovenski
language = "de"

# api_key you got from @botfather for your bot
apikey = ""

# brandmeister api
bmapiactive = 1
bmapi = ""

# ACL for controll the repeater (your own ID should in here) (ID is NOT @username)
grant = []

# ID des Botowner / der Botowner (die bekommen Nachrichten über Statusänderungen)
owner = []

# Call of repeater
botcall = ""

# Liste of processes
prozesse=["MMDVMHost","DMRGateway","YSFGateway","ircddbgatewayd"]

# ID des Repeaters
dmrid = ""

# folder which contains mmdvm-logs
pistar_mmdvmlogs = "/var/log/pi-star"
mmdvmlogs = "/var/log/mmdvm"
mmprefix = "MMDVM"

# folder wich contains the dmr-gw logfiles
pistar_gwlogs = "/var/log/pi-star"
gwlogs = "/var/log/mmdvm"
gwprefix = "DMRGateway"

# how to start mmdvm
mmdvmaufruf = "/usr/bin/screen -d -m -S MMDVM /home/pi/MMDVMHost/MMDVMHost /home/pi/MMDVMHost/MMDVM-DB0SBN.ini"
# how to start dmrgw should it be active?
dmrgwaufruf = "/usr/bin/screen -d -m -S DMRGW /home/pi/DMRGateway/DMRGateway /home/pi/DMRGateway/DMRGateway.ini"
dmrgwaktiv = 1
# how to start ysfgw
ysfgw = "sudo /etc/init.d/YSFGateway.sh start"
ysfgwaktiv = 1
# how to start ircdbbgw
ircdbbgw = "sudo /etc/init.d/ircddbgateway start"
ircdbbgwaktiv = 1


logfile = "botlog.txt"
userfile = "users.csv"

# define pathes to 1-wire sensor data
sensors = [
  ["/sys/bus/w1/devices/28-24d329126461/w1_slave","KA 1"],
  ["/sys/bus/w1/devices/28-a78d29126461/w1_slave","KA 2"]
]

# define gpio ports
gpioactive = 1
gpioports = [
  # [gpio number,"name",invers]
  [11,"TX",0],
  [12,"RX",0],
  [13,"NS1",0],
]

#### SVXLink Settings
svxactive = 0
svxlogic = "/home/pi/remote/svx_pty.RepeaterLogic"

ispistar = 1


#pi-star stuff
###ab zeile 1398
psstopmmdvmdmr = "sudo crudini --set /etc/mmdvmhost 'D-Star Enable 0 & sudo crudini --set /etc/mmdvmhost 'D-Star Network' enable 0"
psstartmmdvmdmr = "sudo crudini --set /etc/mmdvmhost 'D-Star Network' enable 1 & sudo crudini --set /etc/mmdvmhost 'D-Star Network' enable 1"
#################
psstopmmdvmp25 = "sudo crudini --set /etc/mmdvmhost P25 Enable 0 & sudo crudini --set /etc/mmdvmhost P25 Enable 0"
psstartmmdvmp25 = "sudo crudini --set /etc/mmdvmhost P25 Enable 1 & sudo crudini --set /etc/mmdvmhost P25 Enable 1 & sudo crudini --set /etc/ysf2p25 'P25 Network' enable 0"
##################################
psstopmmdvmysf = "sudo crudini --set /etc/mmdvmhost 'System Fusion' enable 0 & sudo crudini --set /etc/mmdvmhost 'System Fusion Network' enable 0"
psstartmmdvmysf = "sudo crudini --set /etc/mmdvmhost 'System Fusion' enable 1 & sudo crudini --set /etc/mmdvmhost 'System Fusion Network' enable 1 & sudo crunini --set /etc/dmr2ysf Enable Enable 0"
#############################
#1468
psstopmmdvmysf2dmr="sudo crudini --set /etc/ysf2dmr Enable Enable 0"
psstartmmdvmysf2dmr="sudo crudini --set /etc/ysf2dmr Enable Enable 1"
		  
		  
psstopmmdvmdmr = "sudo crudini --set /etc/mmdvmhost DMR enable 0 & sudo crudini --set /etc/mmdvmhost 'DMR Network' enable 0"
psstartmmdvmdmr = "sudo crudini --set /etc/mmdvmhost DMR enable 1 & sudo crudini --set /etc/mmdvmhost 'DMR Network' enable 1 & sudo crudini --set /etc/ysf2dmr Enable enable 0"
psstopmmdvmpocsag = "sudo crudini --set /etc/mmdvmhost POCSAG enable 0 & sudo crudini --set /etc/mmdvmhost 'POCSAG Network' enable 0"
psstartmmdvmpocsag = "sudo crudini --set /etc/mmdvmhost POCSAG enable 1 & sudo crudini --set /etc/mmdvmhost 'POCSAG Network' enable 1"
psstop="sudo mount -o remount,rw  / && sudo systemctl stop cron.service > /dev/null 2>/dev/null & sudo systemctl stop dstarrepeater.service > /dev/null 2>/dev/null & sudo systemctl stop mmdvmhost.service > /dev/null 2>/dev/null & sudo systemctl stop ircddbgateway.service > /dev/null 2>/dev/null & sudo systemctl stop timeserver.service > /dev/null 2>/dev/null & sudo systemctl stop pistar-watchdog.service > /dev/null 2>/dev/null & sudo systemctl stop pistar-remote.service > /dev/null 2>/dev/null & sudo systemctl stop ysfgateway.service > /dev/null 2>/dev/null & sudo systemctl stop ysf2dmr.service > /dev/null 2>/dev/null & sudo systemctl stop ysf2nxdn.service > /dev/null 2>/dev/null & sudo systemctl stop ysf2p25.service > /dev/null 2>/dev/null & sudo systemctl stop nxdn2dmr.service > /dev/null 2>/dev/null & sudo systemctl stop ysfparrot.service > /dev/null 2>/dev/null & sudo systemctl stop p25gateway.service > /dev/null 2>/dev/null & sudo systemctl stop p25parrot.service > /dev/null 2>/dev/null & sudo systemctl stop nxdngateway.service > /dev/null 2>/dev/null & sudo systemctl stop nxdnparrot.service > /dev/null 2>/dev/null & sudo systemctl stop dmr2ysf.service > /dev/null 2>/dev/null & sudo systemctl stop dmr2nxdn.service > /dev/null 2>/dev/null & sudo systemctl stop dmrgateway.service > /dev/null 2>/dev/null & sudo systemctl stop dapnetgateway.service > /dev/null 2>/dev/null"
psstart="sudo systemctl daemon-reload > /dev/null 2>/dev/null & sudo systemctl start dstarrepeater.service > /dev/null 2>/dev/null & sudo systemctl start mmdvmhost.service > /dev/null 2>/dev/null & sudo systemctl start ircddbgateway.service > /dev/null 2>/dev/null & sudo systemctl start timeserver.service > /dev/null 2>/dev/null & sudo systemctl start pistar-watchdog.service > /dev/null 2>/dev/null & sudo systemctl start pistar-remote.service > /dev/null 2>/dev/null & sudo systemctl start ysf2dmr.service > /dev/null 2>/dev/null & sudo systemctl start ysf2nxdn.service > /dev/null 2>/dev/null & sudo systemctl start ysf2p25.service > /dev/null 2>/dev/null & sudo systemctl start nxdn2dmr.service > /dev/null 2>/dev/null & sudo systemctl start ysfgateway.service > /dev/null 2>/dev/null & sudo systemctl start ysfparrot.service > /dev/null 2>/dev/null & sudo systemctl start p25gateway.service > /dev/null 2>/dev/null & sudo systemctl start p25parrot.service > /dev/null 2>/dev/null & sudo systemctl start nxdngateway.service > /dev/null 2>/dev/null & sudo systemctl start nxdnparrot.service > /dev/null 2>/dev/null & sudo systemctl start dmr2ysf.service > /dev/null 2>/dev/null & sudo systemctl start dmr2nxdn.service > /dev/null 2>/dev/null & sudo systemctl start dmrgateway.service > /dev/null 2>/dev/null & sudo systemctl start dapnetgateway.service > /dev/null 2>/dev/null & sudo systemctl start cron.service > /dev/null 2>/dev/null & sudo mount -o remount,ro /"