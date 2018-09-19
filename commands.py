



#pi-star stuff
###ab zeile 1398
psstop_mmdvm_dstar = "sudo crudini --set /etc/mmdvmhost D-Star Enable 0 && sudo crudini --set /etc/mmdvmhost 'D-Star Network' enable 0"
psstart_mmdvm_dstar = "sudo crudini --set /etc/mmdvmhost D-Star Enable 1 && sudo crudini --set /etc/mmdvmhost 'D-Star Network' enable 1"
#################
psstop_mmdvm_p25 = "sudo crudini --set /etc/mmdvmhost P25 Enable 0 && sudo crudini --set /etc/mmdvmhost 'P25 Network' Enable 0"
psstart_mmdvm_p25 = "sudo crudini --set /etc/mmdvmhost P25 Enable 1 && sudo crudini --set /etc/mmdvmhost 'P25 Network' Enable 1 && sudo crudini --set /etc/ysf2p25 'P25 Network' enable 0"
##################################
psstop_mmdvm_ysf = "sudo crudini --set /etc/mmdvmhost 'System Fusion' enable 0 && sudo crudini --set /etc/mmdvmhost 'System Fusion Network' enable 0"
psstart_mmdvm_ysf = "sudo crudini --set /etc/mmdvmhost 'System Fusion' enable 1 && sudo crudini --set /etc/mmdvmhost 'System Fusion Network' enable 1 && sudo crudini --set /etc/dmr2ysf Enable Enable 0"
#############################
#1468
psstop_mmdvm_ysf2dmr="sudo crudini --set /etc/ysf2dmr Enabled Enabled 0"
psstart_mmdvm_ysf2dmr="sudo crudini --set /etc/ysf2dmr Enabled Enabled 1"
		  
	  
psstop_mmdvm_dmr = "sudo crudini --set /etc/mmdvmhost DMR enable 0 && sudo crudini --set /etc/mmdvmhost 'DMR Network' enable 0"
psstart_mmdvm_dmr = "sudo crudini --set /etc/mmdvmhost DMR enable 1 && sudo crudini --set /etc/mmdvmhost 'DMR Network' enable 1 && sudo crudini --set /etc/ysf2dmr Enabled Enabled 0"

psstart_mmdvm_dmrxlx = "sudo crudini --set /etc/dmrgateway 'XLX Network' Enabled 1 && sudo crudini --set /etc/dmrgateway 'XLX Network 1' Enabled 1"
psstop_mmdvm_dmrxlx = "sudo crudini --set /etc/dmrgateway 'XLX Network' Enabled 0 && sudo crudini --set /etc/dmrgateway 'XLX Network 1' Enabled 0"

psstop_mmdvm_pocsag = "sudo crudini --set /etc/mmdvmhost POCSAG enable 0 && sudo crudini --set /etc/mmdvmhost 'POCSAG Network' enable 0"
psstart_mmdvm_pocsag = "sudo crudini --set /etc/mmdvmhost POCSAG enable 1 && sudo crudini --set /etc/mmdvmhost 'POCSAG Network' enable 1"

rpirw = "sudo mount -o remount,rw /"
rpiro = "sudo mount -o remount,ro /"
psstop = "sudo mount -o remount,rw / && sudo systemctl stop cron.service > /dev/null 2>/dev/null & sudo systemctl stop dstarrepeater.service > /dev/null 2>/dev/null & sudo systemctl stop mmdvmhost.service > /dev/null 2>/dev/null & sudo systemctl stop ircddbgateway.service > /dev/null 2>/dev/null & sudo systemctl stop timeserver.service > /dev/null 2>/dev/null & sudo systemctl stop pistar-watchdog.service > /dev/null 2>/dev/null & sudo systemctl stop pistar-remote.service > /dev/null 2>/dev/null & sudo systemctl stop ysfgateway.service > /dev/null 2>/dev/null & sudo systemctl stop ysf2dmr.service > /dev/null 2>/dev/null & sudo systemctl stop ysf2nxdn.service > /dev/null 2>/dev/null & sudo systemctl stop ysf2p25.service > /dev/null 2>/dev/null & sudo systemctl stop nxdn2dmr.service > /dev/null 2>/dev/null & sudo systemctl stop ysfparrot.service > /dev/null 2>/dev/null & sudo systemctl stop p25gateway.service > /dev/null 2>/dev/null & sudo systemctl stop p25parrot.service > /dev/null 2>/dev/null & sudo systemctl stop nxdngateway.service > /dev/null 2>/dev/null & sudo systemctl stop nxdnparrot.service > /dev/null 2>/dev/null & sudo systemctl stop dmr2ysf.service > /dev/null 2>/dev/null & sudo systemctl stop dmr2nxdn.service > /dev/null 2>/dev/null & sudo systemctl stop dmrgateway.service > /dev/null 2>/dev/null & sudo systemctl stop dapnetgateway.service > /dev/null 2>/dev/null"
psstart = "sudo systemctl daemon-reload > /dev/null 2>/dev/null & sudo systemctl start dstarrepeater.service > /dev/null 2>/dev/null & sudo systemctl start mmdvmhost.service > /dev/null 2>/dev/null & sudo systemctl start ircddbgateway.service > /dev/null 2>/dev/null & sudo systemctl start timeserver.service > /dev/null 2>/dev/null & sudo systemctl start pistar-watchdog.service > /dev/null 2>/dev/null & sudo systemctl start pistar-remote.service > /dev/null 2>/dev/null & sudo systemctl start ysf2dmr.service > /dev/null 2>/dev/null & sudo systemctl start ysf2nxdn.service > /dev/null 2>/dev/null & sudo systemctl start ysf2p25.service > /dev/null 2>/dev/null & sudo systemctl start nxdn2dmr.service > /dev/null 2>/dev/null & sudo systemctl start ysfgateway.service > /dev/null 2>/dev/null & sudo systemctl start ysfparrot.service > /dev/null 2>/dev/null & sudo systemctl start p25gateway.service > /dev/null 2>/dev/null & sudo systemctl start p25parrot.service > /dev/null 2>/dev/null & sudo systemctl start nxdngateway.service > /dev/null 2>/dev/null & sudo systemctl start nxdnparrot.service > /dev/null 2>/dev/null & sudo systemctl start dmr2ysf.service > /dev/null 2>/dev/null & sudo systemctl start dmr2nxdn.service > /dev/null 2>/dev/null & sudo systemctl start dmrgateway.service > /dev/null 2>/dev/null & sudo systemctl start dapnetgateway.service > /dev/null 2>/dev/null & sudo systemctl start cron.service > /dev/null 2>/dev/null & sudo mount -o remount,ro /"