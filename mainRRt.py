import pygame
from RRT import RRTGraph
from RRT import RRTMap

def main():
    dimensions = (600, 1000)
    start = (50,50)
    goal = (510,510)
    obsDim  = 30
    obsNum = 50

    pygame.init()
    map = RRTMap(start, goal, dimensions, obsDim, obsNum)
    graph = RRTGraph(start, goal, dimensions, obsDim, obsNum)

    obstacles = graph.makeobs()
    map.drawMap(obstacles)

    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)

if __name__ == '__main__':
    main()
