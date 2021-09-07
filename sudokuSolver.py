import os
import numpy as np
import copy

filePath, fileName = "D:\python code\sudoku", "example.txt"
file = open(os.path.join(filePath,fileName))

board = np.loadtxt(os.path.join(filePath,fileName),dtype="int64")

def setBlockToZero(board,num):
    colSplit = 3 * ((num-1) % 3)
    rowSplit = 3 * ((num-1) // 3)
    board[rowSplit:rowSplit+3,colSplit:colSplit+3] = np.zeros((3,3))
    return board

def blockContains(board,num,element):
    colSplit = 3 * ((num-1) % 3)
    rowSplit = 3 * ((num-1) // 3)
    subset = board[rowSplit:rowSplit+3,colSplit:colSplit+3].copy()
    if element in subset:
        return True
    else:
        return False

def blockSubZero(board,num):#1 to 9
    colSplit = 3 * ((num-1) % 3)
    rowSplit = 3 * ((num-1) // 3)
    subset = board[rowSplit:rowSplit+3,colSplit:colSplit+3].copy()
    L = list(subset.reshape(1,9)[0])
    return list(L).count(0)
    
def zeroCount(board,row,col):
    if board[row,col] == 0:
        rCount = list(board[row]).count(0)
        cCount = list(board[:,col]).count(0)
        num = 3*(row//3) + col//3
        bCount = blockSubZero(board, num+1)
        count = bCount+rCount+cCount
    else:
        count = 100
    return count

def rowMiss(board,row): # row = 0 to 8
    numbers = set(range(1,10))
    Row = set(board[row])
    
    if 0 in Row:
        Row.remove(0)
    else:
        return set()
       
    missing = numbers - Row
    return missing

def colMiss(board,col):
    numbers = set(range(1,10))
    column = set(board[:,col])
    
    if 0 in column:
        column.remove(0)
    else:
        return set()
    
    missing = numbers - column
    return missing

def blockMiss(board,block):
    numbers = set(range(1,10))
    colSplit = 3 * ((block-1) % 3)
    rowSplit = 3 * ((block-1) // 3)
    subset = board[rowSplit:rowSplit+3,colSplit:colSplit+3].copy()
    subset = set(subset.reshape(1,9)[0])
    
    if 0 in subset:
        subset.remove(0)
    else:
        return set()
    
    missing = numbers - subset
    return missing

def cellOptions(board,row,col):
    num = 3*(row//3) + col//3
    if board[row,col] > 0:
        return set()
    return rowMiss(board,row).intersection(colMiss(board,col)).intersection(blockMiss(board,num+1))
        

def rowOptions(board,row):
    rows = []
    for col in range(9):
        rows.append(cellOptions(board, row, col))
    return rows

def rowContains(row,element):
    if element in row:
        return True
    else:
        return False

def oneBlock(board,num): #used only for completeBoard method
    colSplit = 3 * ((num-1) % 3) #checks for unique values of 1 in sub block
    rowSplit = 3 * ((num-1) // 3)
    subset = board[rowSplit:rowSplit+3,colSplit:colSplit+3].copy()
   
    if 1 in subset:
        if list(subset.reshape(1,9)[0]).count(1) == 1:
            #print(list(subset.reshape(1,9)[0]))
            return True
        else:
            return False
    else:
        return False

def completeBoard(board):
    
    for element in range(1,10):
        matrix = np.ones((9,9),dtype="int64")
        for num in range(1,10):
            
            if blockContains(board, num, element):
                matrix = setBlockToZero(matrix, num)
          
        for row in range(9):
            if element in board[row]:
                matrix[row] = np.zeros((1,9))
        
        for col in range(9):
            if element in board[:,col]:
                matrix[:,col] = np.zeros((1,9))
       
        for row in range(9):
            for col in range(9):
                if matrix[row,col] == 1 and board[row,col] > 0:
                    matrix[row,col] = 0
        #print(matrix);print()
        for num in range(1,10):
            if not oneBlock(matrix, num):
                matrix = setBlockToZero(matrix, num)
                
        # set the ones in matrix = to element in board
       
        for row in range(9):
            for col in range(9):
                if matrix[row,col] == 1:
                    board[row,col] = element
               
    return board
        
def minZeroes(board):

    matrix = np.ones((9,9),dtype="int64")
    coords = []
    for row in range(9):
        for col in range(9):
            matrix[row,col] = zeroCount(board,row,col)
           
    for row in range(9):
        for col in range(9):
            if matrix[row,col] == matrix.min():
                coords.append((row,col))
                
    return coords
       
def singleton(arr): #returns the singletons with index in array
    L = dict()
    for num in range(len(arr)):
        if len(arr[num]) == 1:
            L[list(arr[num])[0]] = num
    return L        

def function(board,n=1000):
    initialStart = minZeroes(board)
    
    if n == 1:
        if 0 in board:
            print("board not solved\n")
        return board
    
    for start in initialStart:
        row,col = start[0],start[1]
       
        for i in range(9):
             rowChoices = rowOptions(board, row)
             answers = singleton(rowChoices)
             for key in answers:
                 board[row,answers[key]] = key
             if len(answers) == 0:
                 break
    mat = np.matrix.transpose(board)
    initialStart = minZeroes(mat)
    for start in initialStart:
        row = start[0]
        for i in range(9):
              rowChoices = rowOptions(mat, row)
              answers = singleton(rowChoices)
              for key in answers:
                  mat[row,answers[key]] = key
              if len(answers) == 0:
                  break
    board = np.matrix.transpose(mat)   
    if 0 in board:
       board = completeBoard(board)
       return function(board,n-1)
    else:
        return board

board = function(board)
print(board)
print()