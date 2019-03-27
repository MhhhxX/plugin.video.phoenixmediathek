# -*- coding: utf-8 -*-
import json
import libmediathek3 as libMediathek
main_url = 'https://phoenix.de/'
base = main_url + 'response/template/'

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


def parseRubriken():
	response = libMediathek.getUrl(base + 'rubrik_overview_json')
	j = json.loads(response)
	l = __parse_items(j)
	return j


def parseDossiers():
	response = libMediathek.getUrl(base + 'dossier_overview_json')
	j = json.loads(response)
	l = __parse_items(j)
	return j


def parseSendungen():
	response = libMediathek.getUrl(base + 'sendungseite_overview_json')
	j = json.loads(response)
	l = __parse_items(j)
	return l


def search():
	pass


def listSearch():
	pass


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


def __parse_items(j):
	l = []
	for item in j['content']['item']:
		d = {}
		d['_name'] = item['titel']
		d['_plot'] = item['typ']
		if 'icon' in item and item['icon']:
			d['_thumb'] = main_url + item['icon']
		else:
			d['_thumb'] = main_url + item['bild_m']
		d['_type'] = 'dir'
		d['id'] = item['link'].split('-')[-1].split('.')[0]
		d['mode'] = 'listVideos'
		l.append(d)
	return l
