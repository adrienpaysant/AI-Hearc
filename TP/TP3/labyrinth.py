import numpy as np
import matplotlib.pyplot as plt
import sys
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random
import time

#DNA CODES
CODE_LENGTH = 2
MOVE_LEFT   = "10"
MOVE_RIGHT  = "01"
MOVE_UP     = "11"
MOVE_DOWN   = "00"

#general value
TOURNAMENTSIZE = 10


def generate_field(M, N, P=.9, start=(0,0), end=None):
    """ generate random maze """
    if end == None: end = (M-1,N-1)
    field = np.random.choice([0, 1], size=(M,N), p=[P, 1-P])
    field[start] = field[end] = 0
    return field

def display_labyrinth(grid, start_cell, end_cell, solution=None):
    """Display the labyrinth matrix and possibly the solution with matplotlib.
    Free cell will be in light gray.
    Wall cells will be in dark gray.
    Start and end cells will be in dark blue.
    Path cells (start, end excluded) will be in light blue.
    :param grid np.array: labyrinth matrix
    :param start_cell: tuple of i, j indices for the start cell
    :param end_cell: tuple of i, j indices for the end cell
    :param solution: list of successive tuple i, j indices who forms the path
    """
    grid = np.array(grid, copy=True)
    FREE_CELL = 19
    WALL_CELL = 16
    START = 0
    END = 0
    PATH = 2
    grid[grid == 0] = FREE_CELL
    grid[grid == 1] = WALL_CELL
    grid[start_cell] = START
    grid[end_cell] = END
    if solution:
        solution = solution[1:-1]
        for cell in solution:
            grid[cell] = PATH
    else:
        print("No solution has been found")
    plt.matshow(grid, cmap="tab20c")
    
    
