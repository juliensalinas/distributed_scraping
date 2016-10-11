#-*- coding: utf-8 -*-

'''
Formulaires de la plateforme
'''

from django import forms

#-------------------------------------------------------------------

class form_login_plateforme(forms.Form):

	# formulaire de login à la plateforme (pas encore connecté)
	
	nom_utilisateur = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", 'autofocus':'', 'spellcheck':'false', 'value':'', 'maxlength': '100'}))
	mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe", 'spellcheck':'false', 'value':'', 'maxlength': '100'}))

class form_telechargement_tableau(forms.Form):

	# formulaire permettant au client de choisir la date à partir de laquelle télécharger les données

	date = forms.DateField (input_formats=['%d/%m/%Y'],widget=forms.TextInput(attrs={'placeholder': "Cliquez pour ouvrir le calendrier",'type':'text','id':'datepicker','autocomplete':'off'}))


