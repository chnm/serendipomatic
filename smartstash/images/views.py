# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect

from PIL import Image
import requests
from StringIO import StringIO
import logging

logger = logging.getLogger(__name__)


# TODO:
# - add headers to allow browser caching
# - some way to filter urls we're willing to resize
def resize(request, size):
    img_url = request.GET.get('url', None)
    if img_url is None:
        raise Http404

    # test to make sure valid first?
    r = requests.get(img_url)
    if r.status_code != requests.codes.ok:
        raise Http404

    newsize = (int(size), int(size))

    try:
        img = Image.open(StringIO(r.content))
    except IOError as err:
        logger.warn('Failed to open %s as image : %s' % (img_url, err))

        # if there's a problem, just redirect to the original
        return HttpResponseRedirect(img_url)

    img.thumbnail(newsize, Image.ANTIALIAS)

    # serialize to HTTP response
    response = HttpResponse(mimetype="image/png")
    img.save(response, "PNG")
    return response
