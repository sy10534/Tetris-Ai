import random
import time


piece = [[]for x in range(7)]
bitmap = [[False for x in range(10)] for x in range(24)] # 5 blocks above buffer
globalScore = 0
lastBrickCache = [0,0,0]
def initializePieces():
    piece[0].append([[1,1,1,1]])
    piece[0].append([[1],[1],[1],[1]])
    piece[1].append([[1,0,0],[1,1,1]])
    piece[1].append([[1,1],[1,0],[1,0]])
    piece[1].append([[1,1,1],[0,0,1]])
    piece[1].append([[0,1],[0,1],[1,1]])
    piece[2].append([[0,0,1],[1,1,1]])
    piece[2].append([[1,0],[1,0],[1,1]])
    piece[2].append([[1,1,1],[1,0,0]])
    piece[2].append([[1,1],[0,1],[0,1]])
    piece[3].append([[1,1],[1,1]])
    piece[4].append([[0,1,1],[1,1,0]])
    piece[4].append([[1,0],[1,1],[0,1]])
    piece[5].append([[0,1,0],[1,1,1]])
    piece[5].append([[1,0],[1,1],[1,0]])
    piece[5].append([[1,1,1],[0,1,0]])
    piece[5].append([[0,1],[1,1],[0,1]])
    piece[6].append([[1,1,0],[0,1,1]])
    piece[6].append([[0,1],[1,1],[1,0]])

def printMap():
    print('-'*22)

    for i in range(18,-1,-1):
        print('|',end='')
        for y in range(0,10,1):
            if bitmap[i][y]:
                print("[]",end='')
            else:
                print('  ',end='')
        print('|')

    print('-'*22)
    print("Score:",globalScore)

def checkOutOfBound(posx,posy,piece):
    sizex = len(piece[0])
    sizey = len(piece)
    ok = True
    if posx + sizex - 1 > 9:
        ok = False
    if posy - sizey + 1 < 0:
        ok = False
    if posy > 18:
        ok = False
    return ok
def checkCollision(posx,posy,piece):
    ok = True
    for y in range(len(piece)):
        for x in range(len(piece[y])):
            if piece[y][x]:
                if bitmap[posy-y][posx+x]:
                    return False
    return True
def addBrick(posx,posy,piece):
    for y in range(len(piece)):
        for x in range(len(piece[y])):
            if piece[y][x]:
                bitmap[posy-y][posx+x] = True
def removeBrick(posx,posy,piece):
    for y in range(len(piece)):
        for x in range(len(piece[y])):
            if piece[y][x]:
                bitmap[posy-y][posx+x] = False
def findDropPosition(posx,piece):
    cury = 18
    while (checkCollision(posx,cury,piece) and checkOutOfBound(posx,cury,piece)):
        cury-=1
    cury+=1
    return cury
def dropBrick(posx,piece):
    global lastBrickCache
    posy = findDropPosition(posx,piece)
    addBrick(posx,posy,piece)
    lastBrickCache = [posx,posy,piece]
def revertBrick():
    removeBrick(lastBrickCache[0],lastBrickCache[1],lastBrickCache[2])

def clearTetris():
    cury = 0
    clearcnt = 0
    global globalScore
    while cury <= 18:
        ok = True
        for x in range(0,10):
            if not bitmap[cury][x]:
                ok = False
        if ok:
            for y in range(cury,18):
                for x in range(0,10):
                    bitmap[y][x] = bitmap[y+1][x]
            cury -= 1
            clearcnt+=1
        cury+=1
    if clearcnt != 0:
        globalScore += 10**clearcnt
def checkDeath():
    for x in range(0,10):
        if bitmap[19][x]:
            return False
    return True

def findBumpiness():
    bumpiness = 0
    lastHeight = 0
    heightMap = [0 for x in range(10)]
    for x in range(0,10):
        for y in range(18,-1,-1):
            if bitmap[y][x]:
                heightMap[x] = y+1
                break
    for x in range(1,10):
        bumpiness += abs(heightMap[x]-heightMap[x-1])
    return bumpiness
def findHoles():
    holes = 0
    for x in range(0,10):
        start = False
        for y in range(18,-1,-1):
            if bitmap[y][x]:
                start = True
            if start and not bitmap[y][x]:
                holes+=1
    return holes
def findTetris():
    count = 0
    for y in range(18,-1,-1):
        ok = True
        for x in range(0,10):
            if not bitmap[y][x]:
                ok = False
        if ok:
            count += 1
    return count
def findHighest():
    heightMap = [0 for x in range(10)]
    for x in range(0,10):
        for y in range(18,-1,-1):
            if bitmap[y][x]:
                heightMap[x] = y+1
                break
    return max(heightMap)

def evaluate():
    bumpinessScore = findBumpiness()
    holesScore = findHoles()*5
    tetrisScore = findTetris()
    highestScore = findHighest()
    return 0-bumpinessScore-holesScore-highestScore+10**tetrisScore

def findBestMove(pieces):
    global bitmap
    maximumScore = -100000
    bestX = 0
    bestPiece = None
    for piece in pieces:
        for x in range(0,10,1):
            if checkOutOfBound(x,18,piece):
                dropBrick(x,piece)
                score = evaluate()
                revertBrick()
                if score > maximumScore:
                    maximumScore = score
                    bestX = x
                    bestPiece = piece
    return bestX,bestPiece
################################################################################
################################################################################
################################################################################
def generateRandomPieces(n):
    element = []
    for i in range(n):
        element.append(random.choice([x for x in range(7)]))
    return element

initializePieces()
print(generateRandomPieces(10))
# bestX, bestPiece = findBestMove(piece[0])
# dropBrick(bestX,bestPiece)
# bestX, bestPiece = findBestMove(piece[0])
# dropBrick(bestX,bestPiece)
pieces = generateRandomPieces(1000)
cnt = 0
for index in pieces:
    bestX, bestPiece = findBestMove(piece[index])
    dropBrick(bestX,bestPiece)
    clearTetris()
    if checkDeath == False:
        print("Death!!!!!", index)
        break
    printMap()
    print(cnt)
    cnt+=1
    time.sleep(0.01)

clearTetris()
printMap()


# dropBrick(0,piece[3][0])
# dropBrick(1,piece[3][0])