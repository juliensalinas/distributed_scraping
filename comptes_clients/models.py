#-*- coding: utf-8 -*-

'''
Models liés à la gestion des clients et de leurs données
'''

from django.db import models
from django.contrib.auth.models import User

#------------------------------------------------

class Client(models.Model):

	utilisateur = models.OneToOneField(User)
	email_hashe = models.CharField(max_length=100,blank=True, null=True)
	ip_inscription = models.CharField(max_length=30,blank=True, null=True)
	telephone = models.CharField(max_length=30,blank=True, null=True)
	poste_occupe = models.CharField(max_length=100,blank=True, null=True)
	date_inscription = models.DateTimeField()
	raison_sociale_entreprise = models.CharField(max_length=100,blank=True, null=True)
	siren_entreprise = models.CharField(max_length=10,blank=True, null=True)

class Email(models.Model):

	fk_Client_id = models.IntegerField()
	email = models.CharField(max_length=100)

class Telephone(models.Model):

	fk_Client_id = models.IntegerField()
	telephone = models.CharField(max_length=30)

class Scraper(models.Model):

	fk_Client_id = models.IntegerField()
	nom_scraper = models.CharField(max_length=100)
	libelle_commercial_scraper = models.CharField(max_length=1000)
	notification_email = models.BooleanField()
	notification_csv_email = models.BooleanField()
	notification_xls_email = models.BooleanField()
	notification_sms = models.BooleanField()
	frequence_alertes = models.CharField(max_length=20)
	structure_page_scrapee = models.CharField(max_length=10000)

class Donnee_scrapee(models.Model):

	fk_Client_id = models.IntegerField()
	fk_Scrapers_id = models.IntegerField()
	abscisse = models.IntegerField()
	ordonnee = models.IntegerField()
	type = models.CharField(max_length=20)
	nom = models.CharField(max_length=100)
	contenu = models.CharField(max_length=10000)
	envoyer_notification = models.BooleanField()
	afficher_comme_nouveau = models.BooleanField()
	date_extraction = models.DateTimeField()

