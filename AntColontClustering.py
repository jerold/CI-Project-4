from QuadTree import Point
from QuadTree import Actor
import random
import numpy as np
import matplotlib.pyplot as plt
from patternSet import PatternSet


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


### Environment Classes ###############################################################################
#######################################################################################################

class Packet(Actor):
	"""Patterns are moved around our solution space within these Packets which are picked up
	and dropped off by passing ants."""
	packets = []

	def __init__(self, pattern, position):
		super(self.__class__, self).__init__(position)
		Packet.packets.append(self)
		self.pattern = pattern
		self.hasMembership = False

	def update(self):
		"""Pheromone levels decay over time"""
		p = Point(self.position.x, self.position.y)
		p.z = sum(self.pattern['p'])
		self.moveHistory.append(p)

	@classmethod
	def clusterStats(self):
		clusterId = 0
		outLayers = 0
		for p in Packet.packets:
			if not p.hasMembership:
				if len(p.close['Packet']) > 3:
					# New Cluster Collect information on this cluster
					cluster = [p] + p.close['Packet']
					print("Cluster " + str(clusterId) + ": Cnt[" + str(len(cluster)) + "] Prc[" + str(round(float(len(cluster))/len(Packet.packets)*100, 3)) + "] Var[" + str(round(float(averageVarience(cluster)), 3)) + "]")
					for op in p.close['Packet']:
						op.hasMembership = True
					clusterId = clusterId + 1
				else:
					outLayers = outLayers + 1
				p.hasMembership = True
		for p in Packet.packets:
			p.hasMembership = False
		print("OutLayers " + str(outLayers))

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


class Pheromone(Actor):
	"""The value of these are increased by ants as they pass to help other ants search elsewhere"""
	pheromones = []

	def __init__(self, position):
		super(self.__class__, self).__init__(position)
		Pheromone.pheromones.append(self)
		self.concentration = 0.0
		self.cHistory = []

	def update(self):
		"""Pheromone levels decay over time"""
		self.cHistory.append(self.concentration)
		self.concentration = .98*self.concentration


### Ant Class #########################################################################################
#######################################################################################################

