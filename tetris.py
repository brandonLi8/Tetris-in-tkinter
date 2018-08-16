import copy, random ,time#Tetris
from tkinter import * 
def makeboard(data,row,col): #this function sets up the checkerboard backround 
    board =[ ([0] * data.cols) for row in range(data.rows) ] #empty 2d list
    for row in range(0,data.rows):
        for col in range(0,data.cols):#the even row+col of checker board are 
        #different color
            if (row+col)%2 == 0:#evens
                board[row][col] = data.emptyColor[0] #fill in the board with the
                # first empty color
            else:#odds
                board[row][col] = data.emptyColor[1]#fill in the board with the 
                #second empty color     
    return board

#These pieces are in the defualt position according to tetris wiki. 
#http://tetris.wikia.com/wiki/SRS
iPiece = [[False,False,False,False],[True, True, True, True], 
            [False,False,False,False], [False,False,False,False]]
jPiece = [[  True, False, False ],[  True,  True,  True ],[False,False,False]]
lPiece = [[ False, False, True ],[  True,  True,  True ],[False,False,False]]
oPiece = [[  True,  True ],[  True,  True ]]
sPiece = [[ False,  True,  True ],[  True,  True, False ],[False,False,False]]
tPiece = [[ False,  True, False ],[  True,  True,  True ],[False,False,False]]
zPiece = [[  True,  True, False ],[ False,  True,  True ],[False,False,False]]
tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
#the piece colors and border colors correspond with tetris pieces
tetrisPieceColors = [ '#%02x%02x%02x'%(0,162,224), "royalblue3", "darkorange2",
         "darkgoldenrod1", "limegreen", "hotpink3", '#%02x%02x%02x'%(220,20,60)] 
borderColors = [ "dodgerblue3", "blue4", "Tomato4", "darkgoldenrod4", "green4", 
                                                    "darkorchid4", "orangered4"]
#returns a list of len 7 with the correct pieces
def generatePieces(): #this function will generate all the pieces for the game,
# how it works is: it takes  7 pieces, scrambles this, uses them, onces there 
# are 0 pieces, re gather the 7 pieces, then rescramble and use them, then re do 
# this so you get a piece maximum every 14   
    currentResult = [] 
# the current result is the scrambled pieces, then once scrambled, 
#add to the result 
    result = [] 
    # all the pieces in the end in a list
    #once all the pieces are used,
    # or there aren't any pieces left, I re generate pieces
    while len(currentResult) != len(tetrisPieces):  #this while loop scrambles 
    #the. different pieces
        current = random.randrange(len(tetrisPieces))
        if tetrisPieces[current] not in currentResult:
            currentResult.append(tetrisPieces[current])
    for i in range(len(currentResult)): # add each element to the result 
        result.append(currentResult[i])
    currentResult = []#reset
    return result
def init(data):
 data.gamePieces = generatePieces()   #list of all the pieces
 data.rows,  data.cols,  data.margin = 21, 10, 100#boarddimensions and margin
 data.emptyColor = ("grey14","grey16")#empty colors for the checker board 
 data.board = makeboard(data,data.rows,data.cols)# make the board 
 data.tetrisPieces,  data.tetrisPieceColors,  data.borderColors =tetrisPieces,  tetrisPieceColors,  borderColors#defined above
 data.fallingPiece,  data.fallingColor,  data.fallingBorderColor = -1,  -1,  -1#it is -1 because there isn't a falling piece now, but will be changed to the piece when the game starts
 data.firstPiece = newFallingPiece(data)#this is just to generate the first piece
 data.fallingPieceRow,  data.fallingPieceCol = 0,  data.cols // 2 *0.75 -0.75#this is the default position, spawns in the middle top
 data.ghostPiece,  data.ghostPieceRow ,  data.ghostPieceCol= [],  0,  0 # this is the ghost piece defined for tellling the player where the block will land
 data.fallingOrientation = 0 # this is the orientation of the falling piece
 data.delayToGoDownOneTile = 0   #this is the count needed to delay going down one
 data.delayToPlace = 0#this is the count needed to delay to place
 data.delay,  data.isGameOver,  data.firstMove,  data.holdDenied,  data.holdAvailable,  data.paused,  data.helpMode = False,False,True,False,False,False,False
 data.beginningCount,  data.beginningDelay = 0,  3
 data.level,  data.levelDelay,  data.score,  data.rowsCleared,  data.rowsClearedDelay,  data.highestScore = 0,  0,  0,  0,  0,  0,
 data.holdPiece ,  data.holdCount,  data.holdAvailableCount,  data.holdDeniedCount = 0,  0,  0,  0 
 data.doubleTetris = False
 data.doubleList = []#this will be a list of the runs at a tetris so i can tell if there is a double tetris
 data.run = 0 #how many runs have been played
 data.addScore = False #this is True if there is a double tetris and there is a need for a bonus
 data.backroundOn = False #turn the galaxy on
 data.drawCheck = False #this is for the button to turn the backround on
 data.frames = 0
def newFallingPiece(data): #this creates the next falling piece, sets the colors
    data.fallingPiece = data.gamePieces[0] #already generated
    current = data.tetrisPieces.index(data.fallingPiece)#needed to set colors
    data.fallingColor = data.tetrisPieceColors[current]
    data.fallingBorderColor = data.borderColors[current]
    data.fallingPieceRow = 0
    if len(data.fallingPiece)==4 : #the i piece needs to be spawned higher 
        data.fallingPieceRow = -1
    data.fallingPieceCol = data.cols // 2 *0.75 -0.75 #spawn in the middle
    data.fallingOrientation  = 0 #the rotation is in the default at first
    data.gamePieces.pop(0) #get rid of the first item for the next piece
    # if not(fallingPieceIsLegal(data)):#check right away for it the game is over
    #     data.isGameOver = True
def removeFullRows(data): #this function removes the full rows and scores the 
#appropriate points
    current = []
    result =[]
    scorePoints(data) #this scores the points
    for i in range(len(data.board)):    #this takes an intresting approach: 
