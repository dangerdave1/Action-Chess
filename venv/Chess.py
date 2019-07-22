# imports
import itertools
import pygame as pg
from pygame_functions import *
# import chess # package from niklasf
from Figures import *


# fig1 = Figure(3, 3, 5, 10)
# fig1.is_hit(5)
# print (fig1.attack_power)

# DATA STRUCTURES
boardState = {} # pair(x,y) -> Figure object
whiteFigs = {} # sprite -> Figure object
blackFigs = {} # sprite -> Figure object

# kings
whiteKing = King(4, 0, 5, 10, True)
blackKing = King(4, 7, 5, 10, False)

# initialization
whiteTurn = True # white always starts
# board = chess.Board() # from chess package

# set up the screen with background and two labels
screenSize(500, 600)
setBackgroundImage("images/wood.png")
drawRect(0, 0, 500, 50, "dark grey")
titleLabel = makeLabel("Chess Champions", 30, 10, 10, "brown", "Cooper Black", "dark grey")
showLabel(titleLabel)
drawRect(0, 550, 500, 50, "dark grey")
playerLabel = makeLabel("Spieler 1 (Weiß) ist dran!", 20, 10, 563, "white", "Cooper Black", "dark grey")
showLabel(playerLabel)

# HP and AP labels
hpLabel = makeLabel("HP: 5/5", 15, 300, 50, "green", "Cooper Black")
apLabel = makeLabel("AP: 5", 15, 400, 50, "orange", "Cooper Black")


# character labels
startChar = bytes('A', 'utf-8')
for x in range(8):
    s = str(bytes([startChar[0] + x]))
    letterLabel = makeLabel(s[2], 30, 64+x*50, 500, "yellow", "Cooper Black")
    showLabel(letterLabel)

# number labels
for x in range(8):
    numberLabel = makeLabel(str(x+1), 30, 22, 456-x*50, "yellow", "Cooper Black")
    showLabel(numberLabel)

# chessboard and selection sprite
boardSprite = makeSprite("images/chessboard.png")
moveSprite(boardSprite, 50, 100)
showSprite(boardSprite)
selectionSprite = makeSprite("images/selected.png")

# moves the sprite to the specified field and stores it in the correct set
def move_and_store(sprite, column, row, white, object):
    assert column in [0,1,2,3,4,5,6,7] and row in [0,1,2,3,4,5,6,7]
    x = 50 + column*50
    y = 450 - row*50
    moveSprite(sprite, x, y)
    # storing the sprite in correct set
    if (white):
        # fig = King(column, row, 5, 10, True)
        whiteFigs[sprite] = object
        # whiteFigs.add(Figure(column, row, 5, 10, sprite))
        # print("white: " + str(len(whiteFigs)))
    else:
        # fig = King(column, row, 5, 10, False)
        blackFigs[sprite] = object
        # blackFigs.add(Figure(column, row, 5, 10, sprite))
        # print("black: " + str(len(blackFigs)))
    boardState[(column,row)] = object
    # print(len(boardState))

