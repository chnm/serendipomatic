import requests, oauth2, urlparse
from dateutil.parser import parse
from libZotero import zotero
from bs4 import BeautifulSoup

from smartstash.core.utils import tokenize

def get_oauth_access_token():
    consumerKey = "e61504b6e21a1df7d146"
    consumerSecret = "294d72ffd8dce053aadb"

    consumer = oauth2.Consumer(consumerKey, consumerSecret)
    client = oauth2.Client(consumer)

    requestTokenURL = "https://www.zotero.org/oauth/request"
    response, content = client.request(requestTokenURL, "POST")
    requestToken = dict(urlparse.parse_qsl(content))

    authorizeURL = "https://www.zotero.org/oauth/authorize"
    print "Visit this URL: {0}?oauth_token={1}".format(authorizeURL, requestToken['oauth_token'])

    PIN = raw_input("Enter the PIN: ")

    accessTokenURL = "https://www.zotero.org/oauth/access"
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

    feedUrl = feedLink.attrs['href']
    userID = feedUrl[feedUrl.find("users/") + len("users/") : feedUrl.find("/collections")]
    return userID

def get_user_items(userID, public = True, numItems = None):
    if public: zlib = zotero.Library("user", userID, '', '')
    else: zlib = zotero.Library("user", userID, '', get_oauth_access_token())

    items = zlib.fetchItems({'limit': numItems, 'order': 'dateAdded'})

    metadataTypes = ["date", "title", "creatorSummary", "keywords", 'abstractNote']
    results = {m : [] for m in metadataTypes}

    for item in items:
        for metadataType in metadataTypes:
            metadata = item.get(metadataType)

            if not metadata: continue
            metadata = metadata.encode("ascii", "ignore")

            if metadataType == "date":
                metadata = parse(metadata)

            results[metadataType].append(metadata)

    for s in results['abstractNote']: results['keywords'] += tokenize(s)
    return results

if __name__ == "__main__":
    print get_user_items(get_userID("briancroxall"), public = True)