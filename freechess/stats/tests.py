#-*- coding: UTF-8 -*-
import unittest
from django.test import TestCase
from django.core.urlresolvers import reverse


class TestViews(TestCase):
    """tests if the relevant views work"""

    fixtures = ['testdata.json']

    def test_index(self):
        response = self.client.get(reverse('stats-index'))
        self.failUnlessEqual(response.status_code, 200)

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
