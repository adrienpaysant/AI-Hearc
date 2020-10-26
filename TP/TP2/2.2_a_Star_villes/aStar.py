from MyQueue import *
from CityLink import *
import math

#heuristiques 
def h0(n,B): return 0
def h1(n,B): return abs(B.X-n.X)
def h2(n,B): return abs(B.Y-n.Y)
def h3(n,B): return math.sqrt((B.X-n.X)**2+(B.Y+n.Y)**2)
def h4(n,B): return h1(n,B)+h2(n,B)

listHeuris=[h0,h1,h2,h3,h4]
dicHeur={"0":"0","1":"distance selon X","2":"distance selon Y","3":"distance à vol d'oiseau","4":"distance de Manhattan"}

#A*
def aStar(dicCity,cityA,cityB,h):
    """ A* search between two city
        from dicCity with a definned heuristic
    """
    frontier = MyQueue()
    frontier.put(0,cityA)
    sumWeight = {cityA: 0}
    steps = 0

    while not frontier.empty():
        current = frontier.get()
        steps+=1
        if current==cityB:
            return current, steps
            
        for coLeaf in current.getcoLeafs(dicCity):
            tempWeight = sumWeight[current] + current.getWeightOf(coLeaf)
            if coLeaf not in sumWeight or tempWeight < sumWeight[coLeaf]:
                sumWeight[coLeaf] = tempWeight
                coLeaf.parent = current
                priority = h(coLeaf, cityB) + tempWeight
                frontier.put(priority,coLeaf)

    raise Exception("no solution")