# initializes the white (black) pieces if white=True (white=False)
def init_pieces(white):
    if(white):
        # pawns
        for x in range(8):
            pawnSprite = makeSprite("images/w_figures/pawn.png")
            move_and_store(pawnSprite, x, 1, True, Pawn(x, 1, 5, 10, True))
            showSprite(pawnSprite)
        # king
        kingSprite = makeSprite("images/w_figures/king.png")
        move_and_store(kingSprite, 4, 0, True, whiteKing)
        showSprite(kingSprite)
        # queen
        queenSprite = makeSprite("images/w_figures/queen.png")
        move_and_store(queenSprite, 3, 0, True, Queen(3, 0, 5, 10, True))
        showSprite(queenSprite)
        # rooks
        for x in range(2):
            rookSprite = makeSprite("images/w_figures/rook.png")
            if (x == 1):
                move_and_store(rookSprite, 0, 0, True, Rook(0, 0, 5, 10, True))
            else:
                move_and_store(rookSprite, 7, 0, True, Rook(7, 0, 5, 10, True))
            showSprite(rookSprite)
        # knights
        for x in range(2):
            knightSprite = makeSprite("images/w_figures/knight.png")
            if (x == 1):
                move_and_store(knightSprite, 1, 0, True, Knight(1, 0, 5, 10, True))
            else:
                move_and_store(knightSprite, 6, 0, True, Knight(6, 0, 5, 10, True))
            showSprite(knightSprite)
        # bishops
        for x in range(2):
            bishopSprite = makeSprite("images/w_figures/bishop.png")
            if (x == 1):
                move_and_store(bishopSprite, 2, 0, True, Bishop(2, 0, 5, 10, True))
            else:
                move_and_store(bishopSprite, 5, 0, True, Bishop(5, 0, 5, 10, True))
            showSprite(bishopSprite)
    else:
        # pawns
        for x in range(8):
            pawnSprite = makeSprite("images/b_figures/pawn.png")
            move_and_store(pawnSprite, x, 6, False, Pawn(x, 6, 5, 10, False))
            showSprite(pawnSprite)
        # king
        kingSprite = makeSprite("images/b_figures/king.png")
        move_and_store(kingSprite, 4, 7, False, blackKing)
        showSprite(kingSprite)
        # queen
        queenSprite = makeSprite("images/b_figures/queen.png")
        move_and_store(queenSprite, 3, 7, False, Queen(3, 7, 5, 10, False))
        showSprite(queenSprite)
        # rooks
        for x in range(2):
            rookSprite = makeSprite("images/b_figures/rook.png")
            if (x == 1):
                move_and_store(rookSprite, 0, 7, False, Rook(0, 7, 5, 10, False))
            else:
                move_and_store(rookSprite, 7, 7, False, Rook(7, 7, 5, 10, False))
            showSprite(rookSprite)
        # knights
        for x in range(2):
            knightSprite = makeSprite("images/b_figures/knight.png")
            if (x == 1):
                move_and_store(knightSprite, 1, 7, False, Knight(1, 7, 5, 10, False))
            else:
                move_and_store(knightSprite, 6, 7, False, Knight(6, 7, 5, 10, False))
            showSprite(knightSprite)
        # bishops
        for x in range(2):
            bishopSprite = makeSprite("images/b_figures/bishop.png")
            if (x == 1):
                move_and_store(bishopSprite, 2, 7, False, Bishop(2, 7, 5, 10, False))
            else:
                move_and_store(bishopSprite, 5, 7, False, Bishop(5, 7, 5, 10, False))
            showSprite(bishopSprite)

# set up the pieces
init_pieces(True) # white pieces
init_pieces(False) # black pieces

# returns sprite if a figure was clicked, otherwise None
def fig_clicked():
    # if(whiteTurn):
    for x in whiteFigs:
        if(spriteClicked(x)):
            return x
    # else: # black turn
    for x in blackFigs:
        if(spriteClicked(x)):
            return x
    return None


# returns the coordinates if the board was clicked, otherwise None
def boardClicked():
    if(spriteClicked(boardSprite)):
        # determine which field was clicked
        mX = mouseX()
        mY = mouseY()
        x = 0
        while(mX - 50 >= 50):
            mX = mX - 50
            x = x + 1
        y = 7
        while (mY - 50 >= 100):
            mY = mY - 50
            y = y - 1
        return (x, y)
    return None


# deletes figure on the field if there is one. Returns True if the figure may move to the field
def del_fig_on_pos(coordinates, attack_power):
    if whiteTurn:
        for x in blackFigs:
            fig = blackFigs.get(x)
            if (fig.x, fig.y) == coordinates:
                fig.is_hit(attack_power)
                # print(fig.is_dead)
                if fig.armour <= 0:
                    killSprite(x)
                    del blackFigs[x]
                    print("#blackFigs: " + str(len(blackFigs)))
                    return True # may move cause it's dead
                else:
                    return False
        return True # may move because there was no figure
    else:
        for x in whiteFigs:
            fig = whiteFigs.get(x)
            if (fig.x, fig.y) == coordinates:
                fig.is_hit(attack_power)
                if fig.armour <= 0:
                    killSprite(x)
                    del whiteFigs[x]
                    print("#whiteFigs: " + str(len(whiteFigs)))
                    return True  # may move cause it's dead
                else:
                    return False
        return True


# looks up the (x, y) position of the given sprite and returns it
def get_figure_pos(sprite):
    if sprite in whiteFigs:
        fig = whiteFigs.get(sprite)
    else:
        fig = blackFigs.get(sprite)
    return (fig.x, fig.y)


# get letter of a coordinate for chess package
def number_to_letter(number):
    switcher = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h"
    }
    return switcher.get(number)


