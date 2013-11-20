#!/usr/bin/python

import json
import itertools

import math
import random

pageBlock = {'inFiles':['data/block/page-blocks.data'],
             'outFile':'data/block/pageblocks.json',
             'width':10,
             'height':1}

car = {'inFiles':['data/car/car.data'],
             'outFile':'data/car/car.json',
             'width':10,
             'height':1}

flare = {'inFiles':['data/flare/flare.data1',
                    'data/flare/flare.data2'],
             'outFile':'data/flare/flare.json',
             'width':10,
             'height':1}

adult = {'inFiles':['data/adult/adult.data'],
             'outFile':'data/adult/adult.json',
             'width':15,
             'height':1}

wine = {'inFiles':['data/wine/wine.data'],
             'outFile':'data/wine/wine.json',
             'width':14,
             'height':1}

yeast = {'inFiles':['data/yeast/yeast.data'],
         'outFile':'data/yeast/yeast.json',
         'width':9,
         'height':1}

zoo = {'inFiles':['data/zoo/zoo.data'],
         'outFile':'data/zoo/zoo.json',
         'width':16,
         'height':1}

heart = {'inFiles':['data/heart/heart.data'],
         'outFile':'data/heart/heart.json',
         'width':14,
         'height':1}

seeds = {'inFiles':['data/seeds/seeds.data'],
         'outFile':'data/seeds/seeds.json',
         'width':7,
         'height':1}
glass = {'inFiles':['data/glass/glass.data'],
         'outFile':'data/glass/glass.json',
         'width':10,
         'height':1}

ionosphere = {'inFiles':['data/ionosphere/ionosphere.data'],
         'outFile':'data/ionosphere/ionosphere.json',
         'width':34,
         'height':1}

iris = {'inFiles':['data/iris/iris.data'],
         'outFile':'data/iris/iris.json',
         'width':4,
         'height':1}

def parseAdult(lines):
    patSet = []
    attributes = [[] for _ in range(14)]
    attributesAlt = [{'continuous':True},
                     {'Private':8, 'Self-emp-not-inc':6, 'Self-emp-inc':7, 'Federal-gov':5, 'Local-gov':3, 'State-gov':4, 'Without-pay':2, 'Never-worked':1, '?':7, 'continuous':False},
                     {'continuous':True},
                     {'Bachelors':12, 'Some-college':8, '11th':5, 'HS-grad':7, 'Prof-school':9, 'Assoc-acdm':10, 'Assoc-voc':11, '9th':3, '7th-8th':2, '12th':6, 'Masters':13, '1st-4th':1, '10th':4, 'Doctorate':14, '5th-6th':2, 'Preschool':0, 'continuous':False},
                     {'continuous':True},
                     {'Married-civ-spouse':1, 'Divorced':3, 'Never-married':6, 'Separated':4, 'Widowed':5, 'Married-spouse-absent':2, 'Married-AF-spouse':0, 'continuous':False},
                     {'Tech-support':1, 'Craft-repair':2, 'Other-service':3, 'Sales':4, 'Exec-managerial':5, 'Prof-specialty':6, 'Handlers-cleaners':7, 'Machine-op-inspct':8, 'Adm-clerical':9, 'Farming-fishing':10, 'Transport-moving':11, 'Priv-house-serv':12, 'Protective-serv':13, 'Armed-Forces':14, '?':6, 'continuous':False},
                     {'Wife':4, 'Own-child':1, 'Husband':5, 'Not-in-family':3, 'Other-relative':3, 'Unmarried':2, 'continuous':False},
                     {'White':5, 'Asian-Pac-Islander':4, 'Amer-Indian-Eskimo':3, 'Other':2, 'Black':1, 'continuous':False},
                     {'Female':2, 'Male':1, 'continuous':False},
                     {'continuous':True},
                     {'continuous':True},
                     {'continuous':True},
                     {"United-States":1, "Cambodia":2, "England":3, "Puerto-Rico":4, "Canada":5, "Germany":6, "Outlying-US(Guam-USVI-etc)":7, "India":8, "Japan":9, "Greece":10, "South":11, "China":12, "Cuba":13, "Iran":14, "Honduras":15, "Philippines":16, "Italy":17, "Poland":18, "Jamaica":19, "Vietnam":20, "Mexico":21, "Portugal":22, "Ireland":23, "France":24, "Dominican-Republic":25, "Laos":26, "Ecuador":27, "Taiwan":28, "Haiti":29, "Columbia":30, "Hungary":31, "Guatemala":32, "Nicaragua":33, "Scotland":34, "Thailand":35, "Yugoslavia":36, "El-Salvador":37, "Trinadad&Tobago":38, "Peru":39, "Hong":40, "Holand-Netherlands":41, "?":1, 'continuous':False}]
    targets = []
    targetsAlt = {'>50K':1, '<=50K':2}
    for l, line in enumerate(lines):
        line = line.split('\n')[0]
        line = line.split(', ')
        pattern = line[:len(line)-1]
        for i, elem in enumerate(pattern):
            if attributesAlt[i]['continuous']:
                pattern[i] = elem
            else:
                pattern[i] = attributesAlt[i][elem]
            attributes[i].append(pattern[i])
        patternTarget = targetsAlt[line[-1]]
        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        # print(str(l) + ' p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for a, attribute in enumerate(attributes):
        if not attributesAlt[a]['continuous']:
            print(str(a) + " S:" + str(set(attribute)))
        else:
            print(str(a) + " L:" + str(len(set(attribute))))
    return patSet


