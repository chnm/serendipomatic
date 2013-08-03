from django.http import HttpResponseRedirect, HTTPError
from django.core.urlresolvers import reverse
from smartstash.auth.models import ZoteroUser
import smartstash.core.zotero as zotero
from smartstash.core.utils import common_words


# FIXME: consolidate with duplicate code in core.views
# - should almost certainly be using an existing library/tool for this
#   (prettu sure there is something in django we can use)
html_escapes = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}


def zotero_oauth(request):
    request.session['oauth_verifier'] = request.GET['oauth_verifier']

    try:
        token, userid = zotero.access_info(
            request,
            request.GET['oauth_verifier'],
            request.session['request_token']
        )

        terms = zotero.get_user_items(request, userid, token, numItems=20)
        #tokenize
        search_terms = common_words("".join(terms['abstractSummary'] + terms['creatorSummary'] + terms['title']))

        #sanitize
        for key, val in search_terms.iteritems():
            search_terms[key] = [html_escapes.get(c, c) for c in val]

        request.session['search_terms'] = search_terms
        return HttpResponseRedirect(reverse('view-stash'))

    # except HTTPError:
    # FIXME: HTTPerror is not imported; where is this defined?
    # what user state causes this exception?
    except Exception:
        return HttpResponseRedirect(reverse('site-index'))