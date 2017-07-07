#!/usr/bin/env python3
import random
import math
import csv
import ast
import numpy as np
#import tensorflow as tf
import sys
#sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker/Poker2']
from pokergamehead import *
from loadprobs import *

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

    highcard = return_highcard(0, game1.community)
    flush = 0
    for x in suits:
        if suits.count(x) > flush:
            flush = suits.count(x)
    num = list(set(num))
    num.sort()
    straight = [0]
    for x in num:
        tempstraight = 0
        for y in range(5):
            if (x+y) in num:
                tempstraight += 1
        straight.append(tempstraight)
    straight = max(straight)
    
    '''
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
    '''
    returns = [threekind, twopair, onepair, highcard, flush, straight]
    return returns
def check_rnnprob(rounds, game1, player1):
    card1 = max(player1.cards[0].number, player1.cards[1].number)
    card2 = min(player1.cards[0].number, player1.cards[1].number)
    samesuit = 0
    if players.cards[0].cardsuit == players.cards[1].cardsuit:
        samesuit = 1
    if rounds == 0:
        probability = openprobs.get((card1,card2,samesuit), .1)
    else:
        player1.update_score(game1.community)
        handtype = player1.handscore.type
        handlevel = player1.handscore.level
        if rounds == 1:
            probability = rnnflopprobs.get((card1, card2, samesuit, handtype, handlevel), .2)
        elif rounds == 2:
            probability = rnnturnprobs.get((card1, card2, samesuit, handtype, handlevel), .2)
        elif rounds == 3:
            probability = rnnriverprobs.get((card1, card2, samesuit, handtype, handlevel), .2)
    return probability
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
        elif probability >= .6 and game1.previousbet < 80:
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
    return 0, 0
def return_highcard(playerhand, community):
    num = []
    suits = []
    for x in community.cards:
        num.append(x.number)
        suits.append(x.cardsuit)
    if playerhand:
        num.append(playerhand.cards[0].number)
        num.append(playerhand.cards[1].number)
        suits.append(playerhand.cards[0].cardsuit)
        suits.append(playerhand.cards[1].cardsuit)
    check, flush = check_flush(suits, num)
    if check:
        return flush[0]
    straight = check_straight(num)
    if straight:
        return straight
    three, full = check_full(num)
    if three and full:
        return three
    if three:
        templist = []
        for x in num:
            if x != three:
                templist.append(x)
        templist.sort(reverse=True)
        return templist[0]
    twopair, pair = check_pairs(num)
    if twopair and pair:
        templist = []
        for x in num:
            if x != twopair and x != pair:
                templist.append(x)
        templist.sort(reverse=True)
        try:
            return templist[0]
        except:
            return twopair
    if pair:
        templist = []
        for x in num:
            if x != pair:
                templist.append(x)
        templist.sort(reverse=True)
        return templist[0]
    num.sort(reverse=True)
    if playerhand:
        return max([playerhand.cards[0].number, playerhand.cards[1].number])
    return num[0]

    
'''
for x in range(5):
    a = session()
    b = game(a)
    b.start(a, prin=True)
    b.flop(prin=True)
    b.river(prin=True)
    b.river(prin=True)
    print return_highcard(b.player1, b.community)
'''
