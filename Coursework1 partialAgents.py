# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# Global constants
EMPTY = 0
FULL = 1

class PartialAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        """
        Initiate the fields of partial agent
        """
        print "Starting up!"
        name = "Pacman"
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False
        self.hungry = True
        self.survival = False
        self.food_list = []

    # This is what gets run in between multiple games
    def final(self, state):
        """
        Reset the field when run games in a row
        """
        print "Let's play another round!"
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False
        self.hungry = True
        self.survival = False
        self.food_list = []
        
    def map_size(self, state):
        """
        Calculate the height and width of map
        """
        # use corner function to find the size of the map
        corner_list = api.corners(state)
        corner_x_list = []
        corner_y_list = []
        for corner in corner_list:
            corner_x_list.append(corner[0])
            corner_y_list.append(corner[1])
        self.grid_width = max(corner_x_list)
        self.grid_height = max(corner_y_list)
               
    def compute_distance_field(self, state):
        """
        Computes and returns a 2D distance field
        Distance at foods or ghosts is zero
        """        
        # visited is used to check whether a cell has been searched as a neighbor
        visited = [[EMPTY for y in range(self.grid_height)] for x in range(self.grid_width)]
        distance_field = [[self.grid_height * self.grid_width for y in range(self.grid_height)] for x in range(self.grid_width)]
        
        # checklist is a waiting list for cells to be checked        
        checklist = []
        # create copies of the ghost list
        ghost_list = api.ghosts(state)
        
        # decide now is hungry mode or survival mode
        if len(ghost_list) != 0:
            self.hungry = False
            self.survival = True
        else:
            self.hungry = True
            self.survival = False
        
        # survival mode
        if self.survival == True:
            for ghost in ghost_list:
                ghost_x = int(ghost[0])
                ghost_y = int(ghost[1])
                checklist.append((ghost_x, ghost_y))
        
        # hungry mode
        if self.hungry == True:
            # add four corners to food_list
            if self.BL == False and (1, 1) not in self.food_list:
                self.food_list.append((1, 1))
            if self.TL == False and (1, self.grid_height - 1) not in self.food_list:
                self.food_list.append((1, self.grid_height - 1))
            if self.TR == False and (self.grid_width - 1, self.grid_height - 1) not in self.food_list:
                self.food_list.append((self.grid_width - 1, self.grid_height - 1))
            if self.BR == False and (self.grid_width - 1, 1) not in self.food_list:
                self.food_list.append((self.grid_width - 1, 1))
            
            # add foods that pacman has seen into food_list
            pre_food_list = api.food(state)
            for food in pre_food_list:
                if food not in self.food_list:
                    self.food_list.append(food)
                
            # remove food that has been eaten from food_list
            pacman = api.whereAmI(state)
            if pacman in self.food_list:
                self.food_list.remove(pacman)
                        
            for food in self.food_list:
                checklist.append(food)
        
        # code for debugging
        # print "food list: ", self.food_list        
        
        # set visited to be FULL and distance_field to be zero        
        for item in checklist:
            visited[item[0]][item[1]] = FULL
            distance_field[item[0]][item[1]] = 0
        
        # BFS search
        while len(checklist) != 0:
            current_cell = checklist.pop(0)
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:
            # if this grid has not been searched and is not wall
                if visited[neighbor_cell[0]][neighbor_cell[1]] == EMPTY and neighbor_cell not in api.walls(state):
                    visited[neighbor_cell[0]][neighbor_cell[1]] = FULL
                    checklist.append(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    
        return distance_field
    
    def four_neighbors(self, x, y):
        """
        Returns horizontal and vertical neighbors of cell (x, y)
        """        
        ans = []
        if x > 1:
            ans.append((x - 1, y))
        if x < self.grid_width - 1:
            ans.append((x + 1, y))
        if y > 1:
            ans.append((x, y - 1))
        if y < self.grid_height - 1:
            ans.append((x, y + 1))
        return ans
        
    def getAction(self, state):
        """
        Return the moving direction of pacman
        """        
        # calculate the width and height of the map
        self.map_size(state)
        pacman = api.whereAmI(state)        
        
        # code for debugging
        # print "pacman: ", pacman

        # check whether pacman has reached the corners
        if pacman[0] == 1 and pacman[1] == 1:
            self.BL = True
        if pacman[0] == 1 and pacman[1] == self.grid_height - 1:
            self.TL = True
        if pacman[0] == self.grid_width - 1 and pacman[1] == self.grid_height - 1:
            self.TR = True
        if pacman[0] == self.grid_width - 1 and pacman[1] == 1:
            self.BR = True
            
        distance_field = self.compute_distance_field(state)        
        neighbors = self.four_neighbors(pacman[0], pacman[1])
        distance = []
        
        for cell in neighbors:
            # if not wall
            if cell not in api.walls(state): 
                distance.append(distance_field[cell[0]][cell[1]])                    
        
        # minimize pacman's distance to food
        min_distance = min(distance) 
        # maximize pacman's distance to ghost
        max_distance = max(distance)            
                    
        possible_move = []
        # hungry mode
        if self.hungry == True:
            for cell in neighbors:
                if distance_field[cell[0]][cell[1]] == min_distance: 
                    possible_move.append(cell)
            # code for debugging
            # print "possibe move: ", possible_move
        
        # survival mode
        if self.survival ==True:
            for cell in neighbors:
                if distance_field[cell[0]][cell[1]] == max_distance: 
                    possible_move.append(cell)
            # code for debugging
            # print "possibe move: ", possible_move
        
        # Get the actions we can try, and remove "STOP" if that is one of them
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        # code for debugging
        # print "legal move: ", legal

        # delete the legal move that is not in the possible_move list
        delete_east = False
        delete_south = False
        delete_north = False
        delete_west = False
        
        # check for east move
        if Directions.EAST in legal:
            delete_east = True
            for move in possible_move:
                if move[0] > pacman[0]:
                    delete_east = False
        if delete_east == True:
            legal.remove(Directions.EAST)
        
        # check for south move
        if Directions.SOUTH in legal:
            delete_south = True
            for move in possible_move:
                if move[1] < pacman[1]:
                    delete_south = False
        if delete_south == True:
            legal.remove(Directions.SOUTH)
            
        # check for west move
        if Directions.WEST in legal:
            delete_west = True
            for move in possible_move:
                if move[0] < pacman[0]:
                    delete_west = False
        if delete_west == True:
            legal.remove(Directions.WEST)
            
        # check for north move
        if Directions.NORTH in legal:
            delete_north = True
            for move in possible_move:
                if move[1] > pacman[1]:
                    delete_north = False
        if delete_north == True:
            legal.remove(Directions.NORTH)
             
        # code for debugging
        # print "legal move after remove: ", legal

        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)
