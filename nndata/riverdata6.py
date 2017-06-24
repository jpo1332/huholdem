#!/usr/bin/env python3
import random
import math
import csv
import ast
import copy
import sys
sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker']
from pokergamehead import *
from loadprobs import *
from checkprobs import *
from modelheader import *

'''
nnmodel = sys.argv[1]
nnmodel1 = nnmodel + '1'
nnmodel2 = nnmodel + '2'
nnmodel3 = nnmodel + '3'
'''
def betting_round(game1, session1, rounds, firstround=False):
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
        turn_function(session1, game1, game1.turn, rounds)
        #print "Pot:{0}   Player 1:{1}  Player 2:{2}".format(game1.pot, session1.player1.money, session1.secondplayer.money)
        return

def turn_function(session1, game1, turn, rounds):
        if turn == True:
            if session1.secondplayer.status == False:
                return
            if session1.player1.active == False:
                return
            if session1.player1.allin == True:
                return
            #print "Player 1:",

            if rounds == 2:
                _, prob = check_prob(2, game1, game1.player1)
                game1.community.update_score(0)
                difference = game1.player1.handscore.type - game1.community.handscore.type
                if game1.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.player1.handscore.type - 14
                    
                x = [[prob, difference] + [session1.secondplayer.previousmove, session1.bblind]]
                move = nn4sess2.run(predict_op2, feed_dict={X2: x})
            elif rounds == 1:
                _, prob = check_prob(1, game1, game1.player1)
                game1.community.update_score(0)
                difference = game1.player1.handscore.type - game1.community.handscore.type
                if game1.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.player1.handscore.type - 14
                    
                x = [[prob, difference] + [session1.secondplayer.previousmove, session1.bblind]]
                move = nn4sess1.run(predict_op2, feed_dict={X2: x})
            else:
                move, _ = check_prob(rounds, game1, game1.player1)
            if game1.previousbet >= 40:
                move = 1
            move = 1
            if move == 1:
                session1.player1.call(game1)
            elif move == 2:
                session1.player1.raise1(game1, 40, 40)
                session1.secondplayer.active = True
            else:
                if session1.player1.potinvest >= game1.previousbet:
                    session1.player1.call(game1)
                else:
                    session1.player1.fold(game1)
            turn_function(session1, game1, not turn, rounds)
            return
        if turn == False:
            if session1.player1.status == False:
                return
            if session1.secondplayer.active == False:
                return
            if session1.secondplayer.allin == True:
                return
            #print "Player 2:",
            game1.secondplayer.update_score(game1.community)
            tempscore = game1.secondplayer.handscore.type + (game1.secondplayer.handscore.level * .07)
            if rounds == 3:
                _, prob = check_prob(3, game1, game1.secondplayer)
                game1.community.update_score(0)
                difference = game1.secondplayer.handscore.type - game1.community.handscore.type
                if game1.secondplayer.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.secondplayer.handscore.type - 14
                x = [[prob, difference] + [session1.player1.previousmove, not session1.bblind]]
                move = nn4sess3.run(predict_op2, feed_dict={X2: x})
                '''
                if com < 1.4:
                    move = 1
                if com < - .8:
                    move = 2
                '''
            elif rounds == 2:
                _, prob = check_prob(2, game1, game1.secondplayer)
                game1.community.update_score(0)
                difference = game1.secondplayer.handscore.type - game1.community.handscore.type
                if game1.secondplayer.handscore.type < 15 and difference:
                    difference = .5
                elif difference and game1.community.handscore.type < 15:
                    difference = game1.secondplayer.handscore.type - 14
                x = [[prob, difference] + [session1.player1.previousmove, not session1.bblind]]
                move = nn4sess2.run(predict_op2, feed_dict={X2: x})
                '''
                if com < 1.4:
                    move = 1
                if com < - 1.9:
                    move = 2
                '''
            elif rounds == 1:
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
            ran = random.randint(1,100)
            if game1.previousbet >= 120:
                move = 1
            if move == 1:
                session1.secondplayer.call(game1)
            elif move == 2:
                session1.secondplayer.raise1(game1, 40, 40)
                session1.player1.active = True
            else:
                if session1.secondplayer.potinvest >= game1.previousbet:
                    session1.secondplayer.call(game1)
                else:
                    session1.secondplayer.fold(game1)
            turn_function(session1, game1, not turn, rounds)
            return
        return