#I copy all the rows that have color and 
#I dont copy all the rows that have nothing or are completly full     
#then i can add this to a new board and this affectively clears the full rows
        if isColoredRow(data.board[i],data):
            current = copy.deepcopy(data.board[i])
            result.append(current)    
    data.board = makeboard(data,data.rows,data.cols)
    for i in range(len(result)):
        data.board[len(data.board)-i-1] = result[len(result)-i-1] #removes the full rows
def isColoredRow(row,data): #this function returns True if the row has a block in it
# that isn't the empty color, but also returns False if the entire row is filled.
#the reasson that i do this is to copy all the rows that aren't filled when clearing rows filled
    colors = tetrisPieceColors
    for j in range(0,len(row)):
        if (row.count(data.emptyColor[0]) ==5 and row.count(data.emptyColor[1]) ==5): #there is all empty color means completly empty
            return False
        if (row.count(data.emptyColor[0]) ==0 and row.count(data.emptyColor[1]) ==0): #there is no empty color means completly filled
            return False
        if row[j] in colors:
            return True
    return False 

def howManyRowsCleared(data): #This returns the amount of rows cleared
    count = 0
    for i in range(0, len(data.board)):  
        if (data.emptyColor[1] not in data.board[i] and data.emptyColor[0] not in data.board[i]) :
            count += 1
    return count
     
def scorePoints(data):      
    count = howManyRowsCleared(data)
    data.rowsCleared = count
    if data.rowsCleared == 4:
        data.doubleList.append(data.run)#add this to detect if we neeed a double tetris bonus
    if data.rowsClearedDelay > 12: #this is to reset the timer for the message that pops up
        data.rowsClearedDelay = 0
    n = data.level
    if count == 1:
        data.score += 4 * (n + 1)
    if count == 2:
        data.score += 10 * (n + 1)
    if count == 3:
        data.score += 30 * (n + 1)
    if count == 4:
        data.score += 120 * (n + 1)
    if data.score > data.highestScore:     
        data.highestScore = data.score      #scores the points, also tells what message to put

def doubleTetris(data):
    if len(data.doubleList) >= 2 and data.doubleList[len(data.doubleList)-1] - data.doubleList[len(data.doubleList)-2] == 1: #double list is the runs so if you subtract and get 1 then two tetris' occured back to back
        data.doubleTetris = True
        data.addScore = True
        data.doubleList.append(-1)
    if data.addScore:
        data.score += (data.level + 1) *50
        data.addScore = False

def drawRowsCleared(canvas,data): #draws the message of how many rows cleared
    doubleTetris(data)
    if data.rowsClearedDelay <=12 and data.rowsClearedDelay != 0: 
        if data.rowsCleared == 1:
            canvas.create_text(78+2.5 ,data.height-150,text = "Single!", font=('Comic Sans MS', '30', 'bold italic'),fill = "black")
            canvas.create_text(78 ,data.height-150,text = "Single!", font=('Comic Sans MS', '30', 'bold italic'),fill = "cyan2")
        elif data.rowsCleared == 2:
            canvas.create_text(78+2.5 ,data.height-150,text = "Double!", font=('Comic Sans MS', '33', 'bold italic'),fill = "black")
            canvas.create_text(78 ,data.height-150,text = "Double!", font=('Comic Sans MS', '33', 'bold italic'),fill = "orange")
        elif data.rowsCleared == 3:
            canvas.create_text(78+2.5 ,data.height-150,text = "Triple!", font=('Comic Sans MS', '33', 'bold italic'),fill = "black")
            canvas.create_text(78 ,data.height-150,text = "Triple!", font=('Comic Sans MS', '33', 'bold italic'),fill = "green")
        elif data.doubleTetris == True:
            canvas.create_text(68 +1.8 -8,data.height-160+5,text = "    GG\nDOUBLE", font=('Ariel', '25', 'bold '), )
            canvas.create_text(20 +1.8 +2,data.height-130+5,text = "\nT", font=('Ariel', '28', 'bold '),)
            canvas.create_text(20 +1.8 +2,data.height-130+5,text = "\n    E", font=('Ariel', '28', 'bold '),)
            canvas.create_text(20 +1.8+2,data.height-130+5,text = " \n       T", font=('Ariel', '28', 'bold '),)
            canvas.create_text(20 +1.8+2,data.height-130+5,text = " \n           R", font=('Ariel', '28', 'bold '),)
            canvas.create_text(16 +1.8+2,data.height-130+5,text = " \n               I", font=('Ariel', '28', 'bold '))
            canvas.create_text(12 +1.8+2,data.height-130+5,text = " \n                   S", font=('Ariel', '28', 'bold '),)
            canvas.create_text(68-8 ,data.height-160+5,text = "    GG\nDOUBLE", font=('Ariel', '25', 'bold '),fill = "Green",)
            canvas.create_text(20+2 ,data.height-130+5,text = "\nT", font=('Ariel', '28', 'bold '),fill = "fireBrick2",)
            canvas.create_text(20+2 ,data.height-130+5,text = "\n    E", font=('Ariel', '28', 'bold '),fill = "orange")
            canvas.create_text(20+2 ,data.height-130+5,text = "\n        T", font=('Ariel', '28', 'bold '),fill = "yellow",)
            canvas.create_text(20+2 ,data.height-130+5,text = "\n            R", font=('Ariel', '28', 'bold '),fill = "green",)
            canvas.create_text(16+2 ,data.height-130+5,text = "\n                I", font=('Ariel', '28', 'bold '),fill = "cyan2",)
            canvas.create_text(12+2 ,data.height-130+5,text = " \n                   S", font=('Ariel', '28', 'bold '),fill ="darkorchid",)
            return True
        elif data.rowsCleared == 4 and not(data.doubleTetris): #4     
            canvas.create_text(50 +1.8 ,data.height-160,text = "GG", font=('Ariel', '25', 'bold '), )
            canvas.create_text(20 +1.8 ,data.height-130,text = "T", font=('Ariel', '28', 'bold '),)
            canvas.create_text(20 +1.8 ,data.height-130,text = "    E", font=('Ariel', '28', 'bold '),)
            canvas.create_text(20 +1.8,data.height-130,text = "        T", font=('Ariel', '28', 'bold '),)
            canvas.create_text(20 +1.8,data.height-130,text = "            R", font=('Ariel', '28', 'bold '),)
            canvas.create_text(16 +1.8,data.height-130,text = "                I", font=('Ariel', '28', 'bold '))
            canvas.create_text(12 +1.8,data.height-130,text = "                    S", font=('Ariel', '28', 'bold '),)
            canvas.create_text(50 ,data.height-160,text = "GG", font=('Ariel', '25', 'bold '),fill = "Green",)
            canvas.create_text(20 ,data.height-130,text = "T", font=('Ariel', '28', 'bold '),fill = "fireBrick2",)
            canvas.create_text(20 ,data.height-130,text = "    E", font=('Ariel', '28', 'bold '),fill = "orange")
            canvas.create_text(20 ,data.height-130,text = "        T", font=('Ariel', '28', 'bold '),fill = "yellow",)
            canvas.create_text(20 ,data.height-130,text = "            R", font=('Ariel', '28', 'bold '),fill = "green",)
            canvas.create_text(16 ,data.height-130,text = "                I", font=('Ariel', '28', 'bold '),fill = "cyan2",)
            canvas.create_text(12 ,data.height-130,text = "                    S", font=('Ariel', '28', 'bold '),fill ="darkorchid",)
        
            data.doubleTetris = False

