from pulp import *
import numpy as np

filePath, fileName = "D:\python code\sudoku", "example.txt"
file = open(os.path.join(filePath,fileName))

board = np.loadtxt(os.path.join(filePath,fileName),dtype="int64")
print(board,"\n")

solver = LpProblem("solver",LpMaximize)

rows = range(9)
cols = range(9)
#prob += 2*x1 + x2 <= 100
X = LpVariable.dicts("X", (rows,cols),1,9,cat='Integer')

for row in range(9):
    for col in range(9):
        if board[row][col] != 0:
            X[row][col] = board[row,col]

solver.setObjective(lpSum(0))

for r in range(9):
    solver.addConstraint(LpConstraint(e=lpSum([X[r][c] for c in cols]),rhs=45))
    
for c in cols:
    solver.addConstraint(LpConstraint(e=lpSum([X[r][c] for r in rows]),rhs=45))
    
for num in range(1,10):
    colSplit = 3 * ((num-1) % 3)
    rowSplit = 3 * ((num-1) // 3)
    solver.addConstraint(LpConstraint(lpSum(X[rowSplit+r][colSplit+c] for r in range(3) for c in range(3)),rhs=45))
    

solver.solve()
elements = solver.variables()

count = 0
for row in range(9):
    for col in range(9):
        if board[row,col] == 0:
            board[row,col] = int(value(elements[count]))
            count += 1

print(board)