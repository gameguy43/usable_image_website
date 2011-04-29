import unittest2 as unittest
import config
import os
import usable_image_scraper.scraper 
import config
from django.test.client import Client
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def setUp(self):
        self.scraper_name = 'fema'
        self.scraper = usable_image_scraper.scraper.mkscraper(self.scraper_name)
        '''
        scrapers = []
        for name, data in config.image_databases:
            usable_images.scraper.
        '''
    def test_image_files_actually_exist(self):
        c = Client()
        for id in self.scraper.imglib.tests.known_good_indeces:
            url = '/' + self.scraper_name + '/view/' + str(id)
            # go to the page for a known_good thing
            response = c.get(url)
            # assert that we successfully load a page
            self.assertEqual(response.status_code, 200)
            # TODO: look for the known_good metadata as a substring of the contents of the page
            #self.assertEqual()
