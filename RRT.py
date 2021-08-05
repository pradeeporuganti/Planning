import random
import math
import pygame
from pygame.draw import rect

# class includes methods to draw the map itself
class RRTMap:
    def __init__(self, start, goal, mapDimensions, obsDim, obsNum):
        self.start = start
        self.goal = goal
        self.mapDimensions = mapDimensions
        self.maph, self.mapw = mapDimensions
        
        # window settings
        self.mapWindowName = 'RRT path planning'
        pygame.display.set_caption(self.mapWindowName)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.fill((255,255,255))
        self.noderad = 2
        self.nodeThickness = 2
        self.edgeThickness = 1
        self.obstacles = []
        self.obsDim = obsDim
        self.obsNumber = obsNum

        # colors
        self.grey = (70, 70 ,70)
        self.blue = (0,0,255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, self.green, self.start, self.noderad+5, 0)
        pygame.draw.circle(self.map, self.red, self.goal, self.noderad+20, 1)
        self.drawObs(obstacles)

    def drawPath(self):
        pass

    def drawObs(self, obstacles):
        obstaclesList = obstacles.copy()
        while (len(obstaclesList)>0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)


# make obstacles, adding nodes and edges to the tree
class RRTGraph:
    def __init__(self, start, goal, mapDimensions, obsDim, obsNum):
        (x,y) = start
        self.start = start 
        self.goal = goal
        self.goalFlag = False
        self.maph, self.mapw = mapDimensions
        self.mapDimensions = mapDimensions
        self.x = []
        self.y = []
        self.parent = []

        # init tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        # obstacles 
        self.obstacles = []
        self.obsDim = obsDim
        self.obsNum = obsNum

        #path
        self.goalState = None
        self.path = []

    def makeRandomRect(self):
        # obstacle is not generated outside the map
        uppercornerx = int(random.uniform(0, self.mapw-self.obsDim))
        uppercornery = int(random.uniform(0, self.maph-self.obsDim))

        return (uppercornerx, uppercornery)

    def makeobs(self):
        obs = []

        for i in range(0, self.obsNum):
            # holding obstacles temporatly before getting stored 
            rectangle = None
            # Check is start and goal locations are inside a newly
            # created obstacle 
            startGoalCol = True
            while startGoalCol:
                upper = self.makeRandomRect()
                rectangle = pygame.Rect(upper, (self.obsDim, self.obsDim))
                if rectangle.collidepoint(self.start) or rectangle.collidepoint(self.goal):
                    startGoalCol = True
                else:
                    startGoalCol = False 
                obs.append(rectangle)
                        
        self.obstacles = obs.copy()
        return obs

    def add_node(self, n, x, y):
        self.x.insert(n, x)
        self.y.insert(n, y)


    def remove_node(self, n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self, parent, child):
        self.parent.insert(child,parent)      

    def remove_edge(self,n):
        self.parent.pop(n)

    def number_of_nodes(self):
        return len(self.x)

    def distance(self, n1, n2):
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        px = (float(x1) -float(x2))**2
        py = (float(y1) -float(y2))**2

        return (px+py)**0.5

    def sample_env(self):
        x = int(random.uniform(0, self.mapw))
        y = int(random.uniform(0, self.maph))
        return x,y

    def nearest(self):
        pass

    def isFree(self):
        n = self.number_of_nodes()-1
        (x, y) = (self.x[n], self.y[n])
        obs = self.obstacles.copy()
        while len(obs)>0:
            rect = obs.pop(0)
            if rect.collidepoint(x,y):
                self.remove_node(n)
                return False
        return True

    def crossObstacle(self, x1, x2, y1, y2):
        # connection between two nodes crosses obstacle or not
        obs = self.obstacles.copy()
        while (len(obs)>0):
            rect = obs.pop(0)
            for i in range(0, 101):
                u = i/100
                y = y1*u + y2*(1-u)
                x = x1*u + x2*(1-u)
            if rect.collidepoint(x,y):
                return True
        return False

    def connect(self, n1, n2):
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        if self.crossObstacle(x1, x2, y1, y2):
            self.remove_node(n2)
            return False
        else:
            return True

    def step(self):
        pass

    def path_to_goal(self):
        pass

    def getPathCoords(self):
        pass

    def bias(self):
        pass
    
    def expand(self):
        pass

    def cost(self):
        pass