def parseFlare(lines):
    patSet = []
    attributes = [[] for _ in range(10)]
    attributesAlt = [{'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'H':7},
                     {'X':1, 'R':2, 'S':3, 'A':4, 'H':5, 'K':6},
                     {'X':1, 'O':2, 'I':3, 'C':4}]
    targets = [[] for _ in range(3)]
    for line in lines:
        line = line.split('\n')[0]
        line = line.split()
        pattern = line[:-3]
        for i, elem in enumerate(pattern):
            if i < 3:
                pattern[i] = attributesAlt[i][elem]
            else:
                pattern[i] = int(elem)
            attributes[i].append(pattern[i])
        patternTarget = line[-3:]
        patSet.append({'p':pattern, 't':patternTarget})
        targets[0].append(patternTarget[0])
        targets[1].append(patternTarget[1])
        targets[2].append(patternTarget[2])
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets[0]))
    print(set(targets[1]))
    print(set(targets[2]))
    print("Attributes")
    for attribute in attributes:
        print(set(attribute))
    return patSet

def parseCar(lines):
    patSet = []
    attributes = [[] for _ in range(6)]
    attributesAlt = [{'low':1, 'vhigh':4, 'med':2, 'high':3},
                     {'low':1, 'vhigh':4, 'med':2, 'high':3},
                     {'4':3, '5more':4, '2':1, '3':2},
                     {'4':2, 'more':3, '2':1},
                     {'big':3, 'med':2, 'small':1},
                     {'med':2, 'low':1, 'high':3}]
    targets = []
    targetsAlt = {'acc':2, 'good':3, 'unacc':1, 'vgood':4}
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(',')
        pattern = line[:len(line)-1]
        for i, elem in enumerate(pattern):
            pattern[i] = attributesAlt[i][elem]
            attributes[i].append(pattern[i])
        patternTarget = targetsAlt[line[len(line)-1]]
        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(set(attribute))
    return patSet


def parseYeast(lines):
    patSet = []
    attributes = [[] for _ in range(8)]
    targets = []
    targetsAlt = {'CYT':1, 'NUC':2, 'MIT':3, 'ME3':4, 'ME2':5, 'ME1':6, 'EXC':7,
                  'VAC':8, 'POX':9, 'ERL':10}
    for line in lines:
        line = line.split('\n')[0]
        line = line.split()
        pattern = line[1:len(line)-1]
        for i, elem in enumerate(pattern):
            pattern[i] = float(elem)
            attributes[i].append(pattern[i])
        patternTarget = targetsAlt[line[len(line)-1]]
        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(set(attribute))
    return patSet

