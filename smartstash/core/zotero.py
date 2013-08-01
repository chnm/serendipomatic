import requests, oauth2, urlparse, urllib
from libZotero import zotero
from bs4 import BeautifulSoup
import smartstash.core.utils
from smartstash.core.utils import tokenize

consumerKey = "e61504b6e21a1df7d146"
consumerSecret = "294d72ffd8dce053aadb"
requestTokenURL = "https://www.zotero.org/oauth/request"
authorizeURL = "https://www.zotero.org/oauth/authorize"
accessTokenURL = "https://www.zotero.org/oauth/access"
callbackURL = 'http://www.google.com'

def get_oauth_access_token():
    consumer = oauth2.Consumer(consumerKey, consumerSecret)
    client = oauth2.Client(consumer)

    response, content = client.request(requestTokenURL, "POST",
                                       body = urllib.urlencode({'oauth_callback' : callbackURL}))
    requestToken = dict(urlparse.parse_qsl(content))

    print "Visit this URL: {0}?oauth_token={1}".format(authorizeURL, requestToken['oauth_token'])
    PIN = raw_input("Enter the PIN: ")

    token = oauth2.Token(requestToken['oauth_token'], requestToken['oauth_token_secret'])
    token.set_verifier(PIN)
    client = oauth2.Client(consumer, token)

    response, content = client.request(accessTokenURL, "POST")
    accessToken = dict(urlparse.parse_qsl(content))

    return accessToken['oauth_token']

def get_userID(username):
    r = requests.get('https://www.zotero.org/{0}/items'.format(username), verify=False)
    feedLink = BeautifulSoup(r.text).find_all('a', attrs = {"class" : "feed-link"}).pop()
    #Finds the RSS feed link on the page (first with these properties)
    #An okay place to get the userID from, could be better.
    #When Zotero people add an API call to do this, this function should die.

    feedUrl = feedLink.attrs['href']
    userID = feedUrl[feedUrl.find("users/") + len("users/") : feedUrl.find("/collections")]
    return userID

def get_user_items(userID, public = True, startIndex = 0, numItems = 99):
    if public: zlib = zotero.Library("user", userID, '', '')
    else: zlib = zotero.Library("user", userID, '', get_oauth_access_token())

    items = zlib.fetchItems({'limit': numItems, 'start': startIndex})
    metadataTypes = ["date", "title", "creatorSummary", "keywords", "abstractNote", "extra", "tags"]
    results = {m : [] for m in metadataTypes}

    while len(items) == numItems:
        for item in items:
            for metadataType in metadataTypes:
                metadata = item.get(metadataType)

                if not metadata: continue

                try:
                    metadata = metadata.encode("ascii", "ignore")
                    # if metadataType == "date":
                    #     metadata = parse(metadata)

                except ValueError:
                    print "ValueError at {0}".format(metadata)

                results[metadataType].append(metadata)
        #for s in results['abstractNote']: results['keywords'] += tokenize(s)
        startIndex += numItems
        items = zlib.fetchItems({'limit': numItems, 'start': startIndex})

    return results

if __name__ == "__main__":
    print get_user_items(get_userID("briancroxall"), public = True)