# -*- coding: utf-8 -*-
import json
import libmediathek3 as libMediathek
base = 'https://www.phoenix.de/response/template/'

fanart = libMediathek.fanart


def parseMain():
	response = libMediathek.getUrl(base+'sendungseite_overview_json')
	j = json.loads(response)
	l = []
	for item in j['content']['items']:
		d = {}
		d['_name'] = item['titel']
		d['_plot'] = item['typ']
		d['_thumb'] = 'https://www.phoenix.de' + item['bild_m']
		d['_type'] = 'dir'
		d['id'] = item['link'].split('-')[-1].split('.')[0]
		d['mode'] = 'listVideos'
		l.append(d)
	return l
	
def parseVideos(id):
	response = libMediathek.getUrl(base+'vod_main_json?id='+id)
	j = json.loads(response)
	l = []
	if j != None:
		for item in j:
			d = {}
			d['_name'] = item['title']
			d['_plot'] = item['text_vorspann']
			d['_thumb'] = 'https://www.phoenix.de' + item['thumbnail_large']['systemurl']
			d['_type'] = 'video'
			d['smubl'] = item['smubl']
			d['mode'] = 'play'
			l.append(d)
	return l
	
def getVideoUrl(smubl):
	response = libMediathek.getUrl('https://tmd.phoenix.de/tmd/2/ngplayer_2_3/vod/ptmd/phoenix/'+smubl)
	j = json.loads(response)
	for prio in j['priorityList']:
		if prio['formitaeten'][0]['mimeType'] == 'application/x-mpegURL':
			for quality in prio['formitaeten'][0]['qualities']:
				if quality['quality'] == 'auto':
					url = quality['audio']['tracks'][0]['uri']
	d = {}
	d['media'] = []
	d['media'].append({'url':url, 'type': 'video', 'stream':'HLS'})
	return d