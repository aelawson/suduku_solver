"""
@title:         Suduku Puzzle Solver (in Python)
@author:        Andrew Lawson
@date:          6/27/14
"""

# Use NumPy to create multi-dim arrays
import numpy as ny
import math

# Backtracking implementation.
def backtrack(board, currentSpace, emptySpaces):
    # If the current partial solution is a complete solution, process it.
    if is_solution(board, emptySpaces):
        print_solution(board)
    else:
        # Otherwise, retrieve the next candidates and continue backtracking.
        currentSpace = emptySpaces[len(emptySpaces) - 1]
        candidates = next_candidates(board, currentSpace)
        # For each candidate, recursively step forward.
        for currentCandidate in candidates:
            board, emptySpaces = step_forward(currentCandidate, currentSpace, board, emptySpaces)
            backtrack(board, currentSpace, emptySpaces)
            # If solution is found, end the recursion
            if FINISHED:
                return
            board, emptySpaces = step_backward(currentSpace, board, emptySpaces)

# Function that determines if the given partial solution is a complete solution.
def is_solution(board, emptySpaces):
    global FINISHED
    if len(emptySpaces) == 0:
        FINISHED = True
        return True

# Function that prints the final solution of the board.
def print_solution(board):
    # Print the current solution
    print board

# Function that generates the next set of candidates for the current Suduku space.
def next_candidates(board, currentSpace):
    global BOARD_DIM
    global SQUARE_DIM
    # Set vars for the x and y components
    squareX = math.floor(currentSpace.x / SQUARE_DIM)
    squareY = math.floor(currentSpace.y / SQUARE_DIM)
    square = board[SQUARE_DIM * squareX:SQUARE_DIM * squareX + SQUARE_DIM,
        SQUARE_DIM * squareY:SQUARE_DIM * squareY + SQUARE_DIM]
    squareCandidates = []   
    # Find the candidate values in the current square
    for value in range(1, BOARD_DIM + 1):
        if value not in square:
            squareCandidates.append(value)
    # Find the candidate values in the current row and column: 
    column = board[currentSpace.x, :].astype(int).tolist()
    row = board[:, currentSpace.y].astype(int).tolist()
    boardCandidates = []
    for value in range(1, BOARD_DIM + 1):
        if value not in row and value not in column:
            boardCandidates.append(value)
    # Generate the intersection of the square and row / col candidates
    finalCandidates = [val for val in squareCandidates if val in boardCandidates]
    return finalCandidates

# Makes the next move - adds the candidate to the board
def step_forward(candidate, currentSpace, board, emptySpaces):
    # Add this candidate to the board solution
    board[currentSpace.x, currentSpace.y] = candidate
    emptySpaces.pop()
    return board, emptySpaces

# Undos the last move - returns current space to an empty one.
def step_backward(currentSpace, board, emptySpaces):
    # Remove last candidate from the board history
    board[currentSpace.x, currentSpace.y] = 0
    emptySpaces.append(currentSpace)
    return board, emptySpaces

# Defines an object representing a Suduku space - parameterized by x and y coordinates
# Contains getter and setter methods
class SudukuSpace(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def y(self):
        return self._y   
    @y.setter
    def y(self, value):
        self._y = value

# Main function. Takes a file containing a Suduku delimited by commas and new lines.
def solve_suduku(filename):
    global SQUARE_DIM
    global BOARD_DIM
    # Initialize board with empty spaces
    board = ny.zeros((BOARD_DIM, BOARD_DIM))
    # Reads a puzzle and populates the board
    with open(filename, 'r') as file:
        for row, line in enumerate(file):
            spaces = line.split(",")
            for col, value in enumerate(spaces):
                board[row, col] = value
    # Initialize empty spaces with SudukuSpaces
    emptySpaces = []
    for x in range(0, BOARD_DIM):
        for y in range (0, BOARD_DIM):
            if board[x, y] == 0:
                newSpace = SudukuSpace(x, y)
                emptySpaces.append(newSpace)
    # Intialize backtracking / recursive search
    # Intialize null current space
    currentSpace = None
    backtrack(board, currentSpace, emptySpaces)

# Global vars
SQUARE_DIM = 3
BOARD_DIM = 9
FINISHED = False
# Get puzzle file name from user
puzzleFile = raw_input('Please enter the puzzle filename (with .txt ext): ')
# Call solver
solve_suduku(puzzleFile)
