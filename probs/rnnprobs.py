#!/usr/bin/env
import numpy as np
import csv
import random
import math
import timeit
import sys
sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker/poker2']
from pokergamehead import *

def make_hand(card1, card2, suited, deck, scoretype, scorelevel, turn):
    #Weed out impossible hands
    if card1.number < card2.number:
        return 0
    if card1.number == card2.number and suited == 1:
        return 0
    if card1.number == card2.number and scoretype < 15:
        return 0
    if card1.number == card2.number and scoretype == 15 and scorelevel != card1.number:
        return 0
    if scoretype < card1.number:
        return 0
    if scoretype < 15 and scoretype <= scorelevel:
        return 0
    if scoretype < 15 and card1.number > scoretype:
        return 0
    if scoretype < 15 and card2.number > scorelevel:
        return 0
    if turn == 1 and suited == 0 and (scoretype == 19 or scoretype == 22):
        return 0
    if turn == 1 and abs(card1.number - card2.number) > 4 and (scoretype == 18 or 22):
        return 0
    if turn == 1 and scoretype == 21 and (card1.number != scorelevel and card2.number != scorelevel):
        return 0
    if turn == 1 and scoretype == 20 and (card1.number != scorelevel and card2.number != scorelevel):
        return 0
    if turn == 1 and scoretype == 16 and (card1.number > scorelevel and card2.number > scorelevel):
        return 0
    if turn == 1 or turn == 2 and (scoretype == 18 or scoretype == 18) and (abs(card1.number - scorelevel) > 4 and abs(card2.number - scorelevel) > 4):
        return 0
    cards = []
    if scoretype < 15:
        cardsneeded = turn + 2
        needhigh = 0
        if card1.number < scoretype:
            needhigh = 1
            if card1.number > scorelevel or card2.number > scorelevel:
                return 0
        needsecond = 0
        if (needhigh and card1.number < scorelevel) or (not needhigh and card2.number < scorelevel):
            needsecond = 1
        
def index_inlist(a, b, c, handtype, handlevel, thelist):
    '''
    counter = 0
    for x in thelist:
        if x[:5] == [a, b, c, handtype, handlevel]:
            break
        counter += 1
    return counter
    '''
    return handlevel - 2 + 13 * (handtype - 2) + 273 * c + 546 * (b-2) + 7098 * (a - 2)
def main():
    thesession = session()
    flop = []
    turn = []
    river = []
    random.seed()
    for a in range(2, 15):
        for b in range(2, 15):
            #if b > a:
                #continue
            for c in range(2):
                #if a == b and c == 1:
                    #continue
                for d in range(2,23):
                    #if d < a:
                        #continue
                    for e in range(2, 15):
                        #if d < 15 and e >= d:
                            #continue
                        flop.append([a, b, c, d, e, 0, 0])
                        turn.append([a, b, c, d, e, 0, 0])
                        river.append([a, b, c, d, e, 0, 0])
    starttime = timeit.default_timer()
    atime = 0
    btime = 0
    ctime = 0
    categories = 0
    for a in range(2, 15):
        for b in range(2, 15):
            if b > a:
                continue
            print(a, b)
            for c in range(2):
                if a == b and c == 1:
                    continue
                categories += 1
                for d in range(150000):
                    #astart = timeit.default_timer()
                    thegame = game(thesession)
                    thegame.player1.cards.append(card(1, a))
                    if c:
                        thegame.player1.cards.append(card(1, b))
                    else:
                        thegame.player1.cards.append(card(2, b))
                    thegame.thedeck.attributes.remove(thegame.player1.cards[0])
                    thegame.thedeck.attributes.remove(thegame.player1.cards[1])
                    #atime += timeit.default_timer() - astart
                    #bstart = timeit.default_timer()
                    thegame.secondplayer.get_card(thegame.thedeck)
                    thegame.secondplayer.get_card(thegame.thedeck)

                    thegame.community.get_card(thegame.thedeck)
                    thegame.community.get_card(thegame.thedeck)
                    thegame.community.get_card(thegame.thedeck)

                    thegame.compare_score(thegame.player1, thegame.secondplayer)

                    afloptype = thegame.player1.handscore.type
                    afloplevel = thegame.player1.handscore.level
                    bfloptype = thegame.secondplayer.handscore.type
                    bfloplevel = thegame.secondplayer.handscore.level

                    thegame.community.get_card(thegame.thedeck)
                    thegame.compare_score(thegame.player1, thegame.secondplayer)

                    aturntype = thegame.player1.handscore.type
                    aturnlevel = thegame.player1.handscore.level
                    bturntype = thegame.secondplayer.handscore.type
                    bturnlevel = thegame.secondplayer.handscore.level

                    thegame.community.get_card(thegame.thedeck)
                    winner = thegame.compare_score(thegame.player1, thegame.secondplayer)
                    
                    arivertype = thegame.player1.handscore.type
                    ariverlevel = thegame.player1.handscore.level
                    brivertype = thegame.secondplayer.handscore.type
                    briverlevel = thegame.secondplayer.handscore.level
                    #btime += timeit.default_timer() - bstart
                    #cstart = timeit.default_timer()
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
                        
                    index = index_inlist(a, b, c, afloptype, afloplevel, flop)
                    flop[index][5] += team1
                    flop[index][6] += 1
                    #print(index, flop[index], [a, b, c, afloptype, afloplevel])
                    index = index_inlist(seconda, secondb, secondc, bfloptype, bfloplevel, flop)
                    flop[index][5] += team2
                    flop[index][6] += 1

                    index = index_inlist(a, b, c, aturntype, aturnlevel, turn)
                    turn[index][5] += team1
                    turn[index][6] += 1

                    index = index_inlist(seconda, secondb, secondc, bturntype, bturnlevel, turn)
                    turn[index][5] += team2
                    turn[index][6] += 1

                    index = index_inlist(a, b, c, arivertype, ariverlevel, river)
                    river[index][5] += team1
                    river[index][6] += 1

                    index = index_inlist(seconda, secondb, secondc, brivertype, briverlevel, river)
                    river[index][5] += team2
                    river[index][6] += 1
                    #ctime += timeit.default_timer() - cstart
    resultFile1 = open("rnnflop.csv", 'w')
    wr1 = csv.writer(resultFile1, dialect='excel')
    resultFile2 = open("rnnturn.csv", 'w')
    wr2 = csv.writer(resultFile2, dialect='excel')
    resultFile3 = open("rnnriver.csv", 'w')
    wr3 = csv.writer(resultFile3, dialect='excel')
    counter = 0
    for x in flop:
        if flop[counter][6] != 0:
            y = flop[counter][:5] + [float(flop[counter][5]) / flop[counter][6]] + [flop[counter][6]]
            wr1.writerows([y])
        if turn[counter][6] != 0:
            y = turn[counter][:5] + [float(turn[counter][5]) / turn[counter][6]] + [turn[counter][6]]
            wr2.writerows([y])
        if river[counter][6] != 0:
            y = river[counter][:5] + [float(river[counter][5]) / river[counter][6]] + [river[counter][6]]
            wr3.writerows([y])
        counter += 1
    endtime = timeit.default_timer() - starttime
    print(river[:50])
    print(len(river))
    print("time", endtime, "sections", categories)

main()
                    