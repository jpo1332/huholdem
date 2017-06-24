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


def card_onehot(card1, number):
    #print card1
    temp = np.zeros(number)
    temp[card1 - 1] = 1
    temp2 = []
    for x in temp:
        temp2.append(x)
    return temp2

def return_variables(session1, game1, player1):
    if len(game1.community.cards) == 0:
        game1.community.cards.append(card(0,0))
        game1.community.cards.append(card(0,0))
        game1.community.cards.append(card(0,0))
    if len(game1.community.cards) == 3:
        game1.community.cards.append(card(0,0))
        game1.community.cards.append(card(0,0))
    if len(game1.community.cards) == 4:
        game1.community.cards.append(card(0,0))
    samesuit = 0
    if player1.cards[0].attributes[0] == player1.cards[1].attributes[0]:
        samesuit = 1
    returns = []
    '''
    returns = (
            card_onehot(player1.cards[0].number, 14) + card_onehot(player1.cards[0].cardsuit, 5)
            + card_onehot(player1.cards[1].number, 14) + card_onehot(player1.cards[1].cardsuit, 5)
            + card_onehot(game1.community.cards[0].number, 14) + card_onehot(game1.community.cards[0].cardsuit, 5)
            + card_onehot(game1.community.cards[1].number, 14) + card_onehot(game1.community.cards[1].cardsuit, 5)
            + card_onehot(game1.community.cards[2].number, 14) + card_onehot(game1.community.cards[2].cardsuit, 5)
            + card_onehot(game1.community.cards[3].number, 14) + card_onehot(game1.community.cards[3].cardsuit, 5)
            + card_onehot(game1.community.cards[4].number, 14) + card_onehot(game1.community.cards[4].cardsuit, 5))
    '''
    returns = [player1.cards[0].attributes[1], player1.cards[1].attributes[1], samesuit]
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

resultFile = open("pokerriver.csv", 'w')
wr = csv.writer(resultFile, dialect='excel')
a = session()

a = session()
section = []
for x in range(2,23):
    for y in range(2,15):
        for z in range(2,15):
            section.append([x-2,y-2, z-2, 0, 0])
parity = 0
for runs in range(15000000):
    b = game(a)

#high, flush ,fdraw, straight, straighdraw, pair, twopair, threekind, fullhouse
    
    b.start(a)
    b.flop()
    b.river()
    b.river()
    winner = b.compare_score(b.player1, b.secondplayer)
    parity += winner
    x = b.player1.handscore.type
    y = b.player1.handscore.level
    z = b.player1.handscore.high
    length = (13 * (x-2) + (y-2)) * 13 + (z-2)
    if winner < 1:
        winner = 0
    
    section[length][3] = 1 + section[length][3]
    section[length][4] = winner + section[length][4]
    if runs % 100000 == 0:
        print "Run:", runs
for x in section:
    try:
        y = x[:3] + [float(x[4])/x[3]]
    except:
        y = x[:3] + [0]
    wr.writerows([y])
print parity

#print section
'''
for i in range(100):
    b = game(a)
    b.start(a)
    b.flop()
    b.river()
    b.river()
    #b.player1.print_hand()
    #b.secondplayer.print_hand()
    #print '\n'
    #b.community.print_hand()
    winner = [b.compare_score(b.player1, b.secondplayer)]
    #winner = card_onehot(b.player1.handscore.type, 22)
    
    
    """
    if winner == 1:
        winner = [0,0,1]
    elif winner == 0:
        winner = [0,1,0]
    else:
        winner = [1,0,0]
        """
    #print '\n',
    #b.player1.handscore.print_score()
    #b.secondplayer.handscore.print_score()
    temp = return_variables(a, b, b.player1)
    data = []
    for x in temp:
        data.append(x)
    data = data + winner
    #print data
    data = [data]
    wr.writerows(data)
    #print winner
'''
print "success"



