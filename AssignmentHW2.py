# CSCI651
# Assignment 2
# Yu Hou

import sys
import Queue
import time


# create a class
class Node(object):

    def __init__(self,name,color,depth,player,constrains,domain,assignment):


        self.name = name
        self.color = color
        self.depth = depth
        self.player = player
        self.constrains = constrains            # EXAM: {'WA': ['NT', 'SA'], 'Q': ['NSW', 'NT', 'SA'],}
                                                # conflicts between to states.

        self.domain=domain.copy()

        self.a = '-inf'
        self.b = 'inf'
        if player=='2':
            self.value = self.a                 # value is a? or value is -inf directly?
        else:
            self.value= self.b

        self.domain[self.name]=[self.color]     # EXM: {'WA': ['B', 'G', 'R'], 'Q': ['B', 'G', 'R'], 'V': ['G']...}
                                                # remain usable color.

        self.assignment=assignment      # EXM: assignment = {WSN: [R,1], NT:[B,1]...}
                                # the states already have a color.
        # print self.domain
        for key in self.constrains[self.name]:
            if self.color in self.domain[key]:
                tempList=self.domain[key][:]
                tempList.remove(self.color)
                self.domain[key] = tempList
        # print self.domain
        self.assignment[self.name]=[self.color,player]
        self.nextNodeList=[]


        # print self.assignment



    def __lt__(self, other):
        return (self.name == other.name and self.color < other.color) or self.name < other.name
        # create the function again to compare the node


    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def getDepth(self):
        return self.depth

    def getValue(self):
        return self.value
    def getA(self):
        return self.a
    def getB(self):
        return self.b
    def getAssignment(self):
        return self.assignment

    def getDomain(self):
        return self.domain
    def getUtility(self,color1,color2):

        utility = 0
        utility1=0
        utility2=0
        for key, value in self.assignment.items():
            if value[1]=='1':
                utility1=utility1+int(color1[value[0]])
            else:
                utility2=utility2+int(color2[value[0]])

        utility = utility1-utility2
        #print utility
        self.value=utility
    def getNextNodeList(self):
        return self.nextNodeList


    # This method is used to expand new next node (a series of nodes)
    def getNextNodes(self):
        nextNodeList = []
        if self.player=='1':
            player='2'
        else:
            player='1'
        assignedNameList= sorted(self.assignment.keys())
        needAssignedNameList =[]
        #print self.constrains

        for items in assignedNameList:
            for names in self.constrains[items]:
                if (names not in needAssignedNameList) and (names not in assignedNameList):
                    needAssignedNameList.append(names)
        needAssignedNameList.sort()
        #print needAssignedNameList
        #print self.domain
        newDomain = self.domain.copy()

        for iItems in needAssignedNameList:

            for jItems in self.domain[iItems]:
                # print iItems
                # print jItems
                # print self.domain
                # print newDomain
                newAssignment=dict(self.assignment)
                newNode=Node(iItems,jItems,self.depth+1,player,self.constrains,newDomain,newAssignment)

                nextNodeList.append(newNode)

                # print self.domain
        self.nextNodeList=nextNodeList
        return nextNodeList

    # change a or b
    def change(self,letter,value):
        if letter == 'a':
            self.a=value
        elif letter == 'b':
            self.b=value
        elif letter == "v":
            self.value = value

    # This method is used to color a new node in the initial case. Just color it, and change the name of this node.
    def colorNode(self,state,color,player):
        self.player=player
        self.name=state
        self.color=color
        self.domain[self.name] = [self.color]   # In the initial case, the player colors it, so change it directly

        for key in self.constrains[state]:
            if self.color in self.domain[key]:
                self.domain[key].remove(self.color)     # others should remove this color.
        # print self.domain
        self.assignment[self.name]=[self.color,self.player]
        # print self.assignment
        if player=='2':
            self.value = self.a
        else:
            self.value= self.b

    # This method is used to get the description of the node.
    def getResult(self):
        result=''
        result=result+self.name+','
        result=result+' '+self.color+','
        result=result+' '+str(self.depth)+','

        if self.value=='inf' or self.value=='-inf':
            result = result + ' ' + self.value + ','
        else:
            result = result + ' ' + str(self.value) + ','

        if self.a == 'inf' or self.a == '-inf':
            result = result + ' ' + self.a + ','
        else:
            result = result + ' ' + str(self.a) + ','

        if self.b == 'inf' or self.b == '-inf':
            result = result + ' ' + self.b
        else:
            result = result + ' ' + str(self.b)

        return result

    def domainEmpty(self):
        check=True
        for key,value in self.domain.items():
            if key not in self.assignment.keys():
                if value != []:
                    check = False
        return check