class Ant(Actor):
	"""Ants wander around the solution space searching for packets which they attempt to Clustering
	based on how the packet smells.  Similar packets go next to one another"""
	ants = []
	k1 = .5
	k2 = 1 - k1

	def __init__(self, position):
		super(self.__class__, self).__init__(position)
		Ant.ants.append(self)
		self.setRangeOfVision(10)

		self.carrying = False
		self.packetInHand = Packet
		self.mostSimilarPacketSeen = Packet

		self.heading = 0.0

	def update(self):
		"""Have the ant wander, lay down pheromones, and possibly move a packet around"""
		self.depositPheromones()
		self.processEnvironment()
		mag = random.randrange(0, 5)
		if self.carrying:
			self.heading = self.randomAngle()
			if random.random() <= .2:
				self.heading = self.angleToActor(self.mostSimilarPacketSeen)
			self.packetInHand.move(np.cos(self.heading)*mag, np.sin(self.heading)*mag)
		else:
			self.heading = self.angleFromPheromones()
		self.move(np.cos(self.heading)*mag, np.sin(self.heading)*mag)

	def processEnvironment(self):
		"""Minimize looping through neighbors by doing all o(n) time work here"""
		if self.carrying:
			# Maybe the ant will drop whats in its hands
			dropProbability = self.pDropOff(float(len(self.close['Packet']))/len(Packet.packets), float(self.highestPacketDensitySeen)/len(Packet.packets))
			# print("PDO : " + str(round(dropProbability, 4)) + " : " + str(self.highestPacketDensitySeen) + " : " + str(len(self.close['Packet'])))
			if random.random() <= dropProbability and len(self.close['Packet']) > 0:
				# print("Drop!")
				self.setOnMostSimilarOfNeightbors()
				self.carrying = False
		else:
			# Maybe the ant will pick something up
			pickupProbability = self.pPickUp(float(len(self.close['Packet']))/len(Packet.packets), float(self.highestPacketDensitySeen)/len(Packet.packets))
			# print("PPU : " + str(round(pickupProbability, 4)) + " : " + str(self.highestPacketDensitySeen) + " : " + str(len(self.close['Packet'])))
			if random.random() <= pickupProbability and len(self.close['Packet']) > 0:
				# print("Pickup!")
				self.grabMostDifferentOfNeighbors()
				self.carrying = True

	def mostSimilarPacketInMemory(self, packet):
		"""Check the ant's short term memory for a pattern that is similar to the one now in its hands"""
		simIndex = 0
		simValue = 9999
		for i, memPacket in enumerate(self.shortTermMemory):
			memPacketVarience = varience(self.packetInHand.pattern['p'], memPacket.pattern['p'])
			if memPacketVarience < simValue:
				simValue = memPacketVarience
				simIndex = i
		return self.shortTermMemory[simIndex]

	def depositPheromones(self):
		for p in self.close['Pheromone']:
			p.concentration = p.concentration + 10/len(self.close['Pheromone'])

	def randomAngle(self):
		return np.radians(random.randrange(0, 360))

	def angleToActor(self, actor):
		"""Using its short term memory the ant can go searching for a packet it saw similar to the
		packet it is currently carrying"""
		if actor.position.x == self.position.x:
			return 0
		ang = np.arctan((actor.position.y - self.position.y)/(actor.position.x - self.position.x))
		if ang < 0:
			ang = ang + 2*np.pi
		if self.position.x > actor.position.x:
			ang = ang + np.pi
		return ang%(2*np.pi)

	def angleFromPheromones(self):
		"""Dropping pheromones prevents ants from backtracking too much as they avoid high
		concentrations of the stuff.  It therefore keeps ants from spending too much time
		ontop of each other"""
		if len(self.close['Pheromone']) > 0:
			minIndex = 0
			maxIndex = 0
			for i, p in enumerate(self.close['Pheromone']):
				if p.concentration < self.close['Pheromone'][minIndex].concentration:
					minIndex = i
				if p.concentration > self.close['Pheromone'][maxIndex].concentration:
					maxIndex = i
			# print(str(round(self.close['Pheromone'][maxIndex].concentration, 0)) + " " + str(round(self.close['Pheromone'][minIndex].concentration, 0)))
			if self.close['Pheromone'][maxIndex].concentration > 30:
				return self.angleToActor(self.close['Pheromone'][maxIndex])*.1 + self.angleToActor(self.close['Pheromone'][minIndex])*.9
				# return self.angleToActor(pheromones[minIndex])
			else:
				return self.randomAngle()
		else:
			return self.randomAngle()

	def grabMostDifferentOfNeighbors(self):
		"""Return the neighboring packet most different from all of the its peers"""
		highestVarienceValue = 0.0
		highestVarienceIndex = 0
		for i, p in enumerate(self.close['Packet']):
			pVarienceSum = 0.0
			for op in self.close['Packet']:
				if p is not op:
					pVarienceSum = pVarienceSum + varience(p.pattern['p'], op.pattern['p'])
			if pVarienceSum > highestVarienceValue:
				highestVarienceValue = pVarienceSum
				highestVarienceIndex = i
		self.packetInHand = self.close['Packet'][highestVarienceIndex]
		self.packetInHand.moveTo(self.position.x, self.position.y)
		self.mostSimilarPacketSeen = self.mostSimilarPacketInMemory(self.packetInHand)

	def setOnMostSimilarOfNeightbors(self):
		"""Return the neighboring packet most similar to the packet in the ant's hands"""
		lowestVarienceValue = 99999.0
		lowestVarienceIndex = 0
		for i, op in enumerate(self.close['Packet']):
			opVarience = 0.0
			if self.packetInHand is not op:
				opVarience = varience(self.packetInHand.pattern['p'], op.pattern['p'])
				if opVarience < lowestVarienceValue:
					lowestVarienceValue = opVarience
					lowestVarienceIndex = i
		msn = self.close['Packet'][lowestVarienceIndex]
		self.packetInHand.moveTo(msn.position.x, msn.position.y)

	def pPickUp(self, frac, const):
		"""Density based pickup, more sparse == more likely to pick the item up. Const is set to the
		highest fraction of items ever seen in the ants neighborhood, so as the ant starts seeing
		bigger clusters it will be LESS selective about when it picks up"""
		return (const/(const+0.0000001 + frac))**2

	def pDropOff(self, frac, const):
		"""Density based dropoff, more dense == more likely to drop the item off.  Const is set to the
		highest fraction of items ever seen in the ants neighborhood, so as the ant starts seeing
		bigger clusters it will be MORE selective about when it drops off"""
		return (frac/(const+0.0000001 + frac))**2