def parseBlock(lines):
    patSet = []
    attributes = [[] for _ in range(10)]
    targets = []
    for line in lines:
        line = line.split('\n')[0]
        line = line.split()
        pattern = line[:len(line)-1]
        for i in range(len(pattern)):
            pattern[i] = float(pattern[i])
            attributes[i].append(pattern[i])
        patternTarget = int(line[len(line)-1])
        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet

def parseWine(lines):
    patSet = []
    attributes = [[] for _ in range(13)]
    targets = []
    for line in lines:
        line = line.strip('\n')
        line = line.split(',')
        patternTarget = int(line[0])
        pattern = line[1:len(line)]
        for i, elem in enumerate(line[1:]):
            pattern[i] = float(pattern[i])
            attributes[i].append(float(elem))

        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet


def parseZoo(lines):
    patSet = []
    attributes = [[] for _ in range(16)]
    targets = []
    for line in lines:
        line = line.strip('\n')
        line = line.split(',')
        patternTarget = int(line[-1])
        pattern = line[1:len(line)-1]
        for i, elem in enumerate(line[1:len(line)-1]):
            pattern[i] = int(pattern[i])
            attributes[i].append(int(elem))

        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet


def parseHeart(lines):
    patSet = []
    attributes = [[] for _ in range(13)]
    targets = []
    for line in lines:
        line = line.strip('\n')
        line = line.split()
        patternTarget = int(line[-1])-1
        pattern = line[1:len(line)]
        for i, elem in enumerate(line[1:]):
            pattern[i] = float(pattern[i])
            attributes[i].append(float(elem))

        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet


def parseSeeds(lines):
    patSet = []
    attributes = [[] for _ in range(7)]
    targets = []
    for line in lines:
        line = line.strip('\n')
        line = line.split()
        patternTarget = int(line[-1])
        pattern = line[:len(line)-1]
        for i, elem in enumerate(line[:-1]):
            pattern[i] = float(pattern[i])
            attributes[i].append(float(elem))

        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet


def parseGlass(lines):
    patSet = []
    attributes = [[] for _ in range(10)]
    targets = []
    for line in lines:
        line = line.strip('\n')
        line = line.split(',')
        patternTarget = int(line[-1])
        pattern = line[:len(line)-1]
        for i, elem in enumerate(line[:-1]):
            pattern[i] = float(pattern[i])
            attributes[i].append(float(elem))

        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet


def parseIonosphere(lines):
    patSet = []
    attributes = [[] for _ in range(34)]
    targets = []
    targetsAlt = {'g':1, 'b':0}
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(',')
        pattern = line[:len(line)-1]
        for i in range(len(pattern)):
            pattern[i] = float(pattern[i])
            attributes[i].append(pattern[i])
        patternTarget = targetsAlt[line[len(line)-1]]
        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet

def parseIris(lines):
    patSet = []
    attributes = [[] for _ in range(4)]
    targets = []
    targetsAlt = {'Iris-setosa':1, 'Iris-versicolor':2, 'Iris-virginica':3}
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(',')
        pattern = line[:len(line)-1]
        for i in range(len(pattern)):
            pattern[i] = float(pattern[i])
            attributes[i].append(pattern[i])
        patternTarget = targetsAlt[line[-1]]
        patSet.append({'p':pattern, 't':patternTarget})
        targets.append(patternTarget)
        #print('p:' + str(pattern) + '  t:' + str(patternTarget))
    print("Targets")
    print(set(targets))
    print("Attributes")
    for attribute in attributes:
        print(len(set(attribute)))
    return patSet

