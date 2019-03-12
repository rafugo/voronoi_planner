# generates random graphs with a given probability of 
# a space being an object

import random

class GraphGenerator:

    # p is the probablity that a spot is an obstacle
    def __init__(self, rows, cols, p, obstacles, filename):
        self.filename = filename  
        self.graph = []      

        for i in range(rows):
            self.graph.append([])
            for j in range(cols):
                self.graph[i].append(0)

        # create a blank map with walls
        for j in range(cols):
            self.graph[0][j] = 1
            self.graph[rows-1][j] = 1

        for i in range(rows):
            self.graph[i][0] = 1
            self.graph[i][cols-1] = 1

        # create random obstacles
        for o in range(obstacles):
            self.create_random_obstacle(rows, cols, p)

        self.write_map()



    # creates random obstacles of different shapes
    # and takes into account not to generate any
    # outside the map
    def create_random_obstacle(self, rows, cols, p):
        self.create_rectangle(rows, cols, p)

    def create_rectangle(self, rows, cols, p):
        # get random lengths for x and y
        xlen = int(random.uniform(0, rows * p))
        ylen = int(random.uniform(0, cols * p))

        # get random starting spot
        x = random.randint(0, rows)
        y = random.randint(0, cols)

        # mark all the spots
        for i in range(xlen):
            k = x + i
            for j in range(ylen):
                l = y + j

                # if inside the graph
                if k < rows and l < cols:
                    self.graph[k][l] = 1





    def write_map(self):
        f = open(self.filename, "w")
        
        for row in self.graph:
            line = ''
            for c in row:
                line += str(c) + ' '
            line = line[:-1]
            f.write(line + '\n')

        f.close()
