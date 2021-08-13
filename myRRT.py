import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import numpy as np

class Node():

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.parent = None


# Generates map with random obstacles
class Map(Node):

    def __init__(self, start, goal ,mapLength, mapHeight, numObs, obsLength, obsHeight):
        self.start = start
        self.goal = goal
        self.mapLength = mapLength
        self.mapHeight = mapHeight
        self.obs = []
        self.numObs = numObs
        self.obsLength = obsLength
        self.obsHeight = obsHeight
        self.genObs()
        self.drawMap()
        self.genMap()

    # function to generate random map with obstacles
    # Recieves size of map and number of obstacles
    # Returns a map with random obstacles
    def genObs(self):
        n = self.numObs
        while n != 0:
            obsLoc_x = random.uniform(0, self.mapLength - self.obsLength)
            obsLoc_y = random.uniform(0, self.mapHeight - self.obsHeight)
            self.obs.append((obsLoc_x, obsLoc_y))
            n = n - 1

    # Draws current map
    def drawMap(self):
        fig, ax = plt.subplots(1)
        ax.plot(self.start[0], self.start[1], marker=".", markersize=10)
        ax.plot(self.goal[0], self.goal[1], marker=".", markersize=10)
        axlist = fig.axes
        for i in range(0, self.numObs):
            ax.add_patch(Rectangle(self.obs[i], self.obsLength, self.obsHeight))

    def genMap(self):
        return [self.start, self.goal, self.mapLength, self.mapHeight, self.numObs, self.obs, self.obsLength, self.obsHeight]
        
class RRT(Map):

    def __init__(self, h):
        m = h.genMap()
        self.start = m[0]
        self.goal = m[1]
        self.mapLength = m[2]
        self.mapHeight = m[3]
        self.numObs = m[4]
        self.obs = m[5]
        self.obsLength = m[6]
        self.obsHeight = m[7]
    
    def sampleEnv(self):
        #check = [False]*self.numObs
        #while not all(check):
        samp_x = random.uniform(0, self.mapLength)
        samp_y = random.uniform(0, self.mapHeight)
            #for i in range(0, self.numObs):
            #    if samp_x - self.obs[i][0] > self.obsLength and samp_y - self.obs[i][1] > self.obsHeight:
            #        check[i] = True
        return((samp_x, samp_y))
        

def main():
    start = (5, 40)
    goal = (100, 5)
    m = Map(start, goal, 100, 50, 2, 4.5, 1.5)
    ax = plt.gca()
    p = RRT(m)
    iter = 0
    while (iter < 500):
        ax.plot(p.sampleEnv()[0],p.sampleEnv()[1] , 'ro', markersize=2)
        plt.pause(0.005)
        iter = iter + 1
    plt.show()
    
if __name__ == "__main__":
    main()
