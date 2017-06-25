#!/usr/bin/env python3

import pygame
import time
import sys
import copy
#sys.path[0:0] = ['/Users/JackOHara/Desktop/code/Pythonprograms/Poker']
from pokergamehead import *
from loadprobs import *
from checkprobs import *
from modelheader import *

pygame.init()

displayheight = 500
displaywidth = 800
gameDisplay = pygame.display.set_mode((displaywidth, displayheight))
pygame.display.set_caption('Head\'s Up Texas Holdem')


SONG_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_END)

songs = ["card-BMPS/luisichopinscherzo.wav",
         "card-BMPS/LoveDream.wav",
         "card-BMPS/CohensMasterpiece.wav",
         "card-BMPS/Monologue1.wav",
         "card-BMPS/TheWinnerIs.wav"]
current_song = None
#pygame.mixer.music.load("/Users/JackOHara/Desktop/code/Pythonprograms/poker/card-BMPS/dirtytalk.wav")
#pygame.mixer.music.queue("/Users/JackOHara/Desktop/code/Pythonprograms/poker/card-BMPS/LoveDream.wav")

def play_adifferentsong():
    global current_song, songs
    next_song = random.choice(songs)
    while next_song == current_song:
        next_song = random.choice(songs)
    current_song = next_song
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()
    



chipimage = pygame.image.load("/Users/JackOHara/Desktop/code/Pythonprograms/poker/card-BMPS/chip.png")
chipimagesmall = pygame.image.load("/Users/JackOHara/Desktop/code/Pythonprograms/poker/card-BMPS/circle.png")
chipimagesmall = pygame.transform.scale(chipimagesmall, (10, 10))

chipimageside = pygame.image.load("/Users/JackOHara/Desktop/code/Pythonprograms/poker/card-BMPS/chipside.png")
chipimageside = pygame.transform.scale(chipimageside, (15, 3))

pygame.display.set_icon(chipimage)
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
grey = (100, 100, 100)
red = (255, 0, 0)
green = (50, 255, 50)
tableimg = pygame.image.load("/Users/JackOHara/Desktop/code/Pythonprograms/poker/card-BMPS/table.jpeg")
tableimg = pygame.transform.scale(tableimg, (800, 400))
blankcard = pygame.image.load("/Users/JackOHara/Desktop/code/Pythonprograms/poker/card-BMPS/b2fv.bmp")

def card_to_index(card1):
    return (card1.number - 2) + (card1.cardsuit * 13)
def card_string(cards):
    cardlink1 = 0
    if cards.number < 10:
        cardlink1 = '0' + str(cards.number)
    elif cards.number == 14:
        cardlink1 = '01'
    else:
        cardlink1 = str(cards.number)
    if cards.cardsuit == 0:
        cardlink1 = 's' + cardlink1
    elif cards.cardsuit == 1:
        cardlink1 = 'h' + cardlink1
    elif cards.cardsuit == 2:
        cardlink1 = 'd' + cardlink1
    else:
        cardlink1 = 'c' + cardlink1
    cardlink1 = "card-BMPS/" + cardlink1 + ".bmp"
    return cardlink1


allcards = []
for x in range(4):
    for y in range(2,15):
        allcards.append(card(x,y))
cardimages = []
for x in allcards:
    cardimages.append(pygame.image.load(card_string(x)))
cardimages.append(blankcard)                     
def carddisplay(cardimage, x, y):
    gameDisplay.blit(cardimage, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def text_box(msg, x, y):
    smallText = pygame.font.Font("freesansbold.ttf",15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x, y) )
    gameDisplay.blit(textSurf, textRect)
    
