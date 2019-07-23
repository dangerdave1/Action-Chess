import abc
import pygame as pg
from pygame_functions import *

class Figure:
    __metaclass__ = abc.ABCMeta

    def __init__(self, x, y, attack_power, armour, white, sprite):
        self.x = x
        self.y = y
        self.attack_power = attack_power
        self.armour = armour
        self.max_armour = armour
        self.white = white
        # handle sprite
        self.sprite = sprite
        moveSprite(self.sprite, 50 + x * 50, 450 - y * 50)
        showSprite(self.sprite)

    def move_to(self, newx, newy):
        self.x = newx
        self.y = newy
        moveSprite(self.sprite, 50 + newx * 50, 450 - newy * 50)

    def is_dead(self):
        if self.armour <= 0:
            hideSprite(self.sprite)
            return True
        return False

    def is_hit(self, attacker_ap):
        self.armour = self.armour - attacker_ap

    @abc.abstractmethod
    def possible_coordinates(self, boardState):
        return


class King(Figure):
    # returns all the figure can move to
    def possible_coordinates(self, boardState):
        x = self.x
        y = self.y
        # put in possible coordinates
        ret = {(x+1,y),(x-1,y),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1),(x,y+1),(x,y-1)}
        # find the ones out of bound
        outBound = set()
        for pair in ret:
            if (pair[0] > 7) or (pair[1] > 7) or (pair[0] < 0) or (pair[1] < 0) or (pair in boardState and boardState[pair].white == self.white):
                outBound.add(pair)
        # kill the ones out of bound
        for pair in outBound:
            ret.remove(pair)
        return ret

class Rook(Figure):
    def possible_coordinates(self, boardState):
        ret = set()
        # direction x1
        for i in range(self.x+1, 8, 1):
            current = (i,self.y)
            if (current not in boardState):
                ret.add(current)
            else: # figure is on this field -> can't move any further
                if boardState[current].white != self.white: # enemy: add this pair
                    ret.add(current)
                    break
                else: # friend: don't add pair
                    break
        # direction x2
        for i in range(self.x-1,-1,-1): # count down from self.x-1 to 0
            current = (i,self.y)
            if (current not in boardState):
                ret.add(current)
            else: # figure is on this field -> can't move any further
                if boardState[current].white != self.white: # enemy: add this pair
                    ret.add(current)
                    break
                else: # friend: don't add pair
                    break
        # direction y1
        for i in range(self.y + 1, 8, 1):
            current = (self.x, i)
            if (current not in boardState):
                ret.add(current)
            else: # figure is on this field -> can't move any further
                if boardState[current].white != self.white: # enemy: add this pair
                    ret.add(current)
                    break
                else: # friend: don't add pair
                    break
        # direction y2
        for i in range(self.y - 1, -1, -1):
            current = (self.x, i)
            if (current not in boardState):
                ret.add(current)
            else: # figure is on this field -> can't move any further
                if boardState[current].white != self.white: # enemy: add this pair
                    ret.add(current)
                    break
                else: # friend: don't add pair
                    break
        # return
        return ret

class Pawn(Figure):
    def possible_coordinates(self, boardState):
        ret = set()
        if self.white:
            # one step forward: if the field is free
            if (self.x, self.y + 1) not in boardState and self.y + 1 < 8:
                ret.add((self.x, self.y + 1))
            # initial two steps forward: if field is free
            if (self.y == 1) and (self.x, self.y + 2) not in boardState:
                ret.add((self.x, self.y + 2))
            # left diagonal hit if black fig
            if (self.x - 1, self.y + 1) in boardState and not boardState[(self.x - 1, self.y + 1)].white:
                ret.add((self.x - 1, self.y + 1))
            # right diagonal hit if black fig
            if (self.x + 1 , self.y + 1) in boardState and not boardState[(self.x + 1 , self.y + 1)].white:
                ret.add((self.x + 1, self.y + 1))
        else: # black
            # one step forward: if the field is free
            if (self.x, self.y - 1) not in boardState and self.y - 1 >= 0:
                ret.add((self.x, self.y - 1))
            # initial two steps forward: if field is free
            if (self.y == 6) and (self.x, self.y - 2) not in boardState:
                ret.add((self.x, self.y - 2))
            # left diagonal hit if white fig
            if (self.x - 1, self.y - 1) in boardState and boardState[(self.x - 1, self.y - 1)].white:
                ret.add((self.x - 1, self.y - 1))
            # right diagonal hit if white fig
            if (self.x + 1, self.y - 1) in boardState and boardState[(self.x + 1, self.y - 1)].white:
                ret.add((self.x + 1, self.y - 1))
        return ret

