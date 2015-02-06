import folium

def make_map(nodedict, statusdict, map_location, map_name='map'):

	map = folium.Map(location=map_location, width=500, height=500, zoom_start=13, tiles='Stamen Toner')

	for key in dict.keys(nodedict):
		if statusdict[key] == 'outside':
			location_value = [nodedict[key][1],nodedict[key][0]]
			map.circle_marker(location=location_value, radius=20, line_color='#3186cc', fill_color='#3186cc')

	map.create_map(path='%s' % map_name)

	return

