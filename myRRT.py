import matplotlib.pyplot as plt
import numpy as np

class Node():

    def __init__(self, x, y, parent = None):
        self.x = x
        self.y = y
        self.parent = parent

class bbox():

    def __init__(self, n, obsLength = 4.5, obsHeight = 2.5):
        self.ox = n[0]
        self.oy = n[1]
        self.obsLength = obsLength
        self.obsHeight = obsHeight
        self.x = [0]*4
        self.y = [0]*4
        self.genCorner()

    def genCorner(self):
        self.x[0], self.y[0] = self.ox-(self.obsLength/2), self.oy+(self.obsHeight/2)
        self.x[1], self.y[1] = self.ox-(self.obsLength/2), self.oy-(self.obsHeight/2)
        self.x[2], self.y[2] = self.ox+(self.obsLength/2), self.oy-(self.obsHeight/2)
        self.x[3], self.y[3] = self.ox+(self.obsLength/2), self.oy+(self.obsHeight/2)

# Generates map with random obstacles
class Map(Node):

    def __init__(self, start, goal ,mapLength, mapHeight, obsLength, obsHeight, numObs = -1, goalFlag = False):
        self.start = start
        self.goal = goal
        self.mapLength = mapLength
        self.mapHeight = mapHeight
        self.obsList = []
        self.numObs = int(numObs)
        self.obsLength = obsLength
        self.obsHeight = obsHeight
        self.goalFlag = goalFlag

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
    # Returns a list with random obstacles
    def genObs(self):
        n = self.numObs
        while n >= 1:
            obsx = int(np.random.uniform(0, self.mapLength - self.obsLength))
            obsy = int(np.random.uniform(0, self.mapHeight - self.obsHeight))
            rect = bbox((obsx, obsy), self.obsLength, self.obsHeight)
            # check is starting and goal point are within obstacles
            # if yes continue back to loop start
            if ((rect.x[0] < self.start[0] < rect.x[2]) and (rect.y[0] < self.start[1] < rect.y[2])) or \
                ((rect.x[0] < self.goal[0] < rect.x[2]) and (rect.y[0] < self.goal[1] < rect.y[2])):
                continue
            else:
                self.obsList.append(rect)
                n -= 1
        
    # Draws current map
    def drawMap(self):
        fig, ax = plt.subplots(1)
        ax.plot(self.start[0], self.start[1], marker=".", markersize=10)
        ax.plot(self.goal[0], self.goal[1], marker=".", markersize=10)
        for n in range(0, len(self.obsList)):
            x = zip(self.obsList[n].x, self.obsList[n].x[1:]+self.obsList[n].x[:-3])
            y = zip(self.obsList[n].y, self.obsList[n].y[1:]+self.obsList[n].y[:-3])
            for px, py in zip(x, y):
                ax.plot(list(px), list(py), 'r-')

    def drawEdge(self, p1, p2):
        ax = plt.gca()
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')

    # generate a map object to pass around
    def genMap(self):
        return [self.start, self.goal, self.mapLength, self.mapHeight, self.numObs, self.obsList, self.obsLength, self.obsHeight, self.goalFlag]
        
