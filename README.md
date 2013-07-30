
Installation
-------------

Install pip if you don't have it:
easy_install pip (or sudo easy_install pip)

(sudo) pip install -r requirements.txt

open question: do we want to use virtualenv?

Copy smartstash/localsettings.py.dist to smartstash/localsettings.py
and fill in any required settings (SECRET_KEY, API_KEY).

Add new python dependencies to requirements.txt as needed.


To start the local dev server:

python manage.py runserver

