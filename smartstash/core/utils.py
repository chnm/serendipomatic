import string
import json
import requests
import nltk
from nltk.corpus import stopwords

#We want to eliminate all punctuation except single quotes.
#This isn't the only case (sometimes you have single quotes around a word, which we do want to get rid of)
#TODO: a regex that will do this better than the current method (python's string.punctuation without the single quote)
#TODO: find a list of stopwords, don't count them
#nltk?


def common_words(text, max_items=15):
    # TODO: make stopword language configurable?
    stop_words = nltk.corpus.stopwords.words('english')

    tokens = nltk.word_tokenize(text)

    words = [w.lower() for w in tokens
             if w.isalnum() and w.lower() not in stop_words]
    # NOTE: isalnum will restrict to alpha and numeric content (i.e., words & dates);
    # will probalby drop date ranges as well as contractions or quoted terms

    freqdist = nltk.FreqDist()
    for word in words:
        freqdist.inc(word)
    return {'keywords': freqdist.keys()[:max_items]}

    # TODO: also look at using nltk to generate collocations


"""
Returns JSON response from dbpedia spotlight annotate (or other source)
"""
def query( query ) :
	r = requests.get(query['url'], params=query['params'], headers = {'accept': 'application/json'})

	return r.text

"""
Return a set named entities from a Spotting query
"""
def getEntityNameFromSpot( doc ) :
	json_data = simplejson.loads(doc)
	name_set = set()
	for item in json_data['annotation']['surfaceForm'] :
		name_set.add( item['@name'] )

	return name_set

"""
"""
def getEntityNameFromAnnotate( doc ) :
	json_data = simplejson.loads ( doc )
	name_set = set()

	for item in json_data['Resources'] :
		name_set.add( item['@surfaceForm'] )

	return name_set

# Returns a dictionary of search terms ** KEYWORD ONLY **
def getTerms( text ) :
	spot = {
		'url':'http://spotlight.dbpedia.org/rest/spot',
		'params': {
			'text':text,
		}
	}

	annotate = {
		'url': 'http://spotlight.dbpedia.org/rest/annotate',
		'params': {
			'text':sampletext,
			'confidence':0.3,
			'support':60,
		}
	}

	terms = { }

	spot_set = set()
	annotate_set = set()

	resp_s = query( spot )
	spot_set = getEntityNameFromSpot(resp_s)

	resp_a = query( annotate )
	annotate_set = getEntityNameFromAnnotate(resp_a)
	# get list of people
	people_set = getPeople( resp_a )

	terms['keywords'] = spot_set.union(annotate_set)
	terms['people'] = people_set
	term['places'] = place_set
	return terms



"""
Returns the list of DBpedia:Person records
"""
def getPeople( entities ) :
	json_data = simplejson.loads ( entities )
	name_set = set()
	for item in json_data['Resources'] :
		type = str(item['@types'])
		if( 'DBpedia:Person' in type) :
			name_set.add( item['@surfaceForm'] )
	return name_set

