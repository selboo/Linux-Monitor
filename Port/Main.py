#!/usr/bin/env python
#coding=utf8

from func import *
from re     import findall

def Port():
	result = {}
	listen = Cmd('netstat -anlp | grep "LISTEN "')
	listen = listen.splitlines()
	for Port in Port_Watch:
		lists = ReInfo(listen, str(Port))
		if not lists: continue

		conn = Cmd('netstat -anl | grep :%d | grep %s | wc -l' %(Port, 'EST'))
		
		result[Port] = {}
		pid, name    = findall( port_p_na_re, lists)[0].rstrip().split('/')

		result[Port]['name'] = findall( port_name_re, name )[0]
		result[Port]['pid']  = int(pid)
		result[Port]['conn'] = int(conn)
		
	data['port'] = result
	return result

def ReInfo(info, res):
	result = []
	for i in info:
		match=findall( '.*' + res + '.*' , i)
		if match != []:
			return match[0]

			result.append(match[0])
			return result