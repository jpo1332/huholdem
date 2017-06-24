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
    #print threekind, twopair, onepair, flush, straight
    return returns

def betting_round(game1, session1, inputs, ws, sess, firstround=False):
        y = .99
        game1.turn = session1.bblind
        game1.previousbet = 0
        session1.player1.potinvest = 0
        session1.secondplayer.potinvest = 0
        if firstround:
            if session1.bblind:
                session1.secondplayer.potinvest = - session1.blindamount / 2
            else:
                session1.player1.potinvest = - session1.blindamount / 2
        session1.player1.active = True
        session1.secondplayer.active = True
        turn_function(game1, session1)
        '''    s1 = [return_variables(session1, game1, game1.player1)]
        s1 = np.reshape(s1, (1, 18))
        Qout = tf.matmul(inputs, ws)
        Q1 = sess.run(Qout,feed_dict={inputs1:s1})
        nextQ = tf.placeholder(shape=[3,1],dtype=tf.float32)
        loss = tf.reduce_sum(tf.square(nextQ - Qout))
        trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
        updateModel = trainer.minimize(loss)
        maxQ1 = np.max(Q1)
        print a
        print allQ
        print maxQ1
        targetQ = allQ
        #targetQ[0,a[0]] = 0 + y*maxQ1
        
        _,W1 = sess.run([updateModel,W],feed_dict={inputs1:s1,nextQ:targetQ})'''
        #print "Pot:{0}   Player 1:{1}  Player 2:{2}".format(game1.pot, session1.player1.money, session1.secondplayer.money)
        
        return allQ, a, s

def turn_function(game1, session1):
        if game1.turn == True:
            if session1.secondplayer.status == False:
                return allQ, a, s
            if session1.player1.active == False:
                return allQ, a, s
            #print "Player 1:",
            
            move = a[0]
            if move > 1:
                session1.player1.call(game1)
            if move == 1:
                session1.player1.raise1(game1, minimum_bet(session1.blindamount, session1.blindamount) + session1.bblind, game1.previousbet)
                session1.secondplayer.active = True
            if move < 1:
                session1.player1.fold(game1)
            game1.turn = False
            turn_function(game1, session1)
            return 
        if game1.turn == False:
            if session1.player1.status == False:
                return 
            if session1.secondplayer.active == False:
                return 
            #print "Player 2:",
            move = session1.secondplayer.make_move()
            #print move,
            if move > 5 :
                session1.secondplayer.call(game1)
            if move <= 5 and move >= 2:
                session1.secondplayer.raise1(game1, minimum_bet(session1.blindamount, 0) + session1.blindamount, game1.previousbet)
                session1.player1.active = True
            if move == 1 or move == 0:
                session1.secondplayer.fold(game1)
            game1.turn = True
            turn_function(game1, session1)
            return 
        return

resultFile = open("comturn.csv", 'w')
wr = csv.writer(resultFile, dialect='excel')
a = session()
print "suh"
a = session()
parity = 0
for runs in range(500000):
    b = game(a)

#high, flush ,fdraw, straight, straighdraw, pair, twopair, threekind, fullhouse
    
    b.start(a)
    b.flop()
    b.river()
    variables = return_com(b)
    #b.river()
    winner = b.compare_score(b.player1, b.secondplayer)
    #print b.player1.handscore.type, b.secondplayer.handscore.type
    
    s = abs(b.player1.handscore.type + (b.player1.handscore.level * .07))
 
    #print variables, s
    wr.writerows([variables + [s]])
    s1 = abs(b.secondplayer.handscore.type + (b.secondplayer.handscore.level * .07))
    wr.writerows([variables + [s1]])

    
    if runs % 100000 == 0:
        print "Run:", runs
print parity

#print section

print "success"



