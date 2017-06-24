#!/usr/bin/env python3
import random
import math

import numpy as np
import tensorflow as tf
#import sys
#sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker']
from pokergamehead import *
from loadprobs import *
from checkprobs import *
from modelheader import *
#from modelheader2 import *



def betting_round(game1, session1, rounds, firstround=False, prin=False):
        if session1.player1.allin == True or session1.secondplayer.allin == True:
            return
        game1.turn = session1.bblind
        game1.previousbet = 0
        session1.player1.potinvest = 0
        session1.secondplayer.potinvest = 0
        if firstround:
            game1.previousbet = session1.blindamount
            if session1.bblind:
                session1.player1.potinvest = session1.blindamount / 2
                session1.secondplayer.potinvest =  session1.blindamount
            else:
                session1.secondplayer.potinvest = session1.blindamount / 2
                session1.player1.potinvest = session1.blindamount
        session1.player1.active = True
        session1.secondplayer.active = True
        turn_function(session1, game1, game1.turn, rounds, prin)
        #print "Pot:{0}   Player 1:{1}  Player 2:{2}".format(game1.pot, session1.player1.money, session1.secondplayer.money)
        return

def turn_function(session1, game1, turn, rounds, prints):
        if turn == True:
            if session1.secondplayer.status == False:
                return
            if session1.player1.active == False:
                return
            if session1.player1.allin == True:
                return
            if prints:
                print "Player 1:",
            move = 1
            if rounds == 3:
                inputs = return_variables(session1, game1, game1.secondplayer, rounds)
                _, prob = check_prob(3, game1, game1.player1)
                game1.community.update_score(0)
                difference = game1.player1.handscore.type - game1.community.handscore.type
                if game1.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.player1.handscore.type - 14
                    
                x = [[prob, difference] + [session1.secondplayer.previousmove, session1.bblind]]
                move = nn7sess3.run(predict_op2, feed_dict={X2: x})
                if prints:
                    print move,
            elif rounds == 2:
                inputs = return_variables(session1, game1, game1.secondplayer, rounds)
                _, prob = check_prob(2, game1, game1.player1)
                game1.community.update_score(0)
                difference = game1.player1.handscore.type - game1.community.handscore.type
                if game1.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.player1.handscore.type - 14
                    
                x = [[prob, difference] + [session1.secondplayer.previousmove, session1.bblind]]
                move = nn7sess2.run(predict_op2, feed_dict={X2: x})
                if prints:
                    print move,
            elif rounds == 1:
                inputs = return_variables(session1, game1, game1.secondplayer, rounds)
                _, prob = check_prob(1, game1, game1.player1)
                game1.community.update_score(0)
                difference = game1.player1.handscore.type - game1.community.handscore.type
                if game1.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.player1.handscore.type - 14
                    
                x = [[prob, difference] + [session1.secondplayer.previousmove, session1.bblind]]
                move = nn7sess1.run(predict_op2, feed_dict={X2: x})
                if prints:
                    print move,
            else:
                move, _ = check_prob(rounds, game1, game1.player1)
            global calls
            global raises
            global folds
            
            if move == 2 and game1.previousbet > 240:
                move = 1
            
            if move == 1:
                session1.player1.call(game1, prin=prints)
                calls += 1
            elif move == 2:
                session1.player1.raise1(game1, 40, 40, prin=prints)
                session1.secondplayer.active = True
                raises += 1
            else:
                if session1.player1.potinvest >= game1.previousbet:
                    session1.player1.call(game1, prin=prints)
                    calls += 1
                else:
                    session1.player1.fold(game1, prin=prints)
                    folds += 1
            turn_function(session1, game1, not turn, rounds, prints)
            return
        if turn == False:
            if session1.player1.status == False:
                return
            if session1.secondplayer.active == False:
                return
            if session1.secondplayer.allin == True:
                return
            if prints:
                print "Player 2:",
            move = 0
            #winner = game1.compare_score(game1.secondplayer, game1.player1)
            game1.secondplayer.update_score(game1.community)
            tempscore = game1.secondplayer.handscore.type + (game1.secondplayer.handscore.level * .07)
            if rounds == 3:
                inputs = return_variables(session1, game1, game1.secondplayer, rounds)
                _, prob = check_prob(3, game1, game1.secondplayer)
                game1.community.update_score(0)
                difference = game1.secondplayer.handscore.type - game1.community.handscore.type
                if game1.secondplayer.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.secondplayer.handscore.type - 14
                x = [[prob, difference] + [session1.player1.previousmove, not session1.bblind]]
                move = nn4sess3.run(predict_op2, feed_dict={X2: x})
                if prints:
                    print move,
                '''
                if com < 1.4:
                    move = 1
                if com < - .8:
                    move = 2
                '''
            elif rounds == 2:
                inputs = return_variables(session1, game1, game1.secondplayer, rounds)
                _, prob = check_prob(2, game1, game1.secondplayer)
                game1.community.update_score(0)
                difference = game1.secondplayer.handscore.type - game1.community.handscore.type
                if game1.secondplayer.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.secondplayer.handscore.type - 14
                x = [[prob, difference] + [session1.player1.previousmove, not session1.bblind]]
                move = nn4sess2.run(predict_op2, feed_dict={X2: x})
                if prints:
                    print move,
                '''
                if com < 1.4:
                    move = 1
                if com < - 1.9:
                    move = 2
                '''
            elif rounds == 1:
                inputs = return_variables(session1, game1, game1.secondplayer, rounds)
                _, prob = check_prob(1, game1, game1.secondplayer)
                game1.community.update_score(0)
                difference = game1.secondplayer.handscore.type - game1.community.handscore.type
                if game1.secondplayer.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.secondplayer.handscore.type - 14
                    
                x = [[prob, difference] + [session1.player1.previousmove, not session1.bblind]]
                move = nn4sess1.run(predict_op2, feed_dict={X2: x})
                    
            else:
                move, _ = check_prob(rounds, game1, game1.secondplayer)
            if move == 1:
                session1.secondplayer.call(game1, prin=prints)
            elif move == 2:
                session1.secondplayer.raise1(game1, 40, 40, prin=prints)
                session1.player1.active = True
            else:
                if session1.secondplayer.potinvest >= game1.previousbet:
                    session1.secondplayer.call(game1, prin=prints)
                else:
                    session1.secondplayer.fold(game1, prin=prints)
            turn_function(session1, game1, not turn, rounds, prints)
            return
        return
    
