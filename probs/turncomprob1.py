#!/usr/bin/env
import numpy as np
import csv
import tensorflow as tf
from random import randint
from random import seed
import random
import math
import ast

origfile = open("comturn.csv", 'r')
origfile = list(origfile)
resultFile = open("comturn1.csv", 'w')
print "start"
countx = 0
for x in origfile:
    x = x[:len(x)-2]
    x = x.split(",")
    origfile[countx] = x
    countx += 1

wr = csv.writer(resultFile, dialect='excel')
counterx = 0
for x in origfile:
    countery = 0
    for y in x:
        origfile[counterx][countery] = float(y)
        countery += 1
    counterx += 1

origcopy = []
for x in origfile:
    origcopy.append(x[:6]) 
result = []
for x in range(2):
    for y in range(2):
        for z in range(2):
            for v in range(15):
                for w in range(1,5):
                    for a in range(1,5):
                        temp = []
                        for b in origfile:
                            if [x,y,z, v, w,a] == b[:6]:
                                temp.append(b[6])
                        temp = np.mean(temp)
                        if math.isnan(temp):
                            temp = 0
                        if temp:
                            result.append([x,y,z, v, w,a,temp])
            print x * 4 + y * 2 + z + 1, "/ 8 complete"
for x in result:
    wr.writerows([x])

print "success"
