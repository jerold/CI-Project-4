from QuadTree import Point
from QuadTree import Actor
import random
import numpy as np
import matplotlib.pyplot as plt

class Packet(Actor):
	packets = []

	def __init__(self, pattern, position):
		super(self.__class__, self).__init__(position)
		Packet.packets.append(self)
		self.pattern = pattern

class Ant(Actor):
	ants = []

	def __init__(self, position):
		super(self.__class__, self).__init__(position)
		Ant.ants.append(self)
		self.setRangeOfVision(10)

if __name__=="__main__":
	packets = []
	ants = []
	for i in range(2000):
		packets.append(Packet("p1", Point(random.randrange(0, 100), random.randrange(0, 100))))
	for i in range(20):
		ants.append(Ant(Point(random.randrange(0, 100), random.randrange(0, 100))))
		# print(str(packets[i].id) + " : " + str(packets[i].getX()) + ", " + str(packets[i].getY()))

	print("Packets:" + str(len(Packet.packets)))
	print("Ants:" + str(len(Ant.ants)))

	ants[0].move(0, 5)
	for n in ants[0].neighbors:
		print(str(n) + " " + str(ants[0].dist(n)))
	print("")
	ants[0].move(20, 15)
	for n in ants[0].neighbors:
		print(str(n) + " " + str(ants[0].dist(n)))

	# Plot
	x = [a.position.x for a in packets] + [a.position.x for a in ants]
	y = [a.position.y for a in packets] + [a.position.y for a in ants]
	area = [len(a.neighbors) for a in packets] + [len(a.neighbors) for a in ants]
	plt.scatter(x, y, c=area, s=area, alpha=0.5)
	plt.show()