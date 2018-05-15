#!/usr/bin/env python
#coding=utf8

from func import *
from time import sleep

def Net_Usage():
	result = {}

	'''
		keys    eth0
		Status  /sys/class/net/keys/operstate or /sys/class/net/keys/carrier
				http://stackoverflow.com/questions/808560/how-to-detect-the-physical-connected-state-of-a-network-cable-connector
		ipaddr  NULL

	'''
	NetType = {
		'speed'      : ['root',       'speed'     ],
		'address'    : ['root',       'mac'       ],
		'duplex'     : ['root',       'duplex'    ],  # half , full
		'operstate'  : ['root',       'status'    ],
		'ip'         : ['root',       'ip'        ],
		}
	
	Net_Type = [
		'rx_bytes', 'rx_packets', 'rx_dropped', 'rx_errors',
		'tx_bytes', 'tx_packets', 'tx_dropped', 'tx_errors',
		]

	for i in Net_Face():
		avg_net[i] = {}
		for k, v in NetType.items():
			if v[1] == 'ip':
				avg_net[i][v[1]] = Net_Get_IP(i)
			else:
				avg_net[i][v[1]] = str(Read_Sys(i, k, v[0])[0].split('\n')[0])

	for i in range(0, TDM_Number):
		Net_Count(Net_Type)

 	all_net = {
		"rx_bytes"   : 0,
		"rx_packets" : 0,
		"rx_dropped" : 0,
		"rx_errors"  : 0,
		"tx_bytes"   : 0,
		"tx_packets" : 0,
		"tx_dropped" : 0,
		"tx_errors"  : 0
	}

	for i in avg_net:
		for v in Net_Type:
			avg_net[i][v] = int(avg_net[i][v]) / TDM_Number
			if i != 'lo':
				all_net[v] = all_net.get(v) + avg_net[i][v]

	data['net_us'] = avg_net
	data['net_us']["all"] = all_net
	return True

def Net_Count(Net_Type):
	
	result_1 = {}
	result_2 = {}

	for i in Net_Face():
		result_1[i] = {}
		result_1[i]['rx_bytes']   = long(Read_Sys(i, 'rx_bytes'  )[0])
		result_1[i]['rx_packets'] = long(Read_Sys(i, 'rx_packets')[0])
		result_1[i]['rx_dropped'] = long(Read_Sys(i, 'rx_dropped')[0])
		result_1[i]['rx_errors']  = long(Read_Sys(i, 'rx_errors' )[0])
		result_1[i]['tx_bytes']   = long(Read_Sys(i, 'tx_bytes'  )[0])
		result_1[i]['tx_packets'] = long(Read_Sys(i, 'tx_packets')[0])
		result_1[i]['tx_dropped'] = long(Read_Sys(i, 'tx_dropped')[0])
		result_1[i]['tx_errors']  = long(Read_Sys(i, 'tx_errors' )[0])

	sleep(TDM_Sleep)

	for i in Net_Face():
		result_2[i] = {}
		result_2[i]['rx_bytes']   = long(Read_Sys(i, 'rx_bytes'  )[0])
		result_2[i]['rx_packets'] = long(Read_Sys(i, 'rx_packets')[0])
		result_2[i]['rx_dropped'] = long(Read_Sys(i, 'rx_dropped')[0])
		result_2[i]['rx_errors']  = long(Read_Sys(i, 'rx_errors' )[0])
		result_2[i]['tx_bytes']   = long(Read_Sys(i, 'tx_bytes'  )[0])
		result_2[i]['tx_packets'] = long(Read_Sys(i, 'tx_packets')[0])
		result_2[i]['tx_dropped'] = long(Read_Sys(i, 'tx_dropped')[0])
		result_2[i]['tx_errors']  = long(Read_Sys(i, 'tx_errors' )[0])

	for i in Net_Face():
		for l in Net_Type:
			if not avg_net[i].has_key(l):
				avg_net[i][l] = 0
		avg_net[i]['rx_bytes']   = avg_net[i]['rx_bytes']   + result_2[i]['rx_bytes']   - result_1[i]['rx_bytes']
		avg_net[i]['rx_packets'] = avg_net[i]['rx_packets'] + result_2[i]['rx_packets'] - result_1[i]['rx_packets']
		avg_net[i]['rx_dropped'] = avg_net[i]['rx_dropped'] + result_2[i]['rx_dropped'] - result_1[i]['rx_dropped']
		avg_net[i]['rx_errors']  = avg_net[i]['rx_errors']  + result_2[i]['rx_errors']  - result_1[i]['rx_errors']
		avg_net[i]['tx_bytes']   = avg_net[i]['tx_bytes']   + result_2[i]['tx_bytes']   - result_1[i]['tx_bytes']
		avg_net[i]['tx_packets'] = avg_net[i]['tx_packets'] + result_2[i]['tx_packets'] - result_1[i]['tx_packets']
		avg_net[i]['tx_dropped'] = avg_net[i]['tx_dropped'] + result_2[i]['tx_dropped'] - result_1[i]['tx_dropped']
		avg_net[i]['tx_errors']  = avg_net[i]['tx_errors']  + result_2[i]['tx_errors']  - result_1[i]['tx_errors']

	return True

def Net_Face():
	Proc_Net_Dev = Read_Proc('net/dev')
	ExcludeType  = ['Inter-|', 'face', 'usb0']
	Facelist     = []

	for Face in Proc_Net_Dev:
		if Face.split()[0].split(':')[0] not in ExcludeType:
			Facelist.append(Face.split()[0].split(':')[0])

	return Facelist

