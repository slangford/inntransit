def calc_node_boxes(nodedict):

	from collections import defaultdict
	cornerdict = defaultdict(dict)

	for key in dict.keys(nodedict):

		cornerkeyLon = "%.3f" % nodedict[key][0]
		cornerkeyLat = "%.3f" % nodedict[key][1]
		cornerdict[(cornerkeyLon,cornerkeyLat)][key] = (nodedict[key][0],nodedict[key][1])

	return cornerdict

def find_closest_node(cornerdict, coords):

	minval_latlon = 100000.0
	nodeID = 0

	left = float(coords[0]) - 0.001
	down = float(coords[1]) - 0.001

	cornerarray = [("%.3f" % coords[0],"%.3f" % coords[1]),("%.3f" % left,"%.3f" % coords[1]),("%.3f" % left,"%.3f" % down),("%.3f" % coords[0],"%.3f" % down)]
	for value in cornerarray:
		for key in dict.keys(cornerdict[value]):
			diffval = (((coords[1] - cornerdict[value][key][1])**2.) + ((coords[0] - cornerdict[value][key][0])**2.))**0.5
			if(diffval < minval_latlon):
				nodeID = key
				minval_latlon = diffval

	return nodeID