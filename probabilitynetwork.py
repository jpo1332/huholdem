#!/usr/bin/env
# import numpy as np
import csv
import timeit
import sys
import ast
from pokergamehead import *


def card_onehot(card1):
    facevalue = [0] * 13
    facevalue[card1.number - 2] = 1
    suit = [0] * 4
    suit[card1.cardsuit] = 1
    return facevalue + suit

def card_vector(card1, card2, community, rounds):
    result = card_onehot(card1)
    result += card_onehot(card2)
    if rounds == 0:
        return result + ([0] * 85)
    result += card_onehot(community[0]) + card_onehot(community[1]) + card_onehot(community[2])
    if rounds == 1:
        return result + ([0] * 34)
    result += card_onehot(community[3])
    if rounds == 2:
        return result + ([0] * 17)
    result += card_onehot(community[4])
    return result

def index_inlist(a, b, c, handtype, handlevel, thelist):
    return handlevel - 2 + 13 * (handtype - 2) + 273 * c + 546 * ( b -2) + 7098 * (a - 2)

def index_inlistslow(a, b, c, handtype, handlevel, thelist):
    counter = 0
    for x in thelist:
        if x[:5] == [a, b, c, handtype, handlevel]:
            break
        counter += 1
    return counter

def append_parameters(open1, flop, turn, river, all, card1, card2, community, riverfile, index,  win):
    if riverfile[index][6] > 100000:
        if random.randint(1, 20) % 11 == 0:
            parameters = card_vector(card1, card2, community, 0)
            all.append(parameters + [win])
            open1.append(parameters + [win])

            parameters = card_vector(card1, card2, community, 1)
            all.append(parameters + [win])
            flop.append(parameters + [win])

            parameters = card_vector(card1, card2, community, 2)
            all.append(parameters + [win])
            turn.append(parameters + [win])
            parameters = card_vector(card1, card2, community, 3)
            all.append(parameters + [win])
            river.append(parameters + [win])
    elif riverfile[index][6] > 20000:
        if random.randint(1, 9) %  3 == 0:
            parameters = card_vector(card1, card2, community, 0)
            all.append(parameters + [win])
            open1.append(parameters + [win])

            parameters = card_vector(card1, card2, community, 1)
            all.append(parameters + [win])
            flop.append(parameters + [win])

            parameters = card_vector(card1, card2, community, 2)
            all.append(parameters + [win])
            turn.append(parameters + [win])
            parameters = card_vector(card1, card2, community, 3)
            all.append(parameters + [win])
            river.append(parameters + [win])
    else:
        parameters = card_vector(card1, card2, community, 0)
        all.append(parameters + [win])
        open1.append(parameters + [win])

        parameters = card_vector(card1, card2, community, 1)
        all.append(parameters + [win])
        flop.append(parameters + [win])

        parameters = card_vector(card1, card2, community, 2)
        all.append(parameters + [win])
        turn.append(parameters + [win])
        parameters = card_vector(card1, card2, community, 3)
        all.append(parameters + [win])
        river.append(parameters + [win])
    return