### LF Model for Similarity based Clustering ##########################################################
#######################################################################################################

	# def pPickUp(self):
	# 	"""LF Model of Standard Ant Clustering. Probability is based on average difference of packets
	# 	in the ants local area.  More disorder = better chance of picking something up"""
	# 	if len(self.close['Packet']) > 0:
	# 		const1 = 0.5
	# 		avgSim = 0.0
	# 		mostDiffIndex = 0
	# 		mostDiff = 0.0
	# 		for i, p in enumerate(self.close['Packet']):
	# 			localSim = 0.0
	# 			for op in self.close['Packet']:
	# 				if p is not op:
	# 					localSim = localSim + (varience(p.pattern['p'], op.pattern['p']))/2
	# 			avgSim = avgSim + localSim
	# 			if localSim > mostDiff:
	# 				mostDiffIndex = i
	# 		avgSim = avgSim/max(1, len(self.close['Packet']))
	# 		# Put the most different item in the ant's hands. Not to take yet, just to touch
	# 		self.packetInHand = self.close['Packet'][mostDiffIndex]
	# 		return 1.0-((const1/(const1 + avgSim))**2)
	# 	else:
	# 		return 0.0

	# def pDropOff(self):
	# 	"""Like pickup, but now we compare similarity only to the item in the ant's hands"""
	# 	const2 = 0.85
	# 	localSim = 0.0
	# 	for op in self.close['Packet']:
	# 		if self.packetInHand is not op:
	# 			localSim = localSim + (varience(self.packetInHand.pattern['p'], op.pattern['p']))/2
	# 	return (const2/(const2 + localSim))**2

	def updateClosest(self, actor, doAdd):
		if doAdd:
			self.close[str(type(actor).__name__)].append(actor)
			if type(actor) == Packet:
				self.highestPacketDensitySeen = max(self.highestPacketDensitySeen, len(self.close['Packet']))
				self.shortTermMemory.append(actor)
				if len(self.shortTermMemory) > 100:
					self.shortTermMemory.pop(0)
		else:
			self.close[str(type(actor).__name__)].remove(actor)

	def neighborAdded(self, actor):
		"""SuperClass Hooke"""
		self.updateClosest(actor, True)

	def neighborRemoved(self, actor):
		"""SuperClass Hooke"""
		self.updateClosest(actor, False)

	def moved(self, oldPosition):
		"""SuperClass Hooke"""
		oldPosition.z = self.carrying
		self.moveHistory.append(oldPosition)


class Colony:
	def __init__(self):
		self.ants = []


### Main Methods ######################################################################################
#######################################################################################################

