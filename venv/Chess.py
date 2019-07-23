# imports
import itertools
from pygame_functions import *
from Figures import *


# initialization
boardState = {} # pair(x,y) -> Figure object
whiteTurn = True # white always starts

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

# initializes the white (black) pieces if white=True (white=False)
def init_pieces(white):
    if(white):
        # king
        boardState[(4, 0)] = King(4, 0, 5, 10, True, makeSprite("images/w_figures/king.png"))
        # pawns
        for x in range(8):

            boardState[(x, 1)] = Pawn(x, 1, 5, 10, True, makeSprite("images/w_figures/pawn.png"))
        # queen
        boardState[(3, 0)] = Queen(3, 0, 5, 10, True, makeSprite("images/w_figures/queen.png"))
        # rooks
        boardState[(0, 0)] = Rook(0, 0, 5, 10, True, makeSprite("images/w_figures/rook.png"))
        boardState[(7, 0)] = Rook(7, 0, 5, 10, True, makeSprite("images/w_figures/rook.png"))
        # knights
        boardState[(1, 0)] = Knight(1, 0, 5, 10, True, makeSprite("images/w_figures/knight.png"))
        boardState[(6, 0)] = Knight(6, 0, 5, 10, True, makeSprite("images/w_figures/knight.png"))
        # bishops
        boardState[(2, 0)] = Bishop(2, 0, 5, 10, True, makeSprite("images/w_figures/bishop.png"))
        boardState[(5, 0)] = Bishop(5, 0, 5, 10, True, makeSprite("images/w_figures/bishop.png"))
    else:
        # king
        boardState[(4, 7)] = King(4, 7, 5, 10, False, makeSprite("images/b_figures/king.png"))
        # pawns
        for x in range(8):
            boardState[(x, 6)] = Pawn(x, 6, 5, 10, False, makeSprite("images/b_figures/pawn.png"))
        # queen
        boardState[(3, 7)] = Queen(3, 7, 5, 10, False, makeSprite("images/b_figures/queen.png"))
        # rooks
        boardState[(0, 7)] = Rook(0, 7, 5, 10, False, makeSprite("images/b_figures/rook.png"))
        boardState[(7, 7)] = Rook(7, 7, 5, 10, False, makeSprite("images/b_figures/rook.png"))
        # knights
        boardState[(1, 7)] = Knight(1, 7, 5, 10, False, makeSprite("images/b_figures/knight.png"))
        boardState[(6, 7)] = Knight(6, 7, 5, 10, False, makeSprite("images/b_figures/knight.png"))
        # bishops
        boardState[(2, 7)] = Bishop(2, 7, 5, 10, False, makeSprite("images/b_figures/bishop.png"))
        boardState[(5, 7)] = Bishop(5, 7, 5, 10, False, makeSprite("images/b_figures/bishop.png"))

# set up the pieces
init_pieces(True) # white pieces
init_pieces(False) # black pieces

# save the kings separately
whiteKing = boardState.get((4, 0))
blackKing = boardState.get((4, 7))

# new func: transforms mouse position to board coordinates
def pos_2_coords(mX, mY):
    assert mouse_on_board(mX, mY)
    # determine which field was clicked
    x = 0
    while (mX - 50 >= 50):
        mX = mX - 50
        x = x + 1
    y = 7
    while (mY - 50 >= 100):
        mY = mY - 50
        y = y - 1
    # print (str(x)+", "+str(y))
    return (x, y)

# new func: checks if mouse position is on board
def mouse_on_board(mX, mY):
    if mX >= 50 and mX <= 450 and mY >= 100 and mY <= 500:
        # print("Maus im Feld")
        return True
    return False

# switches the playerLabel to white (black) if white = true (white = False)
def switch_player_label(white):
    if white:
        drawRect(0, 550, 500, 50, "dark grey")
        changeLabel(playerLabel, "Spieler 1 (Weiß) ist dran!", "white")
    else:
        changeLabel(playerLabel, "Spieler 2 (Schwarz) ist dran!", "black")

