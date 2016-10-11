#-*- coding: utf-8 -*-

'''
Assure l'orchestration des scrapers
'''

import logging
logging.basicConfig(level=logging.INFO,filename='debug_scraper.log',format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

import time
import datetime
import multiprocessing

from comptes_clients.models import Scrapers

from utils.lecture_ecriture_fichiers import ecriture_heure
from utils.lecture_ecriture_fichiers import ecriture_etat_scraper
from utils.lecture_ecriture_fichiers import lecture_heure
from utils.lecture_ecriture_fichiers import lecture_etat_scraper

from utils.notifications.centre_notifications import envoi_notification
from utils.notifications.envoi_emails import email_alerte_scraper
from comptes_clients.models import Donnees_scrapees

site.addsitedir("utils/scraping/scrapers")

#------------------------------------------------------------------------

def lancement_scraper(id_scraper,nom_scraper):

	logging.info("Debut scraper : "+str(id_scraper)+", "+nom_scraper)

	ecriture_etat_scraper(nom_scraper,"ON")	#on passe le scraper à ON 

	scraper = __import__(nom_scraper) #on importe le scraper (seule façon d'importer un module avec un nom variable)
	code_erreur = scraper.principal(id_scraper) #on exécute le scraper

	if code_erreur: #on regarde si une erreur (gérée par nous) a été soulevée, et si oui on quitte tout

		raise ValueError(code_erreur)

	if Donnees_scrapees.objects.filter(Envoyer_notification=1).exists(): #s'il existe des données à envoyer (normalement il en existe forcément):

		envoi_notification(id_scraper) #on envoie un email avec les données trouvées par ce scraper
		
		queryset_donnees = Donnees_scrapees.objects.filter(Envoyer_notification=1,Fk_Scrapers_id=id_scraper) #on passe le flag envoyer_notification de la donnée à 0 pour ne plus la renvoyer une seconde fois
		for element in queryset_donnees:
			element.Envoyer_notification = 0
			element.save()

	ecriture_heure(nom_scraper) #on consigne l'heure à laquelle le scraper a été exécuté
	ecriture_etat_scraper(nom_scraper,"OFF") #on passe le scraper à OFF

	logging.info("Fin scraper : "+str(id_scraper)+", "+nom_scraper)

def ordonnancement_process():
	
	queryset_scrapers = Scrapers.objects.all()

	for scraper in queryset_scrapers: #on prend tous les scrapers un par un

		id_scraper = scraper.id
		nom_scraper = scraper.Nom_scraper
		frequence_alertes = scraper.Frequence_alertes

		# on regarde si le scraper est ON ou EN ATTENTE ou OFF
		# et on calcule le nb de secondes écoulées depuis la dernière exécution du scraper

		etat_scraper = lecture_etat_scraper(nom_scraper) 
		heure_derniere_requete = lecture_heure(nom_scraper)
		heure_derniere_requete_datetime = datetime.datetime.strptime(heure_derniere_requete, "%Y-%m-%d %H:%M:%S.%f")
		delta = datetime.datetime.now() - heure_derniere_requete_datetime
		delta_secondes = (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6 
	
		
		# if etat_scraper == "ON" and delta_secondes > 600:
		#
		#	logging.error("Probleme scraper : "+str(id_scraper)+", "+nom_scraper)
		#	email_alerte_scraper(id_scraper,nom_scraper)
		#	ecriture_etat_scraper(nom_scraper,"ATTENTE INTERVENTION")
				

		# on n'exécute le scraper que s'il est OFF et que le temps ecoulé depuis
		# la dernière exécution correspond à la fréquence précisée dans la BDD

		if (etat_scraper == "OFF" and frequence_alertes == "instantanee") or (etat_scraper == "OFF" and frequence_alertes == "quotidienne" and delta_secondes > 86400) or (etat_scraper == "OFF" and frequence_alertes == "mensuelle" and delta_secondes > 2592000):

			
			# ne peut pas être utilisé pour le moment car les accès concurrents à la BDD
			# posent problème avec Django 1.6
			#
			# on lance un nouveau process pour chaque scraper
			#
			# si le process principal se coupe brutalement, tous les sous process vont 
			# se terminer proprement et avec l'option daemon ils ne recevront pas du tout l'ordre de se couper
			# si un sous-process se coupe brutalement ça ne coupe pas le programme principal et les autres sous-process
			#
			# d = multiprocessing.Process(name=nom_scraper, target=lancement_scraper, args=(id_scraper,nom_scraper))
			# d.daemon = True
			# d.start()

			# on lance le scraper et s'il plante on log l'erreur
			# et on s'envoie un email d'erreur. On ne bloque pas le programme pour autant,
			# on passe au scraper suivant.

			try:

				lancement_scraper(id_scraper,nom_scraper) 

			except ValueError as e: #on gère les erreurs soulevées par nous
			
				ecriture_etat_scraper(nom_scraper,"ATTENTE INTERVENTION")
								
				if e.args[0] == 1:
				
					message = u"La structure id et class du site surveillé par ce scraper a changé : "+str(id_scraper)+u", "+nom_scraper+u".\nLancer le scraper de façon isolée et aller sur la page à scraper pour voir si les données récupérées sont toujours bonnes, si non alors modifier le scraper. \nLe scraper est mis en attente pour le moment..."
				
				elif e.args[0] == 2: 

					message = u"La structure json du site surveillé par ce scraper a changé : "+str(id_scraper)+u", "+nom_scraper+u".\nLancer le scraper de façon isolée et aller sur la page à scraper pour voir si les données récupérées sont toujours bonnes, si non alors modifier le scraper. \nLe scraper est mis en attente pour le moment..."
				
				logging.exception(message)
				email_alerte_scraper(message)
					
			except:

				# redondant avec la verification de etat_scraper == ON 
				# et delta > 600, mais quand on utilisera des daemons en parallèle 
				# pourra-t-on continuer a recuperer une erreur ici ou faudra-t-il passer par
				# un système de fichiers plats pour faire le lien ? A verifier
				
				ecriture_etat_scraper(nom_scraper,"ATTENTE INTERVENTION")
				message = u"Erreur scraper : "+str(id_scraper)+u", "+nom_scraper
				logging.exception(message)
				email_alerte_scraper(message)
				
if __name__ == '__main__':

	while 1 < 2:

		ordonnancement_process()
		time.sleep(10)
	
