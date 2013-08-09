
[![Build Status](https://travis-ci.org/chnm/serendipomatic.png)](https://travis-ci.org/chnm/serendipomatic)

About
-----
[Serendip-o-matic](http://serendipomatic.org/) connects your sources to digital materials
located in libraries, museums, and archives around the world. By first examining your
research interests, and then identifying related content in locations such as the Digital
Public Library of America (DPLA), Europeana, and Flickr Commons, our serendipity engine
helps you discover photographs, documents, maps and other primary sources.

Whether you begin with text from an article, a Wikipedia page, or a full Zotero
collection, Serendip-o-matic's special algorithm extracts key terms and returns a
surprising reflection of your interests. Because the tool is designed mostly for
inspiration, search results aren't meant to be exhaustive, but rather suggestive,
pointing you to materials you might not have discovered. At the very least, the magical
input-output process helps you step back and look at your work from a new perspective.
Give it a whirl. Your sources may surprise you.

Installation notes for developers
---------------------------------

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

