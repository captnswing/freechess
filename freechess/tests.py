# -*- coding: UTF-8 -*-
import unittest
from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestViews(TestCase):
    """tests if the relevant views work"""

    fixtures = ['initial_data.json.gz']

    def test_index(self):
        """tests that the url works"""
        response = self.client.get(reverse('main-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_elohist(self):
        """tests that the url works and returns valid json"""
        response = self.client.get(reverse('api-elohist'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless(response.has_header('content-type'))
        self.failUnlessEqual(response._headers['content-type'], ('Content-Type', 'application/json'))
        self.failUnless(json.loads(response.content))

    def test_monthlyresult(self):
        """tests that the url works and returns valid json"""
        response = self.client.get(reverse('api-monthlyresult'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless(response.has_header('content-type'))
        self.failUnlessEqual(response._headers['content-type'], ('Content-Type', 'application/json'))
        self.failUnless(json.loads(response.content))

    def test_opponentselo(self):
        """tests that the url works and returns valid json"""
        response = self.client.get(reverse('api-opponentselo'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless(response.has_header('content-type'))
        self.failUnlessEqual(response._headers['content-type'], ('Content-Type', 'application/json'))
        self.failUnless(json.loads(response.content))


if __name__ == "__main__":
    unittest.main()
