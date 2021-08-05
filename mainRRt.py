import pygame
from RRT import RRTGraph
from RRT import RRTMap

def main():
    dimensions = (600, 1000)
    start = (50,50)
    goal = (510,510)
    obsDim  = 30
    obsNum = 50 
    iteration = 0

    pygame.init()
    map = RRTMap(start, goal, dimensions, obsDim, obsNum)
    graph = RRTGraph(start, goal, dimensions, obsDim, obsNum)

    obstacles = graph.makeobs()
    map.drawMap(obstacles)

    while(True):
        x, y = graph.sample_env()
        n = graph.number_of_nodes()
        graph.add_node(n,x,y)
        graph.add_edge(n-1,n)
        x1, y1  = graph.x[n], graph.y[n]
        x2, y2  = graph.x[n-1], graph.y[n-1]
        if(graph.isFree()):
            pygame.draw.circle(map.map, map.red, (graph.x[n], graph.y[n]), map.noderad, map.nodeThickness)
            if not graph.crossObstacle(x1, x2, y1, y2):
                pygame.draw.line(map.map, map.blue, (x1,y1), (x2,y2), map.edgeThickness)
        
        pygame.display.update()


    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)

if __name__ == '__main__':
    main()
