#-*- coding: utf-8 -*-


'''
TEMPLATE à reproduire et compléter pour chaque scraper.
Il s'agit ici à titre d'exemple du scraping du site bolden.fr
'''

#--------------------------------------------------------------------------------
import logging

import requests
from bs4 import BeautifulSoup 
from random import choice
import re
import datetime
import json
import httplib

from comptes_clients.models import Donnees_scrapees
from comptes_clients.models import Scrapers
#----------------------------------------------------

#--------------------------------------------------------------------------------
def ouverture_page(session):

	#--------------------------------------
	# partie à personnaliser. Si un champs n'est pas requis, ne pas supprimer mais laisser vide

	url = "https://bolden.fr/"
	referer = "bolden.fr" 
	host = "bolden.fr"
	donnees_post = {}
	donnees_get = {}
	proxy = {}
	# proxy = {'http': 'http://user:mdp@host:port',
	#	'https': 'http://user:mdp@host:port'}
	#--------------------------------------

	#--------------------------------------
	# ne pas modifier sauf si vraiment nécessaire

	# httplib.HTTPConnection._http_vsn = 10
	# httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
	httplib.HTTPConnection._http_vsn = 11
	httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
	
	liste_user_agents = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0",
				"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36",
				"Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
				"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)", 
				"Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2) Gecko/20100115 Firefox/3.6", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0", 
				"Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1"
				) 

	session.headers.update({'Host': host})
	session.headers.update({'Referer': referer})
	session.headers.update({'User-Agent': choice(liste_user_agents)})
	session.headers.update({'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5'})
	session.headers.update({'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'})
	session.headers.update({'DNT': '1'})
	
	if donnees_post:
	
		session.headers.update({'Content-Type':'application/x-www-form-urlencoded'})
		requete = session.post(url,data=donnees_post,proxies=proxy)
		
	else:
	
		requete = session.get(url,params=donnees_get,proxies=proxy)
	#--------------------------------------
	
	#--------------------------------------
	return requete.text
	#--------------------------------------