# code that handles the stats when you hover your mouse over figs
def hover():
    mX = mouseX()
    mY = mouseY()
    if mouse_on_board(mX, mY):
        # mouse is translated to field
        mousePair = pos_2_coords(mX, mY)
        # there's a fig on the field
        if mousePair in boardState:
            # print(mousePair)
            # get the figure
            hoverFig = boardState.get(mousePair)
            # set the HP and AP labels
            changeLabel(hpLabel, "HP: " + str(hoverFig.armour) + "/" + str(hoverFig.max_armour))
            showLabel(hpLabel)
            changeLabel(apLabel, "AP: " + str(hoverFig.attack_power))
            showLabel(apLabel)
            # draw the life bar
            drawRect(300, 0, 200, 50, "black")
            drawRect(300, 0, round(hoverFig.armour / hoverFig.max_armour * 200), 50, "green")
        else:
            # don't show hover stuff
            drawRect(300, 0, 200, 50, "dark grey")
            hideLabel(hpLabel)
            hideLabel(apLabel)
    else:
        # don't show hover stuff
        drawRect(300, 0, 200, 50, "dark grey")
        hideLabel(hpLabel)
        hideLabel(apLabel)

# outer loop: player selects piece
while not whiteKing.is_dead() and not blackKing.is_dead():
    # hovering code!
    hover()
    # end of hover code!

    if mousePressed():
        mX = mouseX()
        mY = mouseY()
        if mouse_on_board(mX, mY):
            mousePair = pos_2_coords(mX, mY)
            if mousePair in boardState:
                # figure object, no sprite!
                selected = boardState.get(mousePair)
                # you can only select your own figs
                if selected.white == whiteTurn:
                    moveSprite(selectionSprite, 50 + selected.x * 50, 450 - selected.y * 50)
                    showSprite(selectionSprite)
                    pause(100)

                # inner loop: player selects target field
                while True:
                    # hovering code!
                    hover()
                    # end of hover code!

                    if mousePressed():
                        mX = mouseX()
                        mY = mouseY()
                        if mouse_on_board(mX, mY):
                            secondPair = pos_2_coords(mX, mY)
                            # ONE: Same field clicked again
                            if mousePair == secondPair:
                                # piece was unselected again -> go back to outer loop
                                hideSprite(selectionSprite)
                                pause(100)
                                break

                            # TWO: another fig of the current player's team is clicked
                            if secondPair in boardState:
                                # figure on target field:
                                onTarget = boardState.get(secondPair)
                                if onTarget.white == whiteTurn:
                                    # you clicked another one of your figs -> this one is selected now
                                    selected = onTarget
                                    mousePair = (onTarget.x, onTarget.y)
                                    moveSprite(selectionSprite, 50 + onTarget.x * 50, 450 - onTarget.y * 50)
                                    pause(100)
                                    continue

                            # THREE: the move can be made -> other player's turn
                            if secondPair in selected.possible_coordinates(boardState):
                                # move is allowed
                                if secondPair in boardState:
                                    # enemy on target field:
                                    enemy = boardState.get(secondPair)
                                    enemy.is_hit(selected.attack_power)
                                    if enemy.is_dead():
                                        # kill it
                                        del boardState[(enemy.x, enemy.y)]
                                        # update entry in boardState
                                        del boardState[(selected.x, selected.y)]
                                        boardState[secondPair[0], secondPair[1]] = selected
                                        # move selected fig to new field
                                        selected.move_to(secondPair[0], secondPair[1])
                                else:
                                    # target field is free
                                    # update entry in boardState
                                    del boardState[(selected.x, selected.y)]
                                    boardState[secondPair[0], secondPair[1]] = selected
                                    # move selected fig to new field
                                    selected.move_to(secondPair[0], secondPair[1])
                                # switch player
                                whiteTurn = whiteTurn ^ True
                                switch_player_label(whiteTurn)
                                hideSprite(selectionSprite)
                                pause(100)
                                break

                            # FOUR: illegal move -> do nothing
                    tick(20) # inner loop wait
    tick(20)  # outer loop happens only 20 times/second

# AFTERGAME:
# final prints
if whiteKing.is_dead():
    print("Black wins!")
else:
    print("White wins!")
# close window
endWait()