def mygrouper(n, iterable):
    "http://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n"
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in itertools.izip_longest(*args))

def buildKMeansCenters(patterns, w, h, k):
    centers = {}
    for i in range(k):
        centers[i] = emptyPattern(w, h)
        if h > 1:
            centers[i][random.randint(0,h-1)][random.randint(0,w-1)] = 1
        else:
            centers[i][random.randint(0,w-1)] = 1
    dist = 100
    while dist > 3:
        tempCenters = adjustCenters(patterns, centers)
        dist = 0
        for i in range(k):
            dist = dist + euclidianDistance(centers[i], tempCenters[i])
        centers = tempCenters
        print(dist)
    for i in range(k):
        printPattern(centers[i])
        print(i)
    return centers

def adjustCenters(patterns, centers):
    groups = {}
    for k in centers.keys():
        groups[k] = []
    for pattern in patterns:
        bestDist = 99999
        bestKey = ''
        for key in centers.keys():
            center = centers[key]
            dist = euclidianDistance(pattern['p'], center)
            if dist < bestDist:
                bestDist = dist
                bestKey = key
        groups[bestKey].append(pattern)
    newCenters = {}
    for k in centers.keys():
        if len(groups[k]) > 0:
            newCenters[k] = buildMeanPattern(groups[k])
        else:
            newCenters[k] = centers[k]
    return newCenters

def euclidianDistance(p, q):
    sumOfSquares = 0.0
    if isinstance(p[0], list):
        for i in range(len(p)):
            for j in range(len(p[i])):
                sumOfSquares = sumOfSquares + ((p[i][j]-q[i][j])*(p[i][j]-q[i][j]))
    else:
        for i in range(len(p)):
            sumOfSquares = sumOfSquares + ((p[i]-q[i])*(p[i]-q[i]))
    return math.sqrt(sumOfSquares)


def buildCentersAndSigmas(patterns):
    centersTargets = {}
    for pattern in patterns:
        if pattern['t'] not in centersTargets:
            centersTargets[pattern['t']] = []
        centersTargets[pattern['t']].append(pattern)
    centers = {}
    sigmas = {}
    print("Found " + str(len(centersTargets)) + " targets.")
    # build center as mean of all trained k patterns, and sigma as standard deviation
    for k in centersTargets.keys():
        kPats = centersTargets[k]
        centers[k] = buildMeanPattern(kPats)

    print("Centers Post Average:")
    for k in centersTargets.keys():
        print(k)
        printPattern(centers[k])

    # Build Sigmas for each space
    print("Sigma:")
    for k in centersTargets.keys():
        sigmas[k] = buildSigmaPattern(centers[k], kPats)
        printPattern(sigmas[k])

    # refine centers using k-means
    dist = 100
    distDelta = 100
    oldDist = 0
    while dist > 1 and abs(distDelta) > 0.01:
        tempCenters = adjustCenters(patterns, centers)
        dist = 0
        for k in centersTargets.keys():
            dist = dist + euclidianDistance(centers[k], tempCenters[k])
        centers = tempCenters
        distDelta = dist - oldDist
        oldDist = dist
        print("dist:" + str(dist) + ", delta:" + str(distDelta))

    print("Centers Post K-means:")
    for k in centersTargets.keys():
        print(k)
        printPattern(centers[k])

    return {'centers':centers, 'sigmas':sigmas}

def buildMeanPattern(patterns):
    h = 0
    w = len(patterns[0]['p'])
    if isinstance(patterns[0]['p'][0], list):
        h = len(patterns[0]['p'])
        w = len(patterns[0]['p'][0])
    mPat = emptyPattern(w, h)
    for pat in patterns:
        #print(pat['p'])
        if h > 1:
            #print(str(len(pat['p'])) + " x " + str(len(pat['p'][0])))
            for i in range(h):
                for j in range(w):
                    mPat[i][j] = mPat[i][j] + pat['p'][i][j]
        else:
            for j in range(w):
                mPat[j] = mPat[j] + pat['p'][j]
    if h > 1:
        for i in range(h):
            for j in range(w):
                mPat[i][j] = mPat[i][j] / len(patterns)
    else:
        for j in range(w):
            mPat[j] = mPat[j] / len(patterns)
    return mPat