def drawFallingPiece(canvas,data):#draws the falling piece over the board, 
#will actually be inside of the board when placed
    if not(data.firstMove) and data.beginningDelay< 0:  # don't want to draw during the beginning animation  
        rows = len(data.fallingPiece)
        cols = len(data.fallingPiece[0])
        for row in range(rows):
            for col in range(cols):
                if data.fallingPiece[row][col]:
                    drawCell(canvas,data,data.fallingPieceRow+ row,data.fallingPieceCol +col,data.fallingColor,2.4 ,data.fallingBorderColor,True)
def moveFallingPiece(data, drow, dcol): # moves the falling piece in delta row, delta col or change
#in row, change in col, and if it is illegal to do so, it undos the move
    data.fallingPieceRow += drow
    data.fallingPieceCol+= dcol
    if not(fallingPieceIsLegal(data)):
        data.fallingPieceRow -= drow
        data.fallingPieceCol-= dcol 
        return False
    return True

def wallKick(data): #more info at tetris wiki
    count = data.fallingOrientation %4
    if count== 0:
        if moveFallingPiece(data,0,0) :
            return True
        if moveFallingPiece(data,0,-1) :
            return True
        if moveFallingPiece(data,-1,-1) :
            return True
        if moveFallingPiece(data,2,0) :
            return True
        if moveFallingPiece(data,2,-1) :
            return True
        return False
    if count== 1:
        if moveFallingPiece(data,0,0) :
            return True
        if moveFallingPiece(data,0,1):
            return True
        if moveFallingPiece(data,1,1) :
            return True
        if moveFallingPiece(data,-2,0):
            return True
        if moveFallingPiece(data,-2,1):
            return True
        return False
    if count== 2:
        if moveFallingPiece(data,0,0):
            return True
        if moveFallingPiece(data,0,1):
            return True
        if moveFallingPiece(data,0,-1) :
            return True
        if moveFallingPiece(data,-1,1):
            return True
        if moveFallingPiece(data,2,0):
            return True
        if moveFallingPiece(data,2,1):
            return True
        return False
    if count== 3:
        if moveFallingPiece(data,0,0):
            return True
        if moveFallingPiece(data,0,-1):
            return True
        if moveFallingPiece(data,1,-1):
            return True
        if moveFallingPiece(data,-2,0):
            return True
        if moveFallingPiece(data,-2,-1):
            return True
    return False

def iPieceWallKick(data):#iPiece is an exception
    count = data.fallingOrientation %4

    if count== 0:
        if moveFallingPiece(data,0,0) == True:
            return True
        if moveFallingPiece(data,0,-2) == True:
            return True
        if moveFallingPiece(data,0,1) == True:
            return True
        if moveFallingPiece(data,1,-2) == True:
            return True
        if moveFallingPiece(data,-2,1) == True:
            return True
    if count== 1:
        if moveFallingPiece(data,0,0) == True:
 
            return True
        if moveFallingPiece(data,0,-1) == True:

            return True
        if moveFallingPiece(data,0,2) == True:

            return True
        if moveFallingPiece(data,-2,-1) == True:
            return True
        if moveFallingPiece(data,1,2) == True:

            return True
        
        return False
    if count== 2:
        if moveFallingPiece(data,0,0) == True:
            return True
        if moveFallingPiece(data,0,2) == True:
            return True
        if moveFallingPiece(data,0,-1) == True:
            return True
        if moveFallingPiece(data,-1,2) == True:
            return True
        if moveFallingPiece(data,2,-1) == True:
            return True
    if count== 3:
        if moveFallingPiece(data,0,0) == True:
            return True
        if moveFallingPiece(data,0,1) == True:
            return True
        if moveFallingPiece(data,0,-2) == True:
            return True
        if moveFallingPiece(data,-2,1) == True:
            return True
        if moveFallingPiece(data,2,1) == True:
            return True
        if moveFallingPiece(data,-1,-2) == True:
            return True
        return False
    return False

def rotateIPiece(data):#exception the iPiece, harcoded in

    count = data.fallingOrientation  % 4
    if count == 0: 
        data.fallingPiece = [[False, False, False, False],[True, True, True, True], [False, False, False, False], [False, False, False, False]]
    if count == 1:
        data.fallingPiece = [[False,False,True,False],[False,False,True,False],[False,False,True,False],[False,False,True,False]]  
    if count ==2:
        data.fallingPiece =  [[False, False, False, False], [False, False, False, False],[True, True, True, True], [False, False, False, False]]
    if count == 3:
        data.fallingPiece = [[False,True,False,False] ,[False,True,False,False] ,[False,True,False,False] ,[False,True,False,False] ]

