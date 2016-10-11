#-*- coding: utf-8 -*-


#-------Général-------------------------------------------

SECRET_KEY = ''

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [''] 

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'distributed_scraping.urls'

WSGI_APPLICATION = 'distributed_scraping.wsgi.application'

STATIC_ROOT = '~/distributed_scraping/public/static/' 
STATIC_URL = '/static/' 

ADMINS = (
('Juju', 'julien.enilrahc@gmail.com'),
)

TEMPLATE_DIRS = (
  "~/distributed_scraping/templates/",
)

APPEND_SLASH = True 

#-------Apps-------------------------------------------

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	'vitrine',
	'utils',
	'comptes_clients',
	'plateforme',
)

#-------Middleware-------------------------------------------

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.locale.LocaleMiddleware', #pour mettre le site d'admin en Français
	'lockdown.middleware.LockdownMiddleware',
)

#---------BDD----------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'pass',
        'HOST': 'host',
    }
}

#---------Localization----------------------------------------------------

TIME_ZONE = 'Europe/Paris' 
LANGUAGE_CODE = 'fr-FR'
USE_I18N = True
USE_L10N = True

USE_TZ = False

#---------Emails----------------------------------------------------

EMAIL_HOST = "host"
EMAIL_HOST_PASSWORD = "pass"
EMAIL_HOST_USER = "contact email"
MANAGERS = ADMINS

#---------Authentification----------------------------------------------------

AUTH_PROFILE_MODULE = 'comptes_clients.Client'
LOGIN_URL = '/login'

