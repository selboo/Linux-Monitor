#!/usr/bin/env python
#coding=utf8

from func    import *
from config  import *
from glob    import glob
from time    import strftime, localtime, time
from urllib2 import build_opener, ProxyHandler, Request, URLError

class SquidHitCache(object):

	def __init__(self, host='127.0.0.1', post='80', timeout=5):
		self.host  = host
		self.post  = post
		self.proxy = 'http://' + self.host + ':' + self.post

	def SquidConnect(self, url, heads=False):
		http = build_opener(ProxyHandler({'http':self.proxy}))
		if heads:
			requ = Request(url, headers=heads)
		else:
			requ = Request(url)
		try:
			resp = http.open(requ)
		except URLError,e:
			resp = e
		return resp

	def SquidQuestion(self, md5):
		url   = 'http://itiku.speiyou.com/itempool/rest/question/queryQuestionByIds.json?ids=' + md5
		heads = {
			"User-Agent"	: "Cache Squid python",
			"Accept"		: "*/*",
			"Content-type"	: "text/plain",
			"plat"			: "flex",
			"sys"			: "ics3",
			"md5"			: md5
		}

		resp = self.SquidConnect(url, heads)
		return resp.headers.get('X-Cache').split(' ')[0], str(resp.code)

	def SquidResources(self, url):
		resp = self.SquidConnect(url)
		return resp.headers.get('X-Cache').split(' ')[0], str(resp.code)

def Read_log(oFile):
	urlist  = []
	WildcardFile = '/tmp/' + oFile + "/*cacheLog*" + strftime('%Y%m%d',localtime(time())) + '*'
	if (glob(WildcardFile)):
		for oPath in glob(WildcardFile):
			Fopen = open(oPath,'r').readlines()
			for i in Fopen:
				match = squid_http_re.findall(i)
				if match != []:
					urlist.append(match[0])

		HIT, MISS = SquidCache(urlist, oFile)
		return len(urlist), HIT, MISS
	else:
		return 0,0,0

def SquidCache(uList, uType):
	Squidhttp = SquidHitCache()
	if uType == 'static':
		HIT, MISS = 0, 0
		for i in uList:
			url = i.replace('\\', '')
			SquidStatus, SquidCode = Squidhttp.SquidResources(url)
			if SquidStatus == "HIT" and SquidCode == "200":
				HIT = HIT + 1
			else:
				MISS = MISS + 1
	if uType == 'questions':
		HIT, MISS = 0, 0
		for i in uList:
			match = squid_md5_re.findall(i)
			if match != []: md5 = match[0]
			SquidStatus, SquidCode = Squidhttp.SquidQuestion(md5)
			if SquidStatus == "HIT" and SquidCode == "200":
				HIT = HIT + 1
			else:
				MISS = MISS + 1

	return HIT, MISS

def Squid():
	result = {}
	QuestionTotal,  QuestionHIT,  QuestionMISS  = Read_log('questions')
	ResourcesTotal, ResourcesHIT, ResourcesMISS = Read_log('static')

	result['QuestionTotal']  = QuestionTotal
	result['QuestionHIT']    = QuestionHIT
	result['QuestionMISS']   = QuestionMISS
	result['ResourcesTotal'] = ResourcesTotal
	result['ResourcesHIT']   = ResourcesHIT
	result['ResourcesMISS']  = ResourcesMISS
	data['squid'] = result
	return result
