#!/usr/bin/env python
#coding=utf8

from func import *

def Memory_Get_Info():
	Proc_MemInfo = Read_Proc('meminfo')
	Dick_MemInfo = {}
	for i in Proc_MemInfo:
		Dick_MemInfo[i.split()[0][0:-1]] = int(i.split()[1])
	return Dick_MemInfo

def Memory(data):
	Memory    = Memory_Get_Info()
	MemTotal  = Memory['MemTotal']
	MemFree   = Memory['MemFree']
	Buffers   = Memory['Buffers']
	Cached    = Memory['Cached']
	SwapTotal = Memory['SwapTotal']
	SwapFree  = Memory['SwapFree']

	MemUsage  = MemTotal  - MemFree - Buffers - Cached
	SwapUsage = SwapTotal - SwapFree

	result = {}
	result['MemTotal']   = Bytes(MemTotal)
	result['MemUsage']   = Bytes(MemUsage)
	result['MemBuffers'] = Bytes(Buffers)
	result['MemCached']  = Bytes(Cached)
	result['SwapTotal']  = Bytes(SwapTotal)
	result['SwapUsage']  = Bytes(SwapUsage)

	data['memory'] = result
	return data

