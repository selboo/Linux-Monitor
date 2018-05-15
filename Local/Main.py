#!/usr/bin/env python
#coding=utf8

from func import *

import socket

def GetIP():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	except:
		ip = "255.255.255.255"
	finally:
		s.close()

	return ip

def HostName():
	Proc_HostName = Read_Proc('/sys/kernel/hostname')
	Proc_CpuInfo  = Read_Proc('cpuinfo')
	
	Dick_CpuInfo  = {}
	for i in Proc_CpuInfo:
		if len(i.split()):
			Dick_CpuInfo[i.split()[0]] = i.split()

	result = {}
	result['hostname'] = Proc_HostName[0][:-2]
	result['cpu']      = Dick_CpuInfo['vendor_id'][2]
	result['type']     = Dick_CpuInfo['model'][6] + Dick_CpuInfo['model'][7]
	result['Hz']       = Dick_CpuInfo['model'][-1]
	result['ip']       = GetIP()

	data['host'] = result
	return result

