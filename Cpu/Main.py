#!/usr/bin/env python
#coding=utf8

from func import *
from Local.Main  import *
from time import sleep
from os import listdir

def Read_Cpu_Usage():
	Proc_Stat = Read_Proc('stat')
	for line in Proc_Stat:
		l = line.split()
		if l[0] == "cpu":
			return l

def CPU_Get_Info(Cpu, Proc_Stat):

	Column_Stat = [
		'cpu', 			# 0 CPU ID
		'user',			# 1 从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
		'nice',			# 2 从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
		'system',		# 3 从系统启动开始累计到当前时刻，处于核心态的运行时间
		'idle',			# 4 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
		'iowait',		# 5 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
		'irq',			# 6 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
		'softirq',		# 7 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
		'stealstolen',	# 8 which is the time spent in other operating systems when running in a virtualized environment(since 2.6.11)
		'guest',		# 9 which is the time spent running a virtual  CPU  for  guest operating systems under the control of the Linux kernel(since 2.6.24)
		]
	Docs = 'http://www.aikaiyuan.com/9347.html'
	for Devs in Proc_Stat:
		if Devs.split()[0] == Cpu:
			return dict(zip(Column_Stat, Devs.split()))

def CPU_Count_Add(CPU, CPU_INFO_1, CPU_INFO_2, avg_cpu):
	result   = {}
	idle_1   = float(CPU_INFO_1[4])
	user_1   = float(CPU_INFO_1[1]) + float(CPU_INFO_1[2])
	system_1 = float(CPU_INFO_1[3]) + float(CPU_INFO_1[6]) + float(CPU_INFO_1[7])
	iowait_1 = float(CPU_INFO_1[5])
	total_1  = float(CPU_INFO_1[1]) + float(CPU_INFO_1[2]) + float(CPU_INFO_1[3])

	idle_2   = float(CPU_INFO_2[4])
	user_2   = float(CPU_INFO_2[1]) + float(CPU_INFO_2[2])
	system_2 = float(CPU_INFO_2[3]) + float(CPU_INFO_2[6]) + float(CPU_INFO_2[7])
	iowait_2 = float(CPU_INFO_2[5])
	total_2  = float(CPU_INFO_2[1]) + float(CPU_INFO_2[2]) + float(CPU_INFO_2[3])

	idle   = idle_2   - idle_1
	user   = user_2   - user_1
	system = system_2 - system_1
	iowait = iowait_2 - iowait_1
	total  = idle + user + system + iowait

	result['idle']   = str("%.2f" %(idle   / total * 100))
	result['user']   = str("%.2f" %(user   / total * 100))
	result['system'] = str("%.2f" %(system / total * 100))
	result['iowati'] = str("%.2f" %(iowait / total * 100))
	result['total']  = str("%.2f" %((total_2 - total_1) / ((idle_2 + user_2 + system_2 + iowait_2) - (idle_1 + user_1 + system_1 + iowait_1)) * 100))

	if not avg_cpu.has_key(CPU):
		avg_cpu[CPU] = result
	else:
		avg_cpu[CPU]['idle']   = float(avg_cpu[CPU]['idle'])   + float(result['idle'])
		avg_cpu[CPU]['user']   = float(avg_cpu[CPU]['user'])   + float(result['user'])
		avg_cpu[CPU]['system'] = float(avg_cpu[CPU]['system']) + float(result['system'])
		avg_cpu[CPU]['iowati'] = float(avg_cpu[CPU]['iowati']) + float(result['iowati'])
		avg_cpu[CPU]['total']  = float(avg_cpu[CPU]['total'])  + float(result['total'])

	return avg_cpu

def CPU_Count_CPU(avg_cpu):
	avg_cpu = {}
	CPU_INFO_1, CPU_id = CPU_List()
	sleep(TDM_Sleep)
	CPU_INFO_2, CPU_id = CPU_List()

	for CPU in range(0, len(CPU_INFO_1)):
		CPU_Count_Add(CPU_INFO_1[CPU][0], CPU_INFO_1[CPU], CPU_INFO_2[CPU], avg_cpu)

	return avg_cpu
def Cpu_Usage(data):
	result = {}
	avg_cpu = {}

	avg_cpu = CPU_Count_CPU(avg_cpu)

	for i in avg_cpu:
		for k, v in avg_cpu[i].items():
			avg_cpu[i][k] = str("%.2f" %(float(v)))

	data['cpu'] = avg_cpu
 	return data

def Cpu_Load(data):
	proc_loadavg = ','.join(Read_Proc('loadavg'))
	lavg_1       = proc_loadavg.split()[0]
	lavg_5       = proc_loadavg.split()[1]
	lavg_15      = proc_loadavg.split()[2]

	result = {}
	result['lavg_1']  = lavg_1
	result['lavg_5']  = lavg_5
	result['lavg_15'] = lavg_15
	data['cpuload']   = result

	return data

def Press(data):
	result = {}
	proc_loadavg = ','.join(Read_Proc('loadavg'))
	thread       = proc_loadavg.split()[3].split('/')[1]
	process      = 0
	proc         = listdir('/proc/')
	for i in range(0, len(proc)):
		if cpu_pre_re.match( proc[i] ):
			process = process + 1

	result['thread']   = int(thread)
	result['process']  = int(process)

	data['process'] = result
	return data

def CPU_List():
	Proc_Stat     = Read_Proc('stat')
	CPU_Lists     = []
	CPU_Lists_id  = []
	for Line in Proc_Stat:
		if cpu_cpu_re.match( Line.split()[0] ):
			CPU_Lists.append(Line.split())
			CPU_Lists_id.append(Line.split()[0])
	return CPU_Lists, CPU_Lists_id
