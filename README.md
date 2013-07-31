
Installation
-------------

Install pip if you don't have it:
easy_install pip (or sudo easy_install pip)

(sudo) pip install -r requirements.txt

open question: do we want to use virtualenv?

Make a copy of smartstash/localsettings.py.dist named smartstash/localsettings.py
and fill in any required settings:
- **SECRET_KEY**: generate one at http://www.miniwebtool.com/django-secret-key-generator/
- **API_KEY**: api keys will be listed in our dev/design google document
- **DATABASES**: (sqlite3 should be fine for development)


Add new python dependencies to requirements.txt as needed.

Installing the nltk stopwords corpus requires an additional step:

```bash
python -m nltk.downloader stopwords
```

Run syncdb to do initial database setup:

```bash
python manage.py syncdb
```

To start the local dev server:

```bash
python manage.py runserver
```

