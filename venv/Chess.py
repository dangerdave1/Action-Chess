# imports
import itertools
import pygame as pg
from pygame_functions import *
import chess # package from niklasf

# initialization
whiteTurn = True # white always starts
board = chess.Board() # from chess package

# set up the screen with background and two labels
screenSize(500, 600)
setBackgroundImage("images/wood.png")
drawRect(0, 0, 500, 50, "dark grey")
titleLabel = makeLabel("Chess Champions", 30, 10, 10, "brown", "Cooper Black", "dark grey")
showLabel(titleLabel)
drawRect(0, 550, 500, 50, "dark grey")
playerLabel = makeLabel("Spieler 1 (Weiß) ist dran!", 20, 10, 563, "white", "Cooper Black", "dark grey")
showLabel(playerLabel)

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
def moveAndStore(sprite, column, row, white):
    assert column in [0,1,2,3,4,5,6,7] and row in [0,1,2,3,4,5,6,7]
    x = 50 + column*50
    y = 450 - row*50
    moveSprite(sprite, x, y)
    # storing the sprite in correct set
    if (white):
        whiteFigs[sprite] = (column, row)
        # print("white: " + str(len(whiteFigs)))
    else:
        blackFigs[sprite] = (column, row)
        # print("black: " + str(len(blackFigs)))

# initializes the white (black) pieces if white=True (white=False)
def initPieces(white):
    if(white):
        # pawns
        for x in range(8):
            pawnSprite = makeSprite("images/w_figures/pawn.png")
            moveAndStore(pawnSprite, x, 1, True)
            showSprite(pawnSprite)
        # king
        kingSprite = makeSprite("images/w_figures/king.png")
        moveAndStore(kingSprite, 4, 0, True)
        showSprite(kingSprite)
        # queen
        queenSprite = makeSprite("images/w_figures/queen.png")
        moveAndStore(queenSprite, 3, 0, True)
        showSprite(queenSprite)
        # rooks
        for x in range(2):
            rookSprite = makeSprite("images/w_figures/rook.png")
            if (x == 1):
                moveAndStore(rookSprite, 0, 0, True)
            else:
                moveAndStore(rookSprite, 7, 0, True)
            showSprite(rookSprite)
        # knights
        for x in range(2):
            knightSprite = makeSprite("images/w_figures/knight.png")
            if (x == 1):
                moveAndStore(knightSprite, 1, 0, True)
            else:
                moveAndStore(knightSprite, 6, 0, True)
            showSprite(knightSprite)
        # bishops
        for x in range(2):
            bishopSprite = makeSprite("images/w_figures/bishop.png")
            if (x == 1):
                moveAndStore(bishopSprite, 2, 0, True)
            else:
                moveAndStore(bishopSprite, 5, 0, True)
            showSprite(bishopSprite)
    else:
        # pawns
        for x in range(8):
            pawnSprite = makeSprite("images/b_figures/pawn.png")
            moveAndStore(pawnSprite, x, 6, False)
            showSprite(pawnSprite)
        # king
        kingSprite = makeSprite("images/b_figures/king.png")
        moveAndStore(kingSprite, 4, 7, False)
        showSprite(kingSprite)
        # queen
        queenSprite = makeSprite("images/b_figures/queen.png")
        moveAndStore(queenSprite, 3, 7, False)
        showSprite(queenSprite)
        # rooks
        for x in range(2):
            rookSprite = makeSprite("images/b_figures/rook.png")
            if (x == 1):
                moveAndStore(rookSprite, 0, 7, False)
            else:
                moveAndStore(rookSprite, 7, 7, False)
            showSprite(rookSprite)
        # knights
        for x in range(2):
            knightSprite = makeSprite("images/b_figures/knight.png")
            if (x == 1):
                moveAndStore(knightSprite, 1, 7, False)
            else:
                moveAndStore(knightSprite, 6, 7, False)
            showSprite(knightSprite)
        # bishops
        for x in range(2):
            bishopSprite = makeSprite("images/b_figures/bishop.png")
            if (x == 1):
                moveAndStore(bishopSprite, 2, 7, False)
            else:
                moveAndStore(bishopSprite, 5, 7, False)
            showSprite(bishopSprite)

# set up the pieces
whiteFigs = {}
blackFigs = {}
initPieces(True) # white pieces
initPieces(False) # black pieces

# returns sprite if a figure was clicked, otherwise None
def figClicked():
    if(whiteTurn):
        for x in whiteFigs:
            if(spriteClicked(x)):
                return x
    else: # black turn
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


# deletes figure on the field if there is one
def del_fig_on_pos(coordinates):
    if whiteTurn:
        for x in blackFigs:
            if blackFigs.get(x) == coordinates:
                killSprite(x)
                del blackFigs[x]
                print("#blackFigs: " + str(len(blackFigs)))
                break
    else:
        for x in whiteFigs:
            if whiteFigs.get(x) == coordinates:
                killSprite(x)
                del whiteFigs[x]
                print("#whiteFigs: " + str(len(whiteFigs)))
                break


# looks up the (x, y) position of the given sprite and returns it
def getFigurePos(sprite, white):
    if white:
        return whiteFigs.get(sprite)
    else:
        return blackFigs.get(sprite)


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
while True:
    selected = figClicked()
    if selected is not None:
        # piece selected -> selectionSprite and inner loop
        pair = getFigurePos(selected, whiteTurn)
        moveSprite(selectionSprite, 50 + pair[0] * 50 , 450 - pair[1] * 50)
        showSprite(selectionSprite)
        pause(100)
        # inner loop: player selects target field
        while True:
            newPos = boardClicked()
            if newPos is not None:
                # target field selected -> deselect or move
                if newPos[0] == pair[0] and newPos[1] == pair[1]:
                    # piece was unselected again -> go back to outer loop
                    hideSprite(selectionSprite)
                    pause(100)
                    break
                # different position -> move and switch to other player if the move is legal
                move = number_to_letter(pair[0])+str(pair[1]+1)+number_to_letter(newPos[0])+str(newPos[1]+1)
                # move is legal -> do the move in gui and push it to package
                if chess.Move.from_uci(move) in board.legal_moves:
                    # other player on field?
                    del_fig_on_pos(newPos)
                    moveAndStore(selected, newPos[0], newPos[1], whiteTurn)
                    board.push(chess.Move.from_uci(move))
                    whiteTurn = whiteTurn ^ True  # switch player
                    switch_player_label(whiteTurn)
                    hideSprite(selectionSprite)
                    pause(100)
                    break
                else:  # illegal move
                    newPos = None
            tick(20)
    tick(20)  # loop happens only 20 times/second

# necessary at the end
endWait()



