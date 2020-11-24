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

#general values
CXPB = 0.7 # crossover probability
MUTPB = 0.4 # mutation probability (of a chromosome)
TOURNAMENTSIZE = 10


def generate_field(M, N, P=.9, start=(0,0), end=None):
    """ function to generate random maze """
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

    #switching few parameters on the grid shape
    if(grid.shape[0] == 10):
        print("Dimension : 10x10")
        CHROMOSOME_LENGTH = 25 * CODE_LENGTH 
        SIZE_POPULATION = 100
        MAX_TIME = 10
    elif(grid.shape[0] == 15):
        print("Dimension : 15x15")
        CHROMOSOME_LENGTH = 35*CODE_LENGTH
        SIZE_POPULATION = 200
        MAX_TIME = 15
    elif(grid.shape[0] == 20):
        print("Dimension : 20x20")
        CHROMOSOME_LENGTH = 60*CODE_LENGTH 
        SIZE_POPULATION = 300
        MAX_TIME = 30
    elif(grid.shape[0] == 30):
        print("Dimension : 30x30")
        CHROMOSOME_LENGTH = 90*CODE_LENGTH
        SIZE_POPULATION = 400
        MAX_TIME = 60
    elif(grid.shape[0] == 40):
        print("Dimension : 40x40")
        CHROMOSOME_LENGTH = 100*CODE_LENGTH
        SIZE_POPULATION = 800
        MAX_TIME  = 90
    else :
        #default case
        CHROMOSOME_LENGTH = int(grid.shape[0]*grid.shape[1] - np.sum(grid))
        SIZE_POPULATION = 500
        MAX_TIME = max_time_s
    
    print("Work in progress...please wait")
    #Tools
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
    
    #create & evalue population
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
        #population grading
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
        path = computeChromosome(solution, grid)
        print("population generation number : {}".format(sumOfGeneration))
        print("time elapsed : {}".format(elapsed))
    return path

def computeChromosome(individual, grid): 
    """ from individual to a valid path in maze """
    currentPos = nextPos = (0,0)
    codes=indivParser(individual)
    # codes=optimize(individual, codes)
    
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
      
        if(goFurther(nextPos, grid)):    
            currentPos = (nextPos[0],nextPos[1])
            path.append(currentPos)
            if((nextPos[1] == grid.shape[1] -1) and (nextPos[0] == grid.shape[0] -1)):
                return path   
        else:                
            return path
    return path

def fitness(individual, grid):
    """ manhattan distance based fitness function """
    path = computeChromosome(individual, grid)
    last = path[len(path)-1]
    return (abs((grid.shape[0]-1) - last[0]) + abs((grid.shape[1]-1) - last[1]),)
    
def indivParser(individual):
    """ Parse for chromosomes """
    chrom = "".join([str(genome) for genome in individual])
    codes = [(chrom[i: i + CODE_LENGTH]) for i in range(0,len(chrom), CODE_LENGTH)]

    opti = ""
    var = ""
    last=codes[0]
    for currentCodeStr in codes:
        if (currentCodeStr == MOVE_DOWN and last == MOVE_UP) :
            var += currentCodeStr
        elif (currentCodeStr == MOVE_UP and last == MOVE_DOWN) :  
            var += currentCodeStr
        elif (currentCodeStr == MOVE_LEFT and last == MOVE_RIGHT) :
            var += currentCodeStr
        elif (currentCodeStr == MOVE_RIGHT and last == MOVE_LEFT) :
            var += currentCodeStr
        else:
            opti +=currentCodeStr
            last = currentCodeStr
    codes=opti + var
    for i in range(0, len(individual),1):
        individual[i] = int(codes[i],10)
    better=list()
    for i in range(0, len(codes)-1,2):
        better.append(codes[i]+codes[i+1])
    return better
    # return codes

def findWinner(population):
    """ Return the best individual of the population """
    better=sys.maxsize
    winner=population[0]
    for ind in population:
        if ind.fitness.values[0] < better:
            better=ind.fitness.values[0]           
            winner = ind
    return winner

def optimize(individual, codes):
    """ path optimization """
    opti = ""
    var = ""
    last=codes[0]
    for currentCodeStr in codes:
        if (currentCodeStr == MOVE_DOWN and last == MOVE_UP) :
            var += currentCodeStr
        elif (currentCodeStr == MOVE_UP and last == MOVE_DOWN) :  
            var += currentCodeStr
        elif (currentCodeStr == MOVE_LEFT and last == MOVE_RIGHT) :
            var += currentCodeStr
        elif (currentCodeStr == MOVE_RIGHT and last == MOVE_LEFT) :
            var += currentCodeStr
        else:
            opti +=currentCodeStr
            last = currentCodeStr
    codes=opti + var
    for i in range(0, len(individual),1):
        individual[i] = int(codes[i],10)
    better=list()
    for i in range(0, len(codes)-1,2):
        better.append(codes[i]+codes[i+1])
    return better

def goFurther(position, grid):
    """ check a pos in grid to avoid mistakes """
    if ((position[0] < grid.shape[0]) and (position[0] >= 0)):
        if((position[1] < grid.shape[1]) and (position[1] >= 0)):
            if (grid[position[0]][position[1]] == 0):
                return True
    return False

        
