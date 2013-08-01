from urllib2 import Request, urlopen
from urllib import url2pathname
from django.utils import simplejson
from django.conf import settings
from social_auth.utils import setting
from social_auth.backends.google import GoogleOAuthBackend, GoogleOAuth, validate_whitelists

# Google OAuth base configuration
AUTHORIZATION_URL = "https://www.zotero.org/oauth/authorize"
REQUEST_TOKEN_URL = "https://www.zotero.org/oauth/request"
ACCESS_TOKEN_URL = "https://www.zotero.org/oauth/access"

# Backends
class ZoteroBackend(GoogleOAuthBackend):
    """Google App Engine OAuth authentication backend"""
    name = 'zotero'

    def get_user_id(self, details, response):
        """Use google email or appengine user_id as unique id"""
        user_id = super(ZoteroBackend, self).get_user_id(details, response)
        if setting('GOOGLE_APPENGINE_OAUTH_USE_UNIQUE_USER_ID', False):
            return response['id']
        return user_id

    def get_user_details(self, response):
        """Return the information retrieved from the API endpoint"""
        email = response['email']
        return {'username': response.get('nickname', email).split('@', 1)[0],
                'email': email,
                'fullname': '',
                'first_name': '',
                'last_name': ''}

# Auth classes
class ZoteroOAuth(GoogleOAuth):
    """Google App Engine OAuth authorization mechanism"""
    AUTHORIZATION_URL = AUTHORIZATION_URL
    REQUEST_TOKEN_URL = REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = ACCESS_TOKEN_URL
    AUTH_BACKEND = ZoteroBackend
    SETTINGS_KEY_NAME = "e61504b6e21a1df7d146"
    SETTINGS_SECRET_NAME = "294d72ffd8dce053aadb"

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        request = self.oauth_request(access_token, ACCESS_TOKEN_URL)
        url, params = request.to_url().split('?', 1)
        return google_appengine_userinfo(url, params)

    def oauth_request(self, token, url, extra_params=None):
        """Add OAuth parameters to the request"""
        extra_params = extra_params or {}
        # Skip direct super class since scope and other parameters are not supported
        return super(GoogleOAuth, self).oauth_request(token, url, extra_params)

    @classmethod
    def get_key_and_secret(cls):
        """Return key and secret and fix anonymous settings"""
        return (ZoteroOAuth.SETTINGS_KEY_NAME, ZoteroOAuth.SETTINGS_SECRET_NAME)
        # key_and_secret = super(GoogleOAuth, cls).get_key_and_secret()
        # print 'key & secret = ', key_and_secret
        # if key_and_secret == (None, None):
        #     return 'anonymous', 'anonymous'
        # return key_and_secret

def google_appengine_userinfo(url, params):
    """Loads user data from OAuth Profile Google App Engine App.

    Parameters must be passed in queryset and Authorization header as described
    on Google OAuth documentation at:
    http://groups.google.com/group/oauth/browse_thread/thread/d15add9beb418ebc
    and: http://code.google.com/apis/accounts/docs/OAuth2.html#CallingAnAPI
    """
    request = Request(url + '?' + params, headers={'Authorization': params})
    print request
    print "Request = " + url2pathname(url + '?' + params)
    try:
        return simplejson.loads(urlopen(request).read())
    except (ValueError, KeyError, IOError):
        return None


# Backend definition
BACKENDS = {
    'zotero': ZoteroOAuth,
}