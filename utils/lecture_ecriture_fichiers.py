#-*- coding: utf-8 -*-

'''
Plusieurs petites fonctions d'écriture et lecture dans les fichiers textes 
'''

import csv
import datetime

#------------------------------------------------------

def lecture_heure(nom_fichier):

	try:

		lecture_heure_derniere_requete = csv.reader(open("utils/scraping/"+nom_fichier+"_heure","rb"))

	except:

		f = open("utils/scraping/"+nom_fichier+"_heure", "wb")
		ecriture_heure_derniere_requete = csv.writer(f)
		ecriture_heure_derniere_requete.writerow(["2015-01-01 00:00:00.0000"])
		f.close()
		lecture_heure_derniere_requete = csv.reader(open("utils/scraping/"+nom_fichier+"_heure","rb"))
		
	for row in lecture_heure_derniere_requete:

		if row:

			heure = row[0]
			return heure

		else:

			return False

def ecriture_heure(nom_fichier):

	f = open("utils/scraping/"+nom_fichier+"_heure", "wb")
	ecriture_heure_derniere_requete = csv.writer(f)
	ecriture_heure_derniere_requete.writerow([datetime.datetime.now()])
	f.close()

def lecture_curseur():

	lecture_curseur_bdd = csv.reader(open("utils/scraping/curseur_bdd.csv","rb"))	
	
	for row in lecture_curseur_bdd:

		if row:

			curseur = row[0]
			return curseur

		else:

			return 0
	
def ecriture_curseur(curseur):

	f = open("utils/scraping/curseur_bdd.csv", "wb")
	ecriture_curseur_bdd = csv.writer(f)
	ecriture_curseur_bdd.writerow([curseur])
	f.close()

def ecriture_etat_scraper(nom_fichier,etat):

	f = open("utils/scraping/"+nom_fichier+"_etat", "wb")
	ecriture_etat = csv.writer(f)
	ecriture_etat.writerow([etat])
	f.close()

def lecture_etat_scraper(nom_fichier):

	try:

		lecture_etat = csv.reader(open("utils/scraping/"+nom_fichier+"_etat","rb"))
		
	except:

		ecriture_etat_scraper(nom_fichier,"OFF")
		lecture_etat = csv.reader(open("utils/scraping/"+nom_fichier+"_etat","rb"))	
	
	for row in lecture_etat:

		if row:

			etat = row[0]
			return etat

		else:

			return 0


