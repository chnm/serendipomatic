import requests, oauth2, urlparse, urllib
from libZotero import zotero
from bs4 import BeautifulSoup
import smartstash.core.utils
from dateutil.parser import parse
from smartstash.core.utils import tokenize
from django.core.urlresolvers import reverse
from django.conf import settings

consumerKey = settings.API_KEYS['ZOTERO_CONSUMER_KEY']
consumerSecret = settings.API_KEYS['ZOTERO_CONSUMER_SECRET']
requestTokenURL = "https://www.zotero.org/oauth/request"
authorizeURL = "https://www.zotero.org/oauth/authorize"
accessTokenURL = "https://www.zotero.org/oauth/access"

UPPER_LIMIT = 99

def oauth_authorize_url(request):
    consumer = oauth2.Consumer(consumerKey, consumerSecret)
    client = oauth2.Client(consumer)

    # generate callback url relative to the current server url
    # NOTE: if this doesn't match the server, session data won't be preserved
    # across the redirect!!!
    callback_url =  request.build_absolute_uri(reverse('zotero'))
    response, content = client.request(requestTokenURL, "POST",
                                       body = urllib.urlencode({'oauth_callback' : callback_url}))
    requestToken = dict(urlparse.parse_qsl(content))

    request.session['request_token'] = requestToken
    request.session['consumer'] = consumer

    return "{0}?oauth_token={1}".format(authorizeURL, requestToken['oauth_token'])

def accessToken_userID_from_oauth_verifier(request, oauth_verifier, requestToken):
    token = oauth2.Token(requestToken['oauth_token'], requestToken['oauth_token_secret'])

    token.set_verifier(oauth_verifier)
    client = oauth2.Client(request.session['consumer'], token)

    response, content = client.request(accessTokenURL, "POST")
    accessToken = dict(urlparse.parse_qsl(content))
    # print "accessToken_userID_from_oauth_verifier <says>: "
    # print accessToken
    print
    return accessToken['oauth_token'], accessToken['userID']

def get_userID_if_public(username):

    try:
        r = requests.get('https://www.zotero.org/{0}/items'.format(username), verify=False)
        feedLink = BeautifulSoup(r.text).find_all('a', attrs = {"class" : "feed-link"}).pop()
        #Finds the RSS feed link on the page (first with these properties)
        #An okay place to get the userID from, could be better.
        #When Zotero people add an API call to do this, this function should die.

        feedUrl = feedLink.attrs['href']
        userID = feedUrl[feedUrl.find("users/") + len("users/") : feedUrl.find("/collections")]
        return userID

    except:
        return False

def get_user_items(request, userID, userKey, public = True, startIndex = 0, numItems = 50):
    if public: zlib = zotero.Library("user", userID, '', '')
    else: zlib = zotero.Library("user", userID, '', userKey)

    items = zlib.fetchItems({'limit': numItems, 'start': startIndex})

    metadataTypes = ["date", "title", "creatorSummary", "keywords"]
    results = {m : [] for m in metadataTypes}

    for item in items:
        for metadataType in metadataTypes:
            metadata = item.get(metadataType)

            if not metadata: continue

            try:
                metadata = metadata.encode("ascii", "ignore")

            except (ValueError, AttributeError):
                print "{0} at {1}".format("error", metadata)

            results[metadataType].append(metadata)

    print results
    return results
