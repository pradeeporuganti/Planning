import matplotlib.pyplot as plt
import numpy as np

def checkCollision(p1, p2, obs):
    obsx = obs[0]; obsy = obs[1]; a= obs[2]; b = obs[3]
    m = (p2[1] - p1[1])/(p2[0]-p1[0])
    c_org = p1[1]-m*p1[0]
    c_new = c_org + m*obsx - obsy
    D = a**2*m**2 + b**2 - c_new**2 
    if D < 0:
        return True
    else:
        return False

def main():
    theta = np.linspace(0, 2*np.pi, 100)
    numobs = 1
    a = 10; b = 4

    obsx = np.array([[]])
    obsy = np.array([[]])

    p1 = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))
    p2 = (int(np.random.uniform(0, 100)), int(np.random.uniform(0, 100)))
    #p1 = (-5, -5)
    #p2 = (-20, -20)

    for i in range(0, numobs):
        obsx = np.append(obsx, int(np.random.uniform(0, 100)))
        obsy = np.append(obsy, int(np.random.uniform(0, 100)))

    xobs = np.zeros([numobs, 100])
    yobs = np.zeros([numobs, 100])

    for n in range(0, numobs):
        for t in range(0, len(theta)):
            xobs[n][t] = a * np.cos(theta[t]) + obsx[n]
            yobs[n][t] = b * np.sin(theta[t]) + obsy[n]

    fig, ax = plt.subplots(1)
    ax.plot(p1[0], p1[1], marker = '.', markersize = 10)
    ax.plot(p2[0], p2[1], marker = '.', markersize = 10)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-')
    for n in range(0, numobs):
        ax.plot(xobs[n][:], yobs[n][:],'r-')
        
    c = checkCollision(p1, p2, (obsx[n], obsy[n], a, b))
    print(c)

    plt.show()

if __name__ == "__main__":
    main()