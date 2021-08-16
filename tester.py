import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 2*np.pi, 100)
numobs = 3

obsx = np.array([[]])
obsy = np.array([[]])

for i in range(0, numobs):
    obsx = np.append(obsx, [int(np.random.uniform(0, 100))])
    obsy = np.append(obsy, [int(np.random.uniform(0, 100))])

print(obsx)
print(obsy)

xobs = np.zeros([numobs, 100])
yobs = np.zeros([numobs, 100])

for n in range(0, numobs):
    for t in range(0, len(theta)):
        xobs[n][t] = 10 * np.cos(theta[t]) + obsx[n]
        yobs[n][t] = 4 * np.sin(theta[t]) + obsy[n]

fig, ax = plt.subplots(1)
ax.plot(xobs[0][:], yobs[0][:],'r-')
ax.plot(xobs[1][:], yobs[1][:],'k-')
ax.plot(xobs[2][:], yobs[2][:],'b-')

#for n in range(0, numobs):


plt.show()

