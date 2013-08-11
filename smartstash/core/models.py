import urllib

class DisplayItem(object):
    # common item to be used for display
    # results from various apis should be mapped
    # to this common api

    title = None
    # title or label
    format = None
    # format or type (image, text, etc)
    source = None
    # owning institution or provider
    date = None
    # creation date / time period
    url = None
    # link out to original item
    location = None
    # geographic location
    thumbnail = None
    # url to thumbnail image

    def __init__(self, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    def __repr__(self):
        return u'<%s %s>' % (self.title, self.thumbnail or '<no url>')

    @property
    def coins_citation_info(self):
        # generate a dictionary with info to build COinS citation
        info = {
            'rfr_id': 'info:sid/serendipomatic.org',  # referrer id is recommended
            'rft_val_fmt': 'info:ofi/fmt:kev:mtx:dc',  # think this basically means we are using Dublin Core metadata
            'rft.identifier': self.url
        }
        if self.title is not None:
            info['rft.title'] = self.title
        if self.date is not None:
            info['rft.date'] = self.date

        # may not be exact mapping; for books, this is place of publication
        if self.location is not None:
            info['rft.place'] = self.location
        if self.source is not None:
            info['rft.source'] = self.source
        if self.format is not None:
            info['rft.format'] = self.format

        return info


    @property
    def coins_citation(self):
        # COinS citation for this item to be embedded in the title attribute of a span
        return u'ctx_ver=Z39.88-2004&' + \
               u'&'.join(['%s=%s' % (k, urllib.quote(v.encode('utf-8')))
                             for k, v in self.coins_citation_info.iteritems()])


# common result item
'''
dpla results:

format type: image text, moving image sound, physical object
owning institution; also has provider
label/title
creator
description
search results have link within dpla, link out to partner institution
rights
url
created date
location

'''

'''
europeana
title, alt. title
description
geographic coverage
time period
types (format) - e.g. image
url
source, provider

'''
