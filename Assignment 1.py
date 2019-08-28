# Summer 2017
# Yu Hou 6587492109
# Assignment 1

import sys
import Queue


# create a class
class Node(object) :

    def __init__(self,name,parent,cost,level):
        self.name=name
        self.parent=parent
        self.cost=cost
        self.level=level

    def __lt__(self, other):
        return (self.cost == other.cost and self.name < other.name) or self.cost < other.cost
        # create the function again to compare the cost for the priority
        # two case, if less cost, higher priority; same cost, alph first

    # def __cmp__(self, other):
    #     return cmp(self.cost, other.cost)

    def getName(self):
        return self.name
    def getParent(self):
        return self.parent
    def getCost(self):
        return self.cost
    def getLevel(self):
        return self.level


# sort the dictionary by the keys
def sortedDict(adict):
    # keys = adict.keys()
    # keys = list(keys)
    # keys.sort()
    # keys = dict(keys)
    adict = dict([(k, adict[k]) for k in sorted(adict.keys())])
    return adict

# Read the node list into a dictionary
def dataReading(data):
    dictionary = {}
    datametas = data.split(",")
    for meta in datametas:
        metasplit=meta.split("-")
        dictionary[metasplit[0].strip()] = int(metasplit[1].strip())
    dictionary=sortedDict(dictionary)
    return dictionary

def bFSearch(fuel,startLocation,goalLocation,nodeDict):
    expand = Queue.Queue()
    generate = Queue.Queue()
    restCost = 0           # the total cost
    goal=False              # whether find the goal

    optNode=Node(startLocation,None,0,0)
    generate.put(optNode)

    # search to find the opt node

    while goal == False:

        newNode=generate.get()
        expand.put(newNode)
        if newNode.getName()==goalLocation and newNode.getCost()<=fuel:
            goal=True
            optNode=newNode
            restCost= fuel-optNode.getCost()
        if newNode.getName() != goalLocation:
            # if this new node is destination there is no need to generate, otherwise generate new nodes.
            for key,value in nodeDict[newNode.getName()].items():
                if newNode.getParent() == None or key != newNode.getParent().getName():         # avoid the loops
                    generate.put(Node(key,newNode,newNode.getCost()+value,newNode.getLevel()+1))

        if generate.empty():  # generate queue is empty means no new node created, means no path
            goal = True

    # put opt node into solution
    result=""
    if optNode.getName()==startLocation or restCost == 0:
        result="No Path"
    else:
        soluton= Queue.LifoQueue()
        soluton.put(optNode.getName())
        while optNode.getParent() != None:
            soluton.put(optNode.getParent().getName())
            optNode=optNode.getParent()

        while not soluton.empty():          # get result
            result=result+soluton.get()+"-"

        result=result[:-1]                  # remove last "-"
        result=result +" "+ str(restCost)
    return result




def dFSearch(fuel,startLocation,goalLocation,nodeDict):
    expand = Queue.Queue()
    generate = Queue.LifoQueue()      # Last in first out, generate queue
    temp = Queue.LifoQueue()          # Last in first out, temporary queue
    restCost = 0  # the total cost
    goal = False  # whether find the goal

    optNode = Node(startLocation, None, 0, 0)
    generate.put(optNode)           # put the first one into the queue


    # search to find the opt node

    while goal == False:

        newNode = generate.get()
        expand.put(newNode)
        if newNode.getName() == goalLocation and newNode.getCost() <= fuel:
            goal = True
            optNode = newNode
            restCost = fuel - optNode.getCost()

        if newNode.getName() != goalLocation:
            # if this new node is destination there is no need to generate, otherwise generate new nodes.
            for key, value in nodeDict[newNode.getName()].items():
                if newNode.getParent() == None or key != newNode.getParent().getName():  # avoid the loops
                    temp.put(Node(key, newNode, newNode.getCost() + value,
                                  newNode.getLevel() + 1))  # put the node into temp firstly

            while not temp.empty():
                generate.put(temp.get())

        if generate.empty() or newNode.getName() == goalLocation:            # generate queue is empty means no new node created, means no path
            goal = True

    # put opt node into solution
    result = ""
    if optNode.getName() == startLocation or restCost == 0:
        result = "No Path"
    else:
        soluton = Queue.LifoQueue()
        soluton.put(optNode.getName())
        while optNode.getParent() != None:
            soluton.put(optNode.getParent().getName())
            optNode = optNode.getParent()

        while not soluton.empty():  # get result
            result = result + soluton.get() + "-"

        result = result[:-1]  # remove last "-"
        result = result + " " + str(restCost)
    return result



def uCSearch(fuel,startLocation,goalLocation,nodeDict):
    expand = Queue.Queue()
    generate = Queue.PriorityQueue()  # Last in first out, generate queue

    restCost = 0  # the total cost
    goal = False  # whether find the goal

    optNode = Node(startLocation, None, 0, 0)
    generate.put(optNode)  # put the first one into the queue


    # search to find the opt node

    while goal == False:

        newNode = generate.get()
        expand.put(newNode)



        if newNode.getName() != goalLocation:
            # if this new node is destination there is no need to generate, otherwise generate new nodes.
            for key, value in nodeDict[newNode.getName()].items():
                if newNode.getParent() == None or key != newNode.getParent().getName():  # avoid the loops
                    generate.put(Node(key, newNode, newNode.getCost() + value, newNode.getLevel() + 1))

        #if newNode.getName() == goalLocation and newNode.getCost() <= fuel: # whether we need this and?
        if newNode.getName() == goalLocation:
            goal = True
            optNode = newNode
            restCost = fuel - optNode.getCost()

        if generate.empty() or newNode.getName() == goalLocation:  # generate queue is empty means no new node created, means no path
            goal = True




    # put opt node into solution
    result = ""
    if optNode.getName() == startLocation or restCost <= 0:
        result = "No Path"
    else:
        soluton = Queue.LifoQueue()
        soluton.put(optNode.getName())
        while optNode.getParent() != None:
            soluton.put(optNode.getParent().getName())
            optNode = optNode.getParent()

        while not soluton.empty():  # get result
            result = result + soluton.get() + "-"

        result = result[:-1]  # remove last "-"
        result = result + " " + str(restCost)
    return result




# main function
# Read data from file
if __name__ == '__main__':
    lines=[]

    with open("testcases/t2.txt") as f:
        lines.extend(f.read().splitlines())

    #fo= open("input", "w")
    searchMethod = lines[0]
    fuel = int(lines[1])
    startLocation = lines[2]
    goalLocation = lines[3]
    linesNumber = len(lines)
    nodeDict = {}
    # read node list
    for index in range(4,linesNumber):
        splits = lines[index].split(':')
        nodeDict[splits[0].strip()] = dataReading(splits[1])

    print(nodeDict)
    # search
    if searchMethod == "BFS":
        result = bFSearch(fuel,startLocation,goalLocation,nodeDict)
        print result
    if searchMethod == "DFS":
        result = dFSearch(fuel,startLocation,goalLocation,nodeDict)
        print result
    if searchMethod == "UCS":
        result = uCSearch(fuel,startLocation,goalLocation,nodeDict)
        print result

