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
#from foursquare import *
#import foursquare
from TweetMap.settings import YOUR_CLIENT_ID, YOUR_CLIENT_SECRET
# Create your views here.
def getResponse(data):
    try:
        response = HttpResponse(json.dumps(data),mimetype='application/json')
    except:
        response = HttpResponse(json.dumps(data),content_type='application/json')
    return response
@csrf_exempt
def api_v1_canvas(request):
    if request.method == 'GET':
        access_token = request.GET.get('access_token')
        location = request.GET.get('location')
        serialized_data = parse_places_api(location, access_token)
        return getResponse(serialized_data)
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
        'limit':5
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
            print e
            print "Data could not be saved"
            continue
        #db.jobs.update(eachPlace, {'$set':{'StateLastProcess':datetime.datetime.now(), 'state':'processing'}})
    #db.jobs.update(eachPlace, {'$set':{'StateLastProcess':datetime.datetime.now(), 'state':'completed'}})
    #conn.disconnect()
    #print json_http_response
    return json_http_response

def get_place_details(placeId, access_token):
    ''' This method gets details of places using facebook graph api '''
    try:
        data = {}
        url = 'https://graph.facebook.com/' + placeId + '?fields=photos.limit(1).type(profile),description_html,location,checkins&access_token=' + access_token
        r = requests.get(url)
        json_response = json.loads(r.text)
        checkins = json_response['checkins']
        longitude = json_response['location']['longitude']
        latitude = json_response['location']['latitude']
        print json_response['photos']
        place_id = json_response['photos']['data'][0]['from']['id']
        title = json_response['photos']['data'][0]['from']['name']
        profile_pic = json_response['photos']['data'][0]['source']
        data = { 'title' : str(title), 'image' : str(profile_pic), 'rating' : 3.0, 'releaseYear' : 2014, 'genre' : ['action', 'drama'], 'latitude':latitude, 'longitude':longitude }
    except Exception,e:
        print e
        pass
    #print data
    #print description_html
    return data