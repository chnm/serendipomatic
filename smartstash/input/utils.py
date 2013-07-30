import string
#We want to eliminate all punctuation except single quotes.
#This isn't the only case (sometimes you have single quotes around a word, which we do want to get rid of)
#TODO: a regex that will do this better than the current method (python's string.punctuation without the single quote)
#TODO: find a list of stopwords, don't count them
#nltk?

def common_words(textString, n):
    wordList = textString.split()
    sanitizedWordList = map(lambda word: ''.join([c for c in word if c not in string.punctuation or c == "\'"]), wordList)
    wordCounts = {}
    for word in wordList:
        wordCounts[word] = wordCounts.get(word, 0) + 1
    return sorted(wordCounts, key = wordCounts.get, reverse = True)[0:n]