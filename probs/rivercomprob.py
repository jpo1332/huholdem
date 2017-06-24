#!/usr/bin/env
import numpy as np
import csv
import tensorflow as tf
from random import randint
from random import seed
import random
import math
import sys
sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker']
from pokergamehead import *
from checkprobs import *


def card_onehot(card1, number):
    #print card1
    temp = np.zeros(number)
    temp[card1 - 1] = 1
    temp2 = []
    for x in temp:
        temp2.append(x)
    return temp2

def return_variables(session1, game1, player1):
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



resultFile = open("comriver.csv", 'w')
wr = csv.writer(resultFile, dialect='excel')
a = session()
print "suh"
a = session()
parity = 0
for runs in range(1000000):
    b = game(a)

#high, flush ,fdraw, straight, straighdraw, pair, twopair, threekind, fullhouse
    
    b.start(a)
    b.flop()
    b.river()
    b.river()
    winner = b.compare_score(b.player1, b.secondplayer)
    parity += winner
    #print b.player1.handscore.type, b.secondplayer.handscore.type
    variables = return_com(b)
    s = abs(b.player1.handscore.type + (b.player1.handscore.level * .07))
 
    #print variables, s
    wr.writerows([variables + [s]])
    s1 = abs(b.secondplayer.handscore.type + (b.secondplayer.handscore.level *.07))
    wr.writerows([variables + [s1]])
    
    if runs % 100000 == 0:
        print "Run:", runs
print parity

#print section

print "success"



