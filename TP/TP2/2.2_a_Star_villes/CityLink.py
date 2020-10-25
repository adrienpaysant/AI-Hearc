import os

class City :
    """ Class that represent a city in traveller's issue """
    def __init__(self,name,x,y):
        self.name = name
        self.X = int(x)
        self.Y = int(y)
        self.links = []
        self.parent=None
        
    def __str__(self):
        return str(self.name)

    def getcoLeafs(self,dicCity):
        """ return a list of the coLeaf of self"""
        neighbors=[]
        #print ("voisin de "+self.name)
        for l in self.links:
            #print("- "+str(l.destination)+", "+str(l.weight))
            neighbors.append(dicCity[str(l.destination)])
        return neighbors

    def getWeightOf(self,destination):
        """ return the weight of journey between a leaf and self"""
        for l in self.links:
            if str(l.destination)==str(destination.name):
                return int(str(l.weight))

    def createLinks(self,link):
        """ method that add link to self link's list """
        self.links.append(link)
        
####################################
class Links:
    """ class that represent a connection between two city"""
    def __init__(self,destination,weight):
        self.destination=destination
        self.weight=weight
####################################

#PARSING
def readCityFile(dicCity):
    """ getting informations from data files, this case for the city"""
    file=open("./data/positions.txt","r")
    for linePos in file:
        name,x,y=linePos.split()
        dicCity[name]=City(name,x,y)

def readLinksFile(dicCity):
    """ getting informations from data files, this case for the links"""
    file=open("./data/connections.txt","r")
    for lineCon in file:
        src,dst,weight=lineCon.split()
        try:
            dicCity[src].createLinks(Links(dicCity[dst],weight))
            dicCity[dst].createLinks(Links(dicCity[src],weight))
        except:
            print("error in file")

def readAll():
    """ Parsing method to set up the city's dict """
    dicCity={}
    readCityFile(dicCity)
    readLinksFile(dicCity)
    return dicCity