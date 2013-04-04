#-*- coding: UTF-8 -*-
import unittest
import os
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse


class TestViews(TestCase):
    """tests if the relevant views work"""

    fixtures = ['testdata.xml.gz']

    def test_index(self):
        response = self.client.get(reverse('stats-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_deletedata(self):
        response = self.client.get(reverse('upload-delete'))
        self.failUnlessEqual(response.status_code, 200)

    def test_uploaddata(self):
        response = self.client.get(reverse('upload-new'))
        self.failUnlessEqual(response.status_code, 200)


class TestAPI(TestCase):
    """tests the JSON api"""

    fixtures = ['testdata.xml.gz']

    def test_elohist(self):
        response = self.client.get(reverse('api-elohist'))
        self.failUnlessEqual(response.status_code, 200)

    def test_monthlyresult(self):
        response = self.client.get(reverse('api-monthlyresult'))
        self.failUnlessEqual(response.status_code, 200)

    def test_opponentselo(self):
        response = self.client.get(reverse('api-opponentselo'))
        self.failUnlessEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
