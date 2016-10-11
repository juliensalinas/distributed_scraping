#-*- coding: utf-8 -*-


'''
On vérifie que la pages web à scraper n'a pas changé.
Pour cela on récupère sur la page web ce qui semble être une sorte de "signature" de la page.
On traite le cas d'une page json et d'une page html différemment:
- json : on prend un projet au hasard. Chaque projet est décrit sous forme de dictionnaire donc on relève toutes les clés du dictionnaire et on vérifie qu'elles n'ont pas changé. On enlève les doublons et on ne tient pas compte de l'ordre au cas où un élément serait toujours là mais à une place différente dans le dictionnaire.
- html : on extrait les id et les class de toutes les balises. On enlève les doublons (pour ne pas surcharger la base et car on ne tient pas compte du nombre de fois où le même élément apparait, sinon à chaque ajout d'un nouveau projet sur la page on aurait une signature différente) et on ne tient pas compte de l'ordre au cas où un élément aurait été simplément déplacé sur la page.
Ce n'est pas la méthode parfaite, surtout pour le html qui peut changer souvent par rapport au json, mais ça semble être la seule possible.
'''

#--------------------------------------------------------------------------------

import logging
logging.basicConfig(level=logging.INFO,filename='debug_scraper.log',format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

import json
import re

#----------------------------------------------------
from comptes_clients.models import Scrapers
#----------------------------------------------------

#--------------------------------------------------------------------------------

def controle_structure_id_class(id_scraper,soupe):

	liste_soupe = soupe.find_all(True)
	nouvelle_liste_id_class = []

	for tag in liste_soupe:

		try:
			if not re.search(r'\d', str(tag["class"])): #on enlève tous les éléments qui contiennent des chiffres parce que souvent c'est le signe d'un élément à problème qui va changer très souvent (ex: projet_156546resgt4586qqerg) 
				nouvelle_liste_id_class.append(tag["class"])
		except:
			pass
		try:
			if not re.search(r'\d', str(tag["id"])):
				nouvelle_liste_id_class.append(tag["id"])
		except:
			pass

	queryset_scraper = Scrapers.objects.filter(id=id_scraper)[0]
	ancien_json_id_class = queryset_scraper.Structure_page_scrapee

	# on fait en permanence une gymnastique a transformer toutes les listes en tuples car on veut utiliser set()
	#
	# set() permet de travailler sur une liste sans doublon et sans tenir compte de l'ordre à l'interieur
	#
	# or set() peut prendre une liste mais pas une liste de listes. Donc on doit à chaque fois
	# transformer les listes de listes en listes de tuples.
	#
	# le dump json retransforme les tuples en listes donc quand on extrait les données
	# de la base il faut les transformer une fois de plus en liste de tuples.

	nouvelle_liste_de_tuples_id_class = []
	for element in nouvelle_liste_id_class:
		if type(element) is list:
			nouvelle_liste_de_tuples_id_class.append(tuple(element))
		else:
			nouvelle_liste_de_tuples_id_class.append(element)	
	
	if ancien_json_id_class:

		jsonDec = json.decoder.JSONDecoder()		
		ancienne_liste_de_listes_id_class = jsonDec.decode(ancien_json_id_class)
		ancienne_liste_de_tuples_id_class = []
		for element in ancienne_liste_de_listes_id_class:
			if type(element) is list:
				ancienne_liste_de_tuples_id_class.append(tuple(element))
			else:
				ancienne_liste_de_tuples_id_class.append(element)			
		
		# comme les pages web changent souvent de petites choses dans leur structure 
		# sans impact pour moi on ne déclenche une alerte que si la structure a changé de façon significative (> 20%)7
		
		difference1 = set(ancienne_liste_de_tuples_id_class) - set(nouvelle_liste_de_tuples_id_class)
		difference2 = set(nouvelle_liste_de_tuples_id_class) - set(ancienne_liste_de_tuples_id_class)
		
		if not ancienne_liste_de_tuples_id_class:
			
			return True
		
		ratio_difference1 = float(len(difference1))/float(len(ancienne_liste_de_tuples_id_class))
		ratio_difference2 = float(len(difference2))/float(len(ancienne_liste_de_tuples_id_class))

		logging.info("Diff 1 : "+str(ratio_difference1))
		logging.info("Diff 2 : "+str(ratio_difference2))
		
		if ratio_difference1 < 0.2 and ratio_difference2 < 0.2:

			return True

		else:

			queryset_scraper.Structure_page_scrapee = None
			queryset_scraper.save()

			return False

	else:

		queryset_scraper.Structure_page_scrapee = json.dumps(list(set(nouvelle_liste_de_tuples_id_class)))
		queryset_scraper.save()

		return True

def controle_structure_json(id_scraper,dict_projets):

	nouvelle_liste_cles = []

	liste_projets = dict_projets['projects']
	projet1 = liste_projets[0]
	
	for cle in projet1:
		
		if not re.search(r'\d', str(cle)):
			nouvelle_liste_cles.append(cle)
		
	queryset_scraper = Scrapers.objects.filter(id=id_scraper)[0]
	ancien_json_cles = queryset_scraper.Structure_page_scrapee

	nouvelle_liste_de_tuples_cles = []
	for element in nouvelle_liste_cles:
		if type(element) is list:
			nouvelle_liste_de_tuples_cles.append(tuple(element))
		else:
			nouvelle_liste_de_tuples_cles.append(element)		
	
	if ancien_json_cles:

		jsonDec = json.decoder.JSONDecoder()		
		ancienne_liste_de_listes_cles = jsonDec.decode(ancien_json_cles)
		ancienne_liste_de_tuples_cles = []
		for element in ancienne_liste_de_listes_cles:
			if type(element) is list:
				ancienne_liste_de_tuples_cles.append(tuple(element))
			else:
				ancienne_liste_de_tuples_cles.append(element)				
		
		#comme une page json change peu, on fait un controle strict et on arrête tout au moindre changement
		if set(ancienne_liste_de_tuples_cles) == set(nouvelle_liste_de_tuples_cles):

			return True

		else:

			queryset_scraper.Structure_page_scrapee = None
			queryset_scraper.save()

			return False

	else:

		queryset_scraper.Structure_page_scrapee = json.dumps(list(set(nouvelle_liste_de_tuples_cles)))
		queryset_scraper.save()

		return True