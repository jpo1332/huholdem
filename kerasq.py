#!/usr/bin/env
from keras import backend as K
import os

def set_keras_backend(backend):

    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        reload(K)
        assert K.backend() == backend

set_keras_backend("theano")
import numpy as np
import csv
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import optimizers
from random import randint
from random import seed
from pokergamehead import *
from checkprobs import *
from modelheader import *
import copy

class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01
        self.model = self._build_model()
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=optimizers.Adam(lr=self.learning_rate))
        return model
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
              target = reward + self.gamma * \
                       np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    def performance(self):
        temp = list(self.memory)
        if len(temp) < 75:
            temp = temp
        else:
            temp = temp[len(temp)-75:]
        print("length", len(self.memory))
        result = 0
        for x in temp:
            result += x[2]
        return result
def current_state(thegame, thesession, player1, player2):
    prob = check_rnnprob(thegame.round, thegame, thegame.player1)
    if thegame.round == 0:
	rounds = [0,0,0,1]
    elif thegame.round == 1:
	rounds = [ 0,0,1,0]
    elif thegame.round == 2:
	rounds = [0,1,0,0]
    else:
	rounds = [1,0,0,0]
    bb = thesession.bblind
    try:
        pot = float(thegame.pot) / float(player1.money)
        if pot > 1:
            pot = 1.0
    except:
        pot = 1
    try:
        tocall = thegame.lastbet / float(player1.money)
        if tocall > 1:
            tocall = 1
    except:
        tocall = 1
    if player2.previousmove == 2:
        oppomove = [1, 0, 0]
    elif player2.previousmove == 1:
        oppomove = [0, 1, 0]
    else:
        oppomove = [0, 0, 1]

    return [prob, bb, pot, tocall, rounds[0], rounds[1], rounds[2], rounds[3], oppomove[0], oppomove[1], oppomove[2]]

def betting_round(thegame, thesession, dqn, actions, lastmoney, prints=False):
    previousstate = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
    previousstate = np.reshape(previousstate, [1, 11])
    state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
    state = np.reshape(state, [1, 11])
    done = False
    reward = 0
    action = 1
    #lastmoney = thesession.secondplayer.money
    movedyet = 0
    while not thegame.check_endround(thesession):
        if thegame.turn:
	    if prints:
		print "Player 1:",
            move, _ = check_prob(thegame.round, thegame, thegame.player1)
            if move == 1:
                thesession.player1.call(thegame, prin=prints)
            elif move == 2:
                thesession.player1.raise1(thegame, 40, minimum_bet(thesession.blindamount, thegame.lastbet))
            else:
                if thesession.player1.potinvest >= thegame.previousbet:
                    thesession.player1.call(thegame, prin=prints)
                else:
                    thesession.player1.fold(thegame, prin=prints)                       

        else:
	    if prints:
		print "Player 2:",
            state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
            state = np.reshape(state, [1, 11])
            if thegame.round != 0 or movedyet != 0:                       
                #state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
                reward = thesession.secondplayer.money - lastmoney
                #print(reward,thesession.secondplayer.money, lastmoney)
                dqn.remember(previousstate, action, reward, state, done)
            lastmoney = thesession.secondplayer.money
            movedyet = 1
            action = dqn.act(state)
            previousstate = copy.copy(state)
            actions.append(action)
            move = action
            movedyet = 1
            if move == 1:
                thesession.secondplayer.call(thegame, prin=prints)
            elif move == 2:
                minbet =  minimum_bet(thesession.blindamount, thegame.lastbet)
                #print(state[0][0], thesession.secondplayer.money, int(((state[0][0] - .3) ** 2) * (abs(thesession.secondplayer.money - minbet))) * 4)
                thesession.secondplayer.raise1(thegame, int(((state[0][0] - .3) ** 2) * (abs(thesession.secondplayer.money - minbet))) * 4, minbet, prin=prints)
            else:
                if thesession.secondplayer.potinvest >= thegame.previousbet:
                    thesession.secondplayer.call(thegame, prin=prints)
                else:
                    thesession.secondplayer.fold(thegame, prin=prints)
    return previousstate, action, lastmoney
    
