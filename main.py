#!/usr/bin/env python
#coding=utf8

from Memory.Main import *
from Cpu.Main    import *
from Disk.Main   import *
from Net.Main    import *
from File.Main   import *
from Port.Main   import *
from Local.Main  import *
from Raid.Main   import *
from Squid.Main  import *
from func        import *
from urllib2     import Request, urlopen
from urllib      import urlencode
from threading   import Thread
from json        import dumps, loads
from sys         import argv, exit
from os          import geteuid

def Jdump(data):
	return dumps(data, indent=1)

def Pub(Debug=False):

	TDMList = {
		HostName  : "NULL", Memory    : "NULL",
		Cpu_Usage : "NULL", Cpu_Load  : "NULL",
		Press     : "NULL", Disk_Usage: "NULL",
		Disk_IO   : "NULL", Net_Usage : "NULL",
		File      : "NULL", Port      : "NULL",
		#Disk_IO   : "NULL",
	}

	try:
		argv[1]
	except IndexError:
		pass
	else:
		if argv[1] == "raid" : TDMList[Raid]  = "NULL"
		if argv[1] == "squid": TDMList[Squid] = "NULL"

	for Keys,Value in TDMList.items():
		if Value == "NULL":
			threadings.append(Thread(target=Keys))
		else:
			threadings.append(Thread(target=Keys, args=(Value, )))
	for t in threadings:
		t.setDaemon(True)
		t.start()
	for t in threadings:
		t.join()
	
	if Debug:
		print Jdump(data)

	return loads(Post(data))

def is_root():
	if geteuid() != 0:
		print "Please use the super user root"
		exit(1)

if __name__ == '__main__':
	is_root()
	result = Pub(Debug=False)

	if result.has_key('err_msg'):
		print "Error 001"
		print Jdump(result)
	else:
		print "Upload ok..."