def solve_labyrinth(grid, start_cell, end_cell, max_time_s):
    """Attempt to solve the labyrinth by returning the best path found
    :param grid np.array: numpy 2d array
    :start_cell tuple: tuple of i, j indices for the start cell
    :end_cell tuple: tuple of i, j indices for the end cell
    :max_time_s float: maximum time for running the algorithm
    :return list: list of successive tuple i, j indices who forms the path
    """

    #switching parameters on the grid shape
    if(grid.shape[0] == 10):
        print("Dimension : 10x10")
        CXPB = 0.4 
        MUTPB = 0.6 
        CHROMOSOME_LENGTH = 25 * CODE_LENGTH 
        SIZE_POPULATION = 50
        MAX_TIME = 10
    elif(grid.shape[0] == 15):
        print("Dimension : 15x15")
        CXPB = 0.6 
        MUTPB = 0.6 
        CHROMOSOME_LENGTH = 35*CODE_LENGTH
        SIZE_POPULATION = 100
        MAX_TIME = 15
    elif(grid.shape[0] == 20):
        print("Dimension : 20x20")
        CXPB = 0.5 
        MUTPB = 0.6 
        CHROMOSOME_LENGTH = 60*CODE_LENGTH 
        SIZE_POPULATION = 200
        MAX_TIME = 30
    elif(grid.shape[0] == 30):
        print("Dimension : 30x30")
        CXPB = 0.5 
        MUTPB = 0.7 
        CHROMOSOME_LENGTH = 90*CODE_LENGTH
        SIZE_POPULATION = 400
        MAX_TIME = 60
    elif(grid.shape[0] == 40):
        print("Dimension : 40x40")
        CXPB = 0.5 
        MUTPB = 0.6 
        CHROMOSOME_LENGTH = 100*CODE_LENGTH
        SIZE_POPULATION = 600
        MAX_TIME  = 90
    else :
        #default case
        CXPB = 0.4
        MUTPB = 0.7 
        CHROMOSOME_LENGTH = int(grid.shape[0]*grid.shape[1] - np.sum(grid))
        SIZE_POPULATION = 50
        MAX_TIME = max_time_s
    
    print("Work in progress...please wait")
    #DEAP
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin) 
    toolbox = base.Toolbox()
    toolbox.register("fitness", fitness)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
    toolbox.register("select", tools.selTournament)
    toolbox.register("init_gene", random.randint, 0, 1)
    toolbox.register("init_individual", tools.initRepeat, creator.Individual, toolbox.init_gene, CHROMOSOME_LENGTH)
    toolbox.register("init_population", tools.initRepeat, list, toolbox.init_individual)
    
    #population creation + evaluation
    population = toolbox.init_population(SIZE_POPULATION)
    for ind in population:
        ind.fitness.values = toolbox.fitness(ind, grid)
    
    #solving
    startTime = workingTime = time.time()
    sumOfGeneration = 0
    solution=None
    while (findWinner(population).fitness.values[0] != 0) and (workingTime - startTime < MAX_TIME):
        #tournament
        children = toolbox.select(population, len(population), tournsize = TOURNAMENTSIZE)
        children = list(map(toolbox.clone, children))
        #crossover
        for child1, child2 in zip(children[::2], children[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
        #mutation
        for titan in children:
            if random.random() < MUTPB:
                toolbox.mutate(titan)
        #grading children
        for ind in children:
            ind.fitness.values = toolbox.fitness(ind, grid)
        population = children
        #time
        workingTime = time.time()
        sumOfGeneration += 1
    
    #conclude search
    elapsed = time.time() - startTime
    path=list()
    if not solution:
        if elapsed >= MAX_TIME:
            print('the time out he is')
        solution = findWinner(population)
        path = chromosomeProcessing(solution, grid)
        print("population generaton number : {}".format(sumOfGeneration))
        print("time elapsed : {}".format(elapsed))
    return path

def chromosomeProcessing(individual, grid): 
    """ from individual (list of bit) to a path in maze """
    currentPos = nextPos = (0,0)
    codes=indivParser(individual)
    
    path= list()
    path.append(currentPos)
    for i in range(0, len(codes), 1):
        code=codes[i] 
        if (code == MOVE_DOWN):
            nextPos= (currentPos[0] , currentPos[1] +1)
        elif (code == MOVE_UP) :  
            nextPos= (currentPos[0], currentPos[1] -1)
        elif (code == MOVE_LEFT) :
            nextPos= (currentPos[0] -1, currentPos[1])
        elif (code == MOVE_RIGHT) :
            nextPos= (currentPos[0] +1, currentPos[1])
      
        if(goFurtherToNextPos(nextPos, grid)):    
            currentPos = (nextPos[0],nextPos[1])
            path.append(currentPos)
            if((nextPos[1] == grid.shape[1] -1) and (nextPos[0] == grid.shape[0] -1)):
                return path   
        else:                
            return path
    return path

def fitness(individual, grid):
    """ manhattan distance based fitness function """
    path = chromosomeProcessing(individual, grid)
    return (abs((grid.shape[0]-1) - path[len(path)-1][0]) + abs((grid.shape[1]-1) - path[len(path)-1][1]),len(path),)
    
def indivParser(individual):
    """ Parse  chromosomes """
    chrom = "".join([str(genome) for genome in individual])
    codes = [(chrom[i: i + CODE_LENGTH]) for i in range(0,len(chrom), CODE_LENGTH)]

    #computing path
    opti = ""
    var = ""
    for currentCodeStr in codes:
        if (currentCodeStr == MOVE_DOWN and codes[0] == MOVE_UP) :
            var += currentCodeStr
        elif (currentCodeStr == MOVE_UP and codes[0] == MOVE_DOWN) :  
            var += currentCodeStr
        elif (currentCodeStr == MOVE_LEFT and codes[0] == MOVE_RIGHT) :
            var += currentCodeStr
        elif (currentCodeStr == MOVE_RIGHT and codes[0] == MOVE_LEFT) :
            var += currentCodeStr
        else:
            opti +=currentCodeStr
            codes[0] = currentCodeStr
    #sublimed path
    codes=opti + var
    better=list()
    for i in range(0, len(codes)-1,2):
        better.append(codes[i]+codes[i+1])
    return better

def findWinner(population):
    """ Return the best individual of the population """
    comparingBoy=sys.maxsize
    goldenBoy=population[0]
    for individual in population:
        if individual.fitness.values[0] < comparingBoy:
            comparingBoy=individual.fitness.values[0]           
            goldenBoy = individual
    return goldenBoy

def goFurtherToNextPos(pos, grid):
    """ check a pos in grid to avoid mistakes """
    if ((pos[0] < grid.shape[0]) and (pos[0] >= 0)):
        if((pos[1] < grid.shape[1]) and (pos[1] >= 0)):
            if (grid[pos[0]][pos[1]] == 0):
                return True
    return False

        
