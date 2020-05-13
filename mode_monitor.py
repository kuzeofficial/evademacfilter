#! /usr/bin/env python
#! -*- coding: utf-8 -*-

#Author: Cristian Fonseca Comas
#Age: 17
#Date:may 4 of 2020
#Aka: Kuze
from colorama import Fore,Style
import optparse, subprocess
import time
def data_parse():
	parser = optparse.OptionParser()
	parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC Address")
	parser.add_option("-d","--moninterf",dest="moninterf",help="Interface monitor mode")
	(options, args) = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify the interface, use --help for more info")
	elif not options.moninterf:
		parser.error("[-] Please specify the monitor interface ")
	else:
		return options

def start_monitor(moninterf,interface):
	print(Fore.GREEN+"Stopping conflicting services..."+Style.RESET_ALL)
	subprocess.call(["airmon-ng","check","kill"])
	time.sleep(2)
	print(Fore.GREEN+"Changing regdomain to BO..."+Style.RESET_ALL)
	subprocess.call(["iw","reg","set","BO"])
	subprocess.call(["iw","phy0","interface","add",moninterf,"type","monitor"])
	time.sleep(1)
	subprocess.call(["ifconfig",moninterf,"down"])
	subprocess.call(["macchanger","-A",moninterf])
	time.sleep(1)
	subprocess.call(["ifconfig",moninterf,"up"])
	time.sleep(1)
	subprocess.call(["iw","dev",moninterf,"set","channel","11"])
	#random_mac = subprocess.call(["macchanger","-s",moninterf,"|","grep","Current","|","cut","-d","' '","-f","5-"])
	#setchannel=subprocess.call(["iwlist",moninterf,"channel","|","grep","Current","|","awk","'{print $4,$5}'","|","tr","-dc","'0-9'"])
	print(Fore.GREEN+"Creating monitor VAP "+moninterf+"from phy0 channel 11"+Style.RESET_ALL)
	print(Fore.GREEN+"Deleting managed VAP "+interface+Style.RESET_ALL)
	subprocess.call(["ifconfig",interface,"down"])
	subprocess.call(["iw","dev",interface,"del"])
	subprocess.call(["iw","dev",moninterf,"set","txpower","fixed","3000"])
	time.sleep(1)
	subprocess.call(["airmon-ng"])
	raw_input("Press any key to continue? ")
def stop_monitor(moninterf,interface):
	print (Fore.GREEN+"Disabling airplane mode if enabled..."+Style.RESET_ALL)
	subprocess.call(["rfkill","unblock","all"])
	print(Fore.GREEN+"Killing all monitor mode VAPs and return to normal state..."+Style.RESET_ALL)
	print (Fore.GREEN+"Restoring regdomain to US..."+Style.RESET_ALL)
	subprocess.call(["iw","reg","set","US"])
	print (Fore.GREEN+"Deleting monitor VAP "+moninterf+Style.RESET_ALL)
	subprocess.call(["iw","dev",moninterf,"del"])
	time.sleep(1)
	print(Fore.GREEN+"Creating managed VAP "+interface+" from phy0"+Style.RESET_ALL)
	subprocess.call(["iw","phy0","interface","add",interface,"type","managed"])
	time.sleep(1)
	subprocess.call(["ifconfig",interface,"up"])
	print(Fore.GREEN+"Starting Network Services..."+Style.RESET_ALL)
	subprocess.call(["service","NetworkManager","start"])
	#subprocess.call(["service","avahi-daemon","start"])

options = data_parse()
start_monitor(options.moninterf,options.interface)
stop_monitor(options.moninterf,options.interface)