##
##	Title:	Suduku Puzzle Solver (in Python)
##	Author: Andrew Lawson
##	Date:	6/27/14

# Use NumPy to create multi-dim arrays
import numpy as ny
import math

# Generic implementation of a backtrack algorithm.
def backtrack(board, currentSpace, emptySpaces):
	# If the current partial solution is a complete solution, process it.
	if isSolution(board, emptySpaces):
		printSolution(board)
	else:
		# Otherwise, retrieve the next candidates and continue backtracking.
		currentSpace = emptySpaces[len(emptySpaces) - 1]
		candidates = nextCandidates(board, currentSpace)
		# For each candidate, recursively step forward.
		for currentCandidate in candidates:
			board, emptySpaces = stepForward(currentCandidate, currentSpace, board, emptySpaces)
			backtrack(board, currentSpace, emptySpaces)
			board, emptySpaces = stepBackward(currentSpace, board, emptySpaces)

# Function that determines if the given partial solution is a complete solution.
def isSolution(board, emptySpaces):
	if len(emptySpaces) == 0:
		return True

# Function that prints the final solution of the board.
def printSolution(board):
	# Print the current solution
	print board
	return

# Function that generates the next set of candidates for the current Suduku space.
def nextCandidates(board, currentSpace):
	global boardDim
	global squareDim
	# Set vars for the x and y components
	spaceX = currentSpace.getX()
	spaceY = currentSpace.getY()
	squareX = math.floor(spaceX / squareDim)
	squareY = math.floor(spaceY / squareDim)
	square = board[squareDim * squareX:squareDim * squareX + squareDim, squareDim * squareY:squareDim * squareY + squareDim]
	squareCandidates = []	
	# Find the candidate values in the current square
	for value in range(1, boardDim + 1):
		if value not in square:
			squareCandidates.append(value)
	# Find the candidate values in the current row and column: 
	column = board[spaceX, :].astype(int).tolist()
	row = board[:, spaceY].astype(int).tolist()
	boardCandidates = []
	for value in range(1, boardDim + 1):
		if value not in row and value not in column:
			boardCandidates.append(value)
	# Find the intersection of the square and row / col candidates and return them
	finalCandidates = [val for val in squareCandidates if val in boardCandidates]
	return finalCandidates
		
# Makes the next move - adds the candidate to the board
def stepForward(candidate, currentSpace, board, emptySpaces):
	# Add this candidate to the board solution
	board[currentSpace.getX(), currentSpace.getY()] = candidate
	emptySpaces.pop()
	return board, emptySpaces

# Undos the last move - returns current space to an empty one.
def stepBackward(currentSpace, board, emptySpaces):
	# Remove last candidate from the board history
	board[currentSpace.getX(), currentSpace.getY()] = 0
	emptySpaces.append(currentSpace)
	return board, emptySpaces

# Defines an object representing a Suduku space - parameterized by x and y coordinates
# Contains getter and setter methods
class sudukuSpace():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def setX(self, value):
		self.x = value
	def setY(self, value):
		self.y = value

# Main function. Takes a file containing a Suduku delimited by commas and new lines.
def solveSuduku(filename):
	global squareDim
	global boardDim
	# Initialize board with empty spaces
	board = ny.zeros((boardDim, boardDim))
 	# Reads a puzzle and populates the board
	file = open(filename, "r")
	rowNum = 0
	for line in file:
		digitList = line.split(",")
		colNum = 0
		for digit in digitList:
			board[rowNum, colNum] = digit
			colNum += 1
		rowNum += 1	
	file.close()
	# Initialize empty spaces with sudukuSpaces
	emptySpaces = []
	for x in range(0, boardDim):
		for y in range (0, boardDim):
			if board[x, y] == 0:
				newSpace = sudukuSpace(x, y)
				emptySpaces.append(newSpace)
	# Intialize backtracking / recursive search
	# Intialize null current space
	currentSpace = None
	backtrack(board, currentSpace, emptySpaces)

# Execution code
squareDim = 3
boardDim = 9
solveSuduku("puzzle.txt")