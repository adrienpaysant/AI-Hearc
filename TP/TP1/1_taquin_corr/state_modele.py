from copy import deepcopy


class State(object):

    def __init__(self, values, parent=None):
        self.values = values
        self.parent = parent

    def legal(self):
        return True

    def final(self, final_values):
        return self.values == final_values

    # Explain why the following three methods are needed
    def __hash__(self):
        return str(self).__hash__()

    def __str__(self):
        return str(self.values)

    def __eq__(self, other):
        return self.values == other.values

    @staticmethod
    def where_is_x(values, x=0):
        for i, line in enumerate(values):
            for j, elem in enumerate(line):
                if elem == x:
                    return i, j

    @staticmethod
    def swap(values, x1, y1, x2, y2):
        new_values = deepcopy(values)
        new_values[x1][y1], new_values[x2][y2] = new_values[x2][y2], new_values[x1][y1]
        return new_values

    # list of new values after the application of possible operators
    def applicable_operators(self):
        ops = []
        line_len = len(self.values)  # number of lines
        column_len = len(self.values[0])  # number of columns

        i, j = State.where_is_x(self.values)
        if i > 0:  # it is possible to swap with the line above
            ops.append(self.swap(self.values, i, j, i - 1, j))
        if i < line_len - 1:  # it is possible to swap with the line below
            ops.append(self.swap(self.values, i, j, i + 1, j))
        if j > 0:  # it is possible to swap with the column on the left
            ops.append(self.swap(self.values, i, j, i, j - 1))
        if j < column_len - 1:  # it is possible to swap with the column on the right
            ops.append(self.swap(self.values, i, j, i, j + 1))
        return ops

    def apply(self, op):
        return State(op, self)
