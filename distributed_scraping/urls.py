#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#-----------------------------------------------------------

urlpatterns = patterns('',

	url(r'^$','vitrine.views.index'),
	url(r'^contact$','vitrine.views.contact'),
	url(r'^mentionslegales$','vitrine.views.mentionslegales'),

	url(r'^login$','plateforme.views.vue_login'),
	url(r'^plateforme$','plateforme.views.index'),
	url(r'^logout$','plateforme.views.vue_logout'),
	url(r'^ajax_tableau','plateforme.views.ajax_tableau'),
	url(r'^aucune_alerte','plateforme.views.aucune_alerte'),
	url(r'^ajax_graphiques','plateforme.views.ajax_graphiques'),
	url(r'^telechargement_tableau_xls','plateforme.views.telechargement_tableau_xls'),
	
	url(r'^admin/', include(admin.site.urls)),
	
)
