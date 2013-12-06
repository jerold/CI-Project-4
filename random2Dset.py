import json
import random

if __name__=="__main__":
	a = []
	for i in range(50):
		a.append({'p':[float(random.randrange(-1000, 1000))/1000, float(random.randrange(-1000, 1000))/1000], 't':0})
	for i in range(50):
		a.append({'p':[float(random.randrange(-1000, 1000))/1000, float(random.randrange(-1000, 1000))/1000 + 5], 't':0})
	for i in range(50):
		a.append({'p':[float(random.randrange(-1000, 1000))/1000 + 5, float(random.randrange(-1000, 1000))/1000], 't':0})
	for i in range(50):
		a.append({'p':[float(random.randrange(-1000, 1000))/1000 + 5, float(random.randrange(-1000, 1000))/1000 + 5], 't':0})

	with open('psoTestSet.json', 'w+') as outfile:
		json.dump(a, outfile)