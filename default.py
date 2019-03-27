# -*- coding: utf-8 -*-
import libmediathek3 as libMediathek
import resources.lib.jsonparser as jsonParser


translation = libMediathek.getTranslation


def main():
	menu = [{'name': translation(31034), 'mode': 'listRubrics', '_type': 'dir'},
			{'name': 'Dossiers', 'mode': 'listDossiers', '_type': 'dir'},
			{'name': 'Sendungen', 'mode': 'listShows', '_type': 'dir'}]
	return menu


def listVideos():
	return jsonParser.parseVideos(params['id'])


def listRubrics():
	return jsonParser.parseRubrics()


def listDossiers():
	return jsonParser.parseDossiers()


def listShows():
	return jsonParser.parseShows()


def search(term):
	pass


def listSearch():
	pass

	
def play():
	return jsonParser.getVideoUrl(params['smubl'])


modes = {
	'main': main,
	'listVideos': listVideos,
	'play': play,
	'listRubrics': listRubrics,
	'listDossiers': listDossiers,
	'listShows': listShows,
	'search': search,
	'listSearch': listSearch
}	


def list():
	global params
	params = libMediathek.get_params()
	
	mode = params.get('mode', 'main')
	if mode == 'play':
		libMediathek.play(play())
	else:
		l = modes.get(mode)()
		libMediathek.addEntries(l)
		libMediathek.endOfDirectory()
list()