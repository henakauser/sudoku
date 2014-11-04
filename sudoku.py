#!/usr/bin/env python
"""Sudoku solver"""

#
# author: Hena Kauser
# license: MIT
#
# Terminology
# puzzle: The Sudoku input is the puzzle that must be solved
# board:  The playing board which is a grid of 9 rows and 9 columns. The grid is
#         where the puzzle is solved and may represent a newly initialized
#         board, an in process game, or a completed solution.
# square: An individual square on the board.
# row:    9 horizontal squares.
# column: 9 vertical squares.
# box:    9 3x3 squares (each box has 9 squares).
# unit:   The row, column and box that contain a square.
#
# board dictionary keys
# A1 A2 A3 | A4 A5 A6 | A7 A8 A9
# B1 B2 B3 | B4 B5 B6 | B7 B8 B9
# C1 C2 C3 | C4 C5 C6 | C7 C8 C9
# ---------+----------+---------
# D1 D2 D3 | D4 D5 D6 | D7 D8 D9
# E1 E2 E3 | E4 E5 E6 | E7 E8 E9
# F1 F2 F3 | F4 F5 F6 | F7 F8 F9
# ---------+----------+---------
# G1 G2 G3 | G4 G5 G6 | G7 G8 G9
# H1 H2 H3 | H4 H5 H6 | H7 H8 H9
# I1 I2 I3 | I4 I5 I6 | I7 I8 I9
#
# Quality checks (compliant per PEP8):
# pylint sudoku.py
#
# How to run:
# python sudoku.py -i test.csv -o out_test.csv
#

import argparse
import csv


def load_puzzle(input_file):
    """Return the Sudoku puzzle as a dictionary"""
    puzzle = []
    for row in csv.reader(input_file):
        for column in row:
            puzzle.append(column)
    return dict(zip(SQUARES, puzzle))


def save_solution(solution, output_file):
    """Save the Sudoku solution to a CSV file"""
    # The following 2 lines could be collapsed to a single line, however 2 lines
    # is easier to read:
    # (csv.writer(output_file, delimiter=',')).writerows(solution)
    writer = csv.writer(output_file, delimiter=',')
    writer.writerows(solution)


def getopts():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=argparse.FileType('r'),
                        required=True, help="input file (.csv)")
    parser.add_argument("-o", "--output", type=argparse.FileType('w'),
                        required=True, help="output file (.csv)")
    return parser.parse_args()


def generate_list(iterable_a, iterable_b):
    """Return a list of a+b combinations"""
    result = []
    for iter_a in iterable_a:
        for iter_b in iterable_b:
            result.append(iter_a+iter_b)

    return result


def generate_board():
    """Initialize and return the default board with A1...I9 squares with each
    square's value set to 123456789."""
    return dict((s, ALLOWED_NUMBERS) for s in SQUARES)


