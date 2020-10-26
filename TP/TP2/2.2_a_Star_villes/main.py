import math
from queue import PriorityQueue
from CityLink import *
from aStar import *
import os

def cls():
    """ tool to clear console"""
    os.system('cls' if os.name=='nt' else 'clear')




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