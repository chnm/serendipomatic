from social_auth.backends import ConsumerBasedOAuth, OAuthBackend

from django.conf import settings
import urlparse
import oauth2

class ZoteroBackend(OAuthBackend):
    """Zotero OAuth authentication backend"""
    name = 'zotero'
    # EXTRA_DATA = [('userID', 'id')]
    ID_KEY = 'userID'

    # extra data, user data still to do

    def get_user_details(self, response):
        """Return user details from Zotero account"""
        print '#### get user details'
        print response
        return {}

        try:
            first_name, last_name = response['name'].split(' ', 1)
        except:
            first_name = response['name']
            last_name = ''
        return {'username': response['screen_name'],
                'email': '',  # not supplied
                'fullname': response['name'],
                'first_name': first_name,
                'last_name': last_name}


    @classmethod
    def tokens(cls, instance):
        """Return the tokens needed to authenticate the access to any API the
        service might provide. Twitter uses a pair of OAuthToken consisting of
        an oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        print '****zoterobackend tokens'
        token = super(TwitterBackend, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token


class ZoteroAuth(ConsumerBasedOAuth):
    """Zotero OAuth authentication mechanism"""
    AUTHORIZATION_URL = "https://www.zotero.org/oauth/authorize"
    REQUEST_TOKEN_URL = "https://www.zotero.org/oauth/request"
    ACCESS_TOKEN_URL = "https://www.zotero.org/oauth/access"

    AUTH_BACKEND = ZoteroBackend
    SETTINGS_KEY_NAME = 'ZOTERO_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'ZOTERO_CONSUMER_SECRET'


    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        print 'access_token', access_token
        # return {'userID': 'rlskoeser'}  # total cheat


        # response, content = client.request(accessTokenURL, "POST")

        # alt zotero impl
        # response, content = client.request(accessTokenURL, "POST")
        # accessToken = dict(urlparse.parse_qsl(content))

        # if 'oauth_problem' in accessToken: raise HTTPError

        # return accessToken['oauth_token'], accessToken['userID']

        # json = self.fetch_response(request)
        # try:
        #     return simplejson.loads(json)
        # except ValueError:
        #     return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""

        result = super(ZoteroAuth, self).auth_complete(*args, **kwargs)
        print 'auth complete result = ', result
        return result

    #     print '#### auth complete'
    #     print 'args = ', args  # is empty
    #     print 'kwargs = ', kwargs
        # kwargs request=wsgirequest with all info
        #        user=None

        # is there a denied option?
        # if 'denied' in self.data:
            # pass
            # raise AuthCanceled(self)
        # else:
        # return super(ZoteroAuth, self).auth_complete(*args, **kwargs)



# Backend definition
BACKENDS = {
    'zotero': ZoteroAuth,
}
