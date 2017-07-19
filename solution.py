import numpy as np
from itertools import combinations

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(a, b):
    return [ s + t for s in a for t in b ]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = [ ]
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[ s ]) for s in boxes)
    line = '+'.join([ '-' * (width * 3) ] * 3)
    for r in rows:
        print(''.join(values[ r + c ].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            if len(values[peer]) > 1:
                #values[peer] = values[peer].replace(digit,'')
                values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


import numpy as np


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    two_digits = [ box for box in values.keys() if len(values[ box ]) == 2 ]
    for unit in unitlist:
        if len(np.intersect1d(unit, two_digits)) > 1:
            possible_twins = combinations(np.intersect1d(unit, two_digits), 2)
            for a, b in possible_twins:
                if values[ a ] == values[ b ]:

                    # Eliminate the naked twins as possibilities for their peers
                    others = np.setdiff1d(unit, [ a, b ])
                    twin_digits = values[ a ]
                    for box in others:
                        for d in twin_digits:
                            if len(values[ box ]) > 1:
                                # values[box] = values[box].replace(d, "")
                                values = assign_value(values, box, values[ box ].replace(d, ""))
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([ box for box in values.keys() if len(values[ box ]) == 1 ])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([ box for box in values.keys() if len(values[ box ]) == 1 ])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([ box for box in values.keys() if len(values[ box ]) == 0 ]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False  ## Failed earlier

    if all(len(values[ s ]) == 1 for s in boxes):
        if all([ len(np.unique([ values[ k ] for k in unit ])) == 9 for unit in unitlist ]):
            return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    try:
        n, s = min((len(values[ s ]), s) for s in boxes if len(values[ s ]) > 1)
    except:
        return False

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[ s ]:
        new_sudoku = values.copy()
        new_sudoku[ s ] = value
        new_sudoku = reduce_puzzle(new_sudoku)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    values = grid_values(grid)
    reduced = reduce_puzzle(values)
    results = search(reduced)
    if np.sum([len(results[k]) for k, v in results.items()]) == 81:
        return results
    else:
        return False


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')