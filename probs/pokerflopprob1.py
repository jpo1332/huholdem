#!/usr/bin/env
import numpy as np
import csv
import tensorflow as tf
from random import randint
from random import seed
import random
import math

class deck:
    def __init__(self):
        self.attributes = []
        for x in range(4):
            for y in range(2,15):
                self.attributes.append(card(x,y))
        random.shuffle(self.attributes)
        #create 52 cards and then shuffle them
    def deal_card(self, index=0):
        newcard = self.attributes[index]
        del self.attributes[index]
        return newcard

class card:
    def __init__(self, suit, value):
        self.attributes = [suit, value]

    def print_card(self):
        tempnumber = self.attributes[1]
        if self.attributes[1] > 10:
            if self.attributes[1] == 11:
                tempnumber = 'J'
            if self.attributes[1] == 12:
                tempnumber = 'Q'
            if self.attributes[1] == 13:
                tempnumber = 'K'
            if self.attributes[1] == 14:
                tempnumber = 'A'
        if self.attributes[0] == 1:
            print tempnumber, u'\u2660',
        if self.attributes[0] == 2:
            print tempnumber, u'\u2665',
        if self.attributes[0] == 3:
            print tempnumber, u'\u2666',
        if self.attributes[0] == 4:
            print tempnumber, u'\u2663',
        #format for printing suits and royals
        return
    
class hand:
    def __init__(self):
         self.cards = []
         self.handscore = score()
         
    def get_card(self, deck, index=0):
        self.cards.append(deck.deal_card(index))
    def print_hand(self):
        for x in self.cards:
            x.print_card()
    def update_score(self, community):
        newhand = hand()
        newhand.cards = self.cards + community.cards
        suit = []
        num = []
        for x in newhand.cards:
            suit.append(x.attributes[0])
            num.append(x.attributes[1])
        #print num, suit
        #newhand.print_hand()
        flush, flushnumbers = check_flush(suit, num)
        straight = check_straight(num)
        fourkind= check_4kind(num)
        threekind, fulllow = check_full(num)
        twopair, pair = check_pairs(num)

        if straight > 0 and flush > 0:
            #not 100% perfect, should work almost always
            if flushnumbers[0] == straight:
                self.handscore.type = 22
                self.handscore.level = straight
                self.handscore.high = 0
                self.handscore.reserve = 0
                self.handscore.last = 0
                return
            flushnumbers2 = flushnumbers[:5]
            if sum(flushnumbers2)/5 == flushnumbers[2]:
                self.handscore.type = 22
                self.handscore.level = flushnumbers[0]
                self.handscore.high = 0
                self.handscore.reserve = 0
                self.handscore.last = 0
                return
               
        if fourkind > 0:
            self.handscore.type = 21
            self.handscore.level = fourkind
            templist = []
            for y in num:
                if y != fourkind:
                    templist.append(y)
            self.handscore.high = templist[0]
            return
        if threekind > 0 and fulllow > 0:
            self.handscore.type = 20
            self.handscore.level = threekind
            self.handscore.high = fulllow
            self.handscore.reserve = 0
            self.handscore.last = 0
            return
        if flush > 0:
            self.handscore.type = 19
            self.handscore.level = flushnumbers[0]
            self.handscore.high = flushnumbers[1]
            self.handscore.reserve = flushnumbers[2]
            self.handscore.last = flushnumbers[3]
            return

        num.sort(reverse=True)
        if straight > 0:
            self.handscore.type = 18
            self.handscore.level = straight
            self.handscore.high = 0
            self.handscore.reserve = 0
            self.handscore.last = 0
            return
        if threekind >0:
            self.handscore.type = 17
            self.handscore.level = threekind

            templist = []
            for y in num:
                if y != threekind:
                    templist.append(y)

            self.handscore.high = templist[0]
            self.handscore.reserve = templist[1]
            self.handscore.last = 0
            return
        if twopair > 0:
            self.handscore.type = 16
            self.handscore.level = twopair
            self.handscore.high = pair

            templist = []
            for y in num:
                if y != twopair and y != pair:
                    templist.append(y)

            self.handscore.reserve = templist[0]
            self.handscore.last = 0
            return
        if pair > 0:
            self.handscore.type = 15
            self.handscore.level = pair

            templist = []
            for y in num:
                if y != pair:
                    templist.append(y)

            self.handscore.high = templist[0]
            self.handscore.reserve = templist[1]
            self.handscore.last = templist[2]
            return
        self.handscore.type = num[0]
        self.handscore.level = num[1]
        self.handscore.high = num[2]
        self.handscore.reserve = num[3]
        self.handscore.last = num[4]
        return


    