def rotateMatrix(m): # i wrote before when i wrote a function that multiplies matricies
    cols = len(m[0])
    rows =  len(m)
    result = [ ([0] * cols) for row in range(rows) ]
    for col in range(0,cols):   
        for row in range(0,rows):
            result[col][row] =(m[row][col])
    return result

def flipMatrix(m):

    result = [0] * len(m)
    for i in range(len((m))):
        currentReverse = (m[i])[::-1]
        result[i] = copy.deepcopy(currentReverse)
    return result

def rotateFallingPiece(data):
    piece = copy.deepcopy(data.fallingPiece) #this is to make a copy so that if wall kick doesn't not work, the piece stays the same
    if len(data.fallingPiece)==4: #the only piece that is len(4) is the iPiece ,hardcoded in
        rotateIPiece(data) #first rotate it, then wall kick it

        iPieceWallKick(data)

        if not(fallingPieceIsLegal(data)):
            data.fallingPiece = piece #if can't wall kick, return to original
    elif len(data.fallingPiece)==2:#the only piece that is length 2 is the square piece
        data.fallingPiece = piece #do nothing
    else: #every other piece
        data.fallingPiece = flipMatrix(rotateMatrix(data.fallingPiece))
        wallKick(data)  #first rotate it, then wall kick it
        if not(fallingPieceIsLegal(data)):
            data.fallingPiece = piece  #if still illegal than return to original # rotates the piece

def getCellBounds(row, col, data):
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

def hold(data):# make it draw the hold: when c is pressed make get a new falling piece and store that old piece,
# and introduce a count. count goes  up when you press c, reset when in place falling piece, can only switch if count is 0
    if data.holdCount == 0: 
        data.holdAvailable = True
        data.holdCount +=1
        if data.holdPiece == 0:#this is the first move, nothing in the hold
            data.holdPiece = data.fallingPiece
            newFallingPiece(data)
        else:  #swap it out
            copyHoldPiece = data.holdPiece
            copyFallingPiece = data.fallingPiece#make copies to swap
            data.holdPiece = copyFallingPiece
            data.fallingPiece = copyHoldPiece
            for i in range(4): #change the orintation back to original form
                data.fallingPiece = flipMatrix(rotateMatrix(data.fallingPiece)) 
                if data.fallingPiece in data.tetrisPieces: 
                    break
            piece = copyHoldPiece
            for i in range(4): #change the orintation back to original for
                piece = flipMatrix(rotateMatrix(piece))
                if piece in data.tetrisPieces: break
            current = data.tetrisPieces.index(piece)
            data.fallingColor = data.tetrisPieceColors[current]
            data.fallingBorderColor = data.borderColors[current]
            data.fallingPieceRow = 0
            if len(data.fallingPiece)==4 :
                data.fallingPieceRow = -1
            data.fallingPieceCol = data.cols // 2 *0.75 -0.75
    else:  # you can't hold the same piece twice
        data.holdDenied = True
def movePieceEvents(event,data):
    if event.keysym == 'Right': 
        moveFallingPiece(data,0,1)
    if event.keysym == 'Up' or event.keysym == 'x':
        data.fallingOrientation += 1
        rotateFallingPiece(data)
    if event.keysym == 'Left':
        moveFallingPiece(data,0,-1)
    if event.keysym == 'Down':
        moveFallingPiece(data,1,0)

def resetEvent(event,data): #this is when you press r
    highestScore = data.highestScore #we want to call init by keep highest Score
    backround = data.backroundOn
    check = data.drawCheck
    init(data)
    data.highestScore = highestScore
    data.backroundOn = backround
    data.drawCheck = check

def keyPressed(event, data):
    if not(data.firstMove):
        if ( event.keysym == "r" ):#restart
        
            resetEvent(event,data)       
        if not(data.isGameOver): # dont want to pause / help when the game is over
            if ( event.keysym == "p" ) and not(data.helpMode):
                data.paused = not data.paused      
            if ( event.keysym == "h" ) and not(data.paused):
                data.helpMode = not data.helpMode
    if not(data.isGameOver) and not(data.paused)  and not(data.firstMove) and not(data.helpMode): #only play gain if it isn't paused or game over
        if event.keysym == 'space': # hard drop 
            while moveFallingPiece(data,1,0) == True:
                moveFallingPiece(data,1,0)  
            placeFallingPiece(data)
            newFallingPiece(data)
        if event.keysym == 'c' : #hold
            hold(data)
        movePieceEvents(event,data)

def placeFallingPiece(data):#this function actually places the piece inside of the board
    data.run += 1
    data.holdCount = 0#this is a reset for the hold function hold(data) which makes sense becuase
    #you can hold a s soon as you get a new piece
    rows = len(data.fallingPiece)
    cols = len(data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if data.fallingPiece[row][col] == True:
                data.board[int(data.fallingPieceRow+ row)][int(data.fallingPieceCol +col)] = data.fallingColor
    removeFullRows(data)#everytime you place you should remove the full rows

def startScreenAnimationDelay(data):
    if data.beginningDelay == -1:#its over
        data.firstMove = False
    data.beginningCount += 1
    if (data.beginningCount == 12): 
        data.beginningDelay -= 1
        data.beginningCount = 0 #this is the delay from changing it to 3-2-1-Go

def deniedOrAvailableDelay(data):
    if data.holdDenied:
        data.holdDeniedCount += 1
    if data.holdDeniedCount == 5:
        data.holdDenied = False
        data.holdDeniedCount = 0
    if data.holdAvailable:
        data.holdAvailableCount += 1   
    if data.holdAvailableCount == 5:
        data.holdAvailable = False
        data.holdAvailableCount = 0#delay to draw the check or the x depending on if you can hold or not

def delayToGoDownOne(data):
    data.delayToGoDownOneTile += 1 
    if (data.delayToGoDownOneTile == 15-data.level-1): 
        if moveFallingPiece(data,1,0) == False:
            data.delay = True
        else:
            data.delay = False
        data.delayToGoDownOneTile = 0             
    if (data.delayToGoDownOneTile >15-data.level-1):
        data.delayToGoDownOneTile = 0

def delayToPlace(data):
    if data.delay == True:
        data.delayToPlace += 1
    if data.delayToPlace ==5:
        if moveFallingPiece(data,1,0) == False:
            placeFallingPiece(data)
                    
            newFallingPiece(data)
            data.delay = False
            if fallingPieceIsLegal(data) == False:
                data.isGameOver = True
                data.fallingPiece = [data.fallingPiece[1]]
                data.fallingPieceRow = 0
        data.delayToPlace = 0  

def timerFired(data):
    deniedOrAvailableDelay(data)
    if data.firstMove:
        startScreenAnimationDelay(data)
    else: #start screen over
        if not(data.paused) and not(data.helpMode) and not(data.isGameOver):#make sure the game is running
            if data.rowsCleared >0:
                data.rowsClearedDelay += 1
            if data.rowsClearedDelay >= 10:
                data.rowsCleared = 0       
                data.rowsClearedDelay = 0
                data.doubleTetris = False
                
            if data.level <=12:
                data.levelDelay += 1
                if data.levelDelay == 400: #delay to change levels
                    data.level += 1
                    data.levelDelay = 0
            delayToGoDownOne(data)
            delayToPlace(data)
            
def drawGame(canvas, data):   
    if data.backroundOn:
        photo = PhotoImage(file = "h.gif")

        label = Label(image=photo)
        label.image = photo # keep a reference!    
        canvas.create_image(data.width/2,data.height/2, image = photo)
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill="grey50")
    drawBoard(canvas, data)

