from config import SVXOn,SVXOff

rep_logic = "/home/pi/remote/svx_pty.RepeaterLogic"

svxcommands = [
		['link341','*950# 341#'],
		['link951','*340# 951'],
		['SvxSyopOff','*OFFCMD#'],
		['SvxSysopOn','*OnlineCMD#']
	      ]
