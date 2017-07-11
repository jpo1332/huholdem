from checkprobs import *
import math
correct = 0
total = 0
thesession = session()
winnerfull = 0
prob1avg = []
prob2avg = []
number = 20000.0
ties = 0
for x in range(int(number)):
    thegame = game(thesession)
    thegame.start(thesession)
    thegame.flop()
    thegame.river()
    thegame.river()

    winner = thegame.compare_score(thegame.secondplayer, thegame.player1)
    if winner == 0:
        ties += 1
    winnerfull += winner
    _, prob1 = check_prob(thegame.round, thegame, thegame.player1)
    _, prob2 = check_prob(thegame.round, thegame, thegame.secondplayer)
    prob1avg.append(prob1)
    prob2avg.append(prob2)
    '''
    if prob1 >= .5:
        prob1 = 1
    else:
        prob1 = 0
    if prob2 >= .5:
        prob2 = 1
    else:
        prob2 = 0
    '''
    prob1 = random.randint(0, 1)
    prob2 = random.randint(0,1)
    if winner == 1 and prob1:
      correct += 1
    if winner == -1 and not prob1:
        correct += 1
    if winner == -1 and prob2:
      correct += 1
    if winner == 1 and not prob2:
        correct += 1
    total += 2
    if x % 1000 == 0:
        print x

print "Correct", correct, "Total", total, "Percent", correct / float(total), "Ties", ties, "Tie%", ties / number
print "Average score", winnerfull / number, "average 1", sum(prob1avg) / number, "avg 2", sum(prob2avg) / number

