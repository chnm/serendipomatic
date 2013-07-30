from django.db import models

# Create your models here.


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
        return '<%s %s>' % (self.title, self.thumbnail or '<no url>')



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
