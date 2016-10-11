#-*- coding: utf-8 -*-

'''
Gestion de l'envoi des notifications
'''

from comptes_clients.models import Scraper
from comptes_clients.models import Email

from utils.notifications.envoi_emails import email_notification
from utils.notifications.envoi_emails import csv_email_notification
from utils.notifications.envoi_emails import xls_email_notification

#------------------------------------------------------

def envoi_notification(id_scraper):
	
	scraper = Scrapers.objects.filter(id=id_scraper)[0]

	notification_email = scraper.Notification_email
	notification_sms = scraper.Notification_sms
	notification_csv_email = scraper.Notification_csv_email
	notification_xls_email = scraper.Notification_xls_email

	if notification_email:

		fk_Client_id = scraper.Fk_Client_id
		libelle_commercial_scraper = scraper.Libelle_commercial_scraper
		queryset_emails = Emails.objects.filter(Fk_Client_id=fk_Client_id)

		for element in queryset_emails:

			email = element.Email
			email_notification(email,libelle_commercial_scraper,id_scraper)

	if notification_csv_email:

		fk_Client_id = scraper.Fk_Client_id
		libelle_commercial_scraper = scraper.Libelle_commercial_scraper
		queryset_emails = Emails.objects.filter(Fk_Client_id=fk_Client_id)

		for element in queryset_emails:

			email = element.Email
			csv_email_notification(email,libelle_commercial_scraper,id_scraper)
			
	if notification_xls_email:

		fk_Client_id = scraper.Fk_Client_id
		libelle_commercial_scraper = scraper.Libelle_commercial_scraper
		queryset_emails = Emails.objects.filter(Fk_Client_id=fk_Client_id)

		for element in queryset_emails:

			email = element.Email
			xls_email_notification(email,libelle_commercial_scraper,id_scraper)

	if notification_sms:

		pass



