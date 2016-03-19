"""
Django settings for superlists project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9ik*2*geqo2l=t6v+4k9a#j6t4^tyve*v#+zl2#-n-d_p^6dic'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'superlists.urls'

WSGI_APPLICATION = 'superlists.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
#		'BACKEND': 'django.template.backends.jinja2.Jinja2',
		'APP_DIRS': True,
	},
]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'



#===========================================================================================
#===========================================================================================
#===========================================================================================

def tuplePop(mytuple, toremove):
	return [t for t in mytuple if t != toremove]

def tuplePush(mytuple, toadd):
	if toadd not in mytuple:
		mytuple += ( toadd, )
	return mytuple

INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'lists')
INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'django_extensions')
INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'rest_framework')
INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'jsonpickle')
INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'inflect')
INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'suds')
#INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'soap_app')
#INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'soappy')
#INSTALLED_APPS = tuplePush(INSTALLED_APPS, 'django.contrib.sites')

INSTALLED_APPS = tuplePop(INSTALLED_APPS, 'django.contrib.admin')

DATABASES['default']['PASSWORD'] = 'mysqlmysqlmysql'

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))


#REST_FRAMEWORK = {
#    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#    ]
#}