def check_pairs(num):
    num.sort(reverse=True)
    for x in num:
        if num.count(x) == 2:
            templist = []
            for y in num:
                if y != x:
                    templist.append(y)
            for y in templist:
                if templist.count(y) == 2:
                    return x, y
            return False, x
    return False, False

def check_4kind(num):
    for x in num:
        if num.count(x) == 4:
            #print "found 4kind"
            return x
            
    return False

def check_full(num):
    num.sort(reverse=True)
    for x in num:
        if num.count(x) == 3:
            templist = []
            for y in num:
                if y != x:
                    templist.append(y)
            for y in templist:
                if templist.count(y) == 2:
                    #print "full boat"
                    return x, y
            #print "threekind"
            return x, False
    return False, False
                    
    
def check_straight(num):
    num.sort()
    num = list(set(num))
    y = 0
    #Following checks for straight, pain in butt to make; careful
    while y < 2:
        x = 0
        check = 0
        while x < 4:
            #print num[len(num) - 1 - x - y]
            if num[len(num) - 1 - x - y] - 1 == num[len(num) - 2 - x - y]:
                check = 1
            else:
                check = 0
                x = 4
            x += 1
        if check == 1:
            #print "got it"
            return num[len(num) - 1 - y]
        y += 1
    return False

def check_flush(suit, num):
    #Check for a flush
    
    for x in suit:
        if suit.count(x) > 4:
            templist = zip(suit, num)
            temp = []
            for y in templist:
                if y[0] == x:
                    temp.append(y[1])
            temp.sort(reverse=True)
            #print "flush yes"
            return (x + 1), temp
    return False, False

class score:
    def __init__(self):
        self.type = 0
        self.level = 0
        self.high = 0
        self.reserve = 0
        self.last = 0
    def print_score(self):
        templist = [self.type, self.level, self.high, self.reserve, self.last]
        print templist,

class game:
    def __init__(self, session1):
        self.turn = session1.bblind
        self.previousbet = session1.blindamount
        self.pot = 0
        self.thedeck = deck()
        self.community = hand()

        session1.bblind = not session1.bblind
        
        self.player1 = hand()
        self.secondplayer = hand()
    def start(self, session1):
        '''
        if self.turn == False:
            transfer_money(self, session1.player1, session1.blindamount, True)
            session1.player1.potinvest += session1.blindamount
            
            transfer_money(self, session1.secondplayer, session1.blindamount / 2, True)
            session1.secondplayer.potinvest += math.floor(session1.blindamount / 2)
            
        if self.turn == True:
            transfer_money(self, session1.player1, session1.blindamount / 2, True)
            session1.player1.potinvest += math.floor(self.previousbet / 2)
            transfer_money(self, session1.secondplayer, session1.blindamount, True)
            session1.secondplayer.potinvest += session1.blindamount
        '''
        
        self.player1.get_card(self.thedeck)
        self.player1.get_card(self.thedeck)
        
        self.secondplayer.get_card(self.thedeck)
        self.secondplayer.get_card(self.thedeck)
        #print "Pot:{0}   Player 1:{1}  Player 2:{2}".format(self.pot, session1.player1.money, session1.secondplayer.money)
        #self.player1.print_hand(),
        #print '  ',
        #self.secondplayer.print_hand()
        #print '\n'
    def flop(self):
        #del self.community.cards[0:3]
        self.community.get_card(self.thedeck)
        self.community.get_card(self.thedeck)
        self.community.get_card(self.thedeck)
        #self.community.print_hand()
        #print "\n"
    def river(self):
        #del self.community.cards[len(self.community.cards)-1]
        self.community.get_card(self.thedeck)
        #self.community.cards[len(self.community.cards)-1].print_card()
        #print "\n"

    def compare_score(self, x, y):
        x.update_score(self.community)
        y.update_score(self.community)
        #x.handscore.print_score()
        #y.handscore.print_score()
        if x.handscore.type > y.handscore.type:
            return 1
        if y.handscore.type > x.handscore.type:
            return -1
        if x.handscore.level > y.handscore.level:
            return 1
        if y.handscore.level > x.handscore.level:
            return -1
        if x.handscore.high > y.handscore.high:
            return 1
        if y.handscore.high > x.handscore.high:
            return -1
        if x.handscore.reserve > y.handscore.reserve:
            return 1
        if y.handscore.reserve > x.handscore.reserve:
            return -1
        if x.handscore.last > y.handscore.last:
            return 1
        if y.handscore.last > x.handscore.last:
            return -1
        return 0


