# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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
        image_databases[image_database]['num_images'] = myscraper.get_num_images()
    data = {
        'image_databases' : image_databases,
        }
    return render_to_response('index.html', data)

def about(request):
    return render_to_response('about.html')

def view_random(request, repo):
    highest_image_pk = 12049
    # TODO: actually write code to figure out the above
    random_image_pk = random.randrange(highest_image_pk)
    url_to_redirect_to = "view/" + str(random_image_pk)
    return HttpResponseRedirect(url_to_redirect_to)

def view_image(request, repo, image__pk):
    image__pk = int(image__pk)
    repo = str(repo)
    myscraper = usable_image_scraper.scraper.mkscraper(repo)
    kwargs = {
        'web_data_base_dir' : settings.RELATIVE_DATA_ROOT,
    }
    myscraper.set_web_vars(**kwargs)
    image = myscraper.get_image_metadata_dict(image__pk)

    if not image['url_to_lores_img']:
        referrer = request.META.get('HTTP_REFERER')
        if not referrer.find('/view/') == (-1):
            prev_id = int(referrer.rstrip('/').rsplit('/', 1)[1])
            # if they hit the previous button
            if int(image__pk) < prev_id:
                url_to_redirect_to = "/view/" + str(int(image__pk)-1)
            # if they hit the next button
            # (or something fishy is going on)
            else:
                url_to_redirect_to = "/view/" + str(int(image__pk)+1)
        else:
            url_to_redirect_to = "/view_random" 
            
        return HttpResponseRedirect(url_to_redirect_to)
    
    '''
    db_connection = get_metadata_db_connection()
    image_tuples = db_connection.execute("select * from phil where id = %s" % image__pk).fetchone().items()
    image = {}
    image.update(image_tuples)
    '''
    

    html = myscraper.get_image_html_repr(image__pk)

    #return HttpResponse(html)
    next_id = image__pk+1
    prev_id = image__pk-1
    data = {
        'repo' : repo,
        'next_id' : next_id,
        'prev_id' : prev_id,
        'html': html,
        }
    return render_to_response('image.html', data)