class RRT(Map):

    def __init__(self, h):
        m = h.genMap()
        self.start = m[0]
        self.goal = m[1]
        self.mapLength = m[2]
        self.mapHeight = m[3]
        self.numObs = m[4]
        self.obsList = m[5]
        self.obsLength = m[6]
        self.obsHeight = m[7]
        self.goalFlag = m[8]
        self.path = []

        # init tree
        self.tree = []
        self.tree.append(Node(self.start[0], self.start[1], None))
    
    # get sample point but dont sample from within obstacle
    def sampleEnv(self):
        check = [False]*self.numObs
        while not all(check):
            samp_x = int(np.random.uniform(0, self.mapLength))
            samp_y = int(np.random.uniform(0, self.mapHeight))
            for n in range(0, self.numObs):
                if (self.obsList[n].x[0] < samp_x < self.obsList[n].x[2]) and (self.obsList[n].y[1] < samp_y < self.obsList[n].y[0]):
                    check[n] = False
                else:
                    check[n] = True
        return((samp_x, samp_y))

    # Find the node in the tree that is nearest to the sampled node
    def nearest(self):
        nnear = self.start
        while not self.goalFlag:
            nrand = self.sampleEnv()
            near_dist = self.distance(nnear, nrand)
            for n in self.tree:
                if self.distance((n.x, n.y), nrand) <= near_dist:
                    nnear = (n.x, n.y)
                else:
                    pass
            if not self.checkCollision(nnear, nrand):       # True if no collisions with obstacles
                if self.distance(nnear, nrand) > 20:    # make sure new node is lower than 10 units distance
                    v = [nrand[0]-nnear[0], nrand[1]-nnear[1]]
                    u = v/np.linalg.norm(v, 2)
                    nrand = list(nnear) + 20*u          # new point atmost 10 unit distance from nearest node on tree
                else:
                    pass
                self.tree.append(Node(nrand[0], nrand[1], nnear))   # add random point to tree
                ax = plt.gca()
                ax.plot(nrand[0], nrand[1],marker = 'x')
                if self.distance(nrand, self.goal) < 5:     # check if random point close enough to goal
                    self.goalFlag = True
                else:
                    pass
            else:
                pass
        print(self.tree)

    def on_segment(self, p1, p2, p):
        return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])

    def location(self, p1, p2, p):
        check = ((p2[0]-p1[0])*(p[1]-p1[1])) - ((p2[1]-p1[1])*(p[0]-p1[0]))
        return check
        

    def checkCollision(self, p1, p2):
        d = [0]*self.numObs
        for n in range(0, len(self.obsList)):
            crnr = list(zip(self.obsList[n].x, self.obsList[n].y))
            lines = zip(crnr, crnr[1:] + crnr[:-3])
            line = 0; c = [0]*4
            for p3, p4 in lines:
                c1 = self.location(p3, p4, p1)
                c2 = self.location(p3, p4, p2)
                c3 = self.location(p1, p2, p3)
                c4 = self.location(p1, p2, p4)
                if ((c1 > 0 and c2 < 0) or (c1 < 0 and c2 > 0)) and ((c3 > 0 and c4 < 0) or (c3 < 0 and c4 > 0)):
                    c[line] = False
                elif c1 == 0 and self.on_segment(p3, p4, p1):
                    c[line] = False
                elif c2 == 0 and self.on_segment(p3, p4, p2):
                    c[line] = False
                elif c3 == 0 and self.on_segment(p1, p2, p3):
                    c[line] = False
                elif c4 == 0 and self.on_segment(p1, p2, p4):
                    c[line] = False
                else:
                    c[line] = True
                line += 1
            d[n] = all(c)
        #print(d)
        if all(d):
            return False
        else:
            return True

    def distance(self, p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    # Find path to the goal
    #def finalPath(self):
    #    self.path.append(self.tree[-1])
    #    node = self.tree[-1]
    #    while not node.parent == None:
    #        for n in self.tree:
    #            if node.parent == (n.x, n.y):                
        
def main():
    start = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))
    goal = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))
    m = Map(start, goal, 100, 50, 4.5, 2.5, 2)
    ax = plt.gca()
    p = RRT(m)
    #iter = 0
    prev = start
    #while (iter < 500):
    p.nearest()
        #ax.plot(psamp[0], psamp[1], marker = '.')
        #check = p.checkCollision(prev, psamp)
        #if not check:
            #print('here')
            #print(check)
        #    m.drawEdge(prev, psamp)
        #else:
            #print('not here')
            #pass
        #prev = psamp
        #plt.pause(0.05)
        #iter = iter + 1
    plt.show()
    
if __name__ == "__main__":
    main()
