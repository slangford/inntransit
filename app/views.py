from flask import render_template, request, app, Flask, flash, url_for
from app import app
import urllib2
import json 
import findnode
import graphfns
import dist_sphere
import bfs
import pickle
import psycopg2
import re
import math
from pythonds.basic import Queue
from collections import defaultdict

@app.route('/')
def input():
  return render_template('input.html')

@app.route('/error')
def error():
  return render_template('error.html')

@app.route('/output')
def output():
  #pull 'ID' from input field and store it
  strID = request.args.get('strdate')
  endID = request.args.get('enddate')
  threshold = request.args.get('ttime')
  if threshold == '':
    threshold = 60
  location = (-122.401626,37.784138)
  if strID > endID or strID == '' or endID == '':
    error = 'Error in selected dates'
    return render_template('error.html', error=error)
  else:

    minstars = 3
    maxstars = 5

    hotel_filename = 'osm_hotels_' + str(threshold) + 'min_san_francisco.pk1'
    hotelId_file = open(hotel_filename, 'rb')
    hotelinsidelist = pickle.load(hotelId_file)
    hotelId_file.close()
    
    walk_file = open('osm_hotel_walkable_san_francisco.pk1', 'rb')
    walklist = pickle.load(walk_file)
    walk_file.close()

    hotelthreshold_file = open('osm_hotel_threshold_san_francisco.pk1', 'rb')
    hotelthreshold = pickle.load(hotelthreshold_file)
    hotelthreshold_file.close()

    # make lists of hotel details to return to output page
    hotel_results = []
    marker_lon = []
    marker_lat = [] 
    marker_ID = []

    ## URL to call expedia API : input startdate and enddate
    expedia_api_url = 'http://dev.api.ean.com/ean-services/rs/hotel/v3/list?cid=55505&apiKey=9nkuwbprt9fwrrcesqa22r27&customerUserAgent=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_10_1)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F39.0.2171.95%20Safari%2F537.36&customerIpAddress=65.87.19.170&apiExperience=PARTNER_BOT_CACHE'
    expedia_api_url += '&minStarRating='
    expedia_api_url += str(minstars)
    expedia_api_url += '&maxStarRating='
    expedia_api_url += str(maxstars)
    expedia_api_url += '&room1=1'
    expedia_api_url += '&arrivalDate='
    expedia_api_url += str(strID)
    expedia_api_url += '&departureDate='
    expedia_api_url += str(endID)
    expedia_api_url += '&hotelIdList='
    for hotel_id in hotelinsidelist:
      expedia_api_url += str(hotel_id)+','
    expedia_api_response = urllib2.urlopen(expedia_api_url)
    expedia_api_jsondata = json.loads(expedia_api_response.read())

    if len(expedia_api_jsondata['HotelListResponse']) < 3:
      error = 'No hotels available, please try again'
      return render_template('error.html', error=error)
    else:

      for hotel in expedia_api_jsondata['HotelListResponse']['HotelList']['HotelSummary']:
        marker_lat.append(hotel['latitude'])    
        marker_lon.append(hotel['longitude'])
        marker_ID.append(hotel['hotelId'])
        box_text = "test"
        image = "http://images.travelnow.com"+hotel['thumbNailUrl']
        rate = "%.2f" % float(hotel['RoomRateDetailsList']['RoomRateDetails']['RateInfo']['ChargeableRateInfo']['@averageRate'])
        hotel_results.append(dict(hotelidarray=hotel['hotelId'],name=hotel['name'],address=hotel['address1'],rating=int(hotel['hotelRating']),description=hotel['shortDescription'],image=image,link=hotel['deepLink'],rate=rate,box_text=box_text))

      # Page through all the results until all hotels returned
      if(expedia_api_jsondata['HotelListResponse']['moreResultsAvailable'] == True):
        cacheKey = expedia_api_jsondata['HotelListResponse']['cacheKey']
        cacheLocation = expedia_api_jsondata['HotelListResponse']['cacheLocation']
        moreresults = True

        while moreresults == True:
          page_api_url = 'http://dev.api.ean.com/ean-services/rs/hotel/v3/list?cid=55505&apiKey=9nkuwbprt9fwrrcesqa22r27&customerUserAgent=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_10_1)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F39.0.2171.95%20Safari%2F537.36&customerIpAddress=65.87.19.170&apiExperience=PARTNER_BOT_CACHE'
          page_api_url += '&cacheKey='
          page_api_url += cacheKey
          page_api_url += '&cacheLocation='
          page_api_url += cacheLocation

          page_api_response = urllib2.urlopen(page_api_url)
          page_api_jsondata = json.loads(page_api_response.read())

          if len(page_api_jsondata['HotelListResponse']) < 3:
            error = 'Please try again'
            return render_template('error.html', error=error)

          for hotel in page_api_jsondata['HotelListResponse']['HotelList']['HotelSummary']:
            marker_lat.append(hotel['latitude'])    
            marker_lon.append(hotel['longitude'])
            marker_ID.append(hotel['hotelId'])
            box_text = "test"
            image = "http://images.travelnow.com"+hotel['thumbNailUrl']
            rate = "%.2f" % float(hotel['RoomRateDetailsList']['RoomRateDetails']['RateInfo']['ChargeableRateInfo']['@averageRate'])
            hotel_results.append(dict(hotelidarray=hotel['hotelId'],name=hotel['name'],address=hotel['address1'],rating=int(hotel['hotelRating']),description=hotel['shortDescription'],image=image,link=hotel['deepLink'],rate=rate,box_text=box_text))

          if len(page_api_jsondata['HotelListResponse']['HotelList']['HotelSummary']) < 20:
            moreresults = False
        
          cacheKey = page_api_jsondata['HotelListResponse']['cacheKey']
          cacheLocation = page_api_jsondata['HotelListResponse']['cacheLocation']
          page_api_url = None
          page_api_jsondata = None
          page_api_response = None

      return render_template("output.html", hotel_results=hotel_results, strdate=strID, enddate=endID, marker_lat=marker_lat, marker_lon=marker_lon, marker_ID=marker_ID, box_text=box_text, hotelthreshold=hotelthreshold, walklist=walklist)

if __name__ == "__main__":
  app.run()
