from QuadTree import Point
from QuadTree import Actor
from clustering import Packet
import random
import numpy as np


class Particle(Actor):
    particles = []

    def __init__(self, position):
        super(self.__class__, self).__init__(position)
        Particle.particles.append(self)
        self.setRangeOfVision(10)
        self.carrying = None
        self.packetInHand = Packet
        self.mostSimilarPacketSeen = Packet
        self.velocity = [Point(1, 1), np.radians(random.randrange(0, 360))]
        self.personalBest = None
        self.globalBest = Packet
        self.neighborHoodBest = Packet
        self.maxVelocity = 10

    def update(self):
        """Have the particle fly with a new velocity and possibly move a packet around"""
        self.processEnvironment()
        self.velocity = self.calculateNewVelocity()
        self.moveTo(self.velocity[0])

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

    def calculateNewVelocity(self):
        newVelocity = []
        positions = []
        positions.append(Point(self.position.x,  self.position.y))
        positions.append(Point(self.personalBest.position.x, self.personalBest.position.y))
        positions.append(Point(self.neighborHoodBest.position.x, self.neighborHoodBest.position.y))
        positions.append(Point(self.globalBest.position.x, self.globalBest.position.y))
        newPosition = Point(0, 0)
        newDirection = 0.0
        for i, point in enumerate(positions):
            newPosition.x += point.x
            newPosition.y += point.y
            try:
                newDirection += point.angle(positions[i+1])
            except IndexError:
                pass
        newVelocity.append(newPosition)
        newDirection /= len(positions)
        newVelocity.append(newDirection % (2 * np.pi))
        return newVelocity