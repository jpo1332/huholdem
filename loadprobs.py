#!/usr/bin/env python3
import random
import math
import csv
import ast
import numpy as np
import tensorflow as tf
import sys
sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker/Poker2']
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
    

def return_com(game1):
    num = []
    suits = []
    for x in game1.community.cards:
        num.append(x.number)
        suits.append(x.cardsuit)
    num.sort()
    #print num, suits
    threekind = 0
    for x in num:
        if num.count(x) == 3:
            threekind = 1
    twopair, onepair = check_pairs(num)
    if onepair == False:
        onepair = 0
    if twopair == False:
        twopair = 0
    if onepair != 0:
        onepair = 1
    if twopair != 0:
        twopair = 1
    flush = 0
    for x in suits:
        if suits.count(x) > flush:
            flush = suits.count(x)
    num = list(set(num))
    num.sort()
    straight = [0]
    y = 0
    #Following checks for straight, pain in butt to make; careful
    while y < 2:
        x = 0
        check = 0
        while x < 4:
            #print num[len(num) - 1 - x - y] - 1, num[len(num) - 2 - x - y]
            try:
                if num[len(num) - 1 - x - y] - 1 == num[len(num) - 2 - x - y]:
                    check += 1
                else:
                    straight.append(check)
                    check = 0
            except:
                break
            x += 1
        y += 1
    straight = max(straight)
    returns = [threekind, twopair, onepair, flush, straight]
    return returns
def check_prob(rounds, game1, players):
    if rounds == 0:
        card1 = players.cards[0].number
        card2 = players.cards[1].number
        samesuit = 0
        if players.cards[0].cardsuit == players.cards[1].cardsuit:
            samesuit = 1
        probability = openprobs.get((card1,card2,samesuit), .1)
        move = 0
        if probability <= .35:
            move = 0
        elif probability >= .7 and game1.previousbet < 80:
            move = 2
        else:
            move = 1
        return move, probability
    game1.compare_score(game1.player1, game1.secondplayer)
    if rounds == 1:
        probability = flopprobs.get((players.handscore.type - 2, players.handscore.level - 2), .1)
        move = 0
        if probability <= .4:
            move = 0
        elif probability >= .7 and game1.previousbet < 80:
            move = 2
        else:
            move = 1
        return move, probability
    if rounds == 2:
        probability = turnprobs.get((players.handscore.type - 2, players.handscore.level - 2), .1)
        move = 0
        if probability <= .4:
            move = 0
        elif probability >= .75 and game1.previousbet < 120:
            move = 2
        else:
            move = 1
        return move, probability
    if rounds == 3:
        probability = riverprobs.get((players.handscore.type - 2, players.handscore.level - 2, players.handscore.high - 2), .1)
        move = 0
        if probability <= .35:
            move = 0
        elif probability >= .75 and game1.previousbet < 80:
            move = 2
        else:
            move = 1
        return move, probability
    return 0