def isPiece(string,data):
    colors =  tetrisPieceColors
    for i in range(0,len(colors)):
        if string == colors[i]:
            return True
        elif string == data.emptyColor[0]:return False

def drawBoard(canvas, data): 
    pieceColors =  tetrisPieceColors
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == data.emptyColor[0] or data.board[row][col] == data.emptyColor[1]:
                drawCell(canvas, data, row, col,data.board[row][col],1.3,"Grey11",False) #draw the backround cells
 
            if isPiece(data.board[row][col],data) == True : #if there is a piece there, draw the piece
                current = data.board[row][col]
                index = pieceColors.index(current)
                border = borderColors[index]                 
                drawCell(canvas, data, row, col,data.board[row][col],2.4,border,True)

def drawBackround(canvas,data):
    (x0,y0,c,v)= getCellBounds(0,0,data)#c,v dont matter
    (x1,y1,c,v)= getCellBounds(data.rows,data.cols,data)
    if data.backroundOn:
        photo = PhotoImage(file = "lol.gif")

        label = Label(image=photo)
        label.image = photo # keep a reference!

        canvas.create_image(x0+5,y0+33, image = photo,anchor = "sw")
    else:
        canvas.create_rectangle(x0, y0-10, x1+10, y0+31,fill="grey50",outline="grey50")
        canvas.create_rectangle(x0+2, y0+33, x1+7, y1+22,width = 5,outline = "grey10")
    
def drawCell(canvas, data, row, col,color,width,outline,cell):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    if cell == False:
        canvas.create_rectangle(x0+5, y0+20, x1+5, y1+20, fill=color,outline= outline,width=width)
    if cell == True:
        canvas.create_rectangle(x0+6, y0+21, x1+4, y1+19, fill=color,outline= outline, width=width)
        canvas.create_rectangle(x0+9.5, y0+24.5, x1-0.1, y1+15.5, fill=color,outline= outline,width=2)
    if cell == None:
        canvas.create_rectangle(x0+7, y0+22, x1+3, y1+18, fill=color,outline= outline,width=width)

def pieceIsLegal(piece,r,c,data):
    rows = len(piece)
    cols = len(piece[0])
    for row in range(rows):
        for col in range(cols):
            if piece[row][col] :
                nR = (r + row) #new row
                nC = (c + col) # new col
                if (nC > 9 or nC < 0 or nR >= 21 or nR < 0): 
                    return False        
   
                if not((data.board[int(nR)][int(nC)] == data.emptyColor[1] or data.board[int(nR)][int(nC)] == data.emptyColor[0])): 
                    return False
    return True #returns weather the piece is legal or not

def fallingPieceIsLegal(data):
    if len(data.fallingPiece) == 4:
        if data.fallingPieceRow <=3 and data.fallingPieceCol >= -1 and data.fallingPieceCol <=6:
            piece = data.fallingPiece
            rows = len(piece)
            cols = len(piece[0])
            for row in range(rows):
                for col in range(cols):
                    if piece[row][col] :
                        r,c=data.fallingPieceRow,data.fallingPieceCol
                        nR = (r + row) #new row
                        nC = (c + col) # new col
                       
                        if nR >0 and (not((data.board[int(nR)][int(nC)] == data.emptyColor[1] or data.board[int(nR)][int(nC)] == data.emptyColor[0]))) : 
                            return False
            return True
    return pieceIsLegal(data.fallingPiece,data.fallingPieceRow,data.fallingPieceCol,data)

def isGhostPieceLegal(data):
    return pieceIsLegal(data.ghostPiece,data.ghostPieceRow,data.ghostPieceCol,data)

def moveGhostFallingPiece(data,drow,dcol):
    data.ghostPieceRow += drow
    data.ghostPieceCol+= dcol
    if isGhostPieceLegal(data) == False:
        data.ghostPieceRow -= drow
        data.ghostPieceCol-= dcol
        return False
    return True

def drawGhost(canvas,data):
    data.ghostPiece = data.fallingPiece
    if data.ghostPiece == -1:
        return False
    data.ghostPiece = data.fallingPiece
    data.ghostPieceRow = data.fallingPieceRow
    data.ghostPieceCol = data.fallingPieceCol
    if not(data.isGameOver) and data.beginningDelay == -1:
        while moveGhostFallingPiece(data,1,0) == True:
                moveGhostFallingPiece(data,1,0)

        row = data.ghostPieceRow
        col = data.fallingPieceCol

        for i in range(len(data.ghostPiece)):
            for j in range(len(data.ghostPiece[0])):
                if data.ghostPiece[i][j]:  
                    color = data.board[int(row)][int(col)] 
                    outline = "grey2" 
                    width = 2.4
                    drawCell(canvas, data, row+i, col+j,data.board[int(row+i)][int(col+j)],2.4,"grey40",None)   

