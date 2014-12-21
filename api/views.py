from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import Http404
import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from datetime import date,timedelta,datetime
import urllib
import urllib2
import requests
import random
import string
import os
from geopy.geocoders import Nominatim
#from foursquare import *
#import foursquare
#from TweetMap.settings import YOUR_CLIENT_ID, YOUR_CLIENT_SECRET
# Create your views here.
def getResponse(data):
    try:
        response = HttpResponse(json.dumps(data),mimetype='application/json')
    except:
        response = HttpResponse(json.dumps(data),content_type='application/json')
    return response
@csrf_exempt
def api_v1_canvas(request):
    if request.method == 'POST':
        try:
            geolocator = Nominatim()
            access_token = request.POST.get('access_token')
            print "access_token:" + access_token
            text_location = request.POST.get('text_location')
            print "location" + text_location
            gps_location = request.POST.get('gps_location').decode('utf8') 
            print gps_location
            if text_location is not None:
                geo = geolocator.geocode(text_location)
                if hasattr(geo, 'latitude') and hasattr(geo, 'longitude'):
                    print geo.latitude
                    print geo.longitude
                    location = str(geo.latitude) + "," + str(geo.longitude)
                else:
                    pass
            else:
                location = gps_location
                print "location: " + str(location)
                pass
            print "location: " + str(location)
            filename = parse_places_api(location, access_token)
        except Exception,e:
            print e
        return HttpResponse(json.dumps({'success':True,'filename':filename}), content_type="application/javascript; charset=utf-8")
        #return 
        
def parse_places_api(location, access_token):
    ''' This method parses the json response of the places search of the facebook. 
    Note that the query below can be changed to specific words like coffee or books
    or bar or taxi to execute specific search in the facebook. '''
    json_http_response = []
    query = '*'
    url = 'https://graph.facebook.com/search'
    payload= {
        'q':query,
        'center':location,
        'type':'place',
        'access_token':access_token,
        'limit':10
    }
    r = requests.get(url,params=payload)
    json_response = json.loads(r.text)
    #print json_response
    data = json_response['data']
    count = len(json_response['data'])
    """while ('next' in json_response['paging'] and retries < max_pagination):
        #print json_response['paging']
        try:
            url = json_response['paging']['next']
            r = requests.get(url)
            json_response = json.loads(r.text) 
            data.extend(json_response['data'])
            retries += 1
        except:
            print "no data in next field"
            continue"""
    for eachResult in data:
        #print eachResult
        try:
            #print eachResult
            count = count -1
            #db.placeSearchResult.update(eachResult,eachResult,True)
            print eachResult['id']
            placeDetails = get_place_details(eachResult['id'], access_token)
            #json_http_response = json_http_response.append(placeDetails)
            json_http_response.append(placeDetails)
            #json_http_response = ', '.join(json_http_response + [str(placeDetails)])
            ##db.placeDetails.update(placeDetails, placeDetails, True)
        except Exception, e:
            #print e
            print "Data could not be saved"
            continue
        #db.jobs.update(eachPlace, {'$set':{'StateLastProcess':datetime.datetime.now(), 'state':'processing'}})
    #db.jobs.update(eachPlace, {'$set':{'StateLastProcess':datetime.datetime.now(), 'state':'completed'}})
    #conn.disconnect()
    #print json_http_response
    #string = 'abcdefghijklmnopqrstuvwxyz'
    try:
        filename = ''.join(random.choice(string.lowercase) for x in range(10))
        dir = os.path.dirname('/home/ubuntu/tweet_map/TweetMap/static/'+filename+'.json')
        if not os.path.exists(dir):
            os.makedirs(dir)
        fo = open('/home/ubuntu/tweet_map/TweetMap/static/'+filename+'.json', "w+")
        fo.seek(0, 2)
        line = fo.write( json.dumps(json_http_response) )
    except Exception,e:
        print e
    return filename

def get_place_details(placeId, access_token):
    ''' This method gets details of places using facebook graph api '''
    try:
        data = {}
        url = 'https://graph.facebook.com/' + placeId + '?fields=photos.limit(1).type(profile),location,checkins,name,description,id,category&access_token=' + access_token
        r = requests.get(url)
        json_response = json.loads(r.text)
        checkins = json_response['checkins']
        longitude = json_response['location']['longitude']
        latitude = json_response['location']['latitude']
        #place_id = json_response['photos']['data'][0]['from']['id']
        place_id = json_response['id']
        #title = json_response['photos']['data'][0]['from']['name']
        title = json_response['name'].encode('utf-8')
        if 'description' not in json_response:
            description=""
        else:
            description = json_response['description']
        category = json_response['category']
        if 'photos' not in json_response:
            profile_pic = 'https://cdn0.iconfinder.com/data/icons/navigation-4/100/16-256.png'
        else:
            profile_pic = json_response['photos']['data'][0]['source']
        data = { 'title' : str(title), 'image' : str(profile_pic), 'rating' : 3.0, 'releaseYear' : 2014, 'genre' : ['action', 'drama'], 'latitude':latitude, 'longitude':longitude, 'checkins':checkins, 'category':category, 'id':place_id, 'description': description }
    except Exception,e:
        print e
        pass
    #print data
    #print description_html
    return data