#!/usr/bin/env

import random
import math
import copy


class deck:
    def __init__(self):
        self.attributes = []
        for x in range(4):
            for y in range(2,15):
                self.attributes.append(card(x,y))
        random.shuffle(self.attributes)
        #create 52 cards and then shuffle them
    def deal_card(self):
        newcard = self.attributes[0]
        del self.attributes[0]
        return newcard

class card:
    def __init__(self, suit, value):
        self.cardsuit = suit
        self.number = value

    def print_card(self):
        tempnumber = self.number
        if self.number > 10:
            if self.number == 11:
                tempnumber = 'J'
            if self.number == 12:
                tempnumber = 'Q'
            if self.number == 13:
                tempnumber = 'K'
            if self.number == 14:
                tempnumber = 'A'
        if self.cardsuit == 0:
            print tempnumber, u'\u2660',
        if self.cardsuit == 1:
            print tempnumber, u'\u2665',
        if self.cardsuit == 2:
            print tempnumber, u'\u2666',
        if self.cardsuit == 3:
            print tempnumber, u'\u2663',
        #format for printing suits and royals
        return
    
class hand:
    def __init__(self):
         self.cards = []
         self.handscore = score()
         
    def get_card(self, deck):
        self.cards.append(deck.deal_card())
    def print_hand(self):
        for x in self.cards:
            x.print_card()
    def update_score(self, community):
        newhand = hand()
        if community:
            newhand.cards = self.cards + community.cards
        else:
            newhand.cards = self.cards
        suit = []
        num = []
        for x in newhand.cards:
            suit.append(x.cardsuit)
            num.append(x.number)
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
            try:
                self.handscore.high = templist[0]
            except:
                self.handscore.high = 0
            self.handscore.reserve = 0
            self.handscore.last = 0
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
            try:
                self.handscore.high = templist[0]
                self.handscore.reserve = templist[1]
                self.handscore.last = 0
            except:
                self.handscore.high = 0
                self.handscore.reserve = 0
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
            try:
                self.handscore.reserve = templist[0]
                self.handscore.last = 0
            except:
                self.handscore.reserve = 0
                self.handscore.last = 0
            return
        if pair > 0:
            self.handscore.type = 15
            self.handscore.level = pair

            templist = []
            for y in num:
                if y != pair:
                    templist.append(y)
            try:
                self.handscore.high = templist[0]
                self.handscore.reserve = templist[1]
                self.handscore.last = templist[2]
            except:
                self.handscore.high = 0
                self.handscore.reserve = 0
                self.handscore.last = 0
            return
        self.handscore.type = num[0]
        self.handscore.level = num[1]
        try:
            self.handscore.high = num[2]
            self.handscore.reserve = num[3]
            self.handscore.last = num[4]
        except:
            self.handscore.high = 0
            self.handscore.reserve = 0
            self.handscore.last = 0
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
    '''
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
    '''
    straight = []
    for x in num:
        tempstraight = 0
        for y in range(5):
            if (x+y) in num:
                tempstraight += 1
        if tempstraight >= 5:
            straight.append(x + 4)
    try:
        straight = max(straight)
    except:
        straight = False
    return straight

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
        self.round = 0
        session1.bblind = not session1.bblind
        
        self.player1 = hand()
        self.secondplayer = hand()
    def start(self, session1, prin=False):
        if self.turn == True:
            transfer_money(self, session1.player1, session1.blindamount, True)
            session1.player1.potinvest += session1.blindamount
            
            transfer_money(self, session1.secondplayer, session1.blindamount / 2, True)
            session1.secondplayer.potinvest += math.floor(session1.blindamount / 2)
            
        if self.turn == False:
            transfer_money(self, session1.player1, session1.blindamount / 2, True)
            session1.player1.potinvest += math.floor(self.previousbet / 2)
            transfer_money(self, session1.secondplayer, session1.blindamount, True)
            session1.secondplayer.potinvest += session1.blindamount

        
        self.player1.get_card(self.thedeck)
        self.player1.get_card(self.thedeck)
        
        self.secondplayer.get_card(self.thedeck)
        self.secondplayer.get_card(self.thedeck)
        if prin:
            print "Pot:{0}   Player 1:{1}  Player 2:{2}".format(self.pot, session1.player1.money, session1.secondplayer.money)
            self.player1.print_hand(),
            print '  ',
            self.secondplayer.print_hand()
            print '\n'
    def start_human(self, session1, prin=False):
        if self.turn == True:
            transfer_money(self, session1.player1, session1.blindamount, True)
            session1.player1.potinvest += session1.blindamount
            
            transfer_money(self, session1.secondplayer, session1.blindamount / 2, True)
            session1.secondplayer.potinvest += math.floor(session1.blindamount / 2)
            
        if self.turn == False:
            transfer_money(self, session1.player1, session1.blindamount / 2, True)
            session1.player1.potinvest += math.floor(self.previousbet / 2)
            transfer_money(self, session1.secondplayer, session1.blindamount, True)
            session1.secondplayer.potinvest += session1.blindamount

        
        self.player1.get_card(self.thedeck)
        self.player1.get_card(self.thedeck)
        
        self.secondplayer.get_card(self.thedeck)
        self.secondplayer.get_card(self.thedeck)
        if prin:
            print "Pot:{0}   Player 1:{1}  Player 2:{2}".format(self.pot, session1.player1.money, session1.secondplayer.money)
            #self.player1.print_hand(),
            #print '  ',
            self.secondplayer.print_hand()
            print '\n'
    def flop(self, prin=False):
        self.round += 1
        self.community.get_card(self.thedeck)
        self.community.get_card(self.thedeck)
        self.community.get_card(self.thedeck)
        if prin:
            self.community.print_hand()
            print "\n"
    def river(self, prin=False):
        self.round += 1
        self.community.get_card(self.thedeck)
        if prin:
            self.community.cards[len(self.community.cards)-1].print_card()
            #self.community.print_hand()
            print "\n"

    def compare_score(self, x, y, prin=False):
        x.update_score(self.community)
        y.update_score(self.community)
        if prin:
            x.handscore.print_score()
            y.handscore.print_score()
            print '\n'
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
            return True
        if session1.secondplayer.status != True:
            transfer_money(game1, session1.player1, game1.pot, False)
            return True
        return False