def special_round(session1, game1, turn, rounds):
        '''
        if session1.player1.allin == True or session1.secondplayer.allin == True:
            return - 1
        '''
        game1.previousbet = 0
        session1.player1.potinvest = 0
        session1.secondplayer.potinvest = 0
        session1.player1.active = True
        session1.secondplayer.active = True
        if turn == False:
            '''
            if session1.player1.status == False:
                return -1 
            if session1.secondplayer.active == False:
                return -1 
            if session1.secondplayer.allin == True:
                return -1
            '''
            #print "Player 2:",
            #game1.river()
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
            ran = random.randint(1,100)
            if ran % 5 == 0:
                move = 2
            if move == 1:
                session1.secondplayer.call(game1)
            elif move == 2:
                session1.secondplayer.raise1(game1, 40, 40)
                session1.player1.active = True
            else:
                if session1.secondplayer.potinvest >= game1.previousbet:
                    session1.secondplayer.call(game1)
                else:
                    session1.secondplayer.fold(game1)
            turn = not turn         
        if turn == True:
            #print "Player 1:",
            '''
            if session1.secondplayer.status == False:
                return -1 
            if session1.player1.active == False:
                return -1 
            if session1.player1.allin == True:
                return -1
            '''
            winner = game1.compare_score(game1.secondplayer, game1.player1)
            
            optimum = [0, 1, 0]
            if (game1.player1.handscore.level + (game1.player1.handscore.type * .07))- (
                game1.secondplayer.handscore.level + (game1.secondplayer.handscore.type *.07)) >= .8:
                optimum = [0, 0, 1]
            if (game1.player1.handscore.level + (game1.player1.handscore.type * .07))- (
                game1.secondplayer.handscore.level + (game1.secondplayer.handscore.type *.07)) <= -2.5:
                optimum = [1, 0, 0]
            return optimum

def new_game(session1):
    a = game(session1)
    session1.player1.status = True
    session1.secondplayer.status = True
    session1.player1.allin = False
    session1.secondplayer.allin = False
    a.start(session1)
    betting_round(a, session1, 0, firstround=True)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return -1
    a.flop()
    betting_round(a, session1, 1)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return -1
    a.river()
    betting_round(a, session1, 2)
    if end_round(a, session1):
        if session1.player1.status != True:
            return -1
        else:
            return -1
    
    a.river()
    com = tuple(return_com(a))
    cominput = comriver.get(com, 1)
    tempscore = a.secondplayer.handscore.type + (a.secondplayer.handscore.level * .07)
    cominput = tempscore - cominput
    if type(cominput) != list:
        cominput = [cominput]
    #inputs = return_variables(session1, a, a.secondplayer, 3)
    optimum = special_round(session1, a, session1.bblind, 3)
    if type(optimum) != list:
        return -1
    _, prob = check_prob(3, a, a.secondplayer)
    high = return_highcard(a.secondplayer, a.community)
    a.community.update_score(0)
    difference = a.player1.handscore.type - a.community.handscore.type
    if a.player1.handscore.type < 15 and difference:
        difference = .5
    elif difference and a.community.handscore.type < 15:
        difference = a.player1.handscore.type - 14


    return [[prob , difference] + [session1.secondplayer.previousmove, session1.bblind] + optimum]
    

    
def return_variables(session1, game1, players, rounds):
    _, probability = check_prob(rounds, game1, players)
    return [probability, game1.pot, game1.previousbet]

tothands = 0

runs = 100000
rivernndata = open("rivernn6data.csv", 'w')
wr = csv.writer(rivernndata, dialect='excel')
turns = True
for x in range(runs):
    test = 0
    test2 = 0
    a = session(playerchips=1000)
    a.bblind = turns
    tothands += 1
    output = new_game(a)
    if output != -1:
        if output[0][2] != -1:
            wr.writerows(output)

    turns = not turns
    if x % 5000 == 0:
        print "Run:", x
        
    
print tothands

print "Success"