def new_game(session1):
    prints = True
    a = game(session1)
    session1.player1.status = True
    session1.secondplayer.status = True
    session1.player1.allin = False
    session1.secondplayer.allin = False
    a.start(session1, prin=prints)
    betting_round(a, session1, 0, firstround=True, prin=prints)
    global endopen
    global endflop
    global endturn
    global endriver
    if end_round(a, session1):
        endopen += 1
        if session1.player1.status != True:
            return -1
        else:
            return 1
    a.flop(prin=prints)
    betting_round(a, session1, 1, prin=prints)
    if end_round(a, session1):
        endflop += 1
        if session1.player1.status != True:
            return -1
        else:
            return 1
    a.river(prin=prints)
    betting_round(a, session1, 2, prin=prints)
    if end_round(a, session1):
        endturn += 1
        if session1.player1.status != True:
            return -1
        else:
            return 1
    a.river(prin=prints)
    '''
    a.previousbet = 0
    session1.player1.potinvest = 0
    session1.secondplayer.potinvest = 0
    session1.player1.active = True
    session1.secondplayer.active = True
    special_round(session1, a, session1.bblind, 3)
    '''
    endriver += 1
    betting_round(a, session1, 3, prin=prints)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return 1
    winner = a.compare_score(a.player1, a.secondplayer, prin=prints)
    if winner > 0:
        #print "Player 1 wins"
        transfer_money(a, session1.player1, a.pot, False)
        return winner
    if winner< 0:
        #print "Player 2 wins"
        transfer_money(a, session1.secondplayer, a.pot, False)
        return winner
    transfer_money(a, session1.player1, math.floor(a.pot / 2), False)
    transfer_money(a, session1.secondplayer, math.floor(a.pot / 2), False)
    
    #print "Tie game"
    return winner
    
def return_variables(session1, game1, players, rounds):
    _, probability = check_prob(rounds, game1, players)
    return [probability, game1.pot, game1.previousbet]



parity = 0
tothands = 0
win = 0
win2 = 0
endopen = 0
endflop = 0
endturn = 0
endriver = 0
raises = 0
calls = 0
folds = 0

turns = True
runs = 1
for x in range(runs):
    test = 0
    test2 = 0
    a = session(playerchips=1000)
    a.bblind = turns
    while a.player1.money > 0 and a.secondplayer.money > 0:
        tothands += 1
        parity += new_game(a)
        test = a.player1.money
        test2 = a.secondplayer.money
    #print test, test2
    turns = not turns
    if test > 100:
        win += 1
    if test2 > 100:
        win2 += 1
print "Percent Player 1 won:", (win * 100) / runs, (win2 * 100)/ runs
print "Parity, Total hands:", parity, tothands
print "Endopen: {0}, Endflop: {1}, Endturn: {2}, Endriver: {3}".format(endopen, endflop, endturn, endriver)
print "Calls: {0}, Raises: {1}, Folds: {2}".format(calls, raises, folds)

print "Success"

