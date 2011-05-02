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

def should_this_fields_data_be_on_the_page(field, data_schema):
    if field in data_schema.their_fields:
        return True
    for resolution, resolution_data in data_schema.resolutions.items():
        if resolution_data['url_column_name'] == field:
            return True
    return False

def is_iterable(x):
    return getattr(x, '__iter__', False)

def flatten(x):
    result = []
    # if it's already not even a list or something iterable, just return it
    if not is_iterable(x):
        return x
    for el in x:
#if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

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

            # look for the known_good metadata as a substring of the contents of the page
            # grab the metadata from the live db
            metadata = self.scraper.get_image_metadata_dict(id)
                
            # based on this, assemble a flat list of things to look for
            things_to_look_for = []
            for key, value in metadata.items():
                if should_this_fields_data_be_on_the_page(key, self.scraper.imglib.data_schema):
                    value_flat = flatten(value)
                    things_to_look_for.append(value_flat)
                    # TODO: assert that the page contains value_flat
            things_to_look_for = flatten(things_to_look_for)

            # make sure we have everything on the list
            for thing in things_to_look_for:
                self.assertContains(response, thing)
