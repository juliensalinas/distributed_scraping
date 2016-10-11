#-*- coding: utf-8 -*-

'''
Consultation des clients via l'interface admin
'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from comptes_clients.models import Client

#------------------------------------------------

class ClientInline(admin.StackedInline):

    model = Client
    can_delete = False
    verbose_name_plural = 'Client'

class UserAdmin(UserAdmin):

    inlines = (ClientInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
