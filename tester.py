import matplotlib.pyplot as plt
import numpy as np

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

# collision check for an ellipse
#def checkCollision(p1, p2, obs):
#    obsx = obs[0]; obsy = obs[1]; a= obs[2]; b = obs[3]
#    m = (p2[1] - p1[1])/(p2[0]-p1[0])
#    c_org = p1[1]-m*p1[0]
#    c_new = c_org + m*obsx - obsy
#    D = a**2*m**2 + b**2 - c_new**2 
#    if D < 0:
#        return True
#    else:
#        return False

def on_segment(p1, p2, p):
    return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])

def checkCollision(p1, p2, obsList):
    d = [0]*len(obsList)
    for n in range(0, len(obsList)):
        crnr = list(zip(obsList[n].x, obsList[n].y))
        lines = zip(crnr, crnr[1:] + crnr[:-3])
        for p3, p4 in lines:
            c1 = np.cross([p1[0]-p3[0], p1[1]-p3[1]], [p4[0]-p3[0], p4[1]-p3[1]])
            c2 = np.cross([p2[0]-p3[0], p2[1]-p3[1]], [p4[0]-p3[0], p4[1]-p3[1]])
            c3 = np.cross([p3[0]-p1[0], p3[1]-p1[1]], [p2[0]-p1[0], p2[1]-p1[1]])
            c4 = np.cross([p4[0]-p1[0], p4[1]-p1[1]], [p2[0]-p1[0], p2[1]-p1[1]])
            if ((c1 > 0 and c2 < 0) or (c1 < 0 and c2 > 0)) and ((c3 > 0 and c4 < 0) or (c3 < 0 and c4 > 0)):
                d[n] = False
            elif c1 == 0 and on_segment(p3, p4, p1):
                d[n] = False
            elif c2 == 0 and on_segment(p3, p4, p2):
                d[n] = False
            elif c3 == 0 and on_segment(p1, p2, p3):
                d[n] = False
            elif c4 == 0 and on_segment(p1, p2, p4):
                d[n] = False
            else:
                d[n] = True
    if all(d):
        return False
    else:
        return True

     
def main():
    theta = np.linspace(0, 2*np.pi, 100)
    numobs = 10
    obsLength = 4.5; obsHeight = 2.5
    obsList = []
    
    start = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))
    goal = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))

    for i in range(0, numobs):
        obsx = int(np.random.uniform(0, 100))
        obsy = int(np.random.uniform(0, 100))
        obsList.append(bbox((obsx, obsy), obsLength, obsHeight))

    # if obstacle is an ellipse
    #for n in range(0, numobs):
    #    for t in range(0, len(theta)):
    #        xobs[n][t] = a * np.cos(theta[t]) + obsx[n]
    #        yobs[n][t] = b * np.sin(theta[t]) + obsy[n]

    fig, ax = plt.subplots(1)
    #ax.plot([start[0], goal[0]], [start[1], goal[1]],'b-')
    #ax.plot([start[0], goal[0]], [start[1], goal[1]], marker = '.', markerfacecolor = 'b', markersize = 10)
    #ax.plot(goal[0], goal[1], marker = '.', markerfacecolor = 'g', markersize = 10)

    for n in range(0, len(obsList)):
        x = zip(obsList[n].x, obsList[n].x[1:]+obsList[n].x[:-3])
        y = zip(obsList[n].y, obsList[n].y[1:]+obsList[n].y[:-3])
        for px, py in zip(x, y):
            ax.plot(list(px), list(py), 'r-')
    iter = 0
    while (iter < 500):
        p1 = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))
        p2 = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))
        if not checkCollision(p1, p2, obsList):
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
        iter += 1

    plt.show()

if __name__ == "__main__":
    main()