def startScreen(canvas,data):    
    if data.firstMove and data.beginningDelay > 0:
        canvas.create_rectangle(data.width-18, 140, data.width -78, 200,fill="grey2",outline="grey18",width = 6)
        canvas.create_text(data.width/2 ,data.height/2,text = str(data.beginningDelay), font=('Comic Sans MS', '140', 'bold italic'),fill = "black")
        canvas.create_text(data.width/2 ,data.height/2,text = str(data.beginningDelay), font=('Comic Sans MS', '130', 'bold italic'),fill = "orange")
    if data.firstMove and data.beginningDelay == 0:
        canvas.create_rectangle(data.width-18, 140, data.width -78, 200,fill="grey2",outline="grey18",width = 6)
        canvas.create_text(data.width/2 ,data.height/2,text = "GO", font=('Comic Sans MS', '140', 'bold italic'),fill = "black")
        canvas.create_text(data.width/2 ,data.height/2,text = "GO", font=('Comic Sans MS', '130', 'bold italic'),fill = "green")

def pause(canvas,data):
        canvas.create_rectangle(106, data.width/2+149, data.width -100, data.height-247,fill="grey60",outline="grey39")
        canvas.create_text(data.width/2 +4.5 ,data.height/2-50,text = "Paused", font=('Comic Sans MS', '80', 'bold italic'),fill = "black")
        canvas.create_text(data.width/2 ,data.height/2-50,text = "Paused", font=('Comic Sans MS', '80', 'bold italic'),fill = "orange")
        canvas.create_text(data.width/2+2 ,data.height/2+50,text = "Press 'p' to unpause", font=('Comic Sans MS', '20', 'bold italic'),fill = "black")
        canvas.create_text(data.width/2 ,data.height/2+50,text = "Press 'p' to unpause", font=('Comic Sans MS', '20', 'bold italic'),fill = "orange")

def gameOver(canvas,data):
        canvas.create_rectangle(116, data.width/2+149, data.width -117, data.height-247,fill="grey60",outline="grey39")
        canvas.create_text(data.width/2 +4.5 ,data.height/2-50,text = "Game Over", font=('Comic Sans MS', '70', 'bold italic'),fill = "black")
        canvas.create_text(data.width/2 ,data.height/2-50,text = "Game Over", font=('Comic Sans MS', '70', 'bold italic'),fill = "DodgerBlue2")
        canvas.create_text(data.width/2+1 ,data.height/2+50,text = "Press 'r' to retry", font=('Comic Sans MS', '20', 'bold italic'),fill = "black")
        canvas.create_text(data.width/2 ,data.height/2+50,text = "Press 'r' to retry", font=('Comic Sans MS', '20', 'bold italic'),fill = "DodgerBlue2")

def text(canvas,data):
    canvas.create_text(50 +2.5,430,text =  str(data.level), font=('Comic Sans MS', '30', 'bold italic'),fill = "black")
    canvas.create_text(53 ,400,text = "LEVEL:" , font=('Comic Sans MS', '28', 'bold italic'),fill = "hotpink1")
    canvas.create_text(50 ,430,text =  str(data.level), font=('Comic Sans MS', '30', 'bold italic'),fill = "hotpink1")
    canvas.create_text(170 ,117,text = "Score:  " , font=('Comic Sans MS', '30', 'bold italic'),fill = "white")
    canvas.create_text(275 ,117,text =  str(data.score), font=('Comic Sans MS', '30', 'bold italic'),fill = "white")
    canvas.create_text(200 ,84,text = "Highest Score:    " , font=('Comic Sans MS', '20', 'bold italic'),fill = "white")
    canvas.create_text(295 ,84,text = str(data.highestScore), font=('Comic Sans MS', '20', 'bold italic'),fill = "white")
    canvas.create_text(200 ,56,text = "by Brandon Li" , font=('Comic Sans MS', '20', 'bold italic'),fill = "white")

def drawNextCell(canvas, data, row, col,color,width,outline,cell):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    x0 -= (col*6)
    x1 -= (col*6)
    y0 -= (row*6)
    y1 -= (row*6)
    x0 += 67
    x1 += 67
    y0 += 7
    y1 +=7
    if not(cell):
        canvas.create_rectangle(x0+6, y0+21, x1+4, y1+19, fill=color,outline= outline,width=width)
    else:
        canvas.create_rectangle(x0+11, y0+21, x1+4, y1+14, fill=color,outline= outline,width=width)
        canvas.create_rectangle(x0+14, y0+24, x1+1, y1+10.5, fill=color,outline= outline,width=2)

def drawNext(canvas,data):
    canvas.create_text(data.width-50 +3 ,120,text = "Next", font=('Comic Sans MS', '30', 'bold italic'),fill = "black")
    canvas.create_text(data.width-50 ,120,text = "Next", font=('Comic Sans MS', '30', 'bold italic'),fill = "maroon4")
    canvas.create_rectangle(data.width-18, 140, data.width -78, 200,fill="grey2",outline="grey18",width = 6)
    piece = data.gamePieces[0]
    current = data.tetrisPieces.index(piece)
    Color = data.tetrisPieceColors[current]
    outline = data.borderColors[current]
    if piece == oPiece:  
        for row in range(len(piece)): 
            for col  in range(len(piece[0])):
                if piece[row][col] == True:
                    (x0, y0, x1, y1) = getCellBounds(row, col, data)
                    x0 -= (col*6)
                    x1 -= (col*6)
                    y0 -= (row*6)
                    y1 -= (row*6)
                    x0 += 227.5
                    x1 += 227.5
                    y0 += 35
                    y1 += 35 

                    canvas.create_rectangle(x0+11, y0+21, x1+4, y1+14, fill=Color,outline= outline,width=2.4)
                    canvas.create_rectangle(x0+14.5, y0+24, x1+1, y1+10.5, fill=Color,outline= outline,width=2)
        return False
    elif len(piece) == 4: #the iPiece
        for row in range(len(piece)): 
            for col  in range(len(piece[0])):
                if piece[row][col] == True:
                    (x0, y0, x1, y1) = getCellBounds(row, col, data)
                    x0-=(col*6.9)
                    x1 -=(col*6.9)
                    y0-=(row*6.8)
                    y1 -=(row*6.8)
                    x0+=213
                    x1+=213
                    y0 +=30
                    y1+=30
                    canvas.create_rectangle(x0+13, y0+21, x1+4, y1+12, fill=Color,outline= outline,width=2.02)
                    canvas.create_rectangle(x0+15.5, y0+24, x1+0.5, y1+9, fill=Color,outline= outline,width=2)
    else:
        for i in range(len(piece)): 
            for j in range(len(piece[0])): 
                if piece[i][j] == True:     
                    drawNextCell(canvas, data, 2+i, j+11,Color,2.4,outline,True)

