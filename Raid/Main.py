#!/usr/bin/env python
#coding=utf8

from re     import findall
from func   import *
from config import *

def Raid():
	result = {}
	raid   = Cmd('/opt/scripts/Tools/RAID/MegaCli64 -LDInfo -Lall -aALL -NoLog')
	raid   = raid.splitlines()
	info   = Cmd('/opt/scripts/Tools/RAID/MegaCli64 -PDList -aAll -NoLog')
	info   = info.splitlines()

	conn   = len(ReInfo(info, 'IBM FRU'))
	stat   = len(ReInfo(info, 'Firmware state: Online, Spun Up'))
	rtype  = ReInfo(info, 'PD Type')
	size   = ReInfo(info, 'Raw Size')
	sn     = ReInfo(info, 'Inquiry Data')
	dspeed = ReInfo(info, 'Device Speed')
	lspeed = ReInfo(info, 'Link Speed')
	temper = ReInfo(info, 'Drive Temperature')
	dstate = ReInfo(info, 'Firmware state')

	if conn == stat:
		status = True
	else:
		status = False

	result['conn']   = conn
	result['status'] = status
	result['size']   = int(findall( raid_rsize_re, ReInfo(raid, 'Size')[0])[0].split('.')[0])
	result['level']  = int(findall( raid_level_re, ReInfo(raid, 'RAID Level')[0])[0])

	for i in range(conn):
		disk = 'disk_' + str(i)
		result[disk] = {}
		result[disk]['type']   = findall( raid_type_re,   rtype[i])[0]
		result[disk]['sn']     = findall( raid_sn_re,     sn[i])[0]
		result[disk]['dspeed'] = int(findall( raid_dspeed_re, dspeed[i])[0])
		result[disk]['lspeed'] = int(findall( raid_lspeed_re, lspeed[i])[0])
		result[disk]['status'] = disk_status(findall( raid_status_re, dstate[i])[0])
		result[disk]['temper'] = int(findall( raid_temper_re, temper[i])[0])
		result[disk]['size']   = int(findall( raid_size_re , size[i])[0].split('.')[0])

	data['raid'] = result
	return True

def ReInfo(info, res):
	result = []
	for i in info:
		match=findall( '^' + res + '.*' , i)
		if match != []: result.append(match[0])
	return result

def disk_status(str):
	if str == 'Online, Spun Up':
		return True
	else:
		return False
