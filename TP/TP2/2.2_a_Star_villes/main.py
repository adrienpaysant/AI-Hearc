import math
from queue import PriorityQueue
from CityLink import *


#heuristiques 
def h0(n,B): return 0
def h1(n,B): return B.X-n.X
def h2(n,B): return B.Y-n.Y
def h3(n,B): return math.sqrt((B.X-n.X)**2+(B.Y+n.Y)**2)
def h4(n,B): return h1(n,B)+h2(n,B)


def aStar(dicCity,cityA,cityB,h):
    """ A* search between two city
        from dicCity with a definned heuristic
    """
    frontier = PriorityQueue()
    frontier.put((0,cityA))
    sumWeight = {cityA: 0}
    steps = 0

    while not frontier.empty():
        temp = frontier.get()
        steps+=1
        current=temp[1]
        if current==cityB:
            return current, steps
            
        for coLeaf in current.getcoLeafs(dicCity):
            tempWeight = sumWeight[current] + current.getWeightOf(coLeaf)
            if coLeaf not in sumWeight or tempWeight < sumWeight[coLeaf]:
                sumWeight[coLeaf] = tempWeight
                coLeaf.parent = current
                priority = h(coLeaf, cityB) + tempWeight
                frontier.put((priority,coLeaf))

    raise Exception("no solution")


if __name__ == '__main__':
    dicCity = readAll()
    
    path,steps=aStar(dicCity,dicCity["Amsterdam"],dicCity["Naples"],h1)
    print("trajet trouvé en : "+str(steps)+" visites.")
    parent=path.parent
    print("Bilan du Trajet : ")
    listCity=[]
    listCity.append(str(dicCity["Naples"]))
    while parent:
        listCity.append(str(parent))
        parent=parent.parent
    listCity.reverse()
    print("DEPART")
    for element in listCity:
        print(" ->"+element)
    print("ARRIVE")