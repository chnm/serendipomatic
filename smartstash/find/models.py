from django.conf import settings
from django.db import models
from bibs.bibs import Bibs

from smartstash.display.models import DisplayItem


class DPLA(object):

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
        # TODO: restrict to image only, or at least things with preview image
        results = api.search(qry, 'dplav2', 'items')
        # TODO: error handling...

        items = []
        for doc in results['docs']:
            src_res = doc['sourceResource']
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
                idate = src_res['date'].get('displayDate', None)
            if 'spatial' in src_res and src_res['spatial']:
                # sometimes a list but not always
                if isinstance(src_res['spatial'], list):
                    space = src_res['spatial'][0]
                else:
                    space = src_res['spatial']
                # country? state? coords?
                i.location = space.get('name', None)

            items.append(i)

        return items
