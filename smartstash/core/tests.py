"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from smartstash.core.forms import InputForm

class FormTest(TestCase):
    def test_whitespace_validation(self):
        form = InputForm({'text': "   "})
        self.assertFalse(form.is_valid())