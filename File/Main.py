#!/usr/bin/env python
#coding=utf8

from func import *
from os.path import getctime
from os      import mknod
from difflib import HtmlDiff
from base64  import b64encode
from shutil  import copy

def File():
	result = {}
	
	for sFile in File_Watch:
		result[sFile] = {}
		md5           = MD5(sFile)
		ctime         = getctime(sFile)
		status        = MD5_File(sFile, md5)
		diff          = Diff_File(sFile, status)

		result[sFile]['md5']    = md5
		result[sFile]['ctime']  = ctime
		result[sFile]['status'] = status
		result[sFile]['diff']   = diff

	data['file']    = result
	return result

def MD5_File(pFile, md5):
	tFile = '/tmp' + pFile + "/md5"
	dFile = '/tmp' + pFile + "/"

	if not os.path.exists(dFile):	os.makedirs(dFile)

	try:
		rFile = open(tFile, 'r')
	except IOError, e:
		os.mknod(tFile)
		sMD5 = md5
	else:
		sMD5 = rFile.readlines()[0]
	finally:
		dMD5 = md5

	sFile = open(tFile, 'w')
	sFile.write(md5)
	sFile.close()

	if sMD5 == dMD5:
		copy(pFile, dFile + "txt")
		return True
	else:
		return False

def Diff_File(pFile, Status):
	dFile = '/tmp' + pFile + "/txt"

	if Status == 1:	return True
	
	sFile   = open(pFile, 'r')
	sString = ''.join(sFile.readlines()).splitlines()
	sFile.close()

	dFile   = open(dFile, 'r')
	dString = ''.join(dFile.readlines()).splitlines()
	dFile.close()

	#diff = HtmlDiff().make_file(sString, dString)
	diff = HtmlDiff().make_table(sString, dString)
	return b64encode(diff)


