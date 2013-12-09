from QuadTree import Point
from QuadTree import Actor
from QuadTree import QuadTree

import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from patternSet import PatternSet
from clustering import Cluster, Packet, varience, averageVarience



### Helper Methods ####################################################################################
#######################################################################################################

def emptyCopy(p):
	"""Create an empty Vector of the same dimensionality as that of the input vector"""
	c = []
	for i in p:
		c.append(0.0)
	return c

def patternsMean(patterns):
	"""Find the Average value of each element across all of the input patterns assembling and returning a mean pattern"""
	mean = emptyCopy(patterns[0]['p'])
	for pattern in patterns:
		for i, v in enumerate(pattern['p']):
			mean[i] = mean[i] + v
	for i, v in enumerate(mean):
		mean[i] = v/len(patterns)
	return mean

def patternVarience(p, q):
	"""Combined difference between two vectors"""
	var = 0.0
	for i in range(len(p)):
		var = var + (p[i] - q[i])*(p[i] - q[i])
	return var

def patternsStandardDeviation(patterns, mean):
	"""Standard Deviation vector of the same dimensionality as the patterns and their mean"""
	varience = emptyCopy(mean)
	for pattern in patterns:
		for j, item in enumerate(pattern['p']):
			varience[j] += pow(item - mean[j], 2)
	for i, v in enumerate(varience):
		varience[i] = math.sqrt(varience[i] / len(patterns))
	return varience

def euclidianDistance(p, q):
	"""Distance function in multi-dimensional space"""
	sumOfSquares = 0.0
	for i in range(len(p)):
		sumOfSquares = sumOfSquares + ((p[i]-q[i])*(p[i]-q[i]))
	return math.sqrt(sumOfSquares)



