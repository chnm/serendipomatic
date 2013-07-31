
import nltk
from nltk.corpus import stopwords


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
