#!/usr/bin/env python
#coding=utf8

from os import statvfs
from func import *
from Local.Main  import *
from time import sleep
from copy import deepcopy

def Disk_Get_Info(Dev, Proc_Diskstats):

	Column_Diskstats = [
		'm', 			# 主设备号
		'mm', 			# 磁盘设备号
		'dev', 			# 磁盘设备名
		'reads', 		# number of read I/Os processed
		'rd_mrg', 		# number of read I/Os merged with in-queue I/O
		'rd_sectors', 	# number of sectors read
		'ms_reading', 	# total wait time for read requests
		'writes', 		# number of write I/Os processed
		'wr_mrg', 		# number of write I/Os merged with in-queue I/O
		'wr_sectors', 	# number of sectors written
		'ms_writing', 	# total wait time for write requests
		'cur_ios', 		# number of I/Os currently in flight
		'ms_doing_io', 	# total time this block device has been active
		'ms_weighted'	# total wait time for all requests
		]
	Docs = 'https://www.kernel.org/doc/Documentation/block/stat.txt'
	for Devs in Proc_Diskstats:
		if Devs.split()[2] == Dev:
			return dict(zip(Column_Diskstats, Devs.split()))
	return {}

def Disk_Count_Add(Dev, Proc_Diskstats_1, Proc_Diskstats_2, avg_io):
	result = {}
	A_Disk_Info  = Disk_Get_Info(Dev, Proc_Diskstats_1)
	A_Reads_KB_1 = float(A_Disk_Info['rd_sectors'])
	A_Write_KB_2 = float(A_Disk_Info['wr_sectors'])
	A_Reads_IO_1 = float(A_Disk_Info['rd_mrg'])
	A_Write_IO_2 = float(A_Disk_Info['wr_mrg'])

	B_Disk_Info  = Disk_Get_Info(Dev, Proc_Diskstats_2)
	B_Reads_KB_1 = float(B_Disk_Info['rd_sectors'])
	B_Write_KB_2 = float(B_Disk_Info['wr_sectors'])
	B_Reads_IO_1 = float(B_Disk_Info['rd_mrg'])
	B_Write_IO_2 = float(B_Disk_Info['wr_mrg'])

	result["Reads_KB"] = Bytes(B_Reads_KB_1 - A_Reads_KB_1)
	result["Write_KB"] = Bytes(B_Write_KB_2 - A_Write_KB_2)
	result["Reads_IO"] = B_Reads_IO_1 - A_Reads_IO_1
	result["Write_IO"] = B_Write_IO_2 - A_Write_IO_2

	if not avg_io.has_key(Dev):
		avg_io[Dev] = result
	else:
		avg_io[Dev]['Reads_KB'] = avg_io[Dev]['Reads_KB'] + result['Reads_KB']
		avg_io[Dev]['Write_KB'] = avg_io[Dev]['Write_KB'] + result['Write_KB']
		avg_io[Dev]['Reads_IO'] = avg_io[Dev]['Reads_IO'] + result['Reads_IO']
		avg_io[Dev]['Write_IO'] = avg_io[Dev]['Write_IO'] + result['Write_IO']
	
	return avg_io


def Disk_Count_IO(All_Devices, avg_io):
	Proc_Diskstats_1 = Read_Proc('diskstats')
	sleep(TDM_Sleep)
	Proc_Diskstats_2 = Read_Proc('diskstats')

	for Dev in All_Devices:
		Disk_Count_Add(Dev, Proc_Diskstats_1, Proc_Diskstats_2, avg_io)

	return avg_io

def Disk_IO(data):
	Result = {}
	avg_io = {}

	Partitions, Devices = Disk_Partitions()

	for i in Devices:
		Devs = str(disk_dev_re.findall(i)[0])
		if Devs not in Devices:
			Devices.append(Devs)

	avg_io = Disk_Count_IO(Devices, avg_io)

	all_io = {
		"Reads_IO" : 0,
		"Write_IO" : 0,
		"Reads_KB" : 0,
		"Write_KB" : 0
	}

	for i in avg_io:
		for k, v in avg_io[i].items():
			avg_io[i][k] = int(v)
			all_io[k] = all_io.get(k) + avg_io[i][k]

	data['disk_io'] = avg_io
	data['disk_io']['all'] = all_io
	return data

def Disk_Usage(data):
	All_Disk_Total, All_Disk_Free, All_Disk_Used = 0, 0, 0
	All_Inode_Total, All_Inode_Used, All_Inode_Free = 0, 0, 0
	Partitions, Devices = Disk_Partitions()
	Usage      = {}
	for Partition in Partitions:
		Disk_Stat  = statvfs(Partition)
		Disk_Free  = (Disk_Stat.f_bfree  * Disk_Stat.f_frsize) / 1024
		Disk_Total = (Disk_Stat.f_blocks * Disk_Stat.f_frsize) / 1024
		Disk_Used  = Disk_Total - Disk_Free
		Disk_Free  = (Disk_Stat.f_bavail  * Disk_Stat.f_frsize) / 1024
		
		Inode_Total = Disk_Stat.f_files
		Inode_Free  = Disk_Stat.f_ffree
		Inode_Used  = Inode_Total - Inode_Free

		Usage[Partition] = {
			"Total"  : Bytes(Disk_Total),
			"Free"   : Bytes(Disk_Free),
			"Used"   : Bytes(Disk_Used),
			"Inodes" : Inode_Total,
			"IUsed"  : Inode_Used,
			"IFree"  : Inode_Free
		}
		All_Disk_Total  = All_Disk_Total  + Disk_Total
		All_Disk_Free   = All_Disk_Free   + Disk_Free
		All_Disk_Used   = All_Disk_Used   + Disk_Used
		All_Inode_Total = All_Inode_Total + Inode_Total
		All_Inode_Used  = All_Inode_Used  + Inode_Used
		All_Inode_Free  = All_Inode_Free  + Inode_Free
	# All Disk Usage
	Usage['All'] = {
		"Total"  : Bytes(All_Disk_Total),
		"Free"   : Bytes(All_Disk_Free),
		"Used"   : Bytes(All_Disk_Used),
		"Inodes" : All_Inode_Total,
		"IUsed"  : All_Inode_Used,
		"IFree"  : All_Inode_Free
	}
	data['disk_us'] = Usage
	return data

def Disk_Partitions():
	Proc_Mounts = Read_Proc('mounts')
	ExcludeType = ['rootfs', 'proc', 'sysfs', 'devtmpfs', 'devpts', 'tmpfs', 'usbfs', 'binfmt_misc', 'dm', '/dev/mapper/']
	IncludeType = ['ext2', 'ext3', 'ext4', 'vfat', 'zfs', 'gfs', 'btrfs', 'xfs']
	Partitions  = []
	Devices     = []
	for Line in Proc_Mounts:
		if Line.split()[2] in IncludeType:
			s = False
			for exclude in ExcludeType:
				if exclude in Line.split()[0]:
					s = True
					break
			if s: break
			Partitions.append(Line.split()[1])
			Fileln = os.path.realpath(Line.split()[0])
			Devices.append(Fileln.split('/')[-1])

	return Partitions, Devices