def main():
    episodes = 1
    state_size = 11
    dqn = Agent(state_size, 3)
    actions = []
    prints = True
    wins = 0
    handswon = 0
    handsplayed = 0
    for i in range(episodes):
        thesession = session()
        counter = 0
        if i % 25 == 0:
            print(i)
        while thesession.player1.money > 0 and thesession.secondplayer.money > 0:
            #print(counter)
            handsplayed += 1
            if counter > 0:
                if len(dqn.memory) < 100:
                    #print("length", len(dqn.memory))
                    try:
                        dqn.replay(len(dqn.memory)-2)
                    except:
                        print("too small")
                    
                else:
                    dqn.replay(100)
            counter += 1
            thegame = game(thesession)
            if counter % 50 == 0:
                print(thesession.player1.money, thesession.secondplayer.money)
            thegame.start_newround(thesession)
            thegame.start(thesession, prin=prints)
            previousstate = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
            #print(previousstate)
            previousstate = np.reshape(previousstate, [1, state_size])
            state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
            state = np.reshape(state, [1, state_size])
            done = False
            reward = 0
            action = 1
            lastmoney = thesession.secondplayer.money
            movedyet = 0

            previousstate, action, lastmoney = betting_round(thegame, thesession, dqn, actions, lastmoney, prints=prints)
            if thegame.check_endgame(thesession):
                potsize = thegame.pot
                handswon += thegame.end_game(thesession)
                done = True
                if thesession.secondplayer.money > lastmoney:
                    reward = potsize
                else:
                    reward = -potsize
                    
                #print("open", reward, action)
                state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
                state = np.reshape(state, [1, state_size])
                dqn.remember(previousstate, action, reward, state, done)
                continue
            thegame.flop(prin=prints)
            thegame.start_newround(thesession)
            previousstate, action, lastmoney = betting_round(thegame, thesession, dqn, actions, lastmoney, prints=prints)
            if thegame.check_endgame(thesession):
                potsize = thegame.pot
                handswon += thegame.end_game(thesession, prin=prints)
                done = True
                if thesession.secondplayer.money > lastmoney:
                    reward = potsize
                else:
                    reward = -potsize
                #print("flop", reward, action)
                state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
                state = np.reshape(state, [1, state_size])
                dqn.remember(previousstate, action, reward, state, done)
                continue
            thegame.river(prin=prints)
            thegame.start_newround(thesession)
            previousstate, action, lastmoney = betting_round(thegame, thesession, dqn, actions, lastmoney, prints=prints)
            if thegame.check_endgame(thesession):
                potsize = thegame.pot
                handswon += thegame.end_game(thesession, prin=prints)
                done = True
                if thesession.secondplayer.money > lastmoney:
                    reward = potsize
                else:
                    reward = -potsize
                #print("Turn", reward, action)
                state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
                state = np.reshape(state, [1, state_size])
                dqn.remember(previousstate, action, reward, state, done)
            thegame.river(prin=prints)
            thegame.start_newround(thesession)
            previousstate, action, lastmoney = betting_round(thegame, thesession, dqn, actions, lastmoney, prints=prints)
            if thegame.check_endgame(thesession):
                potsize = thegame.pot
                handswon += thegame.end_game(thesession, prin=prints)
                done = True
                if thesession.secondplayer.money > lastmoney:
                    reward = potsize
                else:
                    reward = -potsize
                #print("river", reward, action)
                state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)
                state = np.reshape(state, [1, state_size])
                dqn.remember(previousstate, action, reward, state, done)
                continue
            if counter > 500:
                print("break")
                break
        if thesession.secondplayer.money > 0:
            wins += 1
        if i > 20 and i % 10 == 0:
            print("performance", dqn.performance())
    print("actions:", actions[len(actions)-50:])
    print("performance", dqn.performance())
    print("Games won:", wins, "Games played", episodes, "Handswon:", handswon, "handsplayed", handsplayed)
main()
                    
                        
            




















            
