#-*- coding: utf-8 -*-

'''
Crée les pièces jointes à joindre aux emails
'''

import xlwt
import csv

#------------------------------------------------------

def construction_fichier_csv(queryset_donnees):

	indice_ligne = 0
	indice_arret = 0
	liste_donnees_1 = []
	liste_donnees_2 = []

	for element in queryset_donnees:
	
		if not indice_arret and (indice_ligne == element.Ordonnee or indice_ligne == 0):
	
			liste_donnees_1.append(element.Nom.encode('utf-8'))

		if indice_ligne != element.Ordonnee and indice_ligne != 0 and not indice_arret:
		
			liste_donnees_2.append(liste_donnees_1)
			liste_donnees_1 = []
			indice_arret = 1
			
		indice_ligne = element.Ordonnee
	
	indice_ligne = 0
	
	for element in queryset_donnees:
		
		if indice_ligne == element.Ordonnee or indice_ligne == 0:
		
			if element.Type == "euros":
				
				liste_donnees_1.append(element.Contenu.encode('utf-8')+u" euros")
			
			elif element.Type == "nb_mois":
			
				liste_donnees_1.append(element.Contenu.encode('utf-8')+u" mois")
			
			elif element.Type == "pourcentage":

				liste_donnees_1.append(element.Contenu.encode('utf-8')+u" %")
			
			else:

				liste_donnees_1.append(element.Contenu.encode('utf-8'))		
			
		if indice_ligne != element.Ordonnee and indice_ligne != 0:
		
			liste_donnees_2.append(liste_donnees_1)
			liste_donnees_1 = []
			
			if element.Type == "euros":
				
				liste_donnees_1.append(element.Contenu.encode('utf-8')+u" euros")
			
			elif element.Type == "nb_mois":
			
				liste_donnees_1.append(element.Contenu.encode('utf-8')+u" mois")
			
			elif element.Type == "pourcentage":

				liste_donnees_1.append(element.Contenu.encode('utf-8')+u" %")
			
			else:

				liste_donnees_1.append(element.Contenu.encode('utf-8'))	
			
		indice_ligne = element.Ordonnee
		
	return liste_donnees_2
		
def construction_fichier_xls(queryset_donnees):
	
	indice_ligne = 0
	abscisse = 0
	ordonnee = 0
	indice_arret = 0
	liste_donnees_1 = []
	liste_donnees_2 = []
	fichier_xls = xlwt.Workbook(encoding="UTF-8")
	ma_feuille = fichier_xls.add_sheet("Données extraites")
	style_entete = xlwt.easyxf('font: bold True; borders: left thin, right thin, top thin, bottom thin; alignment: horizontal center;')

	for element in queryset_donnees:
	
		if not indice_arret and (indice_ligne == element.Ordonnee or indice_ligne == 0):
	
			abscisse = abscisse + 1
			ma_feuille.write(ordonnee,abscisse,element.Nom,style_entete)
			
		if indice_ligne != element.Ordonnee and indice_ligne != 0 and not indice_arret:
		
			indice_arret = 1
			abscisse = 0
			
		indice_ligne = element.Ordonnee
		
	indice_ligne = 0
	ordonnee = ordonnee + 1
	abscisse = 0
	
	for element in queryset_donnees:
		
		if indice_ligne == element.Ordonnee or indice_ligne == 0:
		
			abscisse = abscisse + 1
			
			if element.Type == "euros":
				
				ma_feuille.write(ordonnee,abscisse,element.Contenu+u" €")
			
			elif element.Type == "nb_mois":
			
				ma_feuille.write(ordonnee,abscisse,element.Contenu+u" mois")
				
			elif element.Type == "pourcentage":

				ma_feuille.write(ordonnee,abscisse,element.Contenu+u" %")
			
			else:

				ma_feuille.write(ordonnee,abscisse,element.Contenu)
			
		if indice_ligne != element.Ordonnee and indice_ligne != 0:
		
			abscisse = 1
			ordonnee = ordonnee + 1
			
			if element.Type == "euros":
				
				ma_feuille.write(ordonnee,abscisse,element.Contenu+u" €")
			
			elif element.Type == "nb_mois":
			
				ma_feuille.write(ordonnee,abscisse,element.Contenu+u" mois")
				
			elif element.Type == "pourcentage":

				ma_feuille.write(ordonnee,abscisse,element.Contenu+u" %")
			
			else:

				ma_feuille.write(ordonnee,abscisse,element.Contenu)
			
		indice_ligne = element.Ordonnee
		
	return fichier_xls