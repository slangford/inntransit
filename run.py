#!/usr/bin/env python
from app import app
import pickle
import hotelID

nodes_in = open('osm_nodes_san_francisco.pk1', 'rb')
app.nodedict = pickle.load(nodes_in)
nodes_in.close()

graph_in = open('osm_graph_san_francisco_with_bart.pk1', 'rb')
app.graphdict = pickle.load(graph_in)
graph_in.close()

corner_in = open('osm_corners_san_francisco.pk1', 'rb')
app.cornerdict = pickle.load(corner_in)
corner_in.close()

app.hotelIDlist = hotelID.find_hotelIDs()

app.config.from_pyfile("aws.cfg")
app.run(debug=True)
#app.run('0.0.0.0', port=5000)
app.run()