from django.conf import settings
from django.db import models
from bibs.bibs import Bibs
import flickrapi
import simplejson
import logging
import time

from smartstash.core.models import DisplayItem


logger = logging.getLogger(__name__)

# TODO: later refactor / cleanup: rename this module to sources,
# possibly break out into subdirectory
# document required parts for adding a new one

class DPLA(object):

    name = 'DPLA'
    url = 'http://dp.la/'

    API_KEY = settings.API_KEYS['DPLA']

    @staticmethod
    def find_items(keywords):
        # example use:
        # keyword should be a list of terms
        # DPLA.find_items(keywords=['term1', 'term2'])

        api = Bibs()
        qry = 'api_key->%s:q->%s' % (
            DPLA.API_KEY,
            ' OR '.join(keywords)
        )

        #qry from unicode string to regular string
        qry = qry.encode("utf8", "ignore")
        logger.debug('dpla query: %s' % qry)

        # TODO: restrict to image only, or at least things with preview image
        start = time.time()
        results = api.search(qry, 'dplav2', 'items')
        # TODO: error handling...
        logger.info('dpla query completed in %.2f sec' % (time.time() - start))

        items = []
        for doc in results['docs']:
            src_res = doc['sourceResource']

            # for now, just skip items without an image url
            if not doc.get('object', None): continue

            i = DisplayItem(
                title=src_res.get('title', None),
                format=src_res.get('type', None),
                source=doc['provider'].get('name', None),
                # collection or provider here? src_rec['collection']['title']
                # NOTE: collection apparently not set for all items

                thumbnail=doc.get('object', None),
                # according to dpla docs, should be url preview for item
                # docs reference a field for object mimetype, not seeing in results

                # url on provider's website with context
                url=doc.get('isShownAt', None)
            )
            if 'date' in src_res:
                i.date = src_res['date'].get('displayDate', None)

            if 'spatial' in src_res and src_res['spatial']:
                # sometimes a list but not always
                if isinstance(src_res['spatial'], list):
                    space = src_res['spatial'][0]
                else:
                    space = src_res['spatial']
                # country? state? coords?
                i.location = space.get('name', None)

            # Add the aggregator for reference
            i.aggregator = DPLA.name

            items.append(i)

        return items


class Europeana(object):

    name = 'Europeana'
    url = 'http://www.europeana.eu/'

    API_KEY = settings.API_KEYS['Europeana']

    # NOTE: currently using the bibs library for europeana,
    # but there is a europeana-search module on pypi we could also use

    @staticmethod
    def find_items(keywords=[]):
        qry = 'wskey->%s:query->%s' % (
            Europeana.API_KEY,
            # ' OR '.join(['%s' % kw for kw in keywords])
            ' OR '.join(keywords)
        )

        #qry from unicode string to regular string
        qry = qry.encode("utf8", "ignore")

        logger.debug('europeana query: %s' % qry)
        b = Bibs()
        results = b.search(qry, 'europeanav2', 'search')

        items = []
        # no results! log this error?
        if 'items' not in results:
            return items

        for doc in results['items']:
            # NOTE: result includes a 'completeness' score
            # which we could use for a first-pass filter to weed out junk records

            # for now, just skip items without an image url
            if not 'edmPreview' in doc or not doc['edmPreview']:
                continue

            i = DisplayItem(

                format=doc.get('type', None),
                source='; '.join(doc.get('dataProvider', [])),
                # NOTE: provider is aggregator (i.e., 'The European Library')
                # dataProvider is original source

                # url on provider's website with context
                url=doc.get('guid', None),
                date=doc.get('edmTimespanLabel', None)
            )

            # NOTE: doc['link'] provides json with full record data
            # if we want more item details
            # should NOT be displayed to users (includes api key)

            # preview and title are both lists; for now, in both cases,
            # just grab the first one

            if 'edmTimespanLabel' in doc:
                i.date = doc['edmTimespanLabel'][0]['def']
            if 'title' in doc:
                i.title = doc['title'][0]
            if 'edmPreview' in doc:
                i.thumbnail = doc['edmPreview'][0]

            # Add the aggregator for reference
            i.aggregator = Europeana.name

            # NOTE: spatial/location information doesn't seem to be included
            # in this item result
            items.append(i)

        return items


# Flickr Commons API
# Only return image from flicker commons
class Flickr(object):
    name = 'Flickr Commons'
    url = 'http://www.flickr.com/commons'

    API_KEY = settings.API_KEYS['Flickr']

    # TODO rewrite this for Flickr
    @staticmethod
    def find_items(keywords):

        flickr = flickrapi.FlickrAPI(Flickr.API_KEY)

        # photos = flickr.photos_search(user_id='73509078@N00', per_page='10')
        start = time.time()
        # NOTE: flickr does support or, but doesn't like too many terms at once
        # (15 terms is apparently too many)
        query = ' OR '.join(set(keywords[:10]))
        logger.debug('flickr query: %s' % query)
        results = flickr.photos_search(text=query, format='json', is_commons='true',
                                       extras='owner_name',
                                       sort='relevance',
                                       per_page=25)   # restrict to first 25 items
        # comma-delimited list of extra fields
        # need owner name for source
        # TODO: future enhancement: access to date, location info, etc
        #                              extras='owner_name,date_upload,date_taken,geo')

        logger.info('flickr query completed in %.2f sec' % (time.time() - start))

        # this is really stupid and should be uncessary but the 'jsonFlickrApi( )' needs to be stripped for the json to parse properly
        results = results.lstrip('jsonFlickrApi(')
        results = results.rstrip(')')

        results = simplejson.loads(results)
        # import pprint
        # pprint.pprint(results)

        items = []
        # no results! log this error?

        # NOTE: could be bad api key; check code/stat in response
        if not 'photos' in results or 'photo' not in results['photos']:
            return items

        for doc in results['photos']['photo']:
            # NOTE: result includes a 'completeness' score
            # which we could use for a first-pass filter to weed out junk records

            i = DisplayItem(

                format=doc.get('type', None),
                source=doc.get('ownername', None),
                # url on provider's website with context
                # http://www.flickr.com/photos/{user-id}/{photo-id}
                url='http://www.flickr.com/photos/%(owner)s/%(id)s/' % (doc)

                # TODO get date data
                # date=doc.get('edmTimespanLabel', None)
            )

            # NOTE: doc['link'] provides json with full record data
            # if we want more item details
            # should NOT be displayed to users (includes api key)

            # flickr title not a list
            if 'title' in doc:
                i.title = doc['title']
            # build the url back to the image
            # http://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
            i.thumbnail = 'http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_m.jpg' % doc
            # i.thumbnail = 'http://farm'+str(doc['farm'])+'.staticflickr.com/'+str(doc['server'])+'/'+str(doc['id'])+'_'+str(doc['secret'])+'.jpg'

            # Add the aggregator for reference
            i.aggregator = 'Flickr Commons'

            # NOTE: spatial/location information doesn't seem to be included
            # in this item result
            items.append(i)

        return items