def transfer_money(game1, player1, amount, fromorto):
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
        self.allin = False
        self.previousmove = 0
    def raise1(self, game1, bet, minimum, prin=False):
        if self.money < game1.previousbet - self.potinvest:
            self.call(game1)
            return False
        '''
        maxbet = 0
        if game1.turn == True:
            maxbet = session1.secondplayer.money
        else:
            maxbet = session1.player1.money
        if bet > maxbet:
            bet = maxbet
        '''
        if bet >= minimum:
            self.previousmove = 2
            #print "raises",
            if self.money > bet:
                transfer_money(game1, self, game1.previousbet - self.potinvest, True)
                transfer_money(game1, self, bet, True)
                game1.previousbet += bet
                game1.turn = not game1.turn
                self.active = False
                if prin:
                    print "raises", bet
                return False
            else:
                transfer_money(game1, self, game1.previousbet - self.potinvest, True)
                game1.previousbet += self.money
                transfer_money(game1, self, self.money, True)
                game1.turn = not game1.turn
                self.active = False
                self.allin = True
                if prin:
                    print "raises All IN!"
                return False
        self.raise1(game1, minimum, minimum)
        return False
    def call(self, game1, prin=False):
        #print "calls",
        if self.potinvest >= game1.previousbet:
            game1.turn = not game1.turn
            self.active = False
            self.previousmove = 0
            game1.previousbet = self.potinvest
            if prin:            
                print "checks"
            return False
        self.previousmove = 1
        if game1.previousbet - self.potinvest < self.money:
            if prin:
                print "calls", game1.previousbet - self.potinvest
            transfer_money(game1, self, game1.previousbet - self.potinvest, True)
            game1.turn = not game1.turn
            self.active = False
            return False
        transfer_money(game1, self, self.money, True)
        game1.turn = not game1.turn
        self.active = False
        self.allin = True
        if prin:
            print "calls ALL IN!"
        return False
    def fold(self, game1, prin=False):
        self.status = False
        self.active = False
        if prin:
            print "folds"
        return False


