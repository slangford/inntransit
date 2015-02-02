from flask import render_template, request
from app import app
import urllib2
import json 
import startnode
import graphfns
import dist_sphere
import bfs
import pickle
import psycopg2
import re
import math
from pythonds.basic import Queue
from collections import defaultdict
from Flask import current_app

from flask import Flask
app = Flask(__name__)

@app.route('/input')
def cities_input():
  return render_template("input.html")

@app.route('/output')
def cities_output():
  #pull 'ID' from input field and store it
  strID = request.args.get('strdate')
  endID = request.args.get('enddate')
  threshold = request.args.get('ttime')
  moscone_location = (-122.401626,37.784138)

  if(float(threshold) > 0 and float(threshold) <= 10):
    hotelId_file = open('hotelID_10min_san_francisco.pk1', 'rb')
  if(float(threshold) > 10 and float(threshold) <= 20):
    hotelId_file = open('hotelID_20min_san_francisco.pk1', 'rb')
  if(float(threshold) > 20 and float(threshold) <= 30):
    hotelId_file = open('hotelID_30min_san_francisco.pk1', 'rb')
  if(float(threshold) > 30):
    hotelId_file = open('hotelID_45min_san_francisco.pk1', 'rb')

  hotelIdlist = pickle.load(hotelId_file)
  hotelId_file.close()

  ## URL to call expedia API : input startdate and enddate
  expedia_api_url = 'http://dev.api.ean.com/ean-services/rs/hotel/v3/list?cid=55505&apiKey='+current_app.config['apiKey']+'&customerUserAgent='+current_app.config['customerUserAgent']+'&customerIpAddress='+current_app.config['customerIpAddress']+'&apiExperience=PARTNER_BOT_CACHE&arrivalDate='
  expedia_api_url += str(strID)
  expedia_api_url += '&departureDate='
  expedia_api_url += str(endID)
  expedia_api_url += '&hotelIdList='

  for hotel in hotelIdlist:
    expedia_api_url += str(hotel)+','

  expedia_api_response = urllib2.urlopen(expedia_api_url)
  expedia_api_jsondata = json.loads(expedia_api_response.read())

  # make lists of hotel details to return to output page
  hotel_results = []
  marker_lon = []
  marker_lat = []
  for hotel in expedia_api_jsondata['HotelListResponse']['HotelList']['HotelSummary']:
    marker_lat.append(hotel['latitude'])    
    marker_lon.append(hotel['longitude'])
    image = "http://images.travelnow.com"+hotel['thumbNailUrl']
    rate = "%.2f" % float(hotel['RoomRateDetailsList']['RoomRateDetails']['RateInfo']['ChargeableRateInfo']['@averageRate'])
    hotel_results.append(dict(name=hotel['name'],address=hotel['address1'],rating=hotel['hotelRating'],description=hotel['shortDescription'],image=image,link=hotel['deepLink'],rate=rate))
  return render_template("output.html", hotel=hotel_results, strdate=strID, enddate=endID, marker_lat=marker_lat, marker_lon=marker_lon, threshold=threshold)

  if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