def main():
    thesession = session()
    flop = []
    turn = []
    river = []
    all = []
    open1 = []
    random.seed()

    starttime = timeit.default_timer()

    river_probs = open("probs/rnnriver.csv", 'r')
    riverprobs = river_probs.read()
    riverprobs = riverprobs.split("\n")
    counterx = 0
    for x in riverprobs:
        x = x.split(",")
        z = []
        try:
            for y in x:
                z.append(ast.literal_eval(y))
            riverprobs[counterx] = z
        except:
            pass
        counterx += 1
    river_probs.close()
    riverprobs = riverprobs[:len(riverprobs ) -1]

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
                counter = 0
                for d in range(10):
                    # astart = timeit.default_timer()
                    thegame = game(thesession)
                    suit = random.randint(0, 3)
                    thegame.player1.cards.append(card(suit, a))
                    if c:
                        thegame.player1.cards.append(card(suit, b))
                    else:
                        newsuit = suit
                        while suit == newsuit:
                            newsuit = random.randint(0,3)
                        thegame.player1.cards.append(card(newsuit, b))
                    thegame.thedeck.attributes.remove(thegame.player1.cards[0])
                    thegame.thedeck.attributes.remove(thegame.player1.cards[1])
                    # atime += timeit.default_timer() - astart
                    # bstart = timeit.default_timer()
                    thegame.secondplayer.get_card(thegame.thedeck)
                    thegame.secondplayer.get_card(thegame.thedeck)

                    thegame.community.get_card(thegame.thedeck)
                    thegame.community.get_card(thegame.thedeck)
                    thegame.community.get_card(thegame.thedeck)


                    thegame.community.get_card(thegame.thedeck)

                    thegame.community.get_card(thegame.thedeck)
                    winner = thegame.compare_score(thegame.player1, thegame.secondplayer)

                    arivertype = thegame.player1.handscore.type
                    ariverlevel = thegame.player1.handscore.level
                    brivertype = thegame.secondplayer.handscore.type
                    briverlevel = thegame.secondplayer.handscore.level
                    # btime += timeit.default_timer() - bstart
                    # cstart = timeit.default_timer()
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

                    index = index_inlist(a, b, c, arivertype, ariverlevel, riverprobs)
                    append_parameters(open1, flop, turn, river, all, thegame.player1.cards[0], thegame.player1.cards[1],
                                      thegame.community.cards, riverprobs, index, team1)

                    index = index_inlist(seconda, secondb, secondc, brivertype, briverlevel, river)
                    append_parameters(open1, flop, turn, river, all, thegame.secondplayer.cards[0],
                                      thegame.secondplayer.cards[1], thegame.community.cards, riverprobs, index, team2)

                    # ctime += timeit.default_timer() - cstart
    '''
    resultFile1 = open("rnnflop.csv", 'w')
    wr1 = csv.writer(resultFile1, dialect='excel')
    resultFile2 = open("rnnturn.csv", 'w')
    wr2 = csv.writer(resultFile2, dialect='excel')
    resultFile3 = open("rnnriver.csv", 'w')
    wr3 = csv.writer(resultFile3, dialect='excel')
    if len(sys.argv) > 1:
        counter = 0
        for x in flop1:
            index = index_inlist(flop1[counter][0], flop1[counter][1], flop1[counter][2], flop1[counter][3], flop1[counter][4], flop)
            if flop[index][6] != 0:
                newtotal = flop[index][6] + flop1[counter][6]
                newprop = float(flop1[counter][5]) * (flop1[counter][6] / float(newtotal)) + (flop[index][5] / float
                    (flop[index][6])) * (flop[index][6] / float(newtotal))
                newsum = newtotal * newprop
                flop[index] = flop[index][:5] + [newsum, newtotal]
            else:
                flop[index] = flop[index][:5] + [flop1[counter][5] * flop1[counter][6], flop1[counter][6]]
            counter += 1

        counter = 0
        for x in turn1:
            index = index_inlist(turn1[counter][0], turn1[counter][1], turn1[counter][2], turn1[counter][3], turn1[counter][4], turn)
            if turn[index][6] != 0:
                newtotal = turn[index][6] + turn1[counter][6]
                newprop = float(turn1[counter][5]) * (turn1[counter][6] / float(newtotal)) + (turn[index][5] / float
                    (turn[index][6])) * (turn[index][6] / float(newtotal))
                newsum = newtotal * newprop
                turn[index] = turn[index][:5] + [newsum, newtotal]
            else:
                turn[index] = turn[index][:5] + [turn1[counter][5] * turn1[counter][6], turn1[counter][6]]
            counter += 1

        counter = 0
        for x in river1:
            index = index_inlist(river1[counter][0], river1[counter][1], river1[counter][2], river1[counter][3], river1[counter][4], river)
            if river[index][6] != 0:
                newtotal = river[index][6] + river1[counter][6]
                newprop = float(river1[counter][5]) * (river1[counter][6] / float(newtotal)) + (river[index][5] / float
                    (river[index][6])) * (river[index][6] / float(newtotal))
                newsum = newtotal * newprop
                river[index] = river[index][:5] + [newsum, newtotal]
            else:
                river[index] = river[index][:5] + [river1[counter][5] * river1[counter][6], river1[counter][6]]
            counter += 1
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
    '''
    print "length", len(all), len(all[0])
    print "len open", len(open1), "len river", len(river)
    print "first 5", all[:5]

    endtime = timeit.default_timer() - starttime

    print("time", endtime, "sections", categories)

main()
