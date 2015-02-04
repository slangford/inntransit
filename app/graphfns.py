
def create_nodegraph(cur, array):
  """ Function to build graph from array of linestrings and nodeID values"""

  import re
  nodedict = {}

  for element,node in array:
    value = (element,)
    cur.execute("SELECT ST_AsText(%s);", value)
    linestring = cur.fetchall()

    for list in linestring:
      new_linestring = list[0].split("(")[1].split(")")[0]
      match = re.findall(r'(-[0-9]+.[0-9]+) ([0-9]+.[0-9]+)',new_linestring)

      tuplelist = []
      i = 0
      for tuple in match:
        latval = float(tuple[1])
        lonval = float(tuple[0])
        tuplelist.append((node[i],(lonval,latval)))
        nodedict[node[i]] = (lonval,latval)
        i += 1
          
  return nodedict 

def create_weightgraph(cur, array):
  """ Function to build graph of nodeID as key and connectedTo as value, connectedTo dict of nodeID and weights"""

  import re
  import dist_sphere
  from collections import defaultdict
  
  graphdict = defaultdict(dict)

  for element,node in array:
    value = (element,)
    cur.execute("SELECT ST_AsText(%s);", value)
    linestring = cur.fetchall()

    for list in linestring:
      new_linestring = list[0].split("(")[1].split(")")[0]
      match = re.findall(r'(-[0-9]+.[0-9]+) ([0-9]+.[0-9]+)',new_linestring)

      tuplelist = []
      i = 0
      for tuple in match:
        latval = float(tuple[1])
        lonval = float(tuple[0])
        tuplelist.append((node[i],(lonval,latval)))
        i += 1

        if len(tuplelist) != 1:
          key0 = tuplelist[0][0]
          value0 = tuplelist[1][0]
          weight0 = dist_sphere.distance_on_unit_sphere(tuplelist[0][1][1],tuplelist[0][1][0],tuplelist[1][1][1],tuplelist[1][1][0])*20.0
          graphdict[key0][value0] = weight0

          for index in range(1,len(tuplelist)-1):
            key = tuplelist[index][0]
            value1 = tuplelist[index+1][0]
            value2 = tuplelist[index-1][0]
            weight1 = dist_sphere.distance_on_unit_sphere(tuplelist[index][1][1],tuplelist[index][1][0],tuplelist[index+1][1][1],tuplelist[index+1][1][0])*20.0
            weight2 = dist_sphere.distance_on_unit_sphere(tuplelist[index][1][1],tuplelist[index][1][0],tuplelist[index-1][1][1],tuplelist[index-1][1][0])*20.0
            graphdict[key][value1] = weight1
            graphdict[key][value2] = weight2

          keyn = tuplelist[-1][0]
          valuen = tuplelist[-2][0]
          weightn = dist_sphere.distance_on_unit_sphere(tuplelist[-1][1][1],tuplelist[-1][1][0],tuplelist[-2][1][1],tuplelist[-2][1][0])*20.0
          graphdict[keyn][valuen] = weightn
          
  return graphdict 




