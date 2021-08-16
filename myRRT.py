import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

class Node():

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.parent = None


# Generates map with random obstacles
class Map(Node):

    def __init__(self, start, goal ,mapLength, mapHeight, obsLength, obsHeight, numObs = -1):
        self.start = start
        self.goal = goal
        self.mapLength = mapLength
        self.mapHeight = mapHeight
        self.obs = []
        self.numObs = int(numObs)
        self.obsLength = obsLength
        self.obsHeight = obsHeight
        self.obsLoc_x = np.zeros([1, self.numObs])
        self.obsLoc_y = np.zeros([1, self.numObs])
        self.xobs = np.zeros([self.numObs, 100])
        self.yobs = np.zeros([self.numObs, 100])
        self.genObs()
        self.drawMap()
        self.genMap()

    # function to generate random map with obstacles
    # Recieves size of map and number of obstacles
    # Returns a map with random obstacles
    def genObs(self):
        n = self.numObs-1
        while not n < 0:
            self.obsLoc_x[n] = np.random.uniform(0, self.mapLength - self.obsLength)
            self.obsLoc_y[n] = np.random.uniform(0, self.mapHeight - self.obsHeight)
            self.obs.append((self.obsLoc_x[n], self.obsLoc_y[n]))
            n = n - 1

    # Draws current map
    def drawMap(self):
        fig, ax = plt.subplots(1)
        ax.plot(self.start[0], self.start[1], marker=".", markersize=10)
        ax.plot(self.goal[0], self.goal[1], marker=".", markersize=10)
        theta = np.linspace(0, 2*np.pi, 100)
        for n in range(0, self.numObs):
            for t in range(0, len(theta)):
                self.xobs[t][n] = self.obsLength * np.cos(math.radians(theta[t])) + self.obsLoc_x[n]
                self.yobs[t][n] = self.obsHeight * np.sin(math.radians(theta[t])) + self.obsLoc_y[n]
        print(self.xobs[:][0])
        for n in range(0, self.numObs):
            for i in range(0, len(theta)):
                ax.plot(self.xobs[i][n], self.yobs[i][n])

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
        samp_x = np.random.uniform(0, self.mapLength)
        samp_y = np.random.uniform(0, self.mapHeight)
            #for i in range(0, self.numObs):
            #    if samp_x - self.obs[i][0] > self.obsLength and samp_y - self.obs[i][1] > self.obsHeight:
            #        check[i] = True
        return((samp_x, samp_y))

def main():
    start = (5, 40)
    goal = (100, 5)
    m = Map(start, goal, 100, 50, 4.5, 1.5, 2)
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
