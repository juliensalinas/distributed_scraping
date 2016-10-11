#-*- coding: utf-8 -*-

from django.db import models

'''
Model pour loguer en bdd les infos de connexion
'''

#--------------------------------------------

class Requete_http(models.Model):

	date_consultation = models.DateTimeField() 
	url = models.CharField(max_length=100)
	ip_utilisateur = models.CharField(max_length=30)
	referer = models.CharField(max_length=1000)
	user_agent = models.CharField(max_length=1000)
	Hhote_distant = models.CharField(max_length=1000)
	utilisateur_distant = models.CharField(max_length=1000)