### Environment Class #################################################################################
#######################################################################################################


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
			self.packetInHand.move(np.cos(self.heading)*mag, np.sin(self.heading)*mag)
		else:
			self.heading = self.angleFromPheromones()
		self.move(np.cos(self.heading)*mag, np.sin(self.heading)*mag)

	def processEnvironment(self):
		"""Minimize looping through neighbors by doing all o(n) time work here"""
		if self.carrying:
			# Maybe the ant will drop whats in its hands
			dropProbability = self.pDropOff(float(len(self.close['Packet']))/len(Packet.packets), float(self.highestPacketDensitySeen)/len(Packet.packets))
			if random.random() <= dropProbability and len(self.close['Packet']) > 0:
				self.setOnMostSimilarOfNeightbors()
		else:
			# Maybe the ant will pick something up
			pickupProbability = self.pPickUp(float(len(self.close['Packet']))/len(Packet.packets), float(self.highestPacketDensitySeen)/len(Packet.packets))
			if random.random() <= pickupProbability and len(self.close['Packet']) > 0:
				self.grabMostDifferentOfNeighbors()

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

	def setOnMostSimilarOfNeightbors(self):
		"""Return the neighboring packet most similar to the packet in the ant's hands"""
		lowestVarienceValue = 99999.0
		lowestVarienceIndex = 0
		for i, op in enumerate(self.close['Packet']):
			if op is not self.packetInHand:
				opVarience = 0.0
				if self.packetInHand is not op:
					opVarience = varience(self.packetInHand.pattern['p'], op.pattern['p'])
					if opVarience < lowestVarienceValue:
						lowestVarienceValue = opVarience
						lowestVarienceIndex = i
		msn = self.close['Packet'][lowestVarienceIndex]

		ang = self.angleTo(msn)+np.pi%(2*np.pi)
		self.packetInHand.moveTo(np.cos(ang)*2+msn.position.x, np.sin(ang)*2+msn.position.y)

		# self.packetInHand.moveTo(msn.position.x, msn.position.y)
		self.packetInHand.inHand = False
		self.carrying = False

	def grabMostDifferentOfNeighbors(self):
		"""Return the neighboring packet most different from all of the its peers"""
		highestVarienceValue = 0.0
		highestVarienceIndex = 0
		for i, p in enumerate(self.close['Packet']):
			pVarienceSum = 0.0
			for op in self.close['Packet']:
				if p is not op:
					pVarienceSum = pVarienceSum + varience(p.pattern['p'], op.pattern['p'])
			if not p.inHand and pVarienceSum > highestVarienceValue:
				highestVarienceValue = pVarienceSum
				highestVarienceIndex = i
		if not self.close['Packet'][highestVarienceIndex].inHand:
			self.packetInHand = self.close['Packet'][highestVarienceIndex]
			self.packetInHand.moveTo(self.position.x, self.position.y)
			self.mostSimilarPacketSeen = self.mostSimilarPacketInMemory(self.packetInHand)
			self.packetInHand.inHand = True
			self.carrying = True

	def mostSimilarPacketInMemory(self, packet):
		"""Check the ant's short term memory for a pattern that is similar to the one now in its hands"""
		simIndex = 0
		simValue = 9999
		for i, memPacket in enumerate(self.shortTermMemory):
			if not memPacket.inHand and memPacket is not self.packetInHand:
				memPacketVarience = varience(self.packetInHand.pattern['p'], memPacket.pattern['p'])
				if memPacketVarience < simValue:
					simValue = memPacketVarience
					simIndex = i
		return self.shortTermMemory[simIndex]

	def depositPheromones(self):
		"""Higher concentrations of pheromones force ants to vacate the area, to take the path less traveled by"""
		for p in self.close['Pheromone']:
			p.concentration = p.concentration + 10/len(self.close['Pheromone'])

	def randomAngle(self):
		return np.radians(random.randrange(0, 360))

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
			if self.close['Pheromone'][maxIndex].concentration > 30:
				return self.angleTo(self.close['Pheromone'][maxIndex])*.1 + self.angleTo(self.close['Pheromone'][minIndex])*.9
			else:
				return self.randomAngle()
		else:
			return self.randomAngle()

	def angleTo(self, actor):
		"""Using its short term memory the ant can go searching for a packet it saw similar to the
		packet it is currently carrying"""
		if actor.position.x == self.position.x:
			return 0
		ang = np.arctan((actor.position.y - self.position.y)/(actor.position.x - self.position.x))
		if self.position.x > actor.position.x:
			ang = ang + np.pi
		return ang

	def updateClosest(self, actor, doAdd):
		"""Exactly what you would expect this method to do, plus it updates short term memory"""
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
	def __init__(self, antCount, patterns):
		Packet.packets = []
		Pheromone.pheromones = []
		Ant.ants = []
		Actor.actorIdInc = 0
		Actor.quadTree = QuadTree(Point(0.0, 0.0), Point(100, 100), 0)

		for pattern in patterns:
			Packet(pattern, Point(random.randrange(0, 100), random.randrange(0, 100)))
		Packet.baseVarience = averageVarience(Packet.packets)
		print("Base Varience: " + str(round(Packet.baseVarience, 4)))
		print("Packets:" + str(len(Packet.packets)))
		interPheromoneDist = 7
		for i in range(5):
			Ant(Point(random.randrange(0, 100), random.randrange(0, 100)))
		for x in range(120/interPheromoneDist):
			for y in range(120/interPheromoneDist):
				Pheromone(Point(x*interPheromoneDist-10, y*interPheromoneDist-10))
		print("Ants:" + str(len(Ant.ants)))
		print("Pheromones:" + str(len(Pheromone.pheromones)))

	def update(self):
		for p in Packet.packets:
			p.update()
		for f in Pheromone.pheromones:
			f.update()
		for a in Ant.ants:
			a.update()



### Main Methods ######################################################################################
#######################################################################################################

