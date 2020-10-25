# given this final state
final_values = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

class Search :

    def __init__(self, init) :
        self.init = init

    def searchBreadth(self):
        iteration = 1
        border = [self.init]
        legacy = []

        while border:
            print("\riteration count : {}, border depth :{}".format(iteration, len(border)), end="")
            state = border.pop(0)
            legacy.append(state)
            if state.final(final_values):
                return state
            ops = state.applicable_operators()
            for op in ops:
                new = state.apply(op)
                if (new not in border) and new not in legacy and new.legal():
                    #breadth first : Place children last, explore all children of depth D before going to D+1
                    border.append(new)
            iteration += 1
        raise Exception("no solution")


    def searchDepth(self):
        iteration = 1
        border = [self.init]
        legacy = []

        while border:
            print("\riteration count : {}, border depth :{}".format(iteration, len(border)), end="")
            state = border.pop(0)
            legacy.append(state)
            if state.final(final_values):
                return state
            ops = state.applicable_operators()
            for op in ops:
                new = state.apply(op)
                if (new not in border) and new not in legacy and new.legal():
                    #depth search : place children first, explore all children before neighbor
                    border.insert(0, new)
            iteration += 1
        raise Exception("no solution")

  