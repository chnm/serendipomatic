"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from smartstash.core.forms import InputForm
from smartstash.core.models import DisplayItem
from smartstash.core.utils import load_stopwords


class FormTest(TestCase):

    def test_whitespace_validation(self):
        form = InputForm({'text': "   "})
        self.assertFalse(form.is_valid())


class DisplayItemTest(TestCase):

    def test_coins_citation_info(self):
        # minimal record
        item = DisplayItem(title='Hippo', url='http://some.url/to/a/hippo/pic')

        info = item.coins_citation_info
        self.assert_('rfr_id' in info, 'referrer id should be set in COinS info')
        self.assert_('rft_val_fmt' in info, 'format is specified in COinS info')
        self.assertEqual(item.title, info['rft.title'])
        self.assertEqual(item.url, info['rft.identifier'])

        for key in ['rft.date', 'rft.place', 'rft.source', 'rft.format']:
            self.assert_(key not in info,
                         'unavailable data should not be set in COinS info')

        # add all fields to simulate a complete record
        item.date = '1887'
        item.format = 'Image'
        item.source = 'Smithsonian'
        item.location = 'USA'

        info = item.coins_citation_info
        self.assertEqual(item.date, info['rft.date'])
        self.assertEqual(item.format, info['rft.format'])
        self.assertEqual(item.source, info['rft.source'])
        self.assertEqual(item.location, info['rft.place'])

    def test_coins_citation(self):
        # minimal record
        item = DisplayItem(title='Hippo', url='http://some.url/to/a/hippo/pic')

        cit = item.coins_citation
        # just some basic sanity checks
        self.assert_(cit.startswith('ctx_ver=Z39.88-2004'))
        self.assert_('rft.title=%s' % item.title in cit)

        # variant content - lists
        item = DisplayItem(title=['Hippo'], url='http://some.url/to/a/hippo/pic')
        # should not throw an exception
        cit = item.coins_citation
        self.assert_('rft.title=%s' % item.title[0] in cit)

        # variant content - integer
        item = DisplayItem(title='Hippo', url='http://some.url/to/a/hippo/pic',
                           date=1936)
        # should not throw an exception
        cit = item.coins_citation
        self.assert_('rft.date=%s' % item.date in cit)



class LoadStopwordsTest(TestCase):

    def test_extra_stopwords(self):
        sw = load_stopwords('fr')
        self.assert_('les' in sw)
        self.assert_('a' in sw)
            # if lang == 'fr':
    #   stopwords.append('les')
    #   stopwords.append('a')


