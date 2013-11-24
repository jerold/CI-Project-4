from QuadTree import Point
from QuadTree import Actor
import random
import numpy as np
import matplotlib.pyplot as plt


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
		var = var + math.fabs(p[i] - q[i])
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
		self.packetInHand = []
		self.mostSimilarPacketSeen = []

		self.heading = 0.0

	def update(self):
		"""Have the ant wander, lay down pheromones, and possibly move a packet around"""
		self.depositPheromones()
		mag = random.randrange(0, 5)
		if self.carrying:
			# Maybe the ant will drop whats in its hands
			dropProbability = 0
			self.heading = self.angleToActor(mostSimilarPacketSeen)
		else:
			# Maybe the ant will pick something up
			pickupProbability = 0
			self.heading = self.angleFromPheromones()
		self.move(np.cos(self.heading)*mag, np.sin(self.heading)*mag)

	def processEnvironment(self):
		"""Minimize looping through neighbors by doing all o(n) time work here"""


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

	# def angleFromPheromones(self):
	# 	pheromones = self.neighborsOfType(Pheromone)
	# 	if len(pheromones) > 0:
	# 		pheromones.sort(key=lambda x: x.concentration, reverse=True)
	# 		# print(", ".join(str(round(p.concentration, 3)) for p in pheromones))
	# 		if pheromones[0].concentration > 200:
	# 			return self.angleToActor(pheromones[-1])
	# 		else:
	# 			return self.randomAngle()
	# 	else:
	# 		return self.randomAngle()

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

	# def angleFromPheromones(self):
	# 	pheromones = self.neighborsOfType(Pheromone)
	# 	if len(pheromones) > 0:
	# 		cSum = 0.0
	# 		for p in pheromones:
	# 			cSum = cSum + p.concentration
	# 		weightedAngle = 0.0
	# 		for p in pheromones:
	# 			weightedAngle = weightedAngle + self.angleToActor(p)*(p.concentration/cSum)
	# 		weightedAngle = (weightedAngle + np.pi)%(2*np.pi)
	# 		# print(weightedAngle)
	# 		return weightedAngle
	# 	else:
	# 		return self.randomAngle()

	def pPickUp(self):
		"""LF Model of Standard Ant Clustering"""
		return 0

	def updateClosest(self, actor, doAdd):
		if doAdd:
			self.close[str(type(actor).__name__)].append(actor)
			if type(actor) == Packet:
				self.highestPacketDensitySeen = max(self.highestPacketDensitySeen, len(self.close['Packet']))
				self.shortTermMemory.append(actor)
				if len(self.shortTermMemory) > 30:
					self.shortTermMemory.pop(0)
		else:
			self.close[str(type(actor).__name__)].remove(actor)

	def updateMoveHistory(self, oldPosition):
		oldPosition.z = self.carrying
		self.moveHistory.append(oldPosition)

	def neighborAdded(self, actor):
		"""SuperClass Hooke"""
		self.updateClosest(actor, True)

	def neighborRemoved(self, actor):
		"""SuperClass Hooke"""
		self.updateClosest(actor, False)

	def moved(self, oldPosition):
		"""SuperClass Hooke"""
		self.updateMoveHistory(oldPosition)


class Colony:
	def __init__(self):
		self.ants = []


### Main Methods ######################################################################################
#######################################################################################################

if __name__=="__main__":
	# for i in range(200):
	# 	p = Packet("p1", Point(random.randrange(0, 100), random.randrange(0, 100)))
	# for i in range(20):
	# 	a = Ant(Point(random.randrange(0, 100), random.randrange(0, 100)))
	# 	# print(str(packets[i].id) + " : " + str(packets[i].getX()) + ", " + str(packets[i].getY()))

	for i in range(200):
		p = Packet("p1", Point(random.randrange(0, 100), random.randrange(0, 100)))
	interPheromoneDist = 7
	for x in range(120/interPheromoneDist):
		for y in range(120/interPheromoneDist):
			p = Pheromone(Point(x*interPheromoneDist-10, y*interPheromoneDist-10))
	for i in range(10):
		a = Ant(Point(random.randrange(0, 100), random.randrange(0, 100)))

	print("Packets:" + str(len(Packet.packets)))
	print("Pheromone:" + str(len(Pheromone.pheromones)))
	print("Ants:" + str(len(Ant.ants)))

	# Ant.ants[0].move(20, 20)
	# for n in Ant.ants[0].neighbors:
	# 	print(str(n) + " " + str(Ant.ants[0].dist(n)))
	# print("")

	for i in range(1000):
		if i%100 == 0:
			print("Move: " + str(i) + ", D[" + str(Ant.ants[0].highestPacketDensitySeen) + "], P[" + str(len(Ant.ants[0].close['Packet'])) + "]")
		for p in Pheromone.pheromones:
			p.update()
		for a in Ant.ants:
			a.update()

	# Plot
	# x = [p.position.x for p in Packet.packets]
	# y = [p.position.y for p in Packet.packets]
	# area = [2.0 for p in Packet.packets]
	# alph = [.5 for p in Packet.packets]

	x = [p.position.x for p in Pheromone.pheromones]
	y = [p.position.y for p in Pheromone.pheromones]
	area = [p.concentration for p in Pheromone.pheromones]

	for a in Ant.ants:
		x = x + [h.x for h in a.moveHistory]
		y = y + [h.y for h in a.moveHistory]
		area = area + [h.z*10+1 for h in a.moveHistory]

	with open('antAnimator/antMotion.csv', 'w') as file:
		for a in Ant.ants:
			file.write(",".join(str(h.x)+","+str(h.y)+","+str(h.z*10+4) for h in a.moveHistory)+"\n")
		for p in Pheromone.pheromones:
			file.write(",".join(str(p.position.x)+","+str(p.position.y)+","+str(c/3) for c in p.cHistory)+"\n")

	# x = [p.position.x for p in Packet.packets] + [a.position.x for a in Ant.ants]
	# y = [p.position.y for p in Packet.packets] + [a.position.y for a in Ant.ants]
	# area = [2.0 for p in Packet.packets] + [100 for a in Ant.ants]
	plt.scatter(x, y, c=area, s=area, alpha=.5)
	plt.show()


