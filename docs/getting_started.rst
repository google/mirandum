Getting Started
===============

Install the rquirements in the requirements.txt file (pip install -r
requirements.txt); then::

    cd mirandum/alerts
    DJANGO_SETTINGS_MODULE="settings.base" python manage.py migrate
    DJANGO_SETTINGS_MODULE="settings.base" python manage.py runserver

Then you can access a local server at http://localhost:8000/
