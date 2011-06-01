# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
#from mysite.mainapp.models 
import datetime
import sqlalchemy
import json
import usable_image_scraper

from django.conf import settings

import random


def get_metadata_db_connection():
    return sqlalchemy.create_engine(settings.METADATA_ENGINE)


def index(request):
    image_databases = usable_image_scraper.config.image_databases
    for image_database, data in image_databases.items():
        myscraper = usable_image_scraper.scraper.mkscraper(image_database)
        image_databases[image_database]['num_images'] = myscraper.db.get_num_images()
    data = {
        'image_databases' : image_databases,
        }
    return render_to_response('index.html', data)

def about(request):
    return render_to_response('about.html')

def view_random(request, repo):
    print repo
    myscraper = usable_image_scraper.scraper.mkscraper(repo)
    random_image_pk = myscraper.db.get_random_valid_image_id()
    url_to_redirect_to = '/' + repo + "/view/" + str(random_image_pk)
    print url_to_redirect_to
    return HttpResponseRedirect(url_to_redirect_to)

def view_image_json(request, repo, image__pk):
    image__pk = int(image__pk)
    repo = str(repo)
    myscraper = usable_image_scraper.scraper.mkscraper(repo)
    image = myscraper.db.get_image_metadata_dict(image__pk)
    return HttpResponse(simplejson.dumps(image), mimetype='application/json')

def view_image(request, repo, image__pk):
    image__pk = int(image__pk)
    repo = str(repo)
    myscraper = usable_image_scraper.scraper.mkscraper(repo)
    kwargs = {
        'web_data_base_dir' : settings.RELATIVE_DATA_ROOT,
    }
    myscraper.set_web_vars(**kwargs)
    image = myscraper.db.get_image_metadata_dict(image__pk)

    # if we've stumbled upon an image that appears to not be in our database
    # (really, this shouldn't happen--this is a relic from a stupider implementation of next/previous)
    if not image or not image['url_to_lores_img']:
        referrer = request.META.get('HTTP_REFERER')
        if not referrer.find('/view/') == (-1):
            referrer_id = int(referrer.rstrip('/').rsplit('/', 1)[1])

            next_id = myscraper.db.get_next_successful_image_id(image__pk)
            prev_id = myscraper.db.get_next_successful_image_id(image__pk)
            # if they hit the previous button
            if int(image__pk) < referrer_id:
                url_to_redirect_to = "/" + repo + "/view/" + str(prev_id)
            # if they hit the next button
            # (or something fishy is going on)
            else:
                url_to_redirect_to = "/" + repo + "/view/" + str(next_id)
        else:
            url_to_redirect_to = "/" + repo + "/view_random" 
            
        return HttpResponseRedirect(url_to_redirect_to)

    html = myscraper.get_image_html_repr(image__pk)

    #return HttpResponse(html)
    next_id = myscraper.db.get_next_successful_image_id(image__pk)
    prev_id = myscraper.db.get_prev_successful_image_id(image__pk)
    data = {
        'id' : image__pk,
        'repo' : repo,
        'next_id' : next_id,
        'prev_id' : prev_id,
        'html': html,
        }
    return render_to_response('image.html', data)
