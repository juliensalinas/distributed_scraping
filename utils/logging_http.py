#-*- coding: utf-8 -*-

'''
On log en bdd les infos de connexions
'''

#------------------------------------
import datetime

from utils.models import Requete_http

#------------------------------------------------------

def logging_requete_http(request):

	requete_http = Requete_http()

	requete_http.Date_consultation = datetime.datetime.now()
	requete_http.Url = request.get_full_path()

	if "REMOTE_ADDR" in request.META:
		Ip_utilisateur = request.META['REMOTE_ADDR']
		requete_http.Ip_utilisateur = Ip_utilisateur
	if "HTTP_REFERER" in request.META:
		Referer = request.META['HTTP_REFERER']
		requete_http.Referer = Referer
	if "HTTP_USER_AGENT" in request.META:
		User_agent = request.META['HTTP_USER_AGENT']
		requete_http.User_agent = User_agent
	if "REMOTE_HOST" in request.META:
		Hote_distant = request.META['REMOTE_HOST']
		requete_http.Hote_distant = Hote_distant
	if "REMOTE_USER" in request.META:
		Utilisateur_distant = request.META['REMOTE_USER']
		requete_http.Utilisateur_distant = Utilisateur_distant

	requete_http.save()

