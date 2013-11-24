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


### Colony Methods ####################################################################################
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

	def update(self):
		"""Pheromone levels decay over time"""
		self.concentration = .98*self.concentration


class Ant(Actor):
	"""Ants wander around the solution space searching for packets which they attempt to Clustering
	based on how the packet smells.  Similar packets go next to one another"""
	ants = []

	def __init__(self, position):
		super(self.__class__, self).__init__(position)
		Ant.ants.append(self)
		self.setRangeOfVision(10)
		self.carrying = False
		self.packetInHand = []

	def update(self):
		"""Have the ant wander, lay down pheromones, and possibly move a packet around"""
		ang = np.radians(random.randrange(0, 360))
		mag = random.randrange(0, 5)
		self.move(np.cos(ang)*mag, np.sin(ang)*mag)
		for pheromone in self.neighborsOfType(Pheromone):
			pheromone.concentration = pheromone.concentration + 10
		if self.carrying:
			# Maybe the and will drop whats in its hands
			return 0
		else:
			# Maybe the ant will pick something up
			return 0

	def angleToActor(self, actor):
		"""Using its short term memory the ant can go searching for a packet it saw similar to the
		packet it is currently carrying"""
		ang = np.arctan((actor.position.y - self.position.y)/(actor.position.x - self.position.x))
		if ang < 0:
			ang = ang + 2*np.pi
		if self.position.x > actor.position.x:
			ang = ang + np.pi
		return ang%(2*np.pi)

	def pPickUp(self):
		"""LF Model of Standard Ant Clustering"""
		return 0

	def neighborsOfType(self, neighborType):
		"""not all neighbors are the same, sometimes we want to work with neighbors of one type only"""
		nots = []
		for n in self.neighbors:
			if type(n) == neighborType:
				nots.append(n)
		return nots

	def neighborAdded(self, actor):
		"""A hook from the Actor super class allows us to create a memory of things we've seen"""
		if type(actor) == Packet and actor not in self.shortTermMemory:
			self.shortTermMemory.append(actor)
			if len(self.shortTermMemory) > 30:
				self.shortTermMemory.pop(0)

	def moved(self, oldPosition):
		oldPosition.z = self.carrying
		self.moveHistory.append(oldPosition)


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

	# for i in range(200):
	# 	p = Packet("p1", Point(random.randrange(0, 100), random.randrange(0, 100)))
	for x in range(100/7+1):
		for y in range(100/7+1):
			p = Pheromone(Point(x*7, y*7))
	for i in range(1):
		a = Ant(Point(random.randrange(0, 100), random.randrange(0, 100)))

	print("Packets:" + str(len(Packet.packets)))
	# print("Pheromone:" + str(len(Pheromone.pheromones)))
	print("Ants:" + str(len(Ant.ants)))

	# Ant.ants[0].move(20, 20)
	# for n in Ant.ants[0].neighbors:
	# 	print(str(n) + " " + str(Ant.ants[0].dist(n)))
	# print("")

	for i in range(10000):
		if i%100 == 0:
			print("Move: " + str(i))

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

	# x = [p.position.x for p in Packet.packets] + [a.position.x for a in Ant.ants]
	# y = [p.position.y for p in Packet.packets] + [a.position.y for a in Ant.ants]
	# area = [2.0 for p in Packet.packets] + [100 for a in Ant.ants]
	plt.scatter(x, y, c=area, s=area, alpha=.5)
	plt.show()


