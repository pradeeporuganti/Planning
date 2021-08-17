import matplotlib.pyplot as plt
import numpy as np

class Node():

    def __init__(self, x, y, parent = None):
        self.x = x
        self.y = y
        self.parent = parent


# Generates map with random obstacles
class Map(Node):

    def __init__(self, start, goal ,mapLength, mapHeight, obsLength, obsHeight, numObs = -1, goalFlag = False):
        self.start = start
        self.goal = goal
        self.mapLength = mapLength
        self.mapHeight = mapHeight
        self.obs = []
        self.numObs = int(numObs)
        self.obsLength = obsLength
        self.obsHeight = obsHeight
        self.goalFlag = goalFlag

        # init tree
        self.tree = []
        self.tree.append(Node(self.start[0], self.start[1], None))

        # center point of obstacle ellipse
        self.obsLoc_x = np.zeros([1, self.numObs])
        self.obsLoc_y = np.zeros([1, self.numObs])

        # ellipse x-y points
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
            self.obsLoc_x[0][n] = np.random.uniform(0, self.mapLength - self.obsLength)
            self.obsLoc_y[0][n] = np.random.uniform(0, self.mapHeight - self.obsHeight)
            # make sure that start and end goal are not within obstacles
            if  (((self.start[0] - self.obsLoc_x[0][n])**2/(self.obsLength)**2) + ((self.start[1] - self.obsLoc_y[0][n])**2/(self.obsHeight)**2)) > 1 \
                and (((self.goal[0] - self.obsLoc_x[0][n])**2/(self.obsLength)**2) + ((self.goal[1] - self.obsLoc_y[0][n])**2/(self.obsHeight)**2)) > 1:
                self.obs.append((self.obsLoc_x[0][n], self.obsLoc_y[0][n] ))
            n = n - 1
        
    # Draws current map
    def drawMap(self):
        fig, ax = plt.subplots(1)
        ax.plot(self.start[0], self.start[1], marker=".", markersize=10)
        ax.plot(self.goal[0], self.goal[1], marker=".", markersize=10)
        theta = np.linspace(0, 2*np.pi, 100)
        for n in range(0, self.numObs):
            for t in range(0, len(theta)):
                self.xobs[n][t] = self.obsLength * np.cos(theta[t]) + self.obsLoc_x[0][n]
                self.yobs[n][t] = self.obsHeight * np.sin(theta[t]) + self.obsLoc_y[0][n]
        for n in range(0, self.numObs):
                ax.plot(self.xobs[n][:], self.yobs[n][:], 'k-')

    def drawEdge(self):
        pass

    # generate a map object to pass around
    def genMap(self):
        return [self.start, self.goal, self.mapLength, self.mapHeight, self.numObs, self.obs, self.obsLength, self.obsHeight, self.goalFlag]
        
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
        self.goalFlag = m[8]
    
    # get sample point but dont sample from within obstacle
    def sampleEnv(self):
        check = [False]*self.numObs
        while not all(check):
            samp_x = np.random.uniform(0, self.mapLength)
            samp_y = np.random.uniform(0, self.mapHeight)
            for n in range(0, self.numObs):
                if (((samp_x - self.obs[n][0])**2/(self.obsLength)**2) + ((samp_y - self.obs[n][1])**2/(self.obsHeight)**2)) > 1:
                    check[n] = True
        return((samp_x, samp_y))

    # Find the node in the tree that is nearest to the sampled node
    #def nearest(self):
    #    while not self.goalFlag:
    #        nrand = self.sampleEnv()
    #        nnear = self.start
    #        near_dist = self.distance(self.start, nrand)
    #        for n in self.tree:
    #            if self.distance((n.x, n.y), nrand) < near_dist:
    #                nnear = (n.x, n.y)
    #            else:
    #                pass
    #        if self.checkCollision(nnear, nrand):       # True if no collisions with obstacles
    #            if self.distance(nnear, nrand) > 10:    # make sure new node is lower than 10 units distance
    #                v = list(nnear)-list(nrand)
    #                u = v/np.linalg.norm(v, 2)
    #                nrand = list(nnear) + 10*u          # new point atmost 10 unit distance from nearest node on tree
    #            else:
    #                pass
    #            self.tree.append(Node(nrand[0], nrand[1], nnear))   # add random point to tree
    #            if self.distance(nrand, self.goal) < 5:     # check if random point close enough to goal
    #                self.goalFlag = True
    #            else:
    #                pass
    #        else:
    #            pass

    def checkCollision(self):
        for n in range(0, self.numObs):
            
            
            
            
            # generate line equation
            m = (nnear[1]-samp_y)/(nnear[0]-samp_x)
            c = samp_y - m*samp_x
            D = self.obsLength**2*m**2 + self.obsHeight**2 - c**2 
            if D < 0:
                if self.distance()
                self.tree.append(Node(samp_x, samp_y, nnear))
            else:
                pass
            if self.distance((samp_x, samp_y), (self.goal[0], self.goal[1])) < 5:
                self.tree.append(self.goal[0], self.goal[1], (samp_x, samp_y))
                goalFlag= True

    
    def distance(p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    # Find path to the goal
    #def finalPath:
        

def main():
    start = (5, 40)
    goal = (100, 5)
    m = Map(start, goal, 100, 50, 4.5, 1.5, 10)
    ax = plt.gca()
    p = RRT(m)
    iter = 0
    prev = start
    while (iter < 500):
        (px, py) = p.sampleEnv()
        if RRT.checkCollision(prev, (px, py)):
            Map.drawEdge(prev, (px, py))
        plt.pause(0.005)
        iter = iter + 1
    plt.show()
    
if __name__ == "__main__":
    main()
