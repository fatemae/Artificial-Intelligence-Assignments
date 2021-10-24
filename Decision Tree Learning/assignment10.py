# -*- coding: utf-8 -*-
# Decision Tree Learning
# Fatema Engineeringwala  

import pandas as pd
import math
import copy
import csv


colnames = ['Alternate', 'Bar', 'Weekend', 'Hungry','Patrons','Price','Raining','Reservations','Type','WaitEstimate','Result']
allExamples={}
chiSquare = [ 0, 3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919, 18.307]

class Node():
    def __init__(self,depth):
        self.value = None
        self.branch = None
        self.childs = None
        self.depth = depth
    

def DecisionTreeLearning(examples, attribute, parent_examples,depth):
    if(examples.empty):
        return PluralityValue(parent_examples)
    elif(sameClassification(examples)):
        return examples['Result'][0]
    elif(not attribute):
        return PluralityValue(examples)
    else:
        # A = max((Importance(a,examples),a) for a in attribute)[1]
        I={}
        for a in attribute:
            I[a]=(Importance(a,examples))
        max_value = max(I.values())
        max_keys = [k for k, v in I.items() if v == max_value]
        A=max_keys[0]
        tree = Node(depth)
        tree.childs=[]
        tree.value=A
        attr=attribute
        attr.remove(A)
        for v in allExamples[A].unique():
            exs=examples[examples[A] == v]
            exs=exs.reset_index(drop=True)
            subtree = DecisionTreeLearning(exs,attr,examples,depth+1)
            if(isinstance(subtree,Node)):
                subtree.branch = v
                tree.childs.append(subtree)
            else:
                child=Node(depth+1)
                child.value=subtree
                child.branch=v
                tree.childs.append(child)
        return tree

def PluralityValue(examples):
    x=examples.groupby(['Result'], sort=False).size().reset_index(name='Count')
    max=0
    for i in range(0,len(x)-1):
        if(x['Count'][i]<x['Count'][i+1]):
            max=i+1
        else:
            max=i
    return x['Result'][max]

def sameClassification(examples):
    v=examples['Result'][0]
    flag=True
    for i in range(0,len(examples)):
        if(examples['Result'][i]!=v):
            flag=False
    return flag

def Importance(attr,examples):
    x=examples.groupby(['Result'], sort=False).size().reset_index(name='Count')
    p=findCount('Yes',x)
    n=findCount('No',x)
    return Entropy(p/(p+n))-Remainder(attr,examples)

def findCount(v,data):
    if(data['Result'][0]==v):
        idx=0
    else:
        idx=1
    return(data['Count'][idx])

def Entropy(q):
    if(q!=0 and 1-q!=0):
        return (-1 * (q*math.log2(q) + (1-q)*math.log2(1-q)))
    elif(q!=0 and 1-q==0):
        return (-1 * (q*math.log2(q)))
    else:
        return (-1 * (1-q)*math.log2(1-q))


def Remainder(attr,examples):
    l=len(examples)
    count=examples.groupby([attr], sort=True).size().reset_index(name='count')
    df=examples[examples['Result'] == 'Yes']
    positiveCount=df.groupby([attr], sort=True).size().reset_index(name='pos')
    df=examples[examples['Result'] == 'No']
    negativeCount=df.groupby([attr], sort=True).size().reset_index(name='neg')
    z = pd.merge(positiveCount, negativeCount, how = 'outer',left_on=attr, right_on=attr)
    z.fillna(0,inplace=True)
    sum=0
    for i in range(0,len(count)):
        t=z['pos'][i]+z['neg'][i]
        sum+=(t)/l*Entropy(z['pos'][i]/t)
    return sum

def statisticalSignificanceTest(root,examples):
    n={}
    if(root.childs is not None):
        d=len(root.childs)
        p=len(examples[examples['Result']=='Yes'])
        n=len(examples[examples['Result']=='No'])
        delta=0
        for c in root.childs:
            exs=examples[examples[root.value]==c.branch]
            if(len(exs)!=0):
                pk=len(exs[exs['Result']=='Yes'])
                nk=len(exs[exs['Result']=='No'])
                pkp=p*(pk+nk)/(p+n)
                nkp=n*(pk+nk)/(p+n)
                delta+=(pk-pkp)*(pk-pkp)/pkp + (nk-nkp)*(nk-nkp)/nkp
            else:
                delta+=0
        if(delta>chiSquare[d-1]):
            for c in root.childs:
                statisticalSignificanceTest(c,examples[examples[root.value]==c.branch])
        else:
            root.childs=None
            if(p>n):
                root.value='Yes'
            else:
                root.value='No'
    else:
        return



def printTree(start, tree, indent_width=4):

    def ptree(start, tree, indent="   "):
        if tree.depth == start:
            if tree.childs is None:
                if(tree.branch is None):
                    print(tree.value)
                else:
                    print("("+tree.branch+")--"+tree.value)
            else:
                if(tree.branch is None):
                    print(tree.value)
                else:
                    print("("+tree.branch+")--"+tree.value)
                for child in tree.childs[:-1]:
                    # print(indent + "├" + "─" * indent_width, end="")
                    print(indent + "├" + "─" * indent_width, end="")
                    ptree(tree.depth+1, child, indent + "│" + " " * 14)
        # if parent not in tree:
                child = tree.childs[-1]
                print(indent + "└" + "─" * indent_width, end="")
                ptree(tree.depth+1, child, indent + " " * 15)  # 4 -> 5

    parent = start
    ptree(start, tree)


def main():
    global allExamples
    a = pd.read_csv('data.csv', names=colnames,skipinitialspace=True)
    allExamples=a
    colnames.remove('Result')
    x=DecisionTreeLearning(a,colnames,a,0)
    print("############### Decision Tree ############")
    printTree(0,x)

    print("\n\n############### Pruned Decision Tree ############")
    statisticalSignificanceTest(x,a)
    # x=sameClassification(a)
    printTree(0,x)

if __name__=="__main__":main()