#!/usr/bin/env python
#coding=utf8

from Memory.Main import *
from Cpu.Main    import *
from Disk.Main   import *
from Net.Main    import *
from Local.Main  import *
from Raid.Main   import *
from func        import *
from urllib2     import Request, urlopen
from urllib      import urlencode
from threading   import Thread
from json        import dumps, loads
from sys         import argv, exit
from os          import geteuid
from time        import sleep

def Jdump(data):
	return dumps(data, indent=1)

def Run(Debug=False):

	data = {}
	threadings = []

	TDMList = {
		HostName  : "NULL", 
		Memory    : "NULL",
		Net_Usage : "NULL",
		Press     : "NULL", 
		Cpu_Usage : "NULL", 
		Cpu_Load  : "NULL",
		Disk_Usage: "NULL",
		Disk_IO   : "NULL", 
	}

	for Keys,Value in TDMList.items():
		threadings.append(Thread(target=Keys, args=(data, )))
	for t in threadings:
		t.start()
	for t in threadings:
		t.join()
	
	return data

def is_root():
	if geteuid() != 0:
		print "Please use the super user root"
		exit(1)

if __name__ == '__main__':
	is_root()
	while True:
		sleep(1)
		result = Run(Debug=False)
		print Jdump(result)