# switches the playerLabel to white (black) if white = true (white = False)
def switch_player_label(white):
    if white:
        drawRect(0, 550, 500, 50, "dark grey")
        changeLabel(playerLabel, "Spieler 1 (Weiß) ist dran!", "white")
    else:
        changeLabel(playerLabel, "Spieler 2 (Schwarz) ist dran!", "black")


# outer loop: player selects piece
while not whiteKing.is_dead() and not blackKing.is_dead():
    selected = fig_clicked()
    if selected is not None:
        # piece selected -> selectionSprite and inner loop
        pair = get_figure_pos(selected)
        moveSprite(selectionSprite, 50 + pair[0] * 50 , 450 - pair[1] * 50)
        showSprite(selectionSprite)

        drawRect(300, 0, 200, 50, "black")
        if selected in whiteFigs:
            fig = whiteFigs[selected]
        else:
            fig = blackFigs[selected]
        # print(fig.armour)
        drawRect(300, 0, round(fig.armour/fig.max_armour*200), 50, "green")
        # HP and AP labels
        changeLabel(hpLabel, "HP: "+str(fig.armour)+"/"+str(fig.max_armour))
        showLabel(hpLabel)
        changeLabel(apLabel, "AP: "+str(fig.attack_power))
        showLabel(apLabel)

        # was a figure of your own colour selected?
        own_colour = (selected in whiteFigs) == whiteTurn
        print(own_colour)
        pause(100)
        # inner loop: player selects target field
        while True:
            newPos = boardClicked()
            figSprite = fig_clicked()
            if (newPos is not None):
                # target field selected -> deselect or move
                if newPos[0] == pair[0] and newPos[1] == pair[1]:
                    # piece was unselected again -> go back to outer loop
                    hideSprite(selectionSprite)
                    drawRect(300, 0, 200, 50, "dark grey")
                    hideLabel(hpLabel)
                    hideLabel(apLabel)
                    pause(100)
                    break
                # a figure was clicked: determine colour
                if figSprite is not None:
                    figWhite = False
                    if figSprite in whiteFigs:
                        figWhite = True
                    # clicked is same color as selected
                    if boardState[pair].white == figWhite:
                        selected = figSprite
                        pair = get_figure_pos(selected)
                        moveSprite(selectionSprite, 50 + pair[0] * 50, 450 - pair[1] * 50)
                        # hp/ap
                        drawRect(300, 0, 200, 50, "black")
                        drawRect(300, 0, round(boardState[pair].armour / boardState[pair].max_armour * 200), 50, "green")
                        changeLabel(hpLabel, "HP: " + str(boardState[pair].armour) + "/" + str(boardState[pair].max_armour))
                        showLabel(hpLabel)
                        changeLabel(apLabel, "AP: " + str(boardState[pair].attack_power))
                        showLabel(apLabel)
                        pause(100)
                        continue
                # figure of the other colour tried to make a move -> NO
                if not own_colour:
                    print("Diese Figur ist nicht dran")
                    hideSprite(selectionSprite)
                    pause(100)
                    break
                # different position -> move and switch to other player if the move is legal
                # move = number_to_letter(pair[0])+str(pair[1]+1)+number_to_letter(newPos[0])+str(newPos[1]+1)
                # get the corresponding figure object
                if (whiteTurn):
                    fig = whiteFigs[selected]
                else:
                    fig = blackFigs[selected]
                # move is legal -> do the move in gui and push it to package
                if newPos in fig.possible_coordinates(boardState):
                    drawRect(300, 0, 200, 50, "dark grey")
                    hideLabel(hpLabel)
                    hideLabel(apLabel)
                    # other player on field?
                    if del_fig_on_pos(newPos, fig.attack_power):
                        print("Let's move")
                        # the figure may move to the new field
                        # move_and_store(selected, newPos[0], newPos[1], whiteTurn)
                        moveSprite(selected, 50 + newPos[0]*50, 450 - newPos[1]*50)
                        fig.x = newPos[0]
                        fig.y = newPos[1]
                        # change in boardState
                        print(len(boardState))
                        del boardState[pair]
                        print(len(boardState))
                        boardState[newPos] = fig
                        print(len(boardState))
                    whiteTurn = whiteTurn ^ True  # switch player
                    switch_player_label(whiteTurn)
                    hideSprite(selectionSprite)
                    pause(100)
                    break
                else:  # illegal move
                    newPos = None
            tick(20)
    tick(20)  # loop happens only 20 times/second

print ("End of game!")
# TODO find out who's the winner

# necessary at the end
endWait()



