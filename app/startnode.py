def find_closest_node(nodedict, coords):

	"""function to find the node ID closest to the starting lon,lat """
	
	minval_latlon = 1000000.0

	coord_lon = coords[0]
	coord_lat = coords[1]

	startnodeID = 0
	for key in dict.keys(nodedict):
		node_lon = nodedict[key][0]
		node_lat = nodedict[key][1]
		diffval = (((coord_lat - node_lat)**2.) + ((coord_lon - node_lon)**2.))**0.5
		if(diffval < minval_latlon):
			startnodeID = key
			minval_latlon = diffval

	return startnodeID
