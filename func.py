#!/usr/bin/env python
#coding=utf8

import os, sys, re
from socket     import AF_INET, socket, inet_ntoa
from socket     import SOCK_DGRAM, SOCK_STREAM
from struct     import pack
from fcntl      import ioctl
from urllib     import urlencode
from urllib2    import Request, urlopen
from hashlib    import md5
from subprocess import Popen, PIPE
from config     import *

def Read_Proc(file):
	proc_file = '/proc/' + file
	proc = open(proc_file, 'r')
	return proc.readlines()

def Read_Sys(face, type, stat='statistics'):
	if stat == 'statistics': sys_file = '/sys/class/net/' + face + '/statistics/' + type
	if stat == 'root'      : sys_file = '/sys/class/net/' + face + '/' + type
	try:
		sys = open(sys_file, 'r')
	except IOError, e:
		return ['Null\n']
	else:
		try:
			return sys.readlines()
		except IOError, e:
			return ['Null\n']
		else:
			return sys.readlines()

def avg(lists):
	Num = 0
	for i in lists:
		Num = Num + float(i)
	return ('%.2f' %(Num / len(lists)))

def Net_Get_IP(Eth):
	Socket = socket(AF_INET, SOCK_DGRAM).fileno
	Pack   = pack('256s', Eth[:15])
	Flags  = 0X8915
	try:
		return inet_ntoa(ioctl(Socket(), Flags, Pack)[20:24])
	except IOError, e:
		return 'Null'
	else:
		return inet_ntoa(ioctl(Socket(), Flags, Pack)[20:24])

def MD5(oFile):
	md5sum = md5()
	mfiles = open(oFile, 'rb')
	md5sum.update(mfiles.read())
	mfiles.close()
	return md5sum.hexdigest()

def Port_Existen(Ports):
	Socket = socket(AF_INET, SOCK_STREAM)
	try:
		Socket.connect(('127.0.0.1', Ports))
		Socket.shutdown(2)
		return 1
	except:
		return 0

def Cmd(cmds):
	p = Popen(str(cmds), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	m = p.stdout.readlines()
	r = []
	for i in range(len(m)):
		r.append(''.join(m[i]))
	return ''.join(r)

def Bytes(integer, Multiple = 1024):
	return integer * Multiple
