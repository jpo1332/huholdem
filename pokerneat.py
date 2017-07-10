#!/usr/bin/env
from __future__ import print_function
from checkprobs import *
import os
import neat
import visualize
from modelheader import *


def current_state(thegame, thesession, player1, player2):
    prob = check_rnnprob(thegame.round, thegame, thegame.player1)
    if thegame.round == 0:
        rounds = [0, 0, 0, 1]
    elif thegame.round == 1:
        rounds = [0, 0, 1, 0]
    elif thegame.round == 2:
        rounds = [0, 1, 0, 0]
    else:
        rounds = [1, 0, 0, 0]
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

def index_of_max_value(items):
    return max(enumerate(items), key = lambda x: x[1])[0]

def betting_round(thegame, thesession, agent, prints=False):
    while not thegame.check_endround(thesession):
        if thegame.turn:
            if prints:
                print ("Player 1:",)
            if thegame.round == 3:
                _, prob = check_prob(3, thegame, thegame.player1)
                thegame.community.update_score(0)
                difference = thegame.player1.handscore.type - thegame.community.handscore.type
                if thegame.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and thegame.community.handscore.type < 15:
                    difference = thegame.player1.handscore.type - 14

                x = [[prob, difference] + [thesession.secondplayer.previousmove, thesession.bblind]]
                move = nn4sess2.run(predict_op2, feed_dict={X2: x})
            elif thegame.round == 2:
                _, prob = check_prob(2, thegame, thegame.player1)
                thegame.community.update_score(0)
                difference = thegame.player1.handscore.type - thegame.community.handscore.type
                if thegame.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and thegame.community.handscore.type < 15:
                    difference = thegame.player1.handscore.type - 14
                x = [[prob, difference] + [thesession.secondplayer.previousmove, thesession.bblind]]
                move = nn4sess2.run(predict_op2, feed_dict={X2: x})
            elif thegame.round == 1:
                _, prob = check_prob(1, thegame, thegame.player1)
                thegame.community.update_score(0)
                difference = thegame.player1.handscore.type - thegame.community.handscore.type
                if thegame.player1.handscore.type < 15 and difference:
                    difference = .5
                elif difference and thegame.community.handscore.type < 15:
                    difference = thegame.player1.handscore.type - 14

                x = [[prob, difference] + [thesession.secondplayer.previousmove, thesession.bblind]]
                move = nn4sess1.run(predict_op2, feed_dict={X2: x})
            else:
                move, _ = check_prob(thegame.round, thegame, thegame.player1)

            if move == 1:
                thesession.player1.call(thegame, prin=prints)
            elif move == 2:
                bet = thesession.player1.raise1(thegame, 40, 40, prin=prints)
                if bet:
                    thesession.secondplayer.active = True
            else:
                if thesession.player1.potinvest >= thegame.previousbet:
                    thesession.player1.call(thegame, prin=prints)
                else:
                    thesession.player1.fold(thegame, prin=prints)

        else:
            state = current_state(thegame, thesession, thesession.player1, thesession.secondplayer)

            action = agent.activate(state)
            if prints:
                print("Player 2:",)

            move = index_of_max_value(action)
            if move == 1:
                thesession.secondplayer.call(thegame, prin=prints)
            elif move == 2:
                minbet = minimum_bet(thesession.blindamount, thegame.lastbet)
                # print(state[0][0], thesession.secondplayer.money, int(((state[0][0] - .3) ** 2) * (abs(thesession.secondplayer.money - minbet))) * 4)
                bet = thesession.secondplayer.raise1(thegame, int(
                    ((state[0] - .3) ** 2) * (abs(thesession.secondplayer.money - minbet))) * 4, minbet, prin=prints)
                if bet:
                    thesession.player1.active = True
            else:
                if thesession.secondplayer.potinvest >= thegame.previousbet:
                    thesession.secondplayer.call(thegame, prin=prints)
                else:
                    thesession.secondplayer.fold(thegame, prin=prints)
    return

def play_game(agent, runs, prints=False):
    wins = 0
    for i in range(runs):
        thesession = session()
        counter = 0
        handsplayed = 0
        while thesession.player1.money > 0 and thesession.secondplayer.money > 0:
            # print(counter)
            handsplayed += 1
            counter += 1
            thegame = game(thesession)
            thegame.start_newround(thesession)
            thegame.start(thesession, prin=prints)

            betting_round(thegame, thesession, agent, prints=prints)
            if thegame.check_endgame(thesession):
                thegame.end_game(thesession)
                continue
            thegame.flop(prin=prints)
            thegame.start_newround(thesession, prin=prints)
            betting_round(thegame, thesession, agent, prints=prints)
            if thegame.check_endgame(thesession):
                thegame.end_game(thesession)
                continue
            thegame.river(prin=prints)
            thegame.start_newround(thesession, prin=prints)
            betting_round(thegame, thesession, agent, prints=prints)
            if thegame.check_endgame(thesession):
                thegame.end_game(thesession)
                continue
            thegame.river(prin=prints)
            thegame.start_newround(thesession, prin=prints)
            betting_round(thegame, thesession, agent, prints=prints)
            if thegame.check_endgame(thesession):
                thegame.end_game(thesession)
                continue
            if counter > 500:
                print("break")
                break
        if thesession.secondplayer.money > 0:
            wins += 1
    return wins

def eval_genomes(genomes, config):
    counter = 0
    for genome_id, genome in genomes:
        if counter % 10 == 0:
            print(genome_id)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = play_game(net, 50)
        counter += 1

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    #p = neat.Population(config)
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-44')
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 50)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    output = play_game(winner_net, 50)
    print("Winner Net results:", output)
    node_names = {-1:'Prob', -2: 'Blind', -3:'Pot', -4:'Tocall', -5:'River', -6:'Turn', -7:'Flop',
                  -8:'Open', -9:'OppoRaise', -10:'OppoCall', -11:'Oppocheck',
                  0:'Fold', 1:'Call', 2:'Raise'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(eval_genomes, 10)
    stats.save()

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.INI')
    run(config_path)












