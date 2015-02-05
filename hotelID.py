
def find_hotelIDs():
	""" Function to use Expedia API to get list of hotelIDs and lat,lon locations"""

	import urllib2
	import json
	from collections import defaultdict

	hotelId = {}

	city_list = ['Oakland','San%20Jose%20-%20Silicon%20Valley','San%20Francisco']

	for city in city_list:

		hotelId_api_url = 'http://dev.api.ean.com/ean-services/rs/hotel/v3/list?cid=55505&apiKey=9nkuwbprt9fwrrcesqa22r27&customerUserAgent=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_10_1)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F39.0.2171.95%20Safari%2F537.36&customerIpAddress=65.87.19.170&apiExperience=PARTNER_BOT_CACHE\&city='
		hotelId_api_url += city
		hotelId_api_url += '&state=California&countryCode=US'
		hotelId_api_response = urllib2.urlopen(hotelId_api_url)
		hotelId_api_jsondata = json.loads(hotelId_api_response.read())

		for hotel in hotelId_api_jsondata['HotelListResponse']['HotelList']['HotelSummary']:
			hotelId[long(hotel['hotelId'])] = (hotel['longitude'],hotel['latitude'])

	return hotelId
