import oauth2
import urlparse
from libZotero import zotero
consumerKey = "e61504b6e21a1df7d146"
consumerSecret = "294d72ffd8dce053aadb"

consumer = oauth2.Consumer(consumerKey, consumerSecret)
client = oauth2.Client(consumer)

requestTokenURL = "https://www.zotero.org/oauth/request"
response, content = client.request(requestTokenURL, "POST")
requestToken = dict(urlparse.parse_qsl(content))

authorizeURL = "https://www.zotero.org/oauth/authorize"
print "{0}?oauth_token={1}".format(authorizeURL, requestToken['oauth_token'])

PIN = raw_input("Enter the PIN: ")

accessTokenURL = "https://www.zotero.org/oauth/access"
token = oauth2.Token(requestToken['oauth_token'], requestToken['oauth_token_secret'])
token.set_verifier(PIN)
client = oauth2.Client(consumer, token)

response, content = client.request(accessTokenURL, "POST")
accessToken = dict(urlparse.parse_qsl(content))

print accessToken['oauth_token'], accessToken['oauth_token_secret']