def drawHold(canvas,data):
    canvas.create_text(50 +3 ,160,text = "Hold", font=('Comic Sans MS', '30', 'bold italic'),fill = "black")
    canvas.create_text(50 ,160,text = "Hold", font=('Comic Sans MS', '30', 'bold italic'),fill = "steelblue2")
    canvas.create_rectangle(20, 180, 80, 240,fill="grey2",outline="grey18",width = 6)
    if data.holdPiece != 0:
        piece = data.holdPiece
        for i in range(4): #change orientation
            piece = flipMatrix(rotateMatrix(piece))
            if piece in data.tetrisPieces: break
        current = data.tetrisPieces.index(piece)
        color = data.tetrisPieceColors[current]
        outline = data.borderColors[current]

        if len(piece)== 2: 
            for i in range(len(piece)): 
                for j in range(len(piece[0])): 
                    if piece[i][j] == True:     
                        drawNextCell(canvas, data, 4.9+i, j-10.1,color,2.4,outline,True)
            return True
        elif len(piece)== 4: 
            for i in range(len(piece)): 
                for j in range(len(piece[0])): 
                    if piece[i][j] == True:     
                        drawNextCell(canvas, data, 4.4+i, j-11.1,color,2.4,outline,True)
        else: 
            for i in range(len(piece)): 
                for j in range(len(piece[0])): 
                    if piece[i][j] == True:     
                        drawNextCell(canvas, data, 5+i, j-10.6,color,2.4,outline,True)
    
