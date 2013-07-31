import string
import requests
import nltk
from nltk.corpus import stopwords

#We want to eliminate all punctuation except single quotes.
#This isn't the only case (sometimes you have single quotes around a word, which we do want to get rid of)
#TODO: a regex that will do this better than the current method (python's string.punctuation without the single quote)
#TODO: find a list of stopwords, don't count them
#nltk?

"""
Returns JSON response from dbpedia spotlight 
"""	
def query( url, p ) : 
    r = requests.get(url, params=p, headers = {'accept': 'application/json'})
    return r.text




def common_words(text, max_items=15):
    # TODO: make stopword language configurable?
    stopwords = nltk.corpus.stopwords.words('english')

    tokens = nltk.word_tokenize(text)

    words = [w.lower() for w in tokens
             if w.isalpha() and w.lower() not in stopwords]
     # NOTE: isalpha drops numeric content like dates or date ranges
     # as well as contractions or quoted terms

    freqdist = nltk.FreqDist()
    for word in words:
        freqdist.inc(word)
    return {'keywords': freqdist.keys()[:max_items]}

    # TODO: also look at using nltk to generate collocations
