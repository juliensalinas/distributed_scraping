#-*- coding: utf-8 -*-

'''
Gestion de l'envoi des emails
'''

import StringIO
import csv
import xlwt

from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_admins

from comptes_clients.models import Donnee_scrapee

from utils.creation_pieces_jointes import construction_fichier_xls,construction_fichier_csv

#------------------------------------------------------

def email_alerte_scraper(message):
	
	contenu_texte = message
		
	mail_admins(u'Problème avec un scraper !', contenu_texte)
	
def email_notification(email,libelle_commercial_scraper,id_scraper):

	queryset_donnees = Donnee_scrapee.objects.filter(Fk_Scrapers_id=id_scraper,Envoyer_notification=1).order_by('Ordonnee','Abscisse')

	contenu_html = u"<html><body>"

	contenu_texte = libelle_commercial_scraper + u"\n\n"
	contenu_html = contenu_html + libelle_commercial_scraper + u"<br><br>"

	contenu_texte = contenu_texte + u"Voici les dernières données detectées par Soupeo : \n"
	contenu_html = contenu_html + u"Voici les dernières données detectées par Soupeo : <br>"

	indice_ligne = 0

	for element in queryset_donnees:

		if element.Ordonnee != indice_ligne:
		
			contenu_texte = contenu_texte + u"\n\n"
			contenu_html = contenu_html + u"<br><br>"

		contenu_texte = contenu_texte + element.Nom + u" : " + element.Contenu + u"\n"

		if element.Type == "url":

			contenu_html = contenu_html + element.Nom + u" : <a href=\""+element.Contenu+u"\">plus de détails ici</a> <br>"

		elif element.Type == "euros":
		
			contenu_html = contenu_html + element.Nom + u" : " + element.Contenu + u" €<br>"
			
		elif element.Type == "nb_mois":
		
			contenu_html = contenu_html + element.Nom + u" : " + element.Contenu + u" mois<br>"
		
		elif element.Type == "pourcentage":

			contenu_html = contenu_html + element.Nom + u" : " + element.Contenu + u" %<br>"
		
		else:

			contenu_html = contenu_html + element.Nom + u" : " + element.Contenu + u"<br>"

		indice_ligne = element.Ordonnee

	contenu_html = contenu_html + u"</body></html>"
		
	message = EmailMultiAlternatives(u'Nouvelles données apparues', contenu_texte, 'Alerte Soupeo <alerte@soupeo.fr>', [email], bcc=["julien.enilrahc@gmail.com"])                                      
	message.attach_alternative(contenu_html, "text/html") 
	
	message.send()

def csv_email_notification(email,libelle_commercial_scraper,id_scraper):
	
	queryset_donnees = Donnee_scrapee.objects.filter(Fk_Scrapers_id=id_scraper,Envoyer_notification=1).order_by('Ordonnee','Abscisse')

	contenu_html = u"<html><body>"

	contenu_texte = libelle_commercial_scraper + u"\n\n"
	contenu_html = contenu_html + libelle_commercial_scraper + u"<br><br>"

	contenu_texte = contenu_texte + u"Voici en pièce jointe les dernières données detectées par Soupeo.\n"
	contenu_html = contenu_html + u"Voici en pièce jointe les dernières données detectées par Soupeo.<br>"

	contenu_html = contenu_html + u"</body></html>"

	liste_donnees_csv = construction_fichier_csv(queryset_donnees)

	csvfile = StringIO.StringIO()
	csvwriter = csv.writer(csvfile)
	csvwriter.writerows(liste_donnees_csv)

	message = EmailMultiAlternatives(u'Nouvelles données apparues', contenu_texte, 'Alerte Soupeo <alerte@soupeo.fr>', [email], bcc=["julien.enilrahc@gmail.com"])                                      
	message.attach_alternative(contenu_html, "text/html") 
	message.attach('Donnees_extraites.csv', csvfile.getvalue(), 'text/csv')

	message.send()

def xls_email_notification(email,libelle_commercial_scraper,id_scraper):
	
	queryset_donnees = Donnee_scrapee.objects.filter(Fk_Scrapers_id=id_scraper,Envoyer_notification=1).order_by('Ordonnee','Abscisse')

	contenu_html = u"<html><body>"

	contenu_texte = libelle_commercial_scraper + u"\n\n"
	contenu_html = contenu_html + libelle_commercial_scraper + u"<br><br>"

	contenu_texte = contenu_texte + u"Voici en pièce jointe les dernières données detectées par Soupeo.\n"
	contenu_html = contenu_html + u"Voici en pièce jointe les dernières données detectées par Soupeo.<br>"

	contenu_html = contenu_html + u"</body></html>"

	fichier_xls = construction_fichier_xls(queryset_donnees)
	
	reponse = StringIO.StringIO()
	fichier_xls.save(reponse)

	message = EmailMultiAlternatives(u'Nouvelles données apparues', contenu_texte, 'Alerte Soupeo <alerte@soupeo.fr>', [email], bcc=["julien.enilrahc@gmail.com"])                                      
	message.attach_alternative(contenu_html, "text/html") 
	message.attach('Donnees_extraites.xls', reponse.getvalue(), 'application/vnd.ms-excel')

	message.send()