def end_round(game1, session1):
        if session1.player1.status != True:
            transfer_money(game1, session1.secondplayer, game1.pot, False)
            session1.bblind = not session1.bblind
            return True
        if session1.secondplayer.status != True:
            transfer_money(game1, session1.player1, game1.pot, False)
            session1.bblind = not session1.bblind
            return True
        return False

def transfer_money(game1, player1, amount, fromorto=True):
    if fromorto == True:
        if player1.money >= amount:
            player1.money -= amount
            game1.pot += amount
            player1.potinvest += amount
            return
        else:
            game1.pot += player1.money
            player1.potinvest += player1.money
            player1.money = 0
    if fromorto == False:
        player1.money += amount
        game1.pot -= amount

class session:
    def __init__(self, blindamount=20, playerchips=400):
        self.bblind = False
        self.blindamount = blindamount
        self.player1 = player(playerchips)
        self.secondplayer = player(playerchips)
    
def minimum_bet(bigblind, previousbet):
    return bigblind + previousbet

class player:
    def __init__(self, chips):
        self.money = chips
        self.potinvest = 0
        self.status = True
        self.active = True
    def raise1(self, game1, bet, minimum):
        if self.money < game1.previousbet:
            self.call(game1)
            return False
        #print "raises",
        if bet >= minimum:
            if self.money > bet:
                transfer_money(game1, self, game1.previousbet - self.potinvest, True)
                transfer_money(game1, self, bet, True)
                game1.previousbet += bet
                game1.turn = not game1.turn
                self.active = False
                #print bet
                return False
            else:
                transfer_money(game1, self, game1.previousbet - self.potinvest, True)
                transfer_money(game1, self, self.money, True)
                game1.previousbet += bet
                game1.turn = not game1.turn
                self.active = False
                #print "All IN!"
                return False
        self.raise1(game1, minimum, minimum)
        return False
    def call(self, game1):
        #print "calls"
        if self.potinvest >= game1.previousbet:
            game1.turn = not game1.turn
            self.active = False
            return False
        if self.potinvest < game1.previousbet:
            if game1.previousbet < self.money:
                transfer_money(game1, self, game1.previousbet - self.potinvest, True)
                game1.turn = not game1.turn
                self.active = False
                return False
            transfer_money(game1, self, self.money, True)
            game1.turn = not game1.turn
            #print "\bALL IN!"
            return False
    def fold(self, game1):
        self.status = False
        self.active = False
        #print "folds"
        return False
    def make_move(self):
        return randint(0, 18)

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

resultFile = open("pokerflop1.csv", 'w')
wr = csv.writer(resultFile, dialect='excel')
a = session()

a = session()
section = []
for x in range(2,23):
    for y in range(2,15):
        section.append([x-2,y-2, 0, 0])
for runs in range(8000000):
    b = game(a)

#high, flush ,fdraw, straight, straighdraw, pair, twopair, threekind, fullhouse
    
    b.start(a)
    b.flop()
    b.player1.update_score(b.community)
    x = b.player1.handscore.type
    y = b.player1.handscore.level
    z = b.player1.handscore.high
    length = 13 * (x-2) + (y-2)
    b.river()
    b.river()
    winner = b.compare_score(b.player1, b.secondplayer)
    if winner < 1:
        winner = 0
    
    section[length][2] = 1 + section[length][2]
    section[length][3] = winner + section[length][3]
    if runs % 100000 == 0:
        print "Run:", runs
for x in section:
    try:
        y = x[:2] + [float(x[3])/x[2]]
    except:
        y = x[:2] + [0]
    wr.writerows([y])


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



