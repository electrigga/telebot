## Set path to Svxlink symlink > svxlink.conf "DTMF_CTRL_PTY=/path/to/pty" Repeater/SvxlinkLogic

rep_logic = "/home/pi/remote/svx_pty.RepeaterLogic"

# path to svxlink.log (LastHeard Echolink)

svx_log = "/var/log/svxlink.log"

# Set DTMF Commands ['ButtonName','DTMF-Command']
# Repeater need Open Command DTMF * or other

svxcommands = [
                ['link Thr','*950# 341#'],
                ['link ATA','*340# 951#'],
#               ['SvxSyopOff','*986170#'],
#               ['SvxSysopOn','986171#'],
                ['Ansage Info ','**#'],
                ['SVXOn','986171#'],
                ['SVXOff','*986170#'],
                ['Trennen','##']
              ]

# SvxLink start & Stop Command

SVXOff =  'sudo systemctl stop svxlink.service'
SVXOn =  'sudo systemctl start svxlink.service'

### Lastheard in ReflectorLogic

svxlh = [
          ['THR_Logic'],
          ['ATA_Logic']
        ]


