rep_logic = "/home/pi/remote/svx_pty.RepeaterLogic"
svx_log = "/var/log/svxlink.log"

SVXOff =  'sudo systemctl stop svxlink.service'
SVXOn =  'sudo systemctl start svxlink.service'

### DTMF Commands
svxcommands = [
		['link341','*950# 341#'],
		['link951','*340# 951'],
		['SvxSyopOff','*OFFCMD#'],
		['SvxSysopOn','*OnlineCMD#']
	      ]

### Lastheard for locig
svxlh = [
	  ['THR_Logic'],
	  ['ATA_Logic']
	]
