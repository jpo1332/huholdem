#!/usr/bin/env
import numpy as np
import csv
import ast

origfile = open("rivernndata.csv", 'r')
origfile = csv.reader(origfile, dialect='excel')
origfile = list(origfile)
resultFile = open("rivernndata1.csv",'w')
wr = csv.writer(resultFile, dialect='excel')

arrays = []
data = []
data2 = []
length = len(origfile)
print length
for x in range(length):
    data2.append([])
for x in range(len(origfile[0])):
    arrays.append([])
    data.append([])
counterx = 0
for x in origfile:
    countery = 0
    for y in x:
        origfile[counterx][countery] = ast.literal_eval(y)
        countery += 1
    counterx += 1
    



counterx = 0
for x in origfile:
    countery = 0
    for y in x:
        arrays[countery].append(origfile[counterx][countery])
        countery += 1
    counterx += 1

origfile = []

counterx = 0
deletelist = []
for z in range(1):
    x = np.array(arrays[0])
    mean = np.mean(x)
    stdev = 7 * np.std(x)
    print mean, stdev
    countery = 0
    for y in x:
        if abs(y - mean) >= stdev:
            deletelist.append(countery)
        countery += 1
print deletelist
for x in arrays:
    tempx = []
    for y in range(len(x)):
        if (y in deletelist) == False:
            tempx.append(x[y])
    arrays[counterx] = tempx
    counterx += 1

counterx = 0

for x in arrays:
    setmin = min(x)
    setmax = max(x)
    mean = np.mean(np.array(x))
    print counterx, "setmin:", setmin, "setmax:", setmax, "average:", mean
    for y in x:
        z = (float(y) - float(setmin))/(float(setmax) - float(setmin))
        data[counterx].append(z)
    counterx += 1
arrays = 0

print len(data), len(data[0])
print len(data2), len(data2[0])
print data[0][:50]
counterx = 0
while counterx < len(data):
    countery = 0
    if counterx % 50 == 0:
        print "counter", counterx
    while countery < len(data[0]):
        data2[countery].append(data[counterx][countery])
        countery += 1
    counterx += 1
length = len(data[0]) 
for x in range(0, length):
    wr.writerows([data2[x]])
print "success"

