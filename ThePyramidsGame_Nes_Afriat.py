
import random
import pygame
import sys

FPS = 15
WINDOWWIDTH = 600
WINDOWHEIGHT = 480
PYRAMIDHEIGHT= 7
PYRAMIDWIDTH= 13
CELLSIZE= 30

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
BLUE      = (  0,   0, 255)
PINK      = (255,  20, 147)
YELLOW    = (255, 255,   0)
color_set= [BLUE,YELLOW,PINK]
BGCOLOR = WHITE


class Cell():
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
    def setColor(self, new_color):
        self.color= new_color
    def drawCell(self):
        cell_Rect = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)
        if(self.color==-1):
            pygame.draw.rect(DISPLAYSURF, self.color, cell_Rect)
        else:
            pygame.draw.rect(DISPLAYSURF, self.color, cell_Rect)

#get a new random color for a cell from pink,blue,yellow
def getRandomColor():
    return random.choice(color_set)

#compare two tuples of RGB colors
def compare_colors(color1, color2):
    for i in range(3):
        if color1[i]!=color2[i]:
            return False
    return True

#get a row number and change it colors
def random_row(row):
    for i in range(row*2 + 1):
        pyr_mat[row][i].color = getRandomColor()


####Draw functions####
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))

def drawMatrix():
    for i in range(len(pyr_mat)):
        for j in range(len(pyr_mat[i])):
            pyr_mat[i][j].drawCell()
#########################


#################Game Rules###################

#if there is blue cell in one of the triangle ribs change its color
def checkRules1():
    left_index=0
    #bottom rib
    for j in range(PYRAMIDWIDTH):
        if compare_colors(pyr_mat[PYRAMIDHEIGHT-1][j].color, BLUE):
            pyr_mat[PYRAMIDHEIGHT-1][j].color = getRandomColor()
            return False
    #sides rib
    for i in range(0,PYRAMIDHEIGHT-1):
        right_index= left_index + i*2
        if(compare_colors(pyr_mat[i][left_index].color,BLUE)):
            pyr_mat[i][left_index].color= getRandomColor()
            return False
        if (compare_colors(pyr_mat[i][right_index].color,BLUE)):
            pyr_mat[i][right_index].color = getRandomColor()
            return False
    return True

#if there are pink cell in one of a blue cells side change the cell into another
def checkRules2():
    for i in range(1,PYRAMIDHEIGHT-1):
        for j in range(PYRAMIDWIDTH):
            if compare_colors(pyr_mat[i][j].color,BLUE):
                if(compare_colors(pyr_mat[i-1][j-1].color,PINK)):
                    pyr_mat[i-1][j-1].color = getRandomColor()
                    return False
                if (compare_colors(pyr_mat[i+1][j+1].color, PINK)):
                    pyr_mat[i+1][j+1].color = getRandomColor()
                    return False
                if (compare_colors(pyr_mat[i][j+1].color, PINK)):
                    pyr_mat[i][j+1].color = getRandomColor()
                    return False
                if (compare_colors(pyr_mat[i][j - 1].color, PINK)):
                    pyr_mat[i][j-1].color = getRandomColor()
                    return False
    return True

#if there are 4 yellows make a new random row
def checkRules3():
    for i in range(2,PYRAMIDHEIGHT):
        yellow_counter = 0
        for j in range(PYRAMIDWIDTH):
            if compare_colors(pyr_mat[i][j].color,YELLOW):
                yellow_counter+=1
                if yellow_counter == 4:
                    random_row(i)
                    return False
    return True

################Main Code########################################
#main game loop - draw the board, check the rules, if not completed draw again
def runGame():
        complete= False
        while(not complete):
            DISPLAYSURF.fill(BGCOLOR)
            drawMatrix()
            drawGrid()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
           # pygame.time.wait(50)
            if(checkRules1()):
                if(checkRules2()):
                    if(checkRules3()):
                        complete=True

#end of the game - draw the game one last time, wait at the shocking moment and eliminate pygame
def terminate():
    DISPLAYSURF.fill(BGCOLOR)
    drawMatrix()
    drawGrid()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.time.wait(5300)
    pygame.quit()
    sys.exit()

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, pyr_mat
    #init the pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Pyramid')

    #Create a matrix of 7X13 of white cells
    pyr_mat = [[Cell(0,0,WHITE) for j in range(PYRAMIDWIDTH)] for i in range(PYRAMIDHEIGHT)]

    # Set a random Pyramid (x,y and random game colors)
    for i in range(PYRAMIDHEIGHT):
        right = int((WINDOWWIDTH/CELLSIZE + PYRAMIDWIDTH)/2) *CELLSIZE
        left = int((WINDOWWIDTH/CELLSIZE + PYRAMIDWIDTH)/2) * CELLSIZE - PYRAMIDWIDTH*CELLSIZE
        right_ptr = right - i * CELLSIZE
        left_ptr = left + i * CELLSIZE
        if(left<=right):
            for j in range(PYRAMIDWIDTH):
                    if(left_ptr<right_ptr):
                        pyr_mat[PYRAMIDHEIGHT-i-1][j].setColor(random.choice(color_set))
                        pyr_mat[PYRAMIDHEIGHT-i-1][j].x = left_ptr
                        pyr_mat[PYRAMIDHEIGHT-i-1][j].y = WINDOWHEIGHT - (i+1)*CELLSIZE
                    left_ptr+= CELLSIZE
            right -= CELLSIZE
            left += CELLSIZE

    while True:
        runGame()
        terminate()

###########################################################



if __name__ == '__main__':
    main()