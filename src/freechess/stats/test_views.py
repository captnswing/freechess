#-*- coding: UTF-8 -*-
import unittest
import os
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse


class TestMediaRootConfiguration(TestCase):
    """tests if media root is configured correctly"""

    def test_BluePrint(self):
        """test for the presence of a Blueprint CSS file"""
        blueprintpath = os.path.join(settings.STATIC_URL, 'css/blueprint/screen.css')
        msg = """\n
blueprint '%s' not found
ser till att settings.STATIC_URL är rätt konfigurerad
servern skall kunna svara på %s
""" % (os.path.basename(blueprintpath), blueprintpath)
        response = self.client.get(blueprintpath)
        self.failUnlessEqual(response.status_code, 200, msg)

    def test_jQuery(self):
        """test for the presence of a jQuery file"""
        jquerypath = os.path.join(settings.STATIC_URL, 'js/jquery.media.pack.js')
        msg = """\n
jquery '%s' not found
ser till att settings.STATIC_URL är rätt konfigurerad
django dev server skall kunna svara på %s
""" % (os.path.basename(jquerypath), jquerypath)
        response = self.client.get(jquerypath)
        self.failUnlessEqual(response.status_code, 200, msg)


class TestViews(TestCase):
    """tests if the relevant views work"""

    fixtures = ['testdata.xml.gz']

    def test_index(self):
        response = self.client.get(reverse('stats-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_deletedata(self):
        response = self.client.get(reverse('stats-deletedata'))
        self.failUnlessEqual(response.status_code, 200)


class TestImage(TestCase):
    """tests the Google Chart API graph"""

    fixtures = ['testdata.xml.gz']

    def test_monthlyResult(self):
        response = self.client.get(reverse('stats-monthlyresult'))
        self.failUnlessEqual(response.status_code, 200)

    def test_eloHist(self):
        response = self.client.get(reverse('stats-elohist'))
        self.failUnlessEqual(response.status_code, 200)

    def test_opponentsElo(self):
        response = self.client.get(reverse('stats-opponentselo'))
        self.failUnlessEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
