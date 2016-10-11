#-*- coding: utf-8 -*-

'''
Models liés à la gestion des clients et de leurs données
'''

from django.db import models
from django.contrib.auth.models import User

#------------------------------------------------

class Client(models.Model):

	Utilisateur = models.OneToOneField(User)
	Email_hashe = models.CharField(max_length=100,blank=True, null=True)
	Ip_inscription = models.CharField(max_length=30,blank=True, null=True)
	Telephone = models.CharField(max_length=30,blank=True, null=True)
	Poste_occupe = models.CharField(max_length=100,blank=True, null=True)
	Date_inscription = models.DateTimeField()
	Raison_sociale_entreprise = models.CharField(max_length=100,blank=True, null=True)
	Siren_entreprise = models.CharField(max_length=10,blank=True, null=True)

class Email(models.Model):

	Fk_Client_id = models.IntegerField()
	Email = models.CharField(max_length=100)

class Telephone(models.Model):

	Fk_Client_id = models.IntegerField()
	Telephone = models.CharField(max_length=30)

class Scraper(models.Model):

	Fk_Client_id = models.IntegerField()
	Nom_scraper = models.CharField(max_length=100)
	Libelle_commercial_scraper = models.CharField(max_length=1000)
	Notification_email = models.BooleanField()
	Notification_csv_email = models.BooleanField()
	Notification_xls_email = models.BooleanField()
	Notification_sms = models.BooleanField()
	Frequence_alertes = models.CharField(max_length=20)
	Structure_page_scrapee = models.CharField(max_length=10000)

class Donnee_scrapee(models.Model):

	Fk_Client_id = models.IntegerField()
	Fk_Scrapers_id = models.IntegerField()
	Abscisse = models.IntegerField()
	Ordonnee = models.IntegerField()
	Type = models.CharField(max_length=20)
	Nom = models.CharField(max_length=100)
	Contenu = models.CharField(max_length=10000)
	Envoyer_notification = models.BooleanField()
	Afficher_comme_nouveau = models.BooleanField()
	Date_extraction = models.DateTimeField()