if __name__=="__main__":
	# Batch: (ordered by least time complex to most)
	# allDataTypes = ['data/iris/iris.json',
	#				 'data/seeds/seeds.json',
	#				 'data/glass/glass.json',
	#				 'data/wine/wine.json',
	#				 'data/zoo/zoo.json',
	#				 'data/heart/heart.json',
	#				 'data/car/car.json',
	#				 'data/yeast/yeast.json',
	#				 'data/block/pageblocks.json',
	#				 'data/ionosphere/ionosphere.json']

	# Single:
	# allDataTypes = ['data/iris/iris.json']
	# allDataTypes = ['data/seeds/seeds.json']
	# allDataTypes = ['data/glass/glass.json']
	# allDataTypes = ['data/wine/wine.json']
	allDataTypes = ['data/zoo/zoo.json']
	# allDataTypes = ['data/heart/heart.json']
	# allDataTypes = ['data/car/car.json']
	# allDataTypes = ['data/yeast/yeast.json']
	# allDataTypes = ['data/block/pageblocks.json']
	# allDataTypes = ['data/ionosphere/ionosphere.json']

	runsPerDataSet = 1 #10
	iterations = 2000
	for dataSet in allDataTypes:
		for run in range(runsPerDataSet):
			pSet = PatternSet(dataSet)
			for pattern in pSet.patterns:
				p = Packet(pattern, Point(random.randrange(0, 100), random.randrange(0, 100)))
			Packet.baseVarience = averageVarience(Packet.packets)
			print("Base Varience: " + str(Packet.baseVarience))

			interPheromoneDist = 7
			for x in range(120/interPheromoneDist):
				for y in range(120/interPheromoneDist):
					p = Pheromone(Point(x*interPheromoneDist-10, y*interPheromoneDist-10))
			for i in range(5):
				a = Ant(Point(random.randrange(0, 100), random.randrange(0, 100)))
			print("Packets:" + str(len(Packet.packets)))
			print("Pheromone:" + str(len(Pheromone.pheromones)))
			print("Ants:" + str(len(Ant.ants)))

			# Run Simulation
			for i in range(10000):
				if i%100 == 0:
					print("Move: " + str(i) + ", HPD[" + str(Ant.ants[0].highestPacketDensitySeen) + "], P[" + str(len(Ant.ants[0].close['Packet'])) + "]")
					Packet.clusterStats()
				for p in Packet.packets:
					p.update()
				for p in Pheromone.pheromones:
					p.update()
				for a in Ant.ants:
					a.update()


	# Create Recording
	with open('antAnimator/antMotion.csv', 'w') as file:
		for p in Packet.packets:
			file.write(",".join(str(h.x)+","+str(h.y)+","+str(h.z*10+4) for h in p.moveHistory)+"\n")
		for a in Ant.ants:
			file.write(",".join(str(h.x)+","+str(h.y)+","+str(h.z*10+4) for h in a.moveHistory)+"\n")
		# for p in Pheromone.pheromones:
		# 	file.write(",".join(str(p.position.x)+","+str(p.position.y)+","+str(c/3) for c in p.cHistory)+"\n")


	# Plot
	x = [p.position.x for p in Packet.packets]
	y = [p.position.y for p in Packet.packets]
	area = [2.0 for p in Packet.packets]
	# alph = [.5 for p in Packet.packets]

	# x = x + [p.position.x for p in Pheromone.pheromones]
	# y = y + [p.position.y for p in Pheromone.pheromones]
	# area = area + [p.concentration for p in Pheromone.pheromones]

	# for a in Ant.ants:
	# 	x = x + [h.x for h in a.moveHistory]
	# 	y = y + [h.y for h in a.moveHistory]
	# 	area = area + [h.z*10+1 for h in a.moveHistory]

	# x = [p.position.x for p in Packet.packets] + [a.position.x for a in Ant.ants]
	# y = [p.position.y for p in Packet.packets] + [a.position.y for a in Ant.ants]
	# area = [2.0 for p in Packet.packets] + [100 for a in Ant.ants]
	plt.scatter(x, y, c=area, s=area, alpha=.5)
	plt.show()


