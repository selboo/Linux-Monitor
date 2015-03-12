#!/usr/bin/env python
#coding=utf8

from re import compile

# Default global
global data
global TDM_Sleep
global TDM_Number
global Timeout
TDM_Sleep  = 1
TDM_Number = 1
data       = {}
threadings = []
Timeout    = 5
PostUrl    = "http://10.1.8.208:8102/recv/server"

# Port Watch
Port_Watch = [
	80,
	11000,
	3306,
	8080,
	777
	]

# File Watch
File_Watch = [
	'/etc/hosts',
	'/etc/passwd',
	]

# CPU global
avg_cpu    = {}

# DISK global
avg_io     = {}

# NETWORK global
avg_net    = {}

# raid regex
raid_type_re   = compile( '(?<=PD Type: ).*(?=$)' )
raid_size_re   = compile( '(?<=Raw Size: ).*(?= GB)' )
raid_sn_re     = compile( '[0-9A-Za-z]{20}' )
raid_dspeed_re = compile( '(?<=Device Speed: ).*(?=\.)' )
raid_lspeed_re = compile( '(?<=Link Speed: ).*(?=\.)' )
raid_temper_re = compile( '(?<= :).*(?=C \()' )
raid_level_re  = compile( '(?<=y-).*(?=, S)' )
raid_rsize_re  = compile( '(?<=: ).*(?= GB)' )

# cpu regex
cpu_cpu_re = compile( "^cpu*" )
cpu_pre_re = compile( "^[1-9]\d*$" )

# disk regex
disk_dev_re = compile( "^[a-zA-Z]*" )

# squid regex
squid_http_re = compile( "[a-zA-z]+://[^\s]*" )
squid_md5_re  = compile( "[a-fA-F0-9]{32,32}$" )

# port regex
port_p_na_re = compile( '(?<=LISTEN      ).*(?= )' )
port_name_re = compile( '\w+' )

# host regex
host_vend_re = compile( '(?<=: ).*' )

