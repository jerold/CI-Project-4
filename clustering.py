import math
import numpy as np
from QuadTree import Point
from QuadTree import Actor

### Assistance Methods ################################################################################
#######################################################################################################

def euclidianDistance(p, q):
	"""Distance function in multi-dimensional space"""
	sumOfSquares = 0.0
	for i in range(len(p)):
		sumOfSquares = sumOfSquares + ((p[i]-q[i])*(p[i]-q[i]))
	return math.sqrt(sumOfSquares)

def varience(p, q):
	"""Combined difference between two vectors"""
	var = 0.0
	for i in range(len(p)):
		var = var + np.fabs(p[i] - q[i])
	return var

def standardDeviation(collection):
	"""Basid Standard Deviation helps us determine how scattered the patterns are"""
	if len(collection) > 0:
		average = sum(collection)/len(collection)
		squaredDifferences = 0.0
		for val in collection:
			squaredDifferences = squaredDifferences + (val - average)*(val - average)
		meanSquaredDifference = squaredDifferences/len(collection)
		standardDeviation = math.sqrt(meanSquaredDifference)
		return standardDeviation
	return 999999

def averageVarience(packets):
	"""Return the neighboring packet most different from all of the its peers"""
	varSum = 0.0
	for i, p in enumerate(packets):
		pVarienceSum = 0.0
		for op in packets:
			if p is not op:
				pVarienceSum = pVarienceSum + varience(p.pattern['p'], op.pattern['p'])
		varSum = varSum + (pVarienceSum/len(packets))
	return varSum/len(packets)

def addNeighborsToCluster(pattern, cluster):
	for p in pattern.close['Packet']:
		if not p.hasMembership:
			cluster.append(p)
			p.hasMembership = True
			addNeighborsToCluster(p, cluster)


### Environment Classes ###############################################################################
#######################################################################################################

class Cluster:
	clusters = []
	outLayers = []
	hasClusters = False

	def __init__(self, packet):
		"""Cluster represents a set of packets stacked 3 or higher, packets in groups smaller than this
		are considered outlayers."""
		self.packets = []
		addNeighborsToCluster(packet, self.packets)
		if len(self.packets) > 1:
			types = self.types()
			print("C " + str(len(Cluster.clusters)) +
				": Cnt[" + str(self.count()) +
				"] Prc[" + str(self.percentage()) +
				"] Var[" + str(self.varience()) +
				"]  (" + ") (".join(str(k)+":"+str(round(float(len(types[k]))/len(self.packets), 2)) for k in types.keys()) + ")")
			Cluster.clusters.append(self)
			Cluster.hasClusters = True
		else:
			Cluster.outLayers.append(self)

	def count(self):
		return len(self.packets)

	def percentage(self):
		return round(float(len(self.packets))/len(Packet.packets)*100, 1)

	def varience(self):
		if len(self.packets) == 0:
			return 0.0
		return round(averageVarience(self.packets), 2)

	def types(self):
		t = {}
		for packet in self.packets:
			if packet.pattern['t'] not in t:
				t[packet.pattern['t']] = []
			t[packet.pattern['t']].append(packet)
		return t

	@classmethod
	def reset(self):
		"""Clean out Cluster and OutLayer data"""
		Cluster.clusters = []
		Cluster.outLayers = []
		Cluster.hasClusters = False


class Packet(Actor):
	"""Patterns are moved around our solution space within these Packets which are picked up
	and dropped off by passing ants."""
	packets = []
	baseVarience = 0.0

	def __init__(self, pattern, position):
		super(self.__class__, self).__init__(position)
		# self.setRangeOfVision(3)
		Packet.packets.append(self)
		self.pattern = pattern
		self.inHand = False
		self.hasMembership = False

	def update(self):
		"""Pheromone levels decay over time"""
		p = Point(self.position.x, self.position.y)
		p.z = sum(self.pattern['p'])
		self.moveHistory.append(p)

	@classmethod
	def clusterStats(self, setName):
		"""Every so often we collecte cluster details to see how things are going"""
		Cluster.reset()
		for p in Packet.packets:
			p.setRangeOfVision(3)
		avgVarience = 0.0
		for p in Packet.packets:
			if not p.hasMembership:
				c = Cluster(p)
				avgVarience = avgVarience + c.varience()
		avgVarience = avgVarience/len(Cluster.clusters)
		with open('records/'+str(setName)+'.csv', 'a') as file:
			file.write(str(len(Packet.packets))+","+str(len(Cluster.clusters))+","+str(len(Cluster.outLayers))+","+str(round(Packet.baseVarience, 4))+","+str(round(avgVarience, 4))+",".join(str(round(c.varience(), 4)) for c in Cluster.clusters)+"\n")
		print("OutLayers " + str(len(Cluster.outLayers)))
		for p in Packet.packets:
			p.hasMembership = False
		for p in Packet.packets:
			p.setRangeOfVision(0)


	def updateClosest(self, actor, doAdd):
		if doAdd:
			self.close[str(type(actor).__name__)].append(actor)
		else:
			self.close[str(type(actor).__name__)].remove(actor)

	def neighborAdded(self, actor):
		"""SuperClass Hooke"""
		self.updateClosest(actor, True)

	def neighborRemoved(self, actor):
		"""SuperClass Hooke"""
		self.updateClosest(actor, False)