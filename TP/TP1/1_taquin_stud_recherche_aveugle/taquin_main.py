from taquin_viewer import TaquinViewerHTML
from state_modele import State
from taquin_play import Search

def pathFromState(state) :
    stateCurrent = state
    statesPath = []
    while stateCurrent.parent is not None :
        statesPath.insert(0, stateCurrent)
        stateCurrent = stateCurrent.parent
    statesPath.insert(0, stateCurrent)
    return statesPath

def pathToHTML(path, filename) :
    i = 1
    with TaquinViewerHTML(filename + '.html') as viewer:
        for board in path:
            viewer.add_taquin_state(board.values, "move" + str(i))
            i = i+1

if __name__ == '__main__':
    # You should test the following initial configurations:
    # your algorithm should reach the solution in few iterations
    taquin_trivial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]

    taquin_easy = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

        # your algorithm should reach the solution in few hundred iterations
    taquin_medium = [
        [0, 1, 2],
        [7, 4, 3],
        [5, 8, 6]
    ]

    # your algorithm will need more then 100'000 iterations
    taquin_hard = [
        [4, 0, 2],
        [3, 5, 1],
        [6, 7, 8]
    ]

    # just impossible
    taquin_impossible = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]

    #init AI
    stateStart = State(taquin_easy)
    search = Search(stateStart)

    #search
    print("breadth search starting")
    stateFinal = search.searchBreadth()
    print("\nsearch done")
    statesPath = pathFromState(stateFinal)
    pathToHTML(statesPath, "breadth_search")

    #search
    print("depth search starting")
    stateFinal = search.searchDepth()
    print("\nsearch done")
    statesPath = pathFromState(stateFinal)
    pathToHTML(statesPath, "depth_search")