# from folder.file_name import ClassName
from state_modele import State
from taquin_viewer import TaquinViewerHTML


def search(init, final_values):
    # frontiere contains the next following states (nodes) to explore
    frontiere = [init]  # QUESTION: Why frontiere cannot be a 'set'?

    # history contains the states that have been explored
    history = set()
    while frontiere:
        # extract the LAST element from the list
        state = frontiere.pop()
        history.add(state)
        if state.final(final_values):
            print("History length: {}".format(len(history)))
            print("Frontiere length: {}".format(len(frontiere)))
            return state
        ops = state.applicable_operators()
        for op in ops:
            new_state = state.apply(op)
            if (new_state not in frontiere) and (new_state not in history) and new_state.legal():
            # QUESTION: is the alternative in the following line valid? When and why? Test it!
            # if (new_state not in history) and new_state.legal():

                frontiere.insert(0, new_state)  # it is a line (FIFO) => breadth first
                # frontiere.append(new_state)  # it is a pile (FILO) => deep first
        print("Iteration #{}".format(len(history)))

    print("History length: {}".format(len(history)))
    print("Frontiere length: {}".format(len(frontiere)))
    return None


if __name__ == '__main__':

    # few iterations
    taquin_easy = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    # about few hundred iterations
    taquin_medium = [
        [0, 1, 2],
        [7, 4, 3],
        [5, 8, 6]
    ]

    # about 140'000 iterations
    taquin_hard = [
        [4, 0, 2],
        [3, 5, 1],
        [6, 7, 8]
    ]

    taquin_impossible = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]

    final_values = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    init_state = taquin_easy

    result = search(State(init_state), final_values)
    if result is not None:
        print("Solution found!")
        winning_path = []
        while result.parent is not None:
            winning_path.insert(0, result)
            result = result.parent
        winning_path.insert(0, result)
        with TaquinViewerHTML('example.html') as viewer:
            for i, state in enumerate(winning_path):
                viewer.add_taquin_state(state.values, title=i)
    else:
        print("Solution not found!!")