def buildSigmaPattern(meanPat, patterns):
    h = 0
    w = len(patterns[0]['p'])
    if isinstance(patterns[0]['p'][0], list):
        h = len(patterns[0]['p'])
        w = len(patterns[0]['p'][0])
    sPat = emptyPattern(w, h)
    # Sum over all square of distance from means
    if h > 1:
        for i in range(h):
            for j in range(w):
                for pat in patterns:
                    sPat[i][j] = sPat[i][j] + (pat['p'][i][j] - meanPat[i][j])*(pat['p'][i][j] - meanPat[i][j])
                sPat[i][j] = math.sqrt(1.0/len(patterns)*sPat[i][j])
    else:
        for j in range(w):
            for pat in patterns:
                sPat[j] = sPat[j] + (pat['p'][j] - meanPat[j])*(pat['p'][j] - meanPat[j])
            sPat[j] = math.sqrt(1.0/len(patterns)*sPat[j])
    return sPat
        


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

def printPattern(pattern):
    tolerance = 0.7
    if isinstance(pattern[0], list):
        for i in range(len(pattern)):
            print(', '.join(str(round(x+tolerance,3)) for x in pattern[i]))
    else:
        print(', '.join(str(round(x,3)) for x in pattern))


if __name__=="__main__":
    parseSets = [pageBlock, car, flare, adult, wine, yeast, zoo, heart, seeds, ionosphere, iris, glass]
    #parseSet = pageBlock
    #parseSets = [car]
    #parseSets = [flare]
    #parseSets = [adult]
    #parseSets = [wine]
    #parseSets = [yeast]
    #parseSets = [zoo]
    #parseSets = [heart]
    #parseSets = [seeds]
    #parseSets = [glass]
    #parseSets = [ionosphere]
    #parseSets = [iris]

    for parseSet in parseSets:
        lines = []
        for fileName in parseSet['inFiles']:
            with open(fileName) as file:
                fileLines = file.readlines()
                for line in fileLines:
                    lines.append(line)
        # print(parseSet['inFiles'][0])
        
        if parseSet['outFile'] == pageBlock['outFile']:
            patternSet = parseBlock(lines)
        elif parseSet['outFile'] == car['outFile']:
            patternSet = parseCar(lines)
        elif parseSet['outFile'] == flare['outFile']:
            patternSet = parseFlare(lines)
        elif parseSet['outFile'] == adult['outFile']:
            patternSet = parseAdult(lines)
        elif parseSet['outFile'] == wine['outFile']:
            patternSet = parseWine(lines)
        elif parseSet['outFile'] == yeast['outFile']:
            patternSet = parseYeast(lines)
        elif parseSet['outFile'] == zoo['outFile']:
            patternSet = parseZoo(lines)
        elif parseSet['outFile'] == heart['outFile']:
            patternSet = parseHeart(lines)
        elif parseSet['outFile'] == seeds['outFile']:
            patternSet = parseSeeds(lines)
        elif parseSet['outFile'] == glass['outFile']:
            patternSet = parseGlass(lines)
        elif parseSet['outFile'] == ionosphere['outFile']:
            patternSet = parseIonosphere(lines)
        elif parseSet['outFile'] == iris['outFile']:
            patternSet = parseIris(lines)
            
        # print("pats: " + str(len(patternSet)))
        with open(parseSet['outFile'], 'w+') as outfile:
            #data = {'count':len(patternSet),
            #        'width':parseSet['width'],
            #        'height':parseSet['height'],
            #        'patterns':patternSet}
            data = patternSet
            json.dump(data, outfile)
        print("\n")


