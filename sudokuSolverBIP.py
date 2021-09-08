from pulp import *
import numpy as np
from termcolor import colored

filePath, fileName = "D:\python code\sudoku", "example.txt" #change to meet your needs
board = np.loadtxt(os.path.join(filePath,fileName),dtype="int64")
solver = LpProblem("solver",LpMaximize)

rows = range(9)
cols = range(9)
numbers = range(1,10)

X = np.array(LpVariable.matrix("X", (numbers,rows,cols),0,1,cat='Integer'))

for r in rows:
    for c in cols:
        for n in numbers:
            if board[r,c] == n:
                X[n-1,r,c] = 1
                
solver += 0

for r in rows: #uniqueness of numbers
    for c in cols:
        solver.addConstraint(LpConstraint(e=lpSum([X[n-1,r,c] for n in numbers]),rhs=1))

for n in numbers: #uniqueness of rows
    for r in rows:
        solver.addConstraint(LpConstraint(e=lpSum([X[n-1,r,c] for c in cols]),rhs=1))
            
for n in numbers: #uniqueness of columns
    for c in cols:
        solver.addConstraint(LpConstraint(e=lpSum([X[n-1,r,c] for r in rows]),rhs=1))
        
for num in range(1,10): #uniqueness of block sums
    colSplit = 3 * ((num-1) % 3)
    rowSplit = 3 * ((num-1) // 3)
    for n in numbers:
        solver.addConstraint(LpConstraint(e=lpSum(X[n-1,rowSplit:rowSplit+3,colSplit:colSplit+3]),rhs=1))
    
solver.solve()
boardF = board.copy()
for n in numbers:
    for r in rows:
        for c in cols:
             if int(value(X[n-1,r,c])) == 1:
                    boardF[r,c] = n
            
def printBoard():
    global board
    global boardF
    
    print("\nsolved values are green\ngiven values are white\n")
    
    for r in range(9):
        for c in range(9):
            if board[r,c] == boardF[r,c]:
                print(board[r,c],end=" ")
            else:
                print(colored(boardF[r,c],"green",attrs=['bold']),end = " ")
        print()
        
printBoard()