def helpMode(canvas,data):#lol this took too long
    canvas.create_rectangle(0, 0, data.width+200, data.height+20, fill="grey60")    
    canvas.create_text(data.width/2 +4.5 ,data.height/8-20,text = "Help Mode!", font=('Comic Sans MS', '70', 'bold italic'),fill = "black")
    canvas.create_text(data.width/2 ,data.height/8-20,text = "Help Mode!", font=('Comic Sans MS', '70', 'bold italic'),fill = "purple")
    # canvas.create_text(data.width/2 ,data.height/6+50-30,text = "Press 'h' to exit Help Mode", font=('Comic Sans MS', '20', 'bold italic'),fill = "black")
    canvas.create_rectangle(data.width/2-25-50, data.height/6+100-60, data.width/2 +25-50, data.height/6+150-60,fill="grey80",outline="grey6",width = 2)
    canvas.create_polygon(data.width/2-3-50,data.height/6+124-60,data.width/2-50,data.height/6+117-60,data.width/2+3-50,data.height/6+124-60)
    canvas.create_line(data.width/2+10-50,data.height/6+130-60,data.width-100-50,200-50)
    canvas.create_text(data.width-50-50,180-40,text = "rotate clockwise",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_rectangle(data.width/2-25-50, data.height/6+160-60, data.width/2 +25-50, data.height/6+210-60,fill="grey80",outline="grey6",width = 2)
    canvas.create_polygon(data.width/2-3-50,data.height/6+184-60,data.width/2-50,data.height/6+190-60,data.width/2+3-50,data.height/6+184-60)
    canvas.create_line(data.width/2+10-50,data.height/6+190-40,data.width/2-30,350-78)
    canvas.create_text(data.width/2-30,353-78,text = "soft drop",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_rectangle(data.width/2-85-50, data.height/6+160-60, data.width/2 -35-50, data.height/6+210-60,fill="grey80",outline="grey6",width = 2)
    canvas.create_polygon(data.width/2-63-50,data.height/6+180-60,data.width/2-63-50,data.height/6+187-60,data.width/2-68-50,data.height/6+183.5-60)
    canvas.create_line(data.width/2-70-50,data.height/6+190 -60,data.width/2-105-50,190)
    canvas.create_text(data.width/2-110-50,185,text = "move left",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_rectangle(data.width/2+35-50, data.height/6+160-60, data.width/2 +85-50, data.height/6+210-60,fill="grey80",outline="grey6",width = 2)
    canvas.create_polygon(data.width/2+67-50,data.height/6+180-60,data.width/2+67-50,data.height/6+187-60,data.width/2+72-50,data.height/6+183.5-60)
    canvas.create_line(data.width/2+60-50,data.height/6+190-60,data.width-70-50,300-60)
    canvas.create_text(data.width-60-50,290-40,text = "move right",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_rectangle(60+200, data.height/2+20-150, 110+200, data.height/2+70-150,fill="grey80",outline="grey6",width = 2)
    canvas.create_text(75+200,data.height/2+35-150,text = "p",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_line(85+200,data.height/2+45-150,135+200,data.height/2+45-150)
    canvas.create_text(165+190,data.height/2+40-155,text = "pause/unpause",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_rectangle(60+270, data.height/2+100-200, 110+270, data.height/2+150-200,fill="grey80",outline="grey6",width = 2)
    canvas.create_text(75+270,data.height/2+115-200,text = "h",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_line(85+270,data.height/2+125-200,85+270,data.height/2+125-200+45)
    canvas.create_text(95+270,data.height/2+110-200+60,text = "help/ \n exit help",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_rectangle(260, data.height/2-35, 310, data.height/2+15,fill="grey80",outline="grey6",width = 2)
    canvas.create_text(270,data.height/2-35+10,text = "c",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_line(265,data.height/2-35+10,246,data.height/2-35+10)
    canvas.create_text(240,data.height/2-35+10,text = "hold",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_rectangle(15, data.height/2-25, 145, data.height/2+15,fill="grey80",outline="grey6",width = 2)
    canvas.create_text(82.5,data.height/2-5,text = "space",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_line(82.5,data.height/2+2,82.5,data.height/2 +15)
    canvas.create_text(82.5,data.height/2 +20,text = "hard drop",font = ('Comic Sans MS', '13', 'bold italic'))
   
    canvas.create_text(data.width-230,data.height/2 +50,text = "Scoring System",font = ('Comic Sans MS', '15', 'bold italic'))
    canvas.create_text(data.width-200,data.height/2 +70,text = "1 Line   2 Lines   3 Lines   4 Lines   Double Tetris Bonus",font = ('Comic Sans MS', '12', 'bold italic'))
    canvas.create_text(data.width-375,data.height/2 +60,text = "Level",font = ('Comic Sans MS', '12', 'bold italic'))
    canvas.create_text(data.width-375,data.height/2 +190,text = "0\n\n1\n\n2\n\n3\n\n4\n\n...\n\n13",font = ('Comic Sans MS', '12', 'bold italic'))
    canvas.create_text(data.width-225,data.height/2 +190,text = "  4         10          30         120                 50\n\n  8         20         60          240               100\n\n  12        30         90          360               150\n\n  16        40         120         480              200\n\n  20        50         150         600              250\n\n\n\n  56       140         420        1680             700",font = ('Comic Sans MS', '12', 'bold italic'))

    canvas.create_rectangle(260-70, data.height/2-35+30, 310-70, data.height/2+15+30,fill="grey80",outline="grey6",width = 2)
    canvas.create_text(270-70,data.height/2-35+10+30,text = "r",font = ('Comic Sans MS', '13', 'bold italic'))
    canvas.create_line(265-70,data.height/2-35+10+30,246-70,data.height/2-35+10+30)
    canvas.create_text(240-75,data.height/2-35+10+30,text = "reset",font = ('Comic Sans MS', '13', 'bold italic'))
     
    
    canvas.create_text(40,110,text = "  turn on\nbackround",font = ('Comic Sans MS', '13', 'bold italic'))

    canvas.create_rectangle(74, 100, 83, 109,fill="grey80",outline="grey6",width = 1)
    if data.drawCheck:
        canvas.create_text(75.2 ,91.5,text = "✔", font=('Comic Sans MS', '17', 'bold italic'),anchor = "nw")

def mousePressed(event, data): #the event of the mouse being pressed 
#this function is only for the check box in help mode to turn on the backround
    if 74 <= event.x <= 83 and 100 <= event.y <= 109 and data.helpMode:
        if not data.backroundOn:
            data.drawCheck = True
        else: 
            data.drawCheck = False
        data.backroundOn = not(data.backroundOn)

def drawTetris(canvas,data):
    if not(data.helpMode): #don't want to draw in help mode
        canvas.create_text(data.width/2 -70+10 +15,30,text = "T", font=('Ariel', '40', 'bold '),fill = "maroon",)
        canvas.create_text(data.width/2 -70 +10+7+45-10-3,30,text = "E", font=('Ariel', '40', 'bold '),fill = "darkOrange4",)
        canvas.create_text(data.width/2 -70 +8+3+95-10-20,30,text = "T", font=('Ariel', '40', 'bold '),fill = "darkgoldenrod",)
        canvas.create_text(data.width/2 -70 +1+140-10-30,30,text = "R", font=('Ariel', '40', 'bold '),fill = "darkGreen",)
        canvas.create_text(data.width/2 -80+0-7 +185-10-40,30,text = "I", font=('Ariel', '40', 'bold '),fill = "blue",)
        canvas.create_text(data.width/2 -80+3-16 +230-10-60,30,text = "S", font=('Ariel', '40', 'bold '),fill = "darkslateblue",)

        canvas.create_text(data.width/2 -70+10 +15+2.5,30,text = "T", font=('Ariel', '40', 'bold '),fill = "fireBrick2",)
        canvas.create_text(data.width/2 -70 +10+7+45-10-3+2.5,30,text = "E", font=('Ariel', '40', 'bold '),fill = "orange",)
        canvas.create_text(data.width/2 -70 +8+3+95-10-20+2.5,30,text = "T", font=('Ariel', '40', 'bold '),fill = "yellow",)
        canvas.create_text(data.width/2 -70 +1+140-10-30+2.5,30,text = "R", font=('Ariel', '40', 'bold '),fill = "green",)
        canvas.create_text(data.width/2 -80+0-7 +185-10-40+2.5,30,text = "I", font=('Ariel', '40', 'bold '),fill = "cyan2",)
        canvas.create_text(data.width/2 -80+3-16 +230-10-60+2.5,30,text = "S", font=('Ariel', '40', 'bold '),fill = "darkorchid",)

def redrawAll(canvas, data):
    if len(data.gamePieces) == 0: #regenerate the pieces after done every 7
        data.gamePieces = generatePieces()
    drawGame(canvas, data)
    drawGhost(canvas,data)
    drawFallingPiece(canvas,data)
    drawBackround(canvas,data)
    drawRowsCleared(canvas,  data)
    text(canvas,data)
    drawNext(canvas,data)
    drawHold(canvas,data)
    if data.helpMode == True:
        helpMode(canvas,data)
    startScreen(canvas,data)
    drawTetris(canvas,data)  
    if data.paused :
        pause(canvas,data)
    if data.isGameOver:
        gameOver(canvas,data)   
    if data.holdAvailable :
        canvas.create_text(83 ,173,text = "✔", font=('Comic Sans MS', '60', 'bold italic'),fill = "Green")
    if data.holdDenied :
        canvas.create_text(86 ,172,text = "X", font=('Comic Sans MS', '52', 'bold italic'),fill = "Red")

   
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()  
         
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        data.frames += 1 
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    init(data)
    t = time.time()
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)

    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    
    root.mainloop()  

def playTetris():
    rows = 21
    cols = 10
    margin = 100 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height)
    
playTetris() 