#  Copyright 2016 Google Inc. All Rights Reserved.
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License. 

"""
Django settings for alerts project.

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
SECRET_KEY = '-1d5)3@2+h246!tlxifsh5d3fyl8e5m4w+=(4e79z%d^!7^+ec'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'extralife',
    'fanfunding',
    'imraising',
    'registration',
    'patreon',
    'sponsors',
    'twitchalerts',
    'streamjar',
    'streamtip',
    'googaccount',
    'upload',
    'ytsubs',
    'youtubesubs',
    'donations',
    'twitchaccount',
    'twitchfollows',
    'meta',
    'accounts'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'alerts.urls'

WSGI_APPLICATION = 'alerts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
STATIC_ROOT = './static/'

ALLOWED_HOSTS = ['www.livestreamalerts.com', 'livestreamalerts.com', '*']
AUTH_PROFILE_MODULE = 'main.UserProfile'

ACCOUNT_ACTIVATION_DAYS = 7
DEFAULT_FROM_EMAIL = 'crschmidt@crschmidt.net'
DEFAULT_TO_EMAIL = 'crschmidt@crschmidt.net'
LOGIN_URL = '/accounts/login/'
SERVER_BASE = "http://localhost:8000/"
GCS_BUCKET = "storage.livestreamalerts.com"
CURRENCY_CONVERSION = "datafiles/currency.json"
FONT_LIST = "datafiles/font_list.txt"
RUNNER_DEBUG=DEBUG
LOGIN_REDIRECT_URL = '/home/'
