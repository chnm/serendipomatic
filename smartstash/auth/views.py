from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from smartstash.auth.models import ZoteroUser
import smartstash.core.zotero as zotero

html_escapes = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

# Create your views here.

def zotero_oauth(request):

    #zu = ZoteroUser.objects.get(username=request.session['username'])
    request.session['oauth_verifier'] = request.GET['oauth_verifier']

    # Don't save the token in the database like this
    # zu.token, zu.userid = zotero.accessToken_userID_from_oauth_verifier(
    #                                                                     request,
    #                                                                     request.GET['oauth_verifier'],
    #                                                                     request.session['request_token']
    #                                                                     )
    token, userid = zotero.accessToken_userID_from_oauth_verifier(
                                                                    request,
                                                                    request.GET['oauth_verifier'],
                                                                    request.session['request_token']
                                                                    )

    search_terms = {}
    terms = zotero.get_user_items(request, userid, token, numItems=20, public=False)
    search_terms['keywords'] = terms['date'] + terms['creatorSummary'] + terms['keywords']

    for key, val in search_terms.iteritems():
        search_terms[key] = [html_escapes.get(c, c) for c in val]

    request.session['search_terms'] = search_terms

    return HttpResponseRedirect(reverse('view-stash'))