def button(msg,x,y,w,h,ic,ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()      
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def slider(minimum, maximum, x, y, circlex, w, h, r, color):
    pygame.draw.rect(gameDisplay, color, (x, y, w, h))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y and click[0] == 1:
        circlex = mouse[0]

    
    pygame.draw.circle(gameDisplay, color, (circlex, y + (h/2)), r)
    betamount = (maximum - minimum) * (circlex - x) / w + minimum
    if circlex - x < 3:
        betamount = minimum
    if circlex - x > w - 3:
        betamount = maximum
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(str(betamount), smallText)
    textRect.center = ( (circlex), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    return circlex, betamount

def card_animation(img, background, endx, y, speed=5):
    if type(img) != list:
        img = [img]
        endx = [endx]
        y = [y]
    if len(img) != len(endx):
        #print "no match", len(endx), len(img)
        return
    steps = []
    startx = []
    for x in endx:
        distance = displaywidth - x
        steps.append(int(math.ceil(distance/speed)))

    longest = max(steps)
    for x in endx:
        startx.append(x + longest * speed)       
    counter = 0
    while counter < longest:
        gameDisplay.blit(background, (0,0))
        counter2 = 0
        for x in img:              
            gameDisplay.blit(cardimages[x], (startx[counter2] - counter * speed, y[counter2]))
            counter2 += 1
        #pygame.time.delay(1)
        
       
        pygame.display.update()
        counter += 1
        clock.tick(60)
        
intro = True
def exit_intro():
    global intro
    intro = False
def game_intro():

    while intro:
        
        
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Texas Holdem", largeText)
        TextRect.center = ((displaywidth/2),(displayheight/2))
        gameDisplay.blit(TextSurf, TextRect)

        startbutton = button("Start", 325, 350, 125, 40, red, grey, exit_intro)
        pygame.display.update()
        clock.tick(15)
        

game_over = False
def exit_gameoverscreen():
    global game_over
    game_over = True
    
def game_overscreen():
    global game_over
    while not game_over:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        msg = ''
        if thesession.player1.money <= 0:
            msg = "You Won!"
        if thesession.secondplayer.money <= 0:
            msg = "You Lost!"
        TextSurf, TextRect = text_objects(msg, largeText)
        TextRect.center = ((displaywidth/2),(displayheight/2))
        gameDisplay.blit(TextSurf, TextRect)

        overbutton = button("Play Again", 325, 350, 125, 40, red, grey, exit_gameoverscreen)
        pygame.display.update()
        clock.tick(15)
    game_over = False
    return
gameexit = False
def use_quitbutton():
    global gameexit
    gameexit = True

def use_raise():
    pygame.time.delay(200)
    check_state(3)
    return
def use_call():
    pygame.time.delay(200)
    check_state(2)
    return
def use_fold():
    pygame.time.delay(200)
    check_state(1)
    return

def check_endround():
    global thesession, thegame
    if thegame.turn == True:
        if thesession.secondplayer.status == False:
            return True
        if thesession.player1.active == False:
            return True
        else:
            turn_function()
        if thesession.player1.allin == True:
            return True
        return False
    if thegame.turn == False:
        if thesession.player1.status == False:
            return True
        if thesession.secondplayer.active == False:
            return True
        if thesession.secondplayer.allin == True:
            return True
    return True


def endgame():
    #print "game ober"
    global thesession, thegame, reveal, newgame
    winner = thegame.compare_score(thegame.player1, thegame.secondplayer)
    if thesession.player1.status == False:
        winner = -1
    elif thesession.secondplayer.status == False:
        winner = 1
    else:
        reveal = True
    if winner > 0:
        transfer_money(thegame, thesession.player1, thegame.pot, False)
    if winner < 0:
        transfer_money(thegame, thesession.secondplayer, thegame.pot, False)
    if winner == 0:
        transfer_money(thegame, thesession.player1, math.floor(thegame.pot / 2), False)
        transfer_money(thegame, thesession.secondplayer, math.floor(thegame.pot), False)
        thesession.player1.money = int(thesession.player1.money)
        thesession.secondplayer.money = int(thesession.secondplayer.money)
    newgame = True
        
def check_endgame():
    global thesession, thegame, reveal
    if thesession.player1.status == False or thesession.secondplayer.status == False:
        return True
    if thegame.round > 2:
        if thesession.player1.active == True or thesession.secondplayer.active == True:
            return False
        reveal = True
        return True
    return False
        
    
def check_state(playermove=False):
    global thesession, thegame, background, animation_on
    turn_function(playermove)
    if thegame.round == 0:
        if check_endgame():
            endgame()
            return
        if check_endround():
            thegame.flop()
            if animation_on:
                img = [card_to_index(thegame.community.cards[0]),
                       card_to_index(thegame.community.cards[1]),
                       card_to_index(thegame.community.cards[2])]
                endxs = [350, 400, 450]
                endys = [165, 165, 165]
                card_animation(img, background, endxs, endys, speed=6)
            
            bettinground()
            return
    elif thegame.round == 1:
        if check_endgame():
            endgame()
            return
        if check_endround():
            thegame.river()
            if animation_on:
                img = card_to_index(thegame.community.cards[3])
                card_animation(img, background, 500, 165, speed=10)
            bettinground()
            return
    elif thegame.round == 2:
        if check_endgame():
            endgame()
            return
        if check_endround():
            thegame.river()
            if animation_on:
                img = card_to_index(thegame.community.cards[4])
                card_animation(img, background, 550, 165, speed=20)
            bettinground()
            return
    else:
        if check_endgame():
            endgame()
        else:
            turn_function(playermove)
        
         
def bettinground(firstround=False, playermove=False):
    global thesession, thegame
    #time.sleep(1)
    if thesession.player1.allin == True or thesession.secondplayer.allin == True:
        return
    thegame.turn = thesession.bblind
    thegame.previousbet = 0
    thesession.player1.potinvest = 0
    thesession.secondplayer.potinvest = 0
    if firstround:
        thegame.previousbet = thesession.blindamount
        thegame.lastbet = thesession.blindamount / 2
        if thesession.bblind:
            thesession.player1.potinvest = thesession.blindamount / 2
            thesession.secondplayer.potinvest =  thesession.blindamount
        else:
            thesession.secondplayer.potinvest = thesession.blindamount / 2
            thesession.player1.potinvest = thesession.blindamount
    thesession.player1.active = True
    thesession.secondplayer.active = True
    turn_function(playermove)

    return


def turn_function(playermove=False):
    global thesession, thegame, opponentmove, betamount
    if thegame.turn == True:
        if thesession.secondplayer.status == False:
            return True
        if thesession.player1.active == False:
            return True
        if thesession.player1.allin == True:
            return True
        move = 0
        if thegame.round == 3:
            inputs = return_variables(thesession, thegame, thegame.secondplayer, thegame.round)
            _, prob = check_prob(3, thegame, thegame.player1)
            thegame.community.update_score(0)
            difference = thegame.player1.handscore.type - thegame.community.handscore.type
            if thegame.player1.handscore.type < 15 and difference:
                difference = .5
            elif difference and thegame.community.handscore.type < 15:
                difference = thegame.player1.handscore.type - 14
                
            x = [[prob, difference] + [thesession.secondplayer.previousmove, thesession.bblind]]
            move = nn4sess2.run(predict_op2, feed_dict={X2: x})
            #if prints:
                #print move,
        elif thegame.round == 2:
            inputs = return_variables(thesession, thegame, thegame.secondplayer, thegame.round)
            _, prob = check_prob(2, thegame, thegame.player1)
            thegame.community.update_score(0)
            difference = thegame.player1.handscore.type - thegame.community.handscore.type
            if thegame.player1.handscore.type < 15 and difference:
                difference = .5
            elif difference and thegame.community.handscore.type < 15:
                difference = thegame.player1.handscore.type - 14
                
            x = [[prob, difference] + [thesession.secondplayer.previousmove, thesession.bblind]]
            move = nn4sess2.run(predict_op2, feed_dict={X2: x})
            #if prints:
                #print move,
        elif thegame.round == 1:
            inputs = return_variables(thesession, thegame, thegame.secondplayer, thegame.round)
            _, prob = check_prob(1, thegame, thegame.player1)
            thegame.community.update_score(0)
            difference = thegame.player1.handscore.type - thegame.community.handscore.type
            if thegame.player1.handscore.type < 15 and difference:
                difference = .5
            elif difference and thegame.community.handscore.type < 15:
                difference = thegame.player1.handscore.type - 14
                
            x = [[prob, difference] + [thesession.secondplayer.previousmove, thesession.bblind]]
            move = nn4sess1.run(predict_op2, feed_dict={X2: x})
            #move, _ = check_prob(thegame.round, thegame, thegame.player1)
            #if prints:
                #print move,
        else:
            move, _ = check_prob(thegame.round, thegame, thegame.player1)
        #move = 1
        if move == 1:
            thesession.player1.call(thegame)
            opponentmove = "Call"
        if move == 2:
            thesession.player1.raise1(thegame, 40, minimum_bet(thesession.blindamount, thegame.lastbet))
            opponentmove = "Raise"
            thesession.secondplayer.active = True
        if move == 0:
            if thegame.lastbet <= 0:
                thesession.player1.call(thegame)
                opponentmove = "Call"
                
            else:
                thesession.player1.fold(thegame)
                opponentmove = "Fold"
                
        return True
    if thegame.turn == False:
        if thesession.player1.status == False:
            return True
        if thesession.secondplayer.active == False:
            return True
        if thesession.secondplayer.allin == True:
            return True

        if playermove != False:

            #winner = thegame.compare_score(thegame.secondplayer, thegame.player1)
            thegame.secondplayer.update_score(thegame.community)
            tempscore = thegame.secondplayer.handscore.type + (thegame.secondplayer.handscore.level * .07)
            
            if playermove == 2:
                thesession.secondplayer.call(thegame)
            if playermove == 3:
                if betamount > thesession.player1.money:
                    betamount = thesession.player1.money
                thesession.secondplayer.raise1(thegame, betamount, minimum_bet(thesession.blindamount, thegame.lastbet))
                thesession.player1.active = True
            if playermove == 1:
                thesession.secondplayer.fold(thegame)
                return
            turn_function()
            return
    return

def return_variables(session1, game1, players, rounds):
    _, probability = check_prob(rounds, game1, players)
    return [probability, game1.pot, game1.previousbet]

newhand = False
def new_hand():
    global newhand, opponentmove
    newhand = True
    opponentmove = ''
def number_toface(number):
    if number < 11:
        return number
    if number == 11:
        return 'Jack'
    if number == 12:
        return 'Queen'
    if number == 13:
        return 'King'
    if number == 14:
        return 'Ace'
    return number
def show_score():
    scores = [thegame.player1.handscore, thegame.secondplayer.handscore]
    counter = 0
    for x in scores:
        msg = ''
        if x.type < 15:
            msg = "{0} High".format(number_toface(x.type))
        elif x.type == 15:
            msg = "Pair of {0}s".format(number_toface(x.level))
        elif x.type == 16:
            msg = "Two Pair: {0}s and {1}s".format(number_toface(x.level), number_toface(x.high))
        elif x.type == 17:
            msg = "Three {0}s".format(number_toface(x.level))
        elif x.type == 18:
            msg = "{0} High Straight".format(number_toface(x.level))
        elif x.type == 19:
            msg = "{0} High Flush".format(number_toface(x.level))
        elif x.type == 20:
            msg = "Full House: {0}s over {1}s".format(number_toface(x.level), number_toface(x.high))
        elif x.type == 21:
            msg = "Four of a Kind: {0}s".format(number_toface(x.level))
        elif x.type == 22:
            msg = "Straight Flush: {0} High!".format(number_toface(x.level))

        if counter == 0:
            text_box(msg, 455, 290)
        else:
            text_box(msg, 455, 315)
        counter += 1

def place_chips():
    mystartx = 120
    mystarty = 320
    counterx = 0
    countery = 0
    total = int(thesession.secondplayer.money / 20)
    for x in range(total):
        gameDisplay.blit(chipimageside, (mystartx + 17*counterx, mystarty - 2*countery))
        countery +=1
        if countery > 9:
            counterx += 1
            countery = 0

    hisstartx = 610
    hisstarty = 130
    counterx = 0
    countery = 0
    total = int(thesession.player1.money / 20)
    for x in range(total):
        gameDisplay.blit(chipimageside, (hisstartx + 17*counterx, hisstarty - 2*countery))
        countery +=1
        if countery > 9:
            counterx += 1
            countery = 0

    potstartx = 280
    potstarty = 200
    counterx = 0
    countery = 0
    total = int(thegame.pot / 20)
    for x in range(total):
        gameDisplay.blit(chipimageside, (potstartx + 17*counterx, potstarty - 2*countery))
        countery +=1
        if countery > 5:
            counterx += 1
            countery = 0

animation_on = True
def toggle_animation():
    global animation_on
    pygame.time.delay(200)
    animation_on = not animation_on
    
music_on = True
def toggle_music():
    global music_on
    pygame.time.delay(200)
    if music_on == True:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    music_on = not music_on

    
thesession = session()
thegame = game(thesession)
betamount = thesession.blindamount
reveal = False
newgame = False
wintimer = False
wintime = pygame.time.get_ticks()
opponentmove = ""
background = copy.copy(gameDisplay)
def main():

    global gameexit
    global thesession
    global thegame
    global reveal
    global newgame
    global wintimer
    global wintime
    global newhand
    global background
    global animation_on
    global music_on
    thegame.start(thesession)
    bettinground(firstround=True)
    play_adifferentsong()
    #thegame.secondplayer.print_hand()
    #thegame.flop()
    circlex = 125
    global betamount
    while not gameexit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameexit = True

            #print(event)
            if event.type == SONG_END:
                play_adifferentsong()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                background = copy.copy(gameDisplay)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if thesession.player1.status == False or thesession.secondplayer.status == False:
                        endgame()
                    if wintime:
                        new_hand()
                    else:
                        time.sleep(.1)
                        check_state()
                        pygame.event.clear
                if event.key == pygame.K_f:
                    use_call()
                if event.key == pygame.K_d:
                    use_raise()
                if event.key == pygame.K_s:
                    use_fold()
                if event.key == pygame.K_a:
                    toggle_animation()
                if event.key == pygame.K_p:
                    toggle_music()

                    
        gameDisplay.fill(white)
        gameDisplay.blit(tableimg, (0, 0))

        

        raisebutton = button("Raise", 75, 425, 125, 40, green, grey, use_raise)
        callbutton = button("Call", 250, 425, 125, 40, green, grey, use_call)
        foldbutton = button("Fold", 425, 425, 125, 40, green, grey, use_fold)
        quitbutton = button("Quit", 675, 430, 75, 25, red, grey, use_quitbutton)
        if animation_on:
            animebutton = button("ON", 740, 18, 50, 25, white, grey, toggle_animation)
        else:
            animebutton = button("OFF", 740, 18, 50, 25, white, grey, toggle_animation)

        if music_on:
            musicbutton = button('M', 735, 380, 50, 25, white, grey, toggle_music)
        else:
            musicbutton = button('O', 735, 380, 50, 25, red, grey, toggle_music)

            
        if not reveal:
            carddisplay(blankcard, 480, 40)
            carddisplay(blankcard, 520, 40)
        else:
            carddisplay(cardimages[card_to_index(thegame.player1.cards[0])], 480, 40)
            carddisplay(cardimages[card_to_index(thegame.player1.cards[1])], 520, 40)

        carddisplay(cardimages[card_to_index(thegame.secondplayer.cards[0])], 200, 274)
        carddisplay(cardimages[card_to_index(thegame.secondplayer.cards[1])], 290, 274)

        if len(thegame.community.cards) > 0:
            xstart = 350
            counter = 0
            for x in thegame.community.cards:
                carddisplay(cardimages[card_to_index(x)], xstart + counter * 50, 165)
                counter += 1
        
        mychips = text_box("Chips: {0}".format(thesession.secondplayer.money), 145, 335)
        hischips = text_box("Chips: {0}".format(thesession.player1.money), 635, 90)
        potdisplay = text_box("Pot: {0}".format(thegame.pot), 35, 15)
        oppmove = text_box("Opponent: " + opponentmove, 200, 200)
        if thesession.bblind == True:
            gameDisplay.blit(chipimagesmall, (200, 262))
        else:
            gameDisplay.blit(chipimagesmall, (480, 137))

        place_chips()
        minimum = minimum_bet(thesession.blindamount, thegame.previousbet)
        maximum = thesession.secondplayer.money
        if minimum > maximum:
            minimum = maximum
        circlex, betamount = slider(minimum, maximum, 75, 404, circlex, 125, 15, 15, green)
        if newgame or wintimer:
            winner = thegame.compare_score(thegame.player1, thegame.secondplayer)
            if thesession.player1.status == False:
                winner = -1
            if thesession.secondplayer.status == False:
                winner = 1
    
            if winner > 0:
                winnerbox = button("You Lose!", 250, 220, 100, 40, green, grey, new_hand)
            if winner < 0:
                winnerbox = button("You Win!", 250, 220, 100, 40, green, grey, new_hand)
            if winner == 0:
                winnerbox = button("Tie Game!", 250, 220, 100, 40, green, grey, new_hand)
            if reveal:
                show_score()
            wintimer = True
            if newgame:
                wintime = pygame.time.get_ticks()
            newgame = False
        pygame.display.update()
        if wintimer and (pygame.time.get_ticks() - wintime > 10000 or newhand == True):
            if thesession.player1.money <=0 or thesession.secondplayer.money <= 0:
                game_overscreen()
                thesession = session()
            thegame = game(thesession)
            thegame.start(thesession)
            thesession.player1.status = True
            thesession.secondplayer.status = True
            thesession.player1.allin = False
            thesession.secondplayer.allin = False
            bettinground(firstround=True)
            wintimer = False
            newhand = False
            background = copy.copy(gameDisplay)
            if animation_on:
                if reveal:
                    imgs = [52, 52,
                        card_to_index(thegame.secondplayer.cards[0]),
                        card_to_index(thegame.secondplayer.cards[1])]
                    endxs = [480, 520, 200, 290]
                    endys = [40, 40, 274, 274]
                else:
                    imgs = [card_to_index(thegame.secondplayer.cards[0]),
                        card_to_index(thegame.secondplayer.cards[1])]
                    endxs = [200, 290]
                    endys = [274, 274]
                card_animation(imgs, background, endxs, endys, speed=6)
            reveal = False
        clock.tick(60)


game_intro()       
main()
pygame.quit()
quit()