# Get data
def initialCaseReading(data):
    initialqueue = Queue.Queue()

    assignmnets = data.split(",")
    for assignmnet in assignmnets:
        dictionary = {}
        meta=assignmnet.split(":")
        dictionary[meta[0].strip()] = meta[1].strip().split("-")
        initialqueue.put(dictionary)
    # dictionary=sortedDict(dictionary)
    return initialqueue
# Get data
def evaluation(data):
    dictionary = {}
    assignmnets = data.split(",")
    for assignmnet in assignmnets:
        meta=assignmnet.split(":")

        dictionary[meta[0].strip()] = meta[1].strip()
    # dictionary=sortedDict(dictionary)
    return dictionary



# major section
# process search, CSP, and minimax.
def searchAB(color,initial,depth,play1,play2,constrainsDict,domain):
    # the first one in initial case.

    if not initial.empty():
        for key,value in initial.get().items():
            initialNode = Node(key, value[0], 0, value[1], constrainsDict, domain, {})
    # the rest
    while not initial.empty():
        for key, value in initial.get().items():
            initialNode.colorNode(key, value[0], value[1])


    depthCheck=0
    a='-inf'
    b='inf'

    ################
    resultQueue=Queue.Queue()

    expand = Queue.Queue()
    generate = Queue.LifoQueue()  # Last in first out, generate queue
    temp = Queue.LifoQueue()  # Last in first out, temporary queue
    visitList = []
    goal = False  # whether find the goal


    generate.put(initialNode)  # put the first one into the queue

    # search to find the opt node
    count=1
    v=0
    while goal == False:
        #print count
        if count ==99:
            lala=1
        # print time.clock()-t0

        newNode = generate.get()
        expand.put(newNode)


        # next[0].getUtility(play1, play2)
        # newNode.getUtility(play1, play2)
        # print newNode.getResult()
        # print next[0].getResult()

        if (newNode.getDepth() == depth) or (newNode.domainEmpty() == True):# it means we reach the bottom of the search tree, can stop and calculate
                                                                            # the utility.
            visitList.append(newNode)
            newNode.getUtility(play1, play2)
            newNode.change('a',a)
            newNode.change('b',b)
            v=newNode.getValue()


            # record this line into result
            line=newNode.getResult()
            # print line
            resultQueue.put(line)
            visitList.append(newNode)


        if (newNode.getDepth() != depth) and (newNode.domainEmpty() == False): # it means we did not reach the bottom.

            if newNode not in visitList:            # although we didnot reach the bottom but it has two situation
                                                    # this means it has not be expended, we should expand it
                if depthCheck < newNode.getDepth():  # if high level to lower level, just change the a and b
                # can not change the v
                    newNode.change('a', a)
                    newNode.change('b', b)

                # record this line into result
                line=newNode.getResult()
                resultQueue.put(line)
                next = newNode.getNextNodes()
                for index in range(len(next)):
                    temp.put(next[index])
                    temp.put(newNode)

            else:                                   # it has been visited. we just change its a and b.

                if depthCheck<newNode.getDepth():  # if high level to lower level, just change the a and b
                                                    # can not change the v
                    newNode.change('a',a)
                    newNode.change('b',b)

                else:                               # if lower level to high level
                    if (newNode.getDepth()%2==0):                                       # this node is Max
                        if (v < float(newNode.getB()) and v >= float(newNode.getA())):  # how about equal?
                            newNode.change('a',v)
                            if v>float(newNode.getValue()):
                                newNode.change('v',v)
                        elif v<=float(newNode.getA()):
                            if v>float(newNode.getValue()):
                                newNode.change('v',v)
                        elif v>=float(newNode.getB()):                                  # ??? why so complicate???
                            # if newNode.getValue()=='-inf':
                            #     newNode.change('v', v)
                            # else:
                            if v>float(newNode.getValue()):
                                newNode.change('v',v)
                                                        # this is a signal to prune node.
                            nextNodeList = newNode.getNextNodeList()
                            compare = generate.get()
                            if compare in nextNodeList:
                                while compare != nextNodeList[-1]:
                                    compare=generate.get()
                                newNode=generate.get()
                            else:
                                generate.put(compare)


                    else:                                                               # this node is Min
                        if (v <= float(newNode.getB()) and v > float(newNode.getA())):
                            newNode.change('b',v)
                            if v<float(newNode.getValue()):
                                newNode.change('v',v)
                        elif v>float(newNode.getB()):
                            if v<newNode.getValue():
                                newNode.change('v',v)
                        elif v<=float(newNode.getA()):
                            if v<float(newNode.getValue()):
                                newNode.change('v',v)
                            # if newNode.getValue=='inf':
                            #     newNode.change('v',v)
                            # else:
                            #     if v<newNode.getValue():
                            #         newNode.change('v',v)

                                                        # this is a signal to prune node.
                            nextNodeList=newNode.getNextNodeList()
                            compare=generate.get()
                            if compare in nextNodeList:
                                while compare != nextNodeList[-1]:              #??? whether put from genearte to expand?
                                    compare=generate.get()
                                newNode=generate.get()
                            else:
                                generate.put(compare)


                line=newNode.getResult()
                resultQueue.put(line)

            visitList.append(newNode)


            while not temp.empty():
                generate.put(temp.get())

        a = newNode.getA()
        b = newNode.getB()
        v = newNode.getValue()
        depthCheck=newNode.getDepth()
        # print generate.qsize()
        if generate.empty():  # ? complete, so no "or newNode.getName() == goalLocation:"?    # generate queue is empty means no new node created, means no path
            goal = True
        count=count+1
    # while not resultQueue.empty():
    #     print resultQueue.get()
    tempName=""
    tempColor=""
    tempValue='-inf'
    while not expand.empty():
        node = expand.get()
        if node.getDepth()== 1:

            vv=node.getValue()
            if vv>float(tempValue):
                tempName=node.getName()
                tempColor=node.getColor()
                tempValue=vv
    rr= tempName + ', ' + tempColor + ', '+ str(tempValue)
    resultQueue.put(rr)


    return resultQueue