def test():
    """Unit tests"""
    # 9x9
    assert len(SQUARES) == 81
    # 9 rows, 9 columns, 9 units
    assert len(UNIT_LIST) == 27
    # each square has 3 units: row, column, box
    assert all(len(UNITS[s]) == 3 for s in SQUARES)
    # each square has 20 peers
    assert all(len(PEERS[s]) == 20 for s in SQUARES)
    assert UNITS['A1'] == [
        ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'],
        ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
        ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert UNITS['F5'] == [
        ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'],
        ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'],
        ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6']]
    assert PEERS['A1'] == {'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                           'B1', 'B2', 'B3',
                           'C1', 'C2', 'C3',
                           'D1', 'E1', 'F1', 'G1', 'H1', 'I1'}
    assert PEERS['F5'] == {'F1', 'F2', 'F3', 'F4', 'F6', 'F7', 'F8', 'F9',
                           'D4', 'D5', 'D6',
                           'E4', 'E5', 'E6',
                           'A5', 'B5', 'C5', 'G5', 'H5', 'I5'}
    print 'Test results: pass'

ALLOWED_NUMBERS = '123456789'

# row labels
ROWS = 'ABCDEFGHI'

# column numbers
COLS = ALLOWED_NUMBERS

# list of all square labels
SQUARES = generate_list(ROWS, COLS)

# list of all units
# 1. rows
# 2. columns
# 3. units
# (
#   [A1...I1], [A2...I2]...[A9...I9],
#   [A1...A9], [B1...B9]...[I1...I9],
#   [A1, A2, A3...C1, C2, C3]....[G7, G8, G9...I7, I8, I9]
# )
UNIT_LIST = ([generate_list(ROWS, c) for c in COLS] +
             [generate_list(r, COLS) for r in ROWS] +
             [generate_list(rowUnit, colUnit)
                 for rowUnit in ('ABC', 'DEF', 'GHI')
                 for colUnit in ('123', '456', '789')])

# dictionary of all units associated with a square where each unit contains:
# - row
# - column
# - box
# ex: UNITS['A1'] = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
#                    ['A1',
#                     'B1',
#                     'C1',
#                     'D1',
#                     'E1',
#                     'F1',
#                     'G1',
#                     'H1',
#                     'I1'],
#                    ['A1', 'A2', 'A3',
#                     'B1', 'B2', 'B3',
#                     'C1', 'C2', 'C3']]
#for s in SQUARES:
UNITS = dict((s, [u for u in UNIT_LIST if s in u]) for s in SQUARES)

# dictionary of all peers associated with a square
# Each key is a square and the value is the set of all peers
# ex: sorted(PEERS['A1']) = set([
#         'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
#   'B1', 'B2', 'B3',
#   'C1', 'C2', 'C3',
#   'D1',
#   'E1',
#   'F1',
#   'G1',
#   'H1',
#   'I1'])
#
PEERS = dict((s, set(sum(UNITS[s], [])) - set([s])) for s in SQUARES)


def propagate_constraints(puzzle, board):
    """Update board based on local consistency conditions defined in
    remove_value(). Start by assigning the values provided by puzzle."""
    for square, value in puzzle.items():
        if value in ALLOWED_NUMBERS and not assign_value(board, square, value):
            # Send failure up the call stack
            return False
    return board


def assign_value(board, square, value):
    """Assign value to square by deleting all values other than value from
    board[square]. Then delete value from all other squares in this
    square's unit."""
    values_to_eliminate = board[square].replace(value, '')
    if all(remove_value(board, square, val) for val in values_to_eliminate):
        return board
    else:
        # Push failure up the call stack
        return False


def remove_value(board, square, value_to_eliminate):
    """Delete value from board[square].

    Local consistency conditions:
    1. If a square has only one possible value then remove value from peers
    2. If only one square in a unit can have a value then assign the value to
    that square"""

    # Return immediately if the value to eliminate has already been removed
    # from board[square]
    if value_to_eliminate not in board[square]:
        return board

    # Remove value_to_eliminate from board[square]'s possible values
    board[square] = board[square].replace(value_to_eliminate, '')

    # 1) If the square has only one value, then remove the values from all of
    #    square's peers.
    if len(board[square]) == 0:
        # board[square] has no values, therefore we cannot solve the puzzle
        return False
    elif len(board[square]) == 1:
        # If board[square] has only one value left (ie this is the only possible
        # value for board[square]), then recursively remove this value from all
        # of board[square]'s peers.
        final_value = board[square]
        if not all(remove_value(board, peer, final_value)
                   for peer in PEERS[square]):
            # Push failure up the call stack if we were not able to remove
            # board[square]'s final value from it's peers.
            return False

    # 2) If there is only one square within a unit where a value can be set,
    #    then set that square to the value. Each square's unit consists of a
    #    row, column and box. Therefore, this loop iterates 3 times per square.
    for unit in UNITS[square]:
        # unit_squares is a list of all square's in the current square's unit
        # that contain value_to_eliminate
        unit_squares = [sq for sq in unit if value_to_eliminate in board[sq]]
        if len(unit_squares) == 0:
            # Push failure up the call stack. This is a failure b/c no member of
            # the unit contains value_to_eliminate which violates the constraint
            # that each of ALLOWED_NUMBERS must be in exactly 1 square within
            # each unit.
            return False
        elif len(unit_squares) == 1:
            # value_to_eliminate can only be in one square in the unit, which
            # is where we will assign value_to_eliminate.
            if not assign_value(board, unit_squares[0], value_to_eliminate):
                return False
    return board


def depth_first_search(board):
    """Depth first search. First, find a square with the fewest remaining
    values, then try to assign each value and check if we found a solution."""
    if board is False:
        return False

    # Puzzle has already been solved, so return the solution.
    if all(len(board[square]) == 1 for square in SQUARES):
        return board

    # dummy is min_value, but used 'dummy' as var name to prevent pylint warning
    dummy, min_square = min((len(board[sq]), sq) for sq in SQUARES
                            if len(board[sq]) > 1)

    # Check if all constraints can be satisfied for each remaining value in
    # min_square. The calls below eventually pass an iterable to
    # extract_solution() where all items = False except for the solution.
    return extract_solution(depth_first_search(assign_value(board.copy(),
                                                            min_square,
                                                            value))
                            for value in board[min_square])


def extract_solution(search_results):
    """Return the solved Sudoku board from the list of results returned by
    depth_first_search()."""
    for result in search_results:
        if result:
            return result

    return False


def dict_to_2d_list(solution):
    """Convert board dictionary to a two-dimensional list"""
    solution_list = []
    for row in ROWS:
        row_solution = []
        for col in COLS:
            row_solution.append(solution[row+col])
        solution_list.append(row_solution)

    return solution_list


if __name__ == '__main__':
    test()

    CLI_ARGS = getopts()

    PUZZLE = load_puzzle(CLI_ARGS.input)

    DEFAULT_BOARD = generate_board()

    SOLUTION = depth_first_search(propagate_constraints(PUZZLE, DEFAULT_BOARD))

    if SOLUTION is not False:
        save_solution(dict_to_2d_list(SOLUTION), CLI_ARGS.output)
    else:
        print 'Unable to find solution to Sudoku puzzle.'