class Knight(Figure):
    def possible_coordinates(self, boardState):
        x = self.x
        y = self.y
        ret = {(x-1,y+2),(x-2,y+1),(x-2,y-1),(x-1,y-2),(x+1,y-2),(x+2,y-1),(x+2,y+1),(x+1,y+2)}
        # find the ones out of bound
        outBound = set()
        for pair in ret:
            if (pair[0] > 7) or (pair[1] > 7) or (pair[0] < 0) or (pair[1] < 0) or (pair in boardState and boardState[pair].white == self.white):
                outBound.add(pair)
        # kill the ones out of bound
        for pair in outBound:
            ret.remove(pair)
        return ret

class Bishop(Figure):
    def possible_coordinates(self, boardState):
        ret = set()
        # direction top right
        x_i = self.x
        y_i = self.y
        while (x_i + 1 < 8) and (y_i + 1 < 8) :
            x_i = x_i + 1
            y_i = y_i + 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction top left
        x_i = self.x
        y_i = self.y
        while (x_i - 1 >= 0) and (y_i + 1 < 8):
            x_i = x_i - 1
            y_i = y_i + 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction bottom right
        x_i = self.x
        y_i = self.y
        while (x_i + 1 < 8) and (y_i - 1 >= 0):
            x_i = x_i + 1
            y_i = y_i - 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction bottom left
        x_i = self.x
        y_i = self.y
        while (x_i - 1 >= 0) and (y_i - 1 >= 0):
            x_i = x_i - 1
            y_i = y_i - 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        return ret

class Queen(Figure):
    def possible_coordinates(self, boardState):
        ret = set()

        # copy from bishop
        # direction top right
        x_i = self.x
        y_i = self.y
        while (x_i + 1 < 8) and (y_i + 1 < 8):
            x_i = x_i + 1
            y_i = y_i + 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction top left
        x_i = self.x
        y_i = self.y
        while (x_i - 1 >= 0) and (y_i + 1 < 8):
            x_i = x_i - 1
            y_i = y_i + 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction bottom right
        x_i = self.x
        y_i = self.y
        while (x_i + 1 < 8) and (y_i - 1 >= 0):
            x_i = x_i + 1
            y_i = y_i - 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction bottom left
        x_i = self.x
        y_i = self.y
        while (x_i - 1 >= 0) and (y_i - 1 >= 0):
            x_i = x_i - 1
            y_i = y_i - 1
            current = (x_i, y_i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break

        # copy from rook
        # direction x1
        for i in range(self.x + 1, 8, 1):
            current = (i, self.y)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction x2
        for i in range(self.x - 1, -1, -1):  # count down from self.x-1 to 0
            current = (i, self.y)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction y1
        for i in range(self.y + 1, 8, 1):
            current = (self.x, i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # direction y2
        for i in range(self.y - 1, -1, -1):
            current = (self.x, i)
            if (current not in boardState):
                ret.add(current)
            else:  # figure is on this field -> can't move any further
                if boardState[current].white != self.white:  # enemy: add this pair
                    ret.add(current)
                    break
                else:  # friend: don't add pair
                    break
        # return
        return ret

