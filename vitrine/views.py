#-*- coding: utf-8 -*-

'''
Vues de l'application vitrine
'''

#------------------------------------

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from utils.logging_http import logging_requete_http

#------------------------------------------------------

def index(request):

	logging_requete_http(request)

	return render(request, 'vitrine/index.html', locals()) 

def contact(request):

	logging_requete_http(request)

	return render(request, 'vitrine/contact.html', locals()) 	
	
def mentionslegales(request):

	logging_requete_http(request)

	return render(request, 'vitrine/mentionslegales.html', locals()) 
