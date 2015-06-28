from __future__ import absolute_import
from django.shortcuts import render
from TweetMap.local_settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from django.conf import settings
# Create your views here.
from django.http import HttpResponse      
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_service.models import TwitterServiceTwitterfeed2
from twitter_service.alchemyapi import AlchemyAPI
import time
import MySQLdb
import random
import json
from geopy.geocoders import Nominatim
from TweetMap.settings import *
from celery import Celery, task, current_task, shared_task
from datetime import datetime

# from drealtime import iShoutClient
# ishout_client = iShoutClient()

@task(queue='new_tweet_que')
def new_tweet(tweet):
    print 'new tweet: ', tweet.text
    # #ishout_client.emit(
        # tweet.userid,
        # 'notifications',
        # data={ 'tweet' : tweet }
    # )
    # Some other things happening here..
    #return HttpResponseRedirect(reverse('home'))
    return render_to_response('tweet-map.html.html', ctx)

consumer_key=TWITTER_CONSUMER_KEY
consumer_secret=TWITTER_CONSUMER_SECRET

access_token=TWITTER_ACCESS_TOKEN
access_token_secret=TWITTER_ACCESS_TOKEN_SECRET

# Create your MySQL schema and connect to database, ex: mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpwd');
@task(queue='twitter_sentiment_que')
def get_tweet_sentiment(tweet_id):
    try:
        tweet = TwitterServiceTwitterfeed2.objects.get(userid=tweet_id)
    except:
        print "could not find tweet"
        return
    else:
        pass
    alchemyapi = AlchemyAPI()
    #myText = "I'm excited to get started with AlchemyAPI!"
    response = alchemyapi.sentiment("text", tweet.text)
    print "Sentiment: ", response["docSentiment"]["type"]
    tweet.sentiment = response["docSentiment"]["type"]
    tweet.sentiment_score = response["docSentiment"]["score"]
    tweet.save()
    new_tweet.delay(tweet)

XY = []
Coords = dict()
Place = dict()
PlaceCoords = dict()
@task(queue='twitter_service_que')
def get_recent_tweets():
    l = StdOutListener()    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, timeout = 5.0)
    #Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
    while True:
        try:
            # Call tweepy's userstream method 
            # Use either locations or track, not both
            #stream.filter(locations=[-180,-90,180,90], async=False)##These coordinates are approximate bounding box around USA
            stream.filter(track=['love', 'happy'])## This will feed the stream all mentions of 'keyword' 
            #break
        except Exception, e:
             # Abnormal exit: Reconnect
             nsecs=random.randint(60,63)
             print e
             pass
    return
# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html
# GeoSearch crawler written by Chris Cantey, MS GIS/Cartography, University of Wisconsin, https://geo-odyssey.com
# MwSQLdb schema written with great assistance from Steve Hemmy, UW-Madison DoIT



# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers


class StdOutListener(StreamListener):
                """ A listener handles tweets that are the received from the stream. 
                This is a basic listener that inserts tweets into MySQLdb.
                """
                def on_data(self, data):
                    # Twitter returns data in JSON format - we need to decode it first
                    decoded = json.loads(data)
                    geolocator = Nominatim()

                    # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
                    try:
                        Coords.update(decoded['coordinates'])
                        XY = (Coords.get('coordinates'))#Place the coordinates values into a list 'XY'
                        if XY != "None":
                            print "X: ", XY[0]
                            print "Y: ", XY[1]
                    except Exception, e:

                        geo = geolocator.geocode(decoded['user']['location'].encode('ascii', 'ignore'))
                        XY = {}
                        if hasattr(geo, 'latitude') and hasattr(geo, 'longitude'):
                            XY[0] = geo.latitude
                            XY[1] = geo.longitude
                            print "X: ", XY[0]
                            print "Y: ", XY[1]
                        else:
                            XY[0] = ''
                            XY[1] = ''
                        #print e
                        pass
                    try:
                        twit = TwitterServiceTwitterfeed2.objects.create(userid=decoded['id_str'],date=decoded['created_at'],x=XY[0],y=XY[1],text=decoded['text'].encode('ascii', 'ignore'),location=decoded['user']['location'].encode('ascii', 'ignore'))
                    except Exception,e:
                        print e
                        pass
                    else:
                        get_tweet_sentiment.delay(decoded['id_str'])
                    return True

                def on_error(self, status):
                    print status
                    
                def on_status(self, status):
                    #print "Tweet Text: ",status.text
                    text = str(status.text)
                    try:
                        #print status.place
                        tweet = status._json
                        location = tweet['user']['location'].encode('utf-8')
                        #print status.place
                    except Exception, e:
                        print e
                    else:
                        print "got"
                    #print "Time Stamp: ",status.created_at
                    try:
                        Coords.update(status.coordinates)
                        XY = (Coords.get('coordinates'))  #Place the coordinates values into a list 'XY'
                        #print "X: ", XY[0]
                        #print "Y: ", XY[1]
                    except:
                        #Often times users opt into 'place' which is neighborhood size polygon
                        #Calculate center of polygon
                        Place.update(status.place)
                        PlaceCoords.update(Place['bounding_box'])
                        Box = PlaceCoords['coordinates'][0]
                        XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
                        #print "X: ", XY[0]
                        #print "Y: ", XY[1] 
                        pass
                    # Comment out next 4 lines to avoid MySQLdb to simply read stream at console
                    twit = TwitterServiceTwitterfeed2.objects.create(userid=decoded['id_str'],date=decoded['created_at'],x=XY[0],y=XY[1],text=decoded['text'].encode('ascii', 'ignore'),location=decoded['user']['location'].encode('ascii', 'ignore'))