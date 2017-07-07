#!/usr/bin/env python3
import random
import math
import csv
import ast


#import sys
#sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker/Poker2']
from pokergamehead import *


openprobs = []
open_probs = open("probs/pokeropen.csv", 'r')
for x in open_probs:
    x = x[:len(x)-2]
    x = x.split(",")
    z = []
    for y in x:
        z.append(ast.literal_eval(y))
    openprobs.append(z)
open_probs.close()
xs = []
ys = []
for x in openprobs:
    xs.append(tuple(x[:len(x)-1]))
    ys.append(x[len(x)-1])
openprobs = zip(xs, ys)
openprobs = dict(openprobs)

flop_probs = open("probs/pokerflop1.csv", 'r')
flopprobs = flop_probs.read()
flopprobs = flopprobs.split("\n")
flopprobs = flopprobs[0].split("\r")
counterx = 0
for x in flopprobs:
    x = x.split(",")
    z = []
    for y in x:
        z.append(ast.literal_eval(y))
    flopprobs[counterx] = z
    counterx += 1
flop_probs.close()
xs = []
ys = []
for x in flopprobs:
    xs.append(tuple(x[:len(x)-1]))
    ys.append(x[len(x)-1])
flopprobs = zip(xs, ys)
flopprobs = dict(flopprobs)

turn_probs = open("probs/pokerturn.csv", 'r')
turnprobs = turn_probs.read()
turnprobs = turnprobs.split("\n")
turnprobs = turnprobs[0].split("\r")
counterx = 0
for x in turnprobs:
    x = x.split(",")
    z = []
    for y in x:
        z.append(ast.literal_eval(y))
    turnprobs[counterx] = z
    counterx += 1
turn_probs.close()
xs = []
ys = []
for x in turnprobs:
    xs.append(tuple(x[:len(x)-1]))
    ys.append(x[len(x)-1])
turnprobs = zip(xs, ys)
turnprobs = dict(flopprobs)

river_probs = open("probs/pokerriver.csv", 'r')
riverprobs = river_probs.read()
riverprobs = riverprobs.split("\n")
riverprobs = riverprobs[0].split("\r")
counterx = 0
for x in riverprobs:
    x = x.split(",")
    z = []
    for y in x:
        z.append(ast.literal_eval(y))
    riverprobs[counterx] = z
    counterx += 1
river_probs.close()
xs = []
ys = []
for x in riverprobs:
    xs.append(tuple(x[:len(x)-1]))
    ys.append(x[len(x)-1])
riverprobs = zip(xs, ys)
riverprobs = dict(riverprobs)


com_river = open("probs/comriver1.csv", 'r')
comriver = com_river.read()
comriver = comriver.split("\n")
#comriver = comriver.split("\r")
comriver = comriver[:len(comriver)-1]
counterx = 0
com_river.close()
for x in comriver:
    x = x[:len(x)-1]
    x = x.split(",")
    z = []
    for y in x:
        z.append(ast.literal_eval(y))
    comriver[counterx] = z
    counterx += 1
xs = []
ys = []
for x in comriver:
    xs.append(tuple(x[:len(x)-1]))
    ys.append(x[len(x)-1])
comriver = zip(xs, ys)
comriver = dict(comriver)

    
com_turn = open("probs/comturn1.csv", 'r')
comturn = com_turn.read()
comturn = comturn.split("\n")
#comturn = comturn.split("\r")
comturn = comturn[:len(comturn)-1]
counterx = 0
com_turn.close()
for x in comturn:
    x = x[:len(x)-1]
    x = x.split(",")
    z = []
    for y in x:
        z.append(ast.literal_eval(y))
    comturn[counterx] = z
    counterx += 1

xs = []
ys = []
for x in comturn:
    xs.append(tuple(x[:len(x)-1]))
    ys.append(x[len(x)-1])
comturn = zip(xs, ys)
comturn = dict(comturn)

rnnflop_probs = open("probs/rnnflop.csv", 'r')
rnnflopprobs = rnnflop_probs.read()
rnnflopprobs = rnnflopprobs.split("\n")
counterx = 0
for x in rnnflopprobs:
    x = x.split(",")
    z = []
    try:
        for y in x:
            z.append(ast.literal_eval(y))
        rnnflopprobs[counterx] = z
    except:
        pass
    counterx += 1
rnnflop_probs.close()
rnnflopprobs = rnnflopprobs[:len(rnnflopprobs)-1]
xs = []
ys = []
for x in rnnflopprobs:
    xs.append(tuple(x[:len(x)-2]))
    ys.append(x[len(x)-2])
rnnflopprobs = zip(xs, ys)
rnnflopprobs = dict(rnnflopprobs)

rnnturn_probs = open("probs/rnnturn.csv", 'r')
rnnturnprobs = rnnturn_probs.read()
rnnturnprobs = rnnturnprobs.split("\n")
counterx = 0
for x in rnnturnprobs:
    x = x.split(",")
    z = []
    try:
        for y in x:
            z.append(ast.literal_eval(y))
        rnnturnprobs[counterx] = z
    except:
        pass
    counterx += 1
rnnturn_probs.close()
rnnturnprobs = rnnturnprobs[:len(rnnturnprobs)-1]
xs = []
ys = []
for x in rnnturnprobs:
    xs.append(tuple(x[:len(x)-2]))
    ys.append(x[len(x)-2])
rnnturnprobs = zip(xs, ys)
rnnturnprobs = dict(rnnturnprobs)

rnnriver_probs = open("probs/rnnriver.csv", 'r')
rnnriverprobs = rnnriver_probs.read()
rnnriverprobs = rnnriverprobs.split("\n")
counterx = 0
for x in rnnriverprobs:
    x = x.split(",")
    z = []
    try:
        for y in x:
            z.append(ast.literal_eval(y))
        rnnriverprobs[counterx] = z
    except:
        pass
    counterx += 1
rnnriver_probs.close()
rnnriverprobs = rnnriverprobs[:len(rnnriverprobs)-1] 
xs = []
ys = []
for x in rnnriverprobs:
    xs.append(tuple(x[:len(x)-2]))
    ys.append(x[len(x)-2])
rnnriverprobs = zip(xs, ys)
rnnriverprobs = dict(rnnriverprobs)
