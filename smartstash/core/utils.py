import string
import simplejson
import re
import requests
import nltk
import random
import re

from django.conf import settings

#We want to eliminate all punctuation except single quotes.
#This isn't the only case (sometimes you have single quotes around a word, which we do want to get rid of)
#TODO: a regex that will do this better than the current method (python's string.punctuation without the single quote)
#TODO: find a list of stopwords, don't count them
#nltk?

# patch nltk path for heroku
if settings.HEROKU:
    nltk.data.path.append('./smartstash/nltk_data/')

# map language codes provided by guess-language
# to available sets of stopwords in nltk
stopword_lang = {
    'nl': 'dutch',
    'fi': 'finnish',
    'de': 'german',
    'it': 'italian',
    'pt': 'portuguese',
    'es': 'spanish',
    'tr': 'turkish',
    'da': 'danish',
    'en': 'english',
    'fr': 'french',
    'hu': 'hungarian',
    'no': 'norwegian',
    'ru': 'russian',
    'sv': 'swedish'
}


def tokenize(text, lang='en'):
    # if language is not specified or not in our list, fall back to english
    stopwords = nltk.corpus.stopwords.words(stopword_lang.get(lang, 'english'))

    tokens = nltk.word_tokenize(text)

    words = [w.lower() for w in tokens
             if w.isalnum() and w.lower() not in stopwords]
    # NOTE: isalnum will restrict to alpha and numeric content (i.e., words & dates);
    # will probably drop date ranges as well as contractions or quoted terms
    return words

def common_words(text, max_items=15, lang='en'):
    words = tokenize(text, lang)

    freqdist = nltk.FreqDist()
    for word in words:
        freqdist.inc(word)

    if max_items is None:
        return {'keywords': freqdist.keys()}
    return {'keywords': freqdist.keys()[:max_items]}

    # TODO: also look at using nltk to generate collocations


"""
Returns JSON response from dbpedia spotlight annotate (or other source)
"""
def query(query) :
    r = requests.get(query['url'], params=query['params'], headers = {'accept': 'application/json'})

    return r.text

"""
Return a set named entities from a Spotting query
"""
def get_names_from_spotting(doc, lang='en'):
    json_data = simplejson.loads(doc)
    stopwords = nltk.corpus.stopwords.words(stopword_lang.get(lang, 'english'))

    name_set = set()
    # if only a single item is recognized, we don't get a list back
    annotations = json_data['annotation']['surfaceForm']
    # make it a list so we can treat it the same
    if not isinstance(annotations, list):
        annotations = [annotations]
    for item in annotations:
        name = unicode(item['@name']) or ''
        name = name.translate({None: string.punctuation}).strip()
        if(name not in stopwords) :
            name_set.add(name.lower())
    return name_set

"""
"""
def get_names_from_annotate(doc) :
    json_data = simplejson.loads(doc)
    name_set = set()

    for item in json_data.get('Resources', []):
        name_set.add(item['@surfaceForm'].lower())

    return name_set

"""
Returns a dictionary of search terms
keywords - combination of spotting and annotate queries
people -
places -
"""
def get_search_terms(text, lang='en'):
    spot = {
        'url':'http://spotlight.dbpedia.org/rest/spot',
        'params': {
            'text':text,
        }
    }

    annotate = {
        'url': 'http://spotlight.dbpedia.org/rest/annotate',
        'params': {
            'text': text,
            'confidence': 0.3,
            'support': 60,
        }
    }

    terms = { }

    spot_set = set()
    annotate_set = set()

    resp_s = query(spot)
    spot_set = get_names_from_spotting(resp_s, lang)

    resp_a = query(annotate)
    annotate_set = get_names_from_annotate(resp_a)

    terms = _get_types(resp_a)
    # get a random set of keywords from the union of spot and annotate
    terms['keywords'] = _get_random(spot_set.union(annotate_set))
    # gets early and late dates if not present these are enpty strings
    terms['dates'] = _get_dates(text)

    return terms

# Gets a random set of (at most 15) keywords
def _get_random(keywords, max_items=15) :
    if(max_items > len(keywords)) :
        max_items = int(len(keywords)*.7)
    return random.sample(keywords, max_items)


def _get_types(entities) :
    json_data = simplejson.loads ( entities )
    types = {
        'people': [],
        'places': [],
    }
    for item in json_data.get('Resources', []):
        str_types = str(item['@types'])
        if('DBpedia:Person' in str_types) :
            types['people'].append(item['@surfaceForm'])
        if('DBpedia:Place' in str_types) :
            types['places'].append(item['@surfaceForm'])

     # make the lists distinct get_search_terms
    types['places'] = list(set(types['places']))
    types['people'] = list(set(types['people']))

    return types

# Get early and late daetes. Currently only support four digit years
# TODO should expand support at a later point
def _get_dates(text) :
    dates = {
        'early':'',
        'late':''
    }
    regex = re.compile('\d{4}')
    all_dates = regex.findall(text)
    if(all_dates and len(all_dates) >2) :
        dates['early'] = all_dates[0]
        dates['late'] = all_dates[1]
    return dates
