#CS 411 - Assignment 6 Solution
#Iterative Deepening A* Search for 15 puzzle 
#Fatema Engineeringwala
#2021 Spring

import random
import math
import time
import psutil
import os
from collections import deque
import sys

#This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self,tiles):
        self.size = int(math.sqrt(len(tiles))) # defining length/width of the board
        self.tiles = tiles

    def __hash__(self):
        return hash(tuple(self.tiles))

    def __eq__(self,other):
    	return self.tiles == other.tiles
    
    #This function returns the resulting state from taking particular action from current state
    def execute_action(self,action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action=='L':	
            if empty_index%self.size>0:
                new_tiles[empty_index-1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-1]
        if action=='R':
            if empty_index%self.size<(self.size-1): 	
                new_tiles[empty_index+1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+1]
        if action=='U':
            if empty_index-self.size>=0:
                new_tiles[empty_index-self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-self.size]
        if action=='D':
            if empty_index+self.size < self.size*self.size:
                new_tiles[empty_index+self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+self.size]
        return Board(new_tiles)

    # To get x,y co-ordinates of a tile in 4*4 matrix
    def getCoordinates(self,tile):
        new_tiles = self.tiles[:]
        index = new_tiles.index(tile)
        return index//self.size,index%self.size
    
        

#This class defines the node on the search tree, consisting of state, parent and previous action		
class Node:
    def __init__(self,state,parent,action,depth):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.f = f(self)

    #Returns string representation of the state	
    def __repr__(self):
        return str(self.state.tiles)
    
    #Comparing current node with other node. They are equal if states are equal	
    def __eq__(self,other):
        return self.state.tiles == other.state.tiles
        
    def __hash__(self):
        return hash(tuple(self.state.tiles))

# Global variables h used to select which hashing function to use
h=1
nodesExpanded=0
max_memory=0

#Utility function to randomly generate 15-puzzle		
def generate_puzzle(size):
    numbers = list(range(size*size))
    random.shuffle(numbers)
    return Node(Board(numbers),None,None,0)

#This function returns the list of children obtained after simulating the actions on current node
def get_children(parent_node):
    children = []
    actions = ['U','D','L','R'] # left,right, up , down ; actions define direction of movement of empty tile
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        if(child_state.tiles  != parent_node.state.tiles) :
            child_node = Node(child_state,parent_node,action,parent_node.depth+1)
            children.append(child_node)
    return children

#This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
def find_path(node):	
    path = []	
    while(node.parent is not None):
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path

#Calculates the total manhattan distance for a given state    
def manhattanDistance(state):
    goal_state = getGoalBoard()
    tiles = state.tiles[:]
    manhattanDistance=0
    for i in tiles:
        xs,ys=state.getCoordinates(i)
        xg,yg=goal_state.getCoordinates(i)
        if((xs != xg or ys != yg) and i!='0'):
            manhattanDistance+=abs(xs-xg)+abs(ys-yg)
    return manhattanDistance

#Calculates the total number of misplaced tiles in a given state
def misplacedTiles(state):
    goal_state = getGoalBoard()
    tiles = state.tiles[:]
    misplacedTiles=0
    for i in tiles:
        xs,ys=state.getCoordinates(i)
        xg,yg=goal_state.getCoordinates(i)
        if((xs != xg or ys != yg) and i!='0'):
            misplacedTiles+=1
    return misplacedTiles

#Calculates Function f(n)=g(n)+h(n)
#g(n) can also be the depth of a given node as it is also equal to number of steps taken
#h(n) can be either manhattanDistance or misplacedTiles based on the value of global variable h
def f(node):
    if h==1 :
        return node.depth + misplacedTiles(node.state)
    return node.depth + manhattanDistance(node.state)

#Implementation of Iterative Deepening A* star Algorithm with input [root_node]
def ida_star(root_node):
    global nodesExpanded,max_memory
    if h==1:
        bound = misplacedTiles(root_node.state)
    bound = manhattanDistance(root_node.state)
    frontier = [root_node]
    max_memory=0
    while True:
        nodesExpanded=0
        t,node = a_star_search(frontier,bound)
        if t==True:
            return find_path(node)
        elif t is None:
            return "NOT FOUND"
        bound = t


#Function to implement A* search 
# Input  frontier - [root_node] and bound - h() 
# returns True(if reached goal state) or f() or min t value and the current node
def a_star_search(frontier,bound):
    global max_memory,nodesExpanded
    node= frontier[len(frontier)-1]
    if node.f > bound : 
        return node.f,node
    if goal_test(node.state.tiles):
        return True,node
    min = None
    max_memory = max(max_memory, sys.getsizeof(frontier))
    nodesExpanded+=1
    for child in get_children(node):
        if(child not in frontier):          
            frontier.append(child)
            t,node = a_star_search(frontier,bound)
            if t==True:
                return True,node
            elif min is None or (t is not None and t<min):
                min = t
            frontier.pop()

    return min,node

#Main function accepting input from console , runnung A* and showing output	
def main():
    global h,max_memory,nodesExpanded
    initial = str(input("initial configuration: "))
    initial_list = initial.split(" ")

    root = Node(Board(initial_list),None,None,0)
    while True:        
        method = int(input("\nWhich Heuristic do you want to use\nMisplaced Tiles (Type 1)\nManhattan Distance (Type 2)\nExit (Type Number other than 1 and 2)\n"))

        if(method == 1):
            h=1
            print("\nIDA* search using H1 = number of misplacedTiles")
        elif(method==2):
            h=2
            print("\nIDA* search using H2 = manhattanDistance")
        else:
            return
        mt_init_time= time.time()
        mt_path = ida_star(root)
        mt_exit_time = time.time()
        print("Moves: " + " ".join(mt_path))
        print("Number of expanded Nodes: "+ str(nodesExpanded))
        print("Time Taken: " + str(mt_exit_time-mt_init_time))
        print("Max Memory (Bytes): " +  str(max_memory))

        # md_init_time= time.time()
        # h=2
        # md_path = ida_star(root)
        # md_exit_time = time.time()
        # print("\n\nA* search using H2 = manhattan distance")
        # print("Moves: " + " ".join(md_path))
        # print("Number of expanded Nodes: "+ str(nodesExpanded))
        # print("Time Taken: " + str(md_exit_time-md_init_time))
        # print("Max Memory (Bytes): " +  str(max_memory))


def getGoalBoard():
    return Board(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0'])
    # return Board(['1','2','3','0'])

#Utility function checking if current state is goal state or not
def goal_test(cur_tiles):
    return cur_tiles == ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']	
    # return cur_tiles == ['1','2','3','0']
    
if __name__=="__main__":main()	