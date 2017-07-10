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
        if random.randint(1, 12) == 1:
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
        if random.randint(1, 6) == 1:
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
    elif riverfile[index][6] > 3000:
        if random.randint(1, 2) == 1:
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
                for d in range(1000):
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
    resultFile4 = open("traindata/nnalltrain.csv", 'w')
    wr4 = csv.writer(resultFile4, dialect='excel')
    resultFile6 = open("traindata/nnallvalid.csv", 'w')
    wr6 = csv.writer(resultFile6, dialect='excel')
    resultFile7 = open("traindata/nnalltest.csv", 'w')
    wr7 = csv.writer(resultFile7, dialect='excel')
    resultFile1 = open("traindata/nnflop.csv", 'w')
    wr1 = csv.writer(resultFile1, dialect='excel')
    resultFile2 = open("traindata/nnturn.csv", 'w')
    wr2 = csv.writer(resultFile2, dialect='excel')
    resultFile3 = open("traindata/nnriver.csv", 'w')
    wr3 = csv.writer(resultFile3, dialect='excel')
    resultFile5 = open("traindata/nnopen.csv", 'w')
    wr5 = csv.writer(resultFile5, dialect='excel')

    counter = 0
    for x in flop:
        y = flop[counter]
        wr1.writerows([y])

        y = open1[counter]
        wr5.writerows([y])

        y = turn[counter]
        wr2.writerows([y])

        y = river[counter]
        wr4.writerows([y])
        counter += 1

    for x in all:
        test = random.randint(1, 10)
        if test == 1 or test == 2:
            wr6.writerows([x])
        elif test == 3:
            wr7.writerows([x])
        else:
            wr4.writerows([x])
    print "length", len(all), len(all[0])
    print "len open", len(open1), "len river", len(river)
    print "first 5", all[:5]

    endtime = timeit.default_timer() - starttime

    print("time", endtime, "sections", categories)

main()