def principal(id_scraper):
	
	#--------------------------------------
	session = requests.Session()
	#--------------------------------------
	
	#--------------------------------------
	page = ouverture_page(session) 
	soupe = BeautifulSoup(page,'html5lib')	

	liste_principale = soupe.find_all("div", class_=re.compile("^col-sm-6"))

	for element1 in liste_principale:
	
		liste2 = element1.find_all("a", id="fst-detail-link")

		if liste2:

			statut_brut = liste2[0].text.strip()[0]

			if statut_brut == "F":

				statut = "En cours"

			if statut_brut == "L":

				statut = "Clos"

			liste3 = element1.find_all("a", id="snd-detail-link")
			nom = liste3[0].text.strip() 
			lien = "https://bolden.fr"+liste3[0].get('href')
			liste4 = element1.find_all("td")
			montant = liste4[0].text.encode('utf-8').replace("€","").strip() #le encode('utf-8') est nécessaire pour travailler sur les € 
			duree_brute = liste4[1].text.strip().replace("\nans", "")
			duree = int(duree_brute)*12
			taux = liste4[2].text.replace("%","").strip()
			nb_preteurs = ""

			logging.debug([lien,nom,montant,duree,taux,nb_preteurs,statut])
			#--------------------------------------

			#--------------------------------------
			if not Donnees_scrapees.objects.filter(Fk_Scrapers_id=id_scraper,Abscisse=1,Contenu=lien).exists(): #si cette donnée n'existe pas encore dans la bdd (on se base sur l'url comme pk) on l'ajoute :

				#--------------------------------------------------
				# on récupère la toute dernière ligne de la bdd et on relève
				# son id pour plus loin baser l'ordonnée sur ce dernier id existant incrémenté de 1.
				#
				# On pourrait prendre l'ordonnée de la donnée précédente mais dans le cas
				# très improbable où cette dernière n'aurait pas été renseignée l'id semble plus sûr.
				
				derniere_ligne = Donnees_scrapees.objects.order_by('id').last() 

				if derniere_ligne:

					dernier_id = derniere_ligne.id

				else:

					dernier_id = 0
				#--------------------------------------------------

				#--------------------------------------------------
				# on insère toutes les données dans la bdd avec à chaque fois une abscisse
				# et une ordonnée pour représenter virtuellement un tableau
				#
				# besoin seulement de préciser donnee.Type et donnee.Nom,
				# tout le reste peut être copier collé
				
				indice_abscisse = 1			

				donnee = Donnees_scrapees()
				donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
				donnee.Fk_Scrapers_id = id_scraper
				donnee.Abscisse = indice_abscisse
				donnee.Ordonnee = dernier_id + 1
				donnee.Type = "url"
				donnee.Nom = "Lien"
				donnee.Contenu = lien
				donnee.Envoyer_notification = 1
				donnee.Afficher_comme_nouveau = 1
				donnee.Date_extraction = datetime.datetime.now()
				donnee.save()

				indice_abscisse = indice_abscisse + 1

				donnee = Donnees_scrapees()
				donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
				donnee.Fk_Scrapers_id = id_scraper
				donnee.Abscisse = indice_abscisse
				donnee.Ordonnee = dernier_id + 1
				donnee.Type = "texte"
				donnee.Nom = "Nom"
				donnee.Contenu = nom
				donnee.Envoyer_notification = 1
				donnee.Afficher_comme_nouveau = 1
				donnee.Date_extraction = datetime.datetime.now()
				donnee.save()

				indice_abscisse = indice_abscisse + 1

				donnee = Donnees_scrapees()
				donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
				donnee.Fk_Scrapers_id = id_scraper
				donnee.Abscisse = indice_abscisse
				donnee.Ordonnee = dernier_id + 1
				donnee.Type = "nombre"
				donnee.Nom = "Montant"
				donnee.Contenu = montant
				donnee.Envoyer_notification = 1
				donnee.Afficher_comme_nouveau = 1
				donnee.Date_extraction = datetime.datetime.now()
				donnee.save()	

				indice_abscisse = indice_abscisse + 1

				donnee = Donnees_scrapees()
				donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
				donnee.Fk_Scrapers_id = id_scraper
				donnee.Abscisse = indice_abscisse
				donnee.Ordonnee = dernier_id + 1
				donnee.Type = "nombre"
				donnee.Nom = "Duree"
				donnee.Contenu = duree
				donnee.Envoyer_notification = 1
				donnee.Afficher_comme_nouveau = 1
				donnee.Date_extraction = datetime.datetime.now()
				donnee.save()

				indice_abscisse = indice_abscisse + 1

				donnee = Donnees_scrapees()
				donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
				donnee.Fk_Scrapers_id = id_scraper
				donnee.Abscisse = indice_abscisse
				donnee.Ordonnee = dernier_id + 1
				donnee.Type = "nombre"
				donnee.Nom = "Taux"
				donnee.Contenu = taux
				donnee.Envoyer_notification = 1
				donnee.Afficher_comme_nouveau = 1
				donnee.Date_extraction = datetime.datetime.now()
				donnee.save()

				indice_abscisse = indice_abscisse + 1

				donnee = Donnees_scrapees()
				donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
				donnee.Fk_Scrapers_id = id_scraper
				donnee.Abscisse = indice_abscisse
				donnee.Ordonnee = dernier_id + 1
				donnee.Type = "nombre"
				donnee.Nom = "Nombre de prêteurs"
				donnee.Contenu = nb_preteurs
				donnee.Envoyer_notification = 1
				donnee.Afficher_comme_nouveau = 1
				donnee.Date_extraction = datetime.datetime.now()
				donnee.save()

				indice_abscisse = indice_abscisse + 1

				donnee = Donnees_scrapees()
				donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
				donnee.Fk_Scrapers_id = id_scraper
				donnee.Abscisse = indice_abscisse
				donnee.Ordonnee = dernier_id + 1
				donnee.Type = "text"
				donnee.Nom = "Statut"
				donnee.Contenu = statut
				donnee.Envoyer_notification = 1
				donnee.Afficher_comme_nouveau = 1
				donnee.Date_extraction = datetime.datetime.now()
				donnee.save()
				#--------------------------------------------------
			#--------------------------------------

			#--------------------------------------
			# cas particulier : on recommence la même chose, mais cette fois pour vérifier 
			# si un deuxième champs autre que l'url aurait changé. Si l'url n'a pas changé
			# mais que ce 2nd champs a changé on ajoute la donnée dans la bdd.
			#
			# ici ce second champs est le statut.
			
			if Donnees_scrapees.objects.filter(Fk_Scrapers_id=id_scraper,Abscisse=1,Contenu=lien).exists():

				ordonnee = Donnees_scrapees.objects.filter(Fk_Scrapers_id=id_scraper,Abscisse=1,Contenu=lien).order_by('-id')[0].Ordonnee #on prend la derniere car il se peut que le même projet ait changé de statut plusieurs fois et donc qu'il y ait plusieurs fois la même donnée, avec chaque fois le champs statut différent.
				
				if Donnees_scrapees.objects.filter(Fk_Scrapers_id=id_scraper,Abscisse=7,Ordonnee=ordonnee)[0].Contenu != statut:

					derniere_ligne = Donnees_scrapees.objects.order_by('id').last()

					if derniere_ligne:

						dernier_id = derniere_ligne.id

					else:

						dernier_id = 0
		
					indice_abscisse = 1			

					donnee = Donnees_scrapees()
					donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
					donnee.Fk_Scrapers_id = id_scraper
					donnee.Abscisse = indice_abscisse
					donnee.Ordonnee = dernier_id + 1
					donnee.Type = "url"
					donnee.Nom = "Lien"
					donnee.Contenu = lien
					donnee.Envoyer_notification = 1
					donnee.Afficher_comme_nouveau = 1
					donnee.Date_extraction = datetime.datetime.now()
					donnee.save()

					indice_abscisse = indice_abscisse + 1

					donnee = Donnees_scrapees()
					donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
					donnee.Fk_Scrapers_id = id_scraper
					donnee.Abscisse = indice_abscisse
					donnee.Ordonnee = dernier_id + 1
					donnee.Type = "texte"
					donnee.Nom = "Nom"
					donnee.Contenu = nom
					donnee.Envoyer_notification = 1
					donnee.Afficher_comme_nouveau = 1
					donnee.Date_extraction = datetime.datetime.now()
					donnee.save()

					indice_abscisse = indice_abscisse + 1

					donnee = Donnees_scrapees()
					donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
					donnee.Fk_Scrapers_id = id_scraper
					donnee.Abscisse = indice_abscisse
					donnee.Ordonnee = dernier_id + 1
					donnee.Type = "nombre"
					donnee.Nom = "Montant"
					donnee.Contenu = montant
					donnee.Envoyer_notification = 1
					donnee.Afficher_comme_nouveau = 1
					donnee.Date_extraction = datetime.datetime.now()
					donnee.save()	

					indice_abscisse = indice_abscisse + 1

					donnee = Donnees_scrapees()
					donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
					donnee.Fk_Scrapers_id = id_scraper
					donnee.Abscisse = indice_abscisse
					donnee.Ordonnee = dernier_id + 1
					donnee.Type = "nombre"
					donnee.Nom = "Duree"
					donnee.Contenu = duree
					donnee.Envoyer_notification = 1
					donnee.Afficher_comme_nouveau = 1
					donnee.Date_extraction = datetime.datetime.now()
					donnee.save()

					indice_abscisse = indice_abscisse + 1

					donnee = Donnees_scrapees()
					donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
					donnee.Fk_Scrapers_id = id_scraper
					donnee.Abscisse = indice_abscisse
					donnee.Ordonnee = dernier_id + 1
					donnee.Type = "nombre"
					donnee.Nom = "Taux"
					donnee.Contenu = taux
					donnee.Envoyer_notification = 1
					donnee.Afficher_comme_nouveau = 1
					donnee.Date_extraction = datetime.datetime.now()
					donnee.save()

					indice_abscisse = indice_abscisse + 1

					donnee = Donnees_scrapees()
					donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
					donnee.Fk_Scrapers_id = id_scraper
					donnee.Abscisse = indice_abscisse
					donnee.Ordonnee = dernier_id + 1
					donnee.Type = "nombre"
					donnee.Nom = "Nombre de prêteurs"
					donnee.Contenu = nb_preteurs
					donnee.Envoyer_notification = 1
					donnee.Afficher_comme_nouveau = 1
					donnee.Date_extraction = datetime.datetime.now()
					donnee.save()

					indice_abscisse = indice_abscisse + 1

					donnee = Donnees_scrapees()
					donnee.Fk_Client_id = Scrapers.objects.filter(id=id_scraper)[0].Fk_Client_id
					donnee.Fk_Scrapers_id = id_scraper
					donnee.Abscisse = indice_abscisse
					donnee.Ordonnee = dernier_id + 1
					donnee.Type = "text"
					donnee.Nom = "Statut"
					donnee.Contenu = statut
					donnee.Envoyer_notification = 1
					donnee.Afficher_comme_nouveau = 1
					donnee.Date_extraction = datetime.datetime.now()
					donnee.save()
			#--------------------------------------

	#--------------------------------------
	# on retourne à execution_scrapers un témoin
	# pour dire si l'on a trouvé des résultats ou pas.
	#
	# si l'on n'a pas trouvé de resultats ça veut certainement dire 
	# que l'architecture du site a été modifiée et dans ce cas il faut
	# aller voir donc on lève une erreur.

	if liste_principale:

		return True

	else:

		return False
	#--------------------------------------

#--------------------------------------
# pour lancer un test du scraper uniquement

if __name__ == '__main__':

	principal(0)
#--------------------------------------
