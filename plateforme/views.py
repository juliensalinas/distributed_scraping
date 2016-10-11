#-*- coding: utf-8 -*-

'''
Plateforme sur laquelle le client peut se loguer pour récuperer les données scrapées le concernant
'''

#------------------------------------
import logging
logging.basicConfig(level=logging.INFO,filename='debug_django.log',format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

import xlwt
import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from django.contrib.auth.models import User
from comptes_clients.models import Client, Donnees_scrapees, Scrapers

from utils.logging_http import logging_requete_http
from utils.creation_pieces_jointes import construction_fichier_xls

from plateforme.forms import form_login_plateforme, form_telechargement_tableau
#------------------------------------------------------

@login_required
def index(request):

	logging_requete_http(request)
	
	u = User.objects.get(username=request.user)
		
	scrapers = Scrapers.objects.filter(Fk_Client_id=u.client.id) 
	liste_id_libelle_scrapers = [[scraper.id,scraper.Libelle_commercial_scraper] for scraper in scrapers]
	
	form = form_telechargement_tableau()	
			
	return render(request, 'plateforme/index.html', locals()) 

@login_required	
def telechargement_tableau_xls(request):

	id_scraper = request.session.get("id")
			
	if request.method == 'POST':
	
		form = form_telechargement_tableau(request.POST)	
		
		if form.is_valid():
		
			date = form.cleaned_data['date']

			queryset_donnees = Donnees_scrapees.objects.filter(Fk_Scrapers_id=id_scraper,Date_extraction__gte=date).order_by('-Ordonnee','Abscisse')
			
			if queryset_donnees:
			
				fichier_xls = construction_fichier_xls(queryset_donnees)
						
				reponse = HttpResponse(content_type="application/vnd.ms-excel")
				reponse['Content-Disposition'] = 'attachment; filename=Donnees_extraites_Soupeo.xls'
				fichier_xls.save(reponse)	
				return reponse
				
			else:
			
				aucune_donnee = 1
				
				#---------------------------------
				# obligé de remettre ici la liste id_libelle_scrapers sinon en cas d'erreur 
				# du formulaire date, quand on revient sur la page avec un message d'erreur
				# la liste des scrapers en haut ne s'affiche plus.

				u = User.objects.get(username=request.user)
			
				scrapers = Scrapers.objects.filter(Fk_Client_id=u.client.id) 
				liste_id_libelle_scrapers = [[scraper.id,scraper.Libelle_commercial_scraper] for scraper in scrapers]
				#-----------------------------------
			
				return render(request, 'plateforme/index.html', locals())
				
		else:
		
			#---------------------------------
			u = User.objects.get(username=request.user)
		
			scrapers = Scrapers.objects.filter(Fk_Client_id=u.client.id) 
			liste_id_libelle_scrapers = [[scraper.id,scraper.Libelle_commercial_scraper] for scraper in scrapers]
			#-----------------------------------
							
			return render(request, 'plateforme/index.html', locals())
		
	else:
	
		return redirect(reverse('plateforme.views.index'))

def vue_login(request):

	logging_requete_http(request)

	if request.method == 'POST':

		form = form_login_plateforme(request.POST)

		if form.is_valid(): 

			nom_utilisateur = form.cleaned_data['nom_utilisateur']
			mot_de_passe = form.cleaned_data['mot_de_passe']
			user = authenticate(username=nom_utilisateur, password=mot_de_passe)

			if user is not None:

				if user.is_active:

					logging.info("Utilisateur connu : "+str(nom_utilisateur)+", "+str(mot_de_passe))
					login(request, user)
					
					u = User.objects.get(username=request.user)
					
					if Scrapers.objects.filter(Fk_Client_id=u.client.id).exists():
					
						id_scraper = Scrapers.objects.filter(Fk_Client_id=u.client.id)[0].id
						request.session["id"] = id_scraper
						
					else:
						
						return redirect(reverse("plateforme.views.aucune_alerte"))				
				
					return redirect(reverse("plateforme.views.index"))
				else:

			   		logging.info("Utilisateur desactivé : "+str(nom_utilisateur)+", "+str(mot_de_passe))
			else:

				logging.info("Utilisateur inconnu : "+str(nom_utilisateur)+", "+str(mot_de_passe))
	else:

		form = form_login_plateforme()

	return render(request, 'vitrine/login.html', locals())

@login_required	
def vue_logout(request):

	logging_requete_http(request)
	
	logout(request)

	return vue_login(request)
	
@login_required	
def ajax_tableau(request):

	logging_requete_http(request)
	
	if request.GET.get('id'):
	
		id_scraper = request.GET.get('id')
	
	else:
	
		id_scraper = request.session.get("id")

	u = User.objects.get(username=request.user)
	id_client = u.client.id
			
	liste_titres,liste_donnees_scrapees = recuperation_titres_et_donnees(id_client,id_scraper)
	
	request.session["id"] = id_scraper

	return render(request, 'plateforme/ajax_tableau.html', locals())

@login_required	
def aucune_alerte(request):

	logging_requete_http(request)
	
	return render(request, 'plateforme/aucune_alerte.html', locals())	
			
@login_required	
def ajax_graphiques(request):

	logging_requete_http(request)

	id_scraper = request.session.get("id")
	u = User.objects.get(username=request.user)
	id_client = u.client.id
			
	liste_noms_pour_graphique,liste_donnees_scrapees_pour_graphique,liste_dates_pour_graphique = recuperation_donnees_et_dates_pour_graphique(id_client,id_scraper)	
	
	listes_zippees = zip(liste_noms_pour_graphique,liste_donnees_scrapees_pour_graphique,liste_dates_pour_graphique)
	
	logging.info(liste_noms_pour_graphique)
	logging.info(liste_donnees_scrapees_pour_graphique)
	logging.info(liste_dates_pour_graphique)
	
	return render(request, 'plateforme/ajax_graphiques.html', locals())

def recuperation_donnees_et_dates_pour_graphique(id_client,id_scraper):
	
	if Donnees_scrapees.objects.filter(Fk_Client_id=id_client,Fk_Scrapers_id=id_scraper).exists():
	
		liste_noms = Donnees_scrapees.objects.filter(Fk_Client_id=id_client,Fk_Scrapers_id=id_scraper,Type__in=["pourcentage","nombre","nb_mois","euros"]).values_list('Nom',flat=True)
		liste_noms_distincts = list(set(liste_noms))

		liste_donnees = []
		liste_dates = []
		
		for nom in liste_noms_distincts:
					
			queryset_donnees_scrapees_pour_graphique = Donnees_scrapees.objects.filter(Fk_Client_id=id_client,Fk_Scrapers_id=id_scraper,Nom=nom)
			frequence_alertes = Scrapers.objects.filter(id=id_scraper)[0].Frequence_alertes
			
			liste_donnees_temp = []
			liste_dates_temp = []
			
			for donnee in queryset_donnees_scrapees_pour_graphique:
			
				try:
			
					liste_donnees_temp.append(int(donnee.Contenu))
				
				except:
				
					liste_donnees_temp.append("erreur")
				
				if frequence_alertes == "instantanee":
					
					liste_dates_temp.append(donnee.Date_extraction.strftime("%d/%m/%Y %H:%M"))
				
				if frequence_alertes == "quotidienne":
					
					liste_dates_temp.append(donnee.Date_extraction.strftime("%d/%m/%Y"))
					
				if frequence_alertes == "mensuelle":
					
					liste_dates_temp.append(donnee.Date_extraction.strftime("%m/%Y"))
			
			liste_donnees.append(liste_donnees_temp)
			liste_dates.append(liste_dates_temp)
			
		return [liste_noms_distincts,liste_donnees,liste_dates]

def recuperation_titres_et_donnees(id_client,id_scraper):
			
	if Donnees_scrapees.objects.filter(Fk_Client_id=id_client,Fk_Scrapers_id=id_scraper).exists():
	
		liste_ordonnees_avec_doublons = Donnees_scrapees.objects.filter(Fk_Client_id=id_client,Fk_Scrapers_id=id_scraper).values_list('Ordonnee',flat=True)
		liste_ordonnees = list(set(liste_ordonnees_avec_doublons))
		
		donnees_premier_jeu = Donnees_scrapees.objects.filter(Fk_Client_id=id_client,Ordonnee=liste_ordonnees[0],Fk_Scrapers_id=id_scraper).order_by('Abscisse')
		liste_titres = [donnee.Nom for donnee in donnees_premier_jeu]
		liste_titres.append("Date d'extraction")

		liste_donnees_scrapees_intermediaire1 = Donnees_scrapees.objects.filter(Fk_Client_id=id_client,Fk_Scrapers_id=id_scraper).order_by('-Ordonnee','Abscisse').values_list('Type','Contenu','Afficher_comme_nouveau','Date_extraction')
		liste_donnees_scrapees_intermediaire2 = [liste_donnees_scrapees_intermediaire1[i:i+len(donnees_premier_jeu)] for i in range(0, len(liste_donnees_scrapees_intermediaire1), len(donnees_premier_jeu))]	
		liste_donnees_scrapees = []

		for element in liste_donnees_scrapees_intermediaire2:
			
			element.append(('date',element[0][3],True,''))
			element.insert(0,element[0][2])
			liste_donnees_scrapees.append(element)
		
	else:
	
		liste_titres = []
		liste_donnees_scrapees = []
		
	return [liste_titres,liste_donnees_scrapees]

