import math
from queue import PriorityQueue
from CityLink import *
import os

def cls():
    """ tool to clear console"""
    os.system('cls' if os.name=='nt' else 'clear')

#heuristiques 
def h0(n,B): return 0
def h1(n,B): return B.X-n.X
def h2(n,B): return B.Y-n.Y
def h3(n,B): return math.sqrt((B.X-n.X)**2+(B.Y+n.Y)**2)
def h4(n,B): return h1(n,B)+h2(n,B)

listHeuris=[h0,h1,h2,h3,h4]
dicHeur={"0":"0","1":"distance selon X","2":"distance selon Y","3":"distance à vol d'oiseau","4":"distance de Manhattan"}

#A*
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
    #getting data
    dicCity = readAll()
    
    #getting departure and arrival city
    listName=[]
    for k in dicCity.keys():
        listName.append(k)
    cityA=""
    cityB=""

    while cityA not in listName:
        cls()
        cityA=""
        print("Veuillez choisir une ville de départ: ")
        print(listName)
        cityA=input()

    while cityB not in listName:
        cls()
        cityB=""
        print("Veuillez choisir une ville d'arrivée: ")
        print(listName)
        cityB=input()

    #getting heuristic
    tempHeuristic=""
    while tempHeuristic not in dicHeur.keys():
        cls()
        print("Choisissez une heuristique parmis : ")
        for k in dicHeur.keys():
            print(k+"=>"+dicHeur[k])
        tempHeuristic=input()

    #search
    path,steps=aStar(dicCity,dicCity[cityA],dicCity[cityB],listHeuris[int(tempHeuristic)])

    #posttreatment operations
    parent=path.parent
    listCity=[]
    listCity.append(str(dicCity[cityB]))
    while parent:
        listCity.append(str(parent))
        parent=parent.parent
    listCity.reverse()

    #displaying
    cls()
    print("Trajet recherché : "+cityA+"->"+cityB)
    print("trajet trouvé en : "+str(steps)+" visites.")
    print("Bilan du Trajet : ")
    print("    Il y a "+str(len(listCity))+" étapes :")
    print("      DEPART")
    for element in listCity:
        print("        ->"+element)
    print("      ARRIVE")