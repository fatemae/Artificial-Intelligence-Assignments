import os
import copy
import random

# Model (MDP)
class MDP(object):
    def __init__(self, x,y,wallLocations,terminalStates,reward,transitionProbabilities,epsilon,discount):
    # def __init__(self, x,y,wallLocations):
        self.gridx=x
        self.gridy=y
        self.state = [[0 for a in range(self.gridx)] for b in range(self.gridy)]
        self.mdpGrid =  [[reward for a in range(self.gridx)] for b in range(self.gridy)]
        # self.state.reverse()
        # self.mdpGrid.reverse()
        self.wallLocations=[]
        self.terminalStates=[]
        for w in wallLocations:
            self.state[self.gridy-w[1]][w[0]-1]=None
            self.mdpGrid[self.gridy-w[1]][w[0]-1]=None
            self.wallLocations.append([self.gridy-w[1],w[0]-1])
        for t in terminalStates:
            # self.state[self.gridy-t[1]][t[0]-1]=t[2]
            self.mdpGrid[self.gridy-t[1]][t[0]-1]=t[2]
            self.terminalStates.append([self.gridy-t[1],t[0]-1])
        
        self.reward=reward
        self.transitionProbabilities=transitionProbabilities
        self.epsilon=epsilon
        self.discount=discount
    
    def actions(self):
        # return list of all actions
        return ["E", "N", "W", "S"]

    # returns true if a state is terminal or wall
    def isEnd(self, x,y):
        if([x,y] in self.terminalStates or [x,y] in self.wallLocations):
            return True
        else:
            return False
    
    # returns the possible locations after all actions like Left,right,back,forward in a state
    def T(self, x,y,a):
        orientations = ["E", "N", "W", "S"]
        turns = FORWARD,LEFT,RIGHT,BACK = (0,+1, -1,+2)
        def turn_heading(heading, inc, headings=orientations):
            return headings[(headings.index(heading) + inc) % len(headings)]
        result = []

        for i in turns:
            result.append(self.validateActiongetXY(x,y,turn_heading(a,i)))
        # print(result)
        
        return result

    # returns the final state after performing action a on currrent state
    def validateActiongetXY(self,x,y,a):
        if(a=="N" and x-1>=0 and [x-1,y] not in self.wallLocations):
            return [x-1,y]
        elif(a=="S" and x+1<self.gridy and [x+1,y] not in self.wallLocations):
            return [x+1,y]
        elif(a=="E" and y+1<self.gridx and [x,y+1] not in self.wallLocations):
            return [x,y+1]
        elif(a=="W" and y-1>=0 and [x,y-1] not in self.wallLocations):
            return [x,y-1]
        else:
            return [x,y]
        
# to print in grid format
def printGrid(x):
    for r in x:
        str=''
        for item in r:
            if(type(item) == int or type(item)==float):
                str+='    %.12f   '%item
            elif(item is None):
                str+='    None             '
            else:
                str+='    %s                  '%item
        print(str)
    print

# returns the Q value
def Q(mdp,x,y, action,V): 
        transitionStates=mdp.T(x,y,action)
        prob=mdp.transitionProbabilities
        index=0
        sum=0
        for item in transitionStates:
            # print(x," ",y)
            # print(mdp.mdpGrid)
            if(mdp.isEnd(item[0],item[1])):
                sum+=prob[index]*(mdp.mdpGrid[item[0]][item[1]])
            else:
                sum+=prob[index]*(mdp.mdpGrid[x][y]+mdp.discount*V[item[0]][item[1]])
            index+=1
        return sum

# implementation of value iteration algorithm
def valueIteration(mdp):
    i=0
    V=mdp.state
    print("Iteration :",i)
    printGrid(V)
        
    while True:
        i+=1
        # compute the new values (newV) given the old values (V)
        newV = copy.deepcopy(V)
        for row_index, row in enumerate(V):
            for col_index, item in enumerate(row):
                if(mdp.isEnd(row_index,col_index)):
                    newV[row_index][col_index] = mdp.mdpGrid[row_index][col_index]
                else:
                    newV[row_index][col_index] = max(Q(mdp,row_index,col_index,action,V) for action in mdp.actions())

        diff=maxDiff=abs(V[0][0]-newV[0][0])
        for row_index, row in enumerate(V):
            for col_index, item in enumerate(row):
                if(not mdp.isEnd(row_index,col_index)):
                    diff=abs(V[row_index][col_index]-newV[row_index][col_index])
                if(diff>maxDiff):
                    maxDiff=diff
        if(maxDiff <= (mdp.epsilon*(1-mdp.discount)/mdp.discount)):
            break
        print("Iteration :",i)
        printGrid(newV)
        V = newV
        PI=copy.deepcopy(V)
        for row_index, row in enumerate(V):
            for col_index, item in enumerate(row):
                if(not mdp.isEnd(row_index,col_index)):
                    PI[row_index][col_index] = max((Q(mdp,row_index,col_index,action,V),action) for action in mdp.actions())[1]
        # print(PI)
    print("Final Value after Convergence")
    printGrid(newV)
    return PI
    
