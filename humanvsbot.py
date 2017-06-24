#!/usr/bin/env python3
import random
import math
import csv
import ast
import numpy as np
import tensorflow as tf
#import sys
import time
#sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker']
from pokergamehead import *
from loadprobs import *
from checkprobs import *
from modelheader import *
    
def betting_round(game1, session1, rounds, firstround=False, prin=False):
        time.sleep(1)
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
                move = nn4sess2.run(predict_op2, feed_dict={X2: x})
                #if prints:
                    #print move,
            if rounds == 2:
                inputs = return_variables(session1, game1, game1.secondplayer, rounds)
                _, prob = check_prob(2, game1, game1.player1)
                game1.community.update_score(0)
                difference = game1.player1.handscore.type - game1.community.handscore.type
                if game1.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.player1.handscore.type - 14
                    
                x = [[prob, difference] + [session1.secondplayer.previousmove, session1.bblind]]
                move = nn4sess2.run(predict_op2, feed_dict={X2: x})
                #if prints:
                    #print move,
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
                move = nn4sess1.run(predict_op2, feed_dict={X2: x})
                move, _ = check_prob(rounds, game1, game1.player1)
                #if prints:
                    #print move,
            else:
                move, _ = check_prob(rounds, game1, game1.player1)
                
            if move == 1:
                session1.player1.call(game1, prin=prints)
            if move == 2:
                session1.player1.raise1(game1, 40, 40, prin=prints)
                session1.secondplayer.active = True
            if move == 0:
                if session1.player1.potinvest >= game1.previousbet:
                    session1.player1.call(game1, prin=prints)
                else:
                    session1.player1.fold(game1, prin=prints)
            time.sleep(.4)
            turn_function(session1, game1, not turn, rounds, prints)
            return
        if turn == False:
            if session1.player1.status == False:
                return
            if session1.secondplayer.active == False:
                return
            if session1.secondplayer.allin == True:
                return


            move = -1
            while (move < 0 or move > 2):
                move = raw_input("Please enter your move:")
                try:
                    move = ast.literal_eval(move)
                except:
                    move = -1
            time.sleep(.5)
            if prints:
                print "Player 2:",
            #winner = game1.compare_score(game1.secondplayer, game1.player1)
            game1.secondplayer.update_score(game1.community)
            tempscore = game1.secondplayer.handscore.type + (game1.secondplayer.handscore.level * .07)
            
            if move == 1:
                session1.secondplayer.call(game1, prin=prints)
            if move == 2:
                session1.secondplayer.raise1(game1, 40, 40, prin=prints)
                session1.player1.active = True
            if move == 0:
                if session1.secondplayer.potinvest >= game1.previousbet:
                    session1.secondplayer.call(game1, prin=prints)
                else:
                    session1.secondplayer.fold(game1, prin=prints)
            turn_function(session1, game1, not turn, rounds, prints)
            return
        return
def special_round(session1, game1, turn, rounds):
        if session1.player1.allin == True or session1.secondplayer.allin == True:
            return
        if turn == True:
            if session1.secondplayer.status == False:
                return
            if session1.player1.active == False:
                return
            if session1.player1.allin == True:
                return
            

            move, _ = check_prob(rounds, game1, game1.player1)
                
            if move == 1:
                session1.player1.call(game1)
            if move == 2:
                session1.player1.raise1(game1, minimum_bet(session1.blindamount,0) + session1.blindamount, game1.previousbet)
                session1.secondplayer.active = True
            if move == 0:
                if session1.player1.potinvest >= game1.previousbet:
                    session1.player1.call(game1)
                else:
                    session1.player1.fold(game1)
            special_round(session1, game1, not turn, rounds)
            return
        if turn == False:
            #print "suh"
            if session1.player1.status == False:
                return
            if session1.secondplayer.active == False:
                return
            if session1.secondplayer.allin == True:
                return
            #print "Player 2:",
            inputs = return_variables(session1, game1, game1.secondplayer, rounds)
            com = tuple(return_com(game1))
            com = comprobs.get(com, 1)
            if type(com) != list:
                com = [com]
            x = [inputs + com]
            move = sess.run(predict_op, feed_dict={X: x})
            if move == 0:
                if session1.secondplayer.potinvest >= game1.previousbet:
                    session1.secondplayer.call(game1)
                else:
                    session1.secondplayer.fold(game1)
            if move == 1:
                session1.secondplayer.call(game1)
            if move == 2:
                session1.secondplayer.raise1(game1, minimum_bet(session1.blindamount, 0) + session1.blindamount, game1.previousbet)
                session1.player1.active = True
            special_round(session1, game1, not turn, rounds)
            return
        return
    
def new_game(session1):
    prints = True
    a = game(session1)
    session1.player1.status = True
    session1.secondplayer.status = True
    session1.player1.allin = False
    session1.secondplayer.allin = False
    a.start_human(session1, prin=prints)
    time.sleep(1)
    betting_round(a, session1, 0, firstround=True, prin=prints)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return 1
    time.sleep(1)
    a.flop(prin=prints)
    betting_round(a, session1, 1, prin=prints)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return 1
    time.sleep(1)
    a.river(prin=prints)
    betting_round(a, session1, 2, prin=prints)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return 1
    time.sleep(1)
    a.river(prin=prints)
    '''
    a.previousbet = 0
    session1.player1.potinvest = 0
    session1.secondplayer.potinvest = 0
    session1.player1.active = True
    session1.secondplayer.active = True
    special_round(session1, a, session1.bblind, 3)
    '''
    betting_round(a, session1, 3, prin=prints)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return 1
    print "Player 1 hand:  ",
    a.player1.print_hand()
    print "\nScores: ",
    winner = a.compare_score(a.player1, a.secondplayer, prin=prints)
    if winner > 0:
        if prints:
            print "Player 1 wins"
        transfer_money(a, session1.player1, a.pot, False)
        return winner
    if winner< 0:
        if prints:
            print "Player 2 wins"
        transfer_money(a, session1.secondplayer, a.pot, False)
        return winner
    transfer_money(a, session1.player1, math.floor(a.pot / 2), False)
    transfer_money(a, session1.secondplayer, math.floor(a.pot / 2), False)
    
    if prints:
        print "Tie game"
    return winner
    
def return_variables(session1, game1, players, rounds):
    _, probability = check_prob(rounds, game1, players)
    return [probability, game1.pot, game1.previousbet]



parity = 0
tothands = 0
win = 0
win2 = 0
runs = 1
print ("\nThis is head to head Texas Holdem. Big blinds is 20 chips. " +
       "You are Player 2. \nEnter a \'0\' to check/fold, a \'1\' to call, "
       "and a \'2\' to raise. \'Cntrl Z\' to Quit.\n")
time.sleep(2)
for x in range(runs):
    test = 0
    test2 = 0
    a = session(playerchips=500)
    while a.player1.money > 0 and a.secondplayer.money > 0:
        tothands += 1
        parity += new_game(a)
        test = a.player1.money
        test2 = a.secondplayer.money
    #print test, test2
    if test > 100:
        win += 1
    if test2 > 100:
        win2 += 1
print "Percent Player 1 won:", (win * 100) / runs, (win2 * 100)/ runs
print "Parity, Total hands:", parity, tothands

print "Success"

