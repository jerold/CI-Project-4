#!/usr/bin/python
# patternSet.py

import json
import random
import math

def findUniqueTargets(patterns):
	targets = []
	counts = {}
	for pattern in patterns:
		if pattern['t'] not in targets:
			targets.append(pattern['t'])
			try:
				counts[pattern['t']] = 1
			except TypeError:
				counts[str(pattern['t'])] = 1
		else:
			try:
				counts[pattern['t']] = counts[pattern['t']] + 1
			except TypeError:
				counts[str(pattern['t'])] = counts[str(pattern['t'])] + 1
	targets.sort()
	try:
		print("Targets: [" + ", ".join(str(t) + "x" + str(counts[t]) for t in targets) + "]")
	except TypeError:
		pass
	return {'targets':targets, 'counts':counts}

# Creates and empty pattern of the given dimensionality
def emptyPattern(w, h):
	pat = []
	if h > 1:
		for i in range(h):
			pat.append([])
			for j in range(w):
				pat[i].append(0.0)
	else:
		for j in range(w):
			pat.append(0.0)
	return pat  

# print an individual pattern with or without target value
def printPatterns(pattern):
	if isinstance(pattern, dict):
		for key in pattern.keys():
			if key == 't':
				print("Target: " + str(key))
			elif key == 'p':
				printPatterns(pattern['p'])
	elif isinstance(pattern[0], list):
		for pat in pattern:
			printPatterns(pat)
	else:
		print(', '.join(str(round(x, 3)) for x in pattern))

# A Pattern set contains sets of 3 types of patterns
# and can be used to retrieve only those patterns of a certain type
class PatternSet:
	confusionMatrix = {}
	correctness = []

	# Reads patterns in from a file, and puts them in their coorisponding set
	def __init__(self, fileName):
		with open(fileName) as jsonData:
			data = json.load(jsonData)
		self.name = fileName

		# Assign Patterns and Randomize order
		self.patterns = data
		self.inputMagX = len(self.patterns[0]['p'])
		self.inputMagY = 1
		if isinstance(self.patterns[0]['p'][0], list):
			self.inputMagX = len(self.patterns[0]['p'][0])
			self.inputMagY = len(self.patterns[0]['p'])

		targetsWithCounts = findUniqueTargets(self.patterns)
		self.targets = targetsWithCounts['targets']
		self.counts = targetsWithCounts['counts']

		random.shuffle(self.patterns)
		print(str(len(self.patterns)) + " Patterns Available (" + str(self.inputMagY) + "x" + str(self.inputMagX) + ")")