# find the values of policy PI
def policy_evaluation(PI,U,mdp):
    newU=copy.deepcopy(U)
    for row_index, row in enumerate(newU):
        for col_index, item in enumerate(row):
            if(mdp.isEnd(row_index,col_index)):
                newU[row_index][col_index] = mdp.mdpGrid[row_index][col_index]
            else:
                newU[row_index][col_index] = Q(mdp,row_index,col_index,PI[row_index][col_index],U)
    return newU
    
# implementation of policy iteration algorithm
def policy_iteration(mdp):
    PI=copy.deepcopy(mdp.state)
    U=copy.deepcopy(mdp.state)
    for row_index, row in enumerate(PI):
        for col_index, item in enumerate(row):
            if(mdp.isEnd(row_index,col_index)):
                PI[row_index][col_index] = mdp.mdpGrid[row_index][col_index]
            else:
                PI[row_index][col_index] = random.choice(mdp.actions())
        # return PI
    print("Random Policy")
    printGrid(PI)
    i=0
    while True:
        i+=1
        U=policy_evaluation(PI,U,mdp)
        # printGrid(U)
        unchanged=True
        for row_index, row in enumerate(U):
            for col_index, item in enumerate(row):
                if(not mdp.isEnd(row_index,col_index)):
                    a = max((Q(mdp,row_index,col_index,action,U),action) for action in mdp.actions())[1]
                    if(Q(mdp,row_index,col_index,a,U)>Q(mdp,row_index,col_index,PI[row_index][col_index],U)):
                    # if(a!=PI[row_index][col_index]):
                        unchanged=False
                        PI[row_index][col_index]=a
        # print("Iteration ",i)
        # printGrid(PI)
        if unchanged:
            return PI
        
# support function to split input list
def getSplitList(str):
    str = [x.strip().split(" ") for x in str]
    str = [[int(x) for x in y] for y in str]
    return str

def main():

    # reads mdp_input.txt file and stores the values
    with open("mdp_input.txt") as fp:
        Lines = fp.readlines()
        for line in Lines:
            print(line)
            if(line[0]!='#' and line[0]!='\r' and line[0]!='\n'):
                print(line)
                valType=line.split(':')[0].strip()
                value=line.split(':')[1].strip()
                if(valType=='size'):
                    gridx,gridy=map(int,value.strip().split())
                elif(valType=='walls'):
                    wallLocations=value.split(',')
                    wallLocations=getSplitList(wallLocations)
                elif(valType=='terminal_states'):
                    terminalStates=value.split(',')
                    terminalStates=getSplitList(terminalStates)
                elif(valType=="reward"):
                    reward=float(value)
                elif(valType=="transition_probabilities"):
                    transitionProbabilities=[float(x) for x in value.split()]
                elif(valType=="discount_rate"):
                    discount=float(value)
                elif(valType=="epsilon"):
                    epsilon=float(value)


    # gridx,gridy=5,4
    # wallLocations=[[2,2],[2,3]]
    # terminalStates=[[4, 2 ,1] , [5,4,2],[5,3,-3]]
    # reward=-0.04
    # transitionProbabilities= [0.8, 0.1, 0.1, 0.0]   
    # discount=0.85
    # epsilon=0.001
    mdp=MDP(gridx,gridy,wallLocations,terminalStates,reward,transitionProbabilities,epsilon,discount)
    # mdp=MDP(gridx,gridy,wallLocations)
    # print(mdp.T(0,0,"N"))
    print("########################VALUE ITERATION##############################")
    optimalPI=valueIteration(mdp)
    print("Optimal Policy after Value Iteration")
    printGrid(optimalPI)
    # print(mdp.state)
    print("########################POLICY ITERATION##############################")
    PI=policy_iteration(mdp)
    print("\nOptimal Policy After Convegence")
    printGrid(PI)



if __name__=="__main__":main()