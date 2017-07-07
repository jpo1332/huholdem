#!/usr/bin/env
#import numpy as np
import csv
import random
import math
import timeit
import sys
import ast
sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker/poker2']
from pokergamehead import *

def index_inlist(a, b, c, thelist):
    return c + 2 * (b-2) + 26 * (a - 2)

def main():
    starttime = timeit.default_timer()
    thesession = session()
    open2 = []
    if len(sys.argv) > 1:
        open_probs = open("rnnopen.csv", 'r')
        openprobs = open_probs.read()
        openprobs = openprobs.split("\n")
        counterx = 0
        for x in openprobs:
            x = x.split(",")
            z = []
            try:
                for y in x:
                    z.append(ast.literal_eval(y))
                openprobs[counterx] = z
            except:
                pass
            counterx += 1
        open_probs.close()
        open2 = openprobs[:len(openprobs)-1]

        
    open1 = []
    for a in range(2, 15):
        for b in range(2, 15):
            #if b > a:
                #continue
            for c in range(2):
                #if a == b and c == 1:
                    #continue
                open1.append([a,b,c, 0, 0])
    random.seed()
    for a in range(2, 15):
        for b in range(2, 15):
            if b > a:
                continue
            print(a, b)
            for c in range(2):
                if a == b and c == 1:
                    continue
                for d in range(10000):
                    thegame = game(thesession)
                    thegame.player1.cards.append(card(1, a))
                    if c:
                        thegame.player1.cards.append(card(1, b))
                    else:
                        thegame.player1.cards.append(card(2, b))
                    thegame.thedeck.attributes.remove(thegame.player1.cards[0])
                    thegame.thedeck.attributes.remove(thegame.player1.cards[1])

                    thegame.secondplayer.get_card(thegame.thedeck)
                    thegame.secondplayer.get_card(thegame.thedeck)

                    thegame.community.get_card(thegame.thedeck)
                    thegame.community.get_card(thegame.thedeck)
                    thegame.community.get_card(thegame.thedeck)

                    thegame.community.get_card(thegame.thedeck)

                    thegame.community.get_card(thegame.thedeck)
                    winner = thegame.compare_score(thegame.player1, thegame.secondplayer)

                    team1 = 0
                    team2 = 0
                    if winner == 1:
                        team1 = 1
                    elif winner == -1:
                        team2 = 1
                    else:
                        team1 = .5
                        team2 = .5
                    seconda = max(thegame.secondplayer.cards[0].number, thegame.secondplayer.cards[1].number)
                    secondb = min(thegame.secondplayer.cards[0].number, thegame.secondplayer.cards[1].number)
                    if thegame.secondplayer.cards[0].cardsuit == thegame.secondplayer.cards[1].cardsuit:
                        secondc = 1
                    else:
                        secondc = 0

                    index = index_inlist(a, b, c, open1)
                    open1[index][3] += team1
                    open1[index][4] += 1
                    #print(index, flop[index], [a, b, c, afloptype, afloplevel])
                    index = index_inlist(seconda, secondb, secondc, open1)
                    open1[index][3] += team2
                    open1[index][4] += 1
    resultFile1 = open("rnnopen.csv", 'w')
    wr1 = csv.writer(resultFile1, dialect='excel')
    print("0", open1[0], "3", open1[3], "20", open1[20], "200", open1[200])
    if len(sys.argv) > 1:
        print("inside")
        counter = 0
        for x in open2:
            index = index_inlist(open2[counter][0], open2[counter][1], open2[counter][2],  open1)
            if open1[index][4] != 0:
                newtotal = open1[index][4] + open2[counter][4]
                newprop = float(open2[counter][3]) * (open2[counter][4] / float(newtotal)) + (open1[index][3] / float(open1[index][4])) * (open1[index][4] / float(newtotal))
                newsum = newtotal * newprop
                open1[index] = open1[index][:3] + [newsum, newtotal]
            else:
                open1[index] = open1[index][:3] + [open2[counter][3] * open2[counter][4], open2[counter][4]]
            counter += 1
    counter = 0
    for x in open1:
        if open1[counter][4] != 0:
            y = open1[counter][:3] + [float(open1[counter][3]) / open1[counter][4]] + [open1[counter][4]]
            wr1.writerows([y])
        
        counter += 1
    endtime = timeit.default_timer() - starttime
    print(len(open1))
    print("time", endtime )
main()





                    
