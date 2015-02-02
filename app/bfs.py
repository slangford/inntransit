def bfs_graph(threshold, startnodeID, graphdict, nodedict):

	from pythonds.basic import Queue
	from collections import defaultdict
  
  	subnodedict = defaultdict(dict)
	statusdict = dict(zip(dict.keys(nodedict), ['undiscovered']*len(dict.keys(nodedict))))

	nodeQueue = Queue()
	nodeQueue.enqueue({startnodeID: 0.0})

	while (nodeQueue.size() > 0):
		currentNode = nodeQueue.dequeue()    
		currentNodeStatus = statusdict[dict.keys(currentNode)[0]]
		if(currentNodeStatus == 'undiscovered' or currentNodeStatus == 'outside'):
			transitTime = dict.values(currentNode)[0]
			if(transitTime > threshold):
				statusdict[dict.keys(currentNode)[0]] = 'outside'
			else:
				statusdict[dict.keys(currentNode)[0]] = 'inside'
				subnodedict[dict.keys(currentNode)[0]] = nodedict[dict.keys(currentNode)[0]]
				for connectedNodeKey, connectedNodeValue in graphdict[dict.keys(currentNode)[0]].iteritems():     
					graphdict[dict.keys(currentNode)[0]][connectedNodeKey] += transitTime  
					nodeQueue.enqueue({connectedNodeKey: graphdict[dict.keys(currentNode)[0]][connectedNodeKey]})

	return statusdict, subnodedict