if __name__=="__main__":
	# Batch: (ordered by least time complex to most)
	# allDataTypes = ['data/iris/iris.json',
	# 				 'data/seeds/seeds.json',
	# 				 'data/glass/glass.json',
	# 				 'data/wine/wine.json',
	# 				 'data/zoo/zoo.json',
	# 				 'data/heart/heart.json',
	# 				 'data/car/car.json',
	# 				 'data/yeast/yeast.json',
	# 				 'data/block/pageblocks.json',
	# 				 'data/ionosphere/ionosphere.json',
	# 				 'data/pendigits/pendigits.json',
	# 				 'data/flare/flare.json',
	# 				 'data/letter/letter-recognition.json']

	# Single:
	# allDataTypes = ['data/iris/iris.json']
	# allDataTypes = ['data/seeds/seeds.json']
	# allDataTypes = ['data/glass/glass.json']
	# allDataTypes = ['data/wine/wine.json']
	# allDataTypes = ['data/zoo/zoo.json']
	# allDataTypes = ['data/heart/heart.json']
	# allDataTypes = ['data/car/car.json']
	# allDataTypes = ['data/yeast/yeast.json']
	# allDataTypes = ['data/block/pageblocks.json']
	# allDataTypes = ['data/ionosphere/ionosphere.json']

	# allDataTypes = ['data/pendigits/pendigits.json']
	# allDataTypes = ['data/flare/flare.json']
	allDataTypes = ['data/letter/letter-recognition.json']

	runsPerDataSet = 1 #10
	for dataSet in allDataTypes:
		setName = dataSet.split('.')[0].split('/')[-1]
		print(setName)
		pSet = PatternSet(dataSet)
		colony = Colony(5, pSet.patterns)

		# Run Simulation
		iterations = 25000
		startTime = time.time()
		for i in range(iterations):
			colony.update()
			if i%100 == 0:
				print("Move: " + str(i) + ", HPD[" + str(Ant.ants[0].highestPacketDensitySeen) + "]")
				Packet.clusterStats(setName)
		endTime = time.time()
		print("Run Time: [" + str(round(endTime-startTime, 2)) + " sec]")

		with open('records/antResults.txt', 'a') as file:
			file.write('\n\nNUMBER OF CLUSTERS: ' + str(len(Cluster.clusters)) + '\n')
			file.write('CURRENT DATA SET: ' + str(setName) + '\n')
			file.write('================PARTICLE SWARM================\n')
			for i, c1 in enumerate(Cluster.clusters):
				file.write('CLUSTER:' + str(i) + '\n')
				file.write('Cluster contains ' + str(float(len(c1.packets))/len(pSet.patterns)) + ' percent of the data\n')
				mean1 = patternsMean(list(p.pattern for p in c1.packets))
				file.write('Cluster mean is ' + str(mean1) + '\n')
				file.write('Cluster standard deviation is ' + str(patternsStandardDeviation(list(p.pattern for p in c1.packets), mean1)) + '\n')
				for j, c2 in enumerate(Cluster.clusters):
					if j > i:
						mean2 = patternsMean(list(p.pattern for p in c2.packets))
						file.write('The distance between this cluster and cluster ' + str(j) + ' is ' + str(euclidianDistance(mean1, mean2)) + '\n')

		print("Data Set: " + setName)
		print("Packets:" + str(len(Packet.packets)))
		print("Ants:" + str(len(Ant.ants)))
		print("Pheromones:" + str(len(Pheromone.pheromones)))

		# Create Recording
		# with open('antAnimator/'+setName+'AntMotion.csv', 'w') as file:
		# 	for p in Packet.packets:
		# 		file.write(",".join(str(ph.x)+","+str(ph.y)+","+str(p.rangeOfVision) for ph in p.moveHistory)+"\n")

			# for a in Ant.ants:
			# 	file.write(",".join(str(ah.x)+","+str(ah.y)+","+str(a.rangeOfVision) for ah in a.moveHistory)+"\n")
			# for f in Pheromone.pheromones:
			# 	file.write(",".join(str(f.position.x)+","+str(f.position.y)+","+str(fc/3) for fc in f.cHistory)+"\n")


	# Plot
	# x = [p.position.x for p in Packet.packets]
	# y = [p.position.y for p in Packet.packets]
	# area = [2.0 for p in Packet.packets]
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
	# plt.scatter(x, y, c=area, s=area, alpha=.5)
	# plt.show()
	print("Done!")


