from __future__ import absolute_import
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from twitter_service.models import TwitterServiceTwitterfeed2
import MySQLdb
from django.template import RequestContext
from notifications.models import Notification
from notifications import notify
from django.core.urlresolvers import reverse

from django.contrib.staticfiles.storage import staticfiles_storage
from drealtime import iShoutClient
ishout_client = iShoutClient()

# This is our pseudo view code
def new_tweet(request):
    tweet = TwitterServiceTwitterfeed2.objects.all().filter(x__isnull = False,y__isnull = False).order_by('id')[0]
    # Process stuff, handle forms, do whatever you want.
    ishout_client.emit(
        tweet.userid,
        'notifications',
        data={ 'msg' : 'You have a new comment!' }
    )
    # Some other things happening here..
    return render_to_response('tweet-map.html.html', ctx)
    
def home(request):
    tweets = TwitterServiceTwitterfeed2.objects.all().filter(x__isnull = False,y__isnull = False)[0:20000]
    context = {'tweets' : tweets}
    return render_to_response("tweet-map.html", {'tweets' : tweets}, RequestContext(request))

def tweet_sync(request):
    return render(request,"tweet-sync.html", locals())