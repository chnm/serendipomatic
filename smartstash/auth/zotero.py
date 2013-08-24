from urlparse import parse_qsl

from oauth2 import Token

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend


class ZoteroBackend(OAuthBackend):
    """Zotero OAuth authentication backend"""
    name = 'zotero'
    EXTRA_DATA = [
        ('id', 'id'),
        ('username', 'username'),
    ]

    def get_user_details(self, response):
        """Return user details"""
        return {'username': response['username'], 'email': '',
                'uid': response['id']}

    @classmethod
    def tokens(cls, instance):
        """Return the tokens needed to authenticate the access to any API the
        service might provide. Zotero (much like Twitter) uses a pair of
        OAuthToken consisting of an oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        token = super(ZoteroBackend, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                         for tok in token['access_token'].split('&'))
        return token



class ZoteroAuth(ConsumerBasedOAuth):
    """Zotero OAuth authentication mechanism

    **ZOTERO_PERMISSIONS** can be used to configure requested permissions,
    as listed at http://www.zotero.org/support/dev/server_api/v2/oauth,
    and can include any of library_access, notes_access, write_access,
    group_read, group_write.  If no permissions are specified, Zotero
    will assume a default of library_access only.

    """
    AUTH_BACKEND = ZoteroBackend
    AUTHORIZATION_URL = 'https://www.zotero.org/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://www.zotero.org/oauth/request'
    ACCESS_TOKEN_URL = 'https://www.zotero.org/oauth/access'
    SETTINGS_KEY_NAME = 'ZOTERO_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'ZOTERO_CONSUMER_SECRET'
    SCOPE_VAR_NAME = 'ZOTERO_PERMISSIONS'
    # e.g.,
    # ZOTERO_PERMISSIONS = ['library_access', 'notes_access', group_read']
    # ZOTERO_PERMISSIONS = ['library_access', 'notes_access', 'write_access', 'group_write']

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return {
            'id': access_token.user_id,
            'username': access_token.username
        }

    def access_token(self, token):
        """Return request for access token value"""
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        response = self.fetch_response(request)
        data = dict(parse_qsl(response))
        token = Token.from_string(response)
        token.user_id = data['userID']
        token.username = data['username']
        return token


    def auth_extra_arguments(self):
        params = super(ZoteroAuth, self).auth_extra_arguments() or {}
        for scope in self.get_scope():
            if scope == 'group_read':
                params['all_groups'] = 'read'
            elif scope == 'group_write':
                params['all_groups'] = 'write'
            else:
                # all other perms are on/off; request on if specified
                params[scope] = 1


BACKENDS = {
    'zotero': ZoteroAuth
}