def compare(file1,file2):
    lines1=[]
    lines2=[]

    with open(file1) as f:
        lines1.extend(f.read().splitlines())
    with open(file2) as f:
        lines2.extend(f.read().splitlines())
    for index in range(len(lines2)):
        if lines1[index] != lines2[index]:
            print index
            print lines1[index]
            print lines2[index]
    print "ok"

# main function
# Read data from file
if __name__ == '__main__':
    t0=time.clock()
    lines=[]

    with open("testcases/t0.txt") as f:
        lines.extend(f.read().splitlines())


    colorList = lines[0].replace(' ','').split(',')
    colorList.sort()
    #print colorList

    initialCase = initialCaseReading(lines[1])
    #print initialCase

    depthRequired = int(lines[2].strip())
    #print depthRequired

    colorEvaluPlay1 = evaluation(lines[3].strip())
    # print colorEvaluPlay1
    colorEvaluPlay2 = evaluation(lines[4].strip())
    #print colorEvaluPlay2

    linesNumber = len(lines)
    constrainsDict = {}
    # read constrains list
    for index in range(5,linesNumber):
        splits = lines[index].replace(' ','').split(':')
        list = splits[1].strip().split(',')
        list.sort()
        constrainsDict[splits[0].strip()] = list
    # print constrainsDict

    domain = {}
    for key,value in constrainsDict.items():

        # list = constrainsDict[key]
        domain[key] = colorList[:]
    #print domain



    result=searchAB(colorList,initialCase,depthRequired,colorEvaluPlay1,colorEvaluPlay2,constrainsDict,domain)


    fo= open("output.txt", "w")

    number=0
    size = result.qsize()
    while not result.empty():
        fo.write(result.get())
        number=number+1
        if number != size:
            fo.write('\n')
    fo.close()

    print time.clock()-t0
    compare("output.txt","testcases/output_t0.txt")
