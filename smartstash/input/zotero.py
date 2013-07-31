import requests
from libZotero import zotero
from bs4 import BeautifulSoup

def get_userID(username):
    r = requests.get('https://www.zotero.org/{0}/items'.format(username), verify=False)
    feedLink = BeautifulSoup(r.text).find_all('a', attrs = {"class" : "feed-link"}).pop()
    #Finds the RSS feed link on the page (first with these properties)
    #An okay place to get the userID from, could be better.

    feedUrl = feedLink.attrs['href']
    userID = feedUrl[feedUrl.find("users/") + len("users/") : feedUrl.find("/collections")]
    return userID

def get_user_items(userID, numItems = 20):
    zlib = zotero.Library("user", userID, '', '')
    items = zlib.fetchItems({'limit': numItems, 'order': 'dateAdded'})

    metadataTypes = ["abstractNote", "date", "title", "author"]
    results = {m : [] for m in metadataTypes}

    for item in items:
        for metadataType in metadataTypes:
            #conversion from unicode to ascii
            metadata = item.get(metadataType).encode("ascii", "ignore")
            if metadata: results[metadataType].append(metadata)

    return results

print get_user_items(get_userID("erose1"))