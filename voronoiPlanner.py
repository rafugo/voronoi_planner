# this class will take a graph and generate a labelling of the graph with
# the voronoi paths

class VoronoiPlanner:

    def __init__(self, filename):
        # this is the graph given as a two-dimensional array
        # there will be 1's for the obstacles/walls, 0 otherwise
        self.graph = []
        self.obstacle_wave = {}
        
        f = open(filename, "r")
        x = 0
        for line in f:
            line = line.strip().split(' ')

            row = []
            y = 0
            for c in line:
                row.append(int(c))

                # initialize the tagging
                self.obstacle_wave[(x, y)] = []
                y += 1

            self.graph.append(row)
            x += 1

        f.close()

        # this is the adjacency list of the points that are considered
        # as the Voronoi edges
        self.voronoi_paths = {}

        # initialize the obstacle wave
        self.init_obstacle_wave()

    # fills in the initial wave tags for the obstacles and walls
    def init_obstacle_wave(self):

        # give each obstacle a tag
        # first mark the boundaries
        for j in range(len(self.graph[0])):
            self.obstacle_wave[(0, j)] = ['w1']
            self.obstacle_wave[(len(self.graph)-1, j)] = ['w3']

        for i in range(len(self.graph)):
            self.obstacle_wave[(i, len(self.graph[0])-1)] = ['w2']
            self.obstacle_wave[(i, 0)] = ['w4']

        # this allows us to track each wave
        # from each obstacle, and set the 
        # voronoi edges where the waves meet
        obs_num = 1
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                # skip if already labelled or not an obstacle
                if self.obstacle_wave[(i, j)] != [] or self.graph[i][j] != 1:
                    continue

                # look around to identify which obstacle group it pertains to
                tag = None
                for k in [-1, 0, 1]:
                    for l in [-1, 0, 1]:

                        # check nondiagonals for obstacle tags, as well as
                        # dont check for wall tags
                        if k*l == 0 and \
                                self.obstacle_wave.get((i+k, j+l)) != [] \
                                and self.obstacle_wave.get((i+k, j+l))[0][0] != 'w':

                            tag = self.obstacle_wave[(i+k, j+l)][0]

                # if there are no surrounding tags, create our own
                if tag == None:
                    tag = 'o' + str(obs_num)
                    obs_num += 1
                    
                self.obstacle_wave[(i, j)] = [tag]
                


    # Performs the wavefront algorithm on the graph,
    # populating the Voronoi paths structure
    def do_wavefront(self):
        # the way this works:
        # start at 1.
        # for all boxes around the number that do not already have a set number,
        # increment the counter for that box. If there is more than 1 counter,
        # that box is a voronoi edge point.
        #
        # once we have all the voronoi edge points, we then must generate the 
        # edges that connect the points together and populate the voronoi_paths

        # tracks if we have added a number to a box. 
        # Once False, we will be done
        modified = True
        wave_iteration = 0

        
        voronoi_counter = {}

        while (modified == True):
            modified = False
            wave_iteration += 1

            # counts how many times a given box was attempted to be modified
            voronoi_counter = {}

            # iterate through all the graph
            for i in range(len(self.graph)):
                for j in range(len(self.graph[i])):
                    current_tags = self.obstacle_wave[(i, j)]

                    # if the box is a wave_iteration, +1 to all the boxes
                    # around it that are 0
                    if self.graph[i][j] == wave_iteration:
                       
                        # go around the box, NOT including diagonals
                        for k in [-1, 0, 1]:
                            for l in [-1, 0, 1]:
                                # this ensures we dont diagonalize
                                if k * l == 0:

                                    # if inside the graph
                                    if i + k < len(self.graph) and i + k >= 0:
                                        if j + l < len(self.graph[i]) and j + l >= 0:

                                            # if it is 0, increase the counter
                                            # and add a wave tag
                                            if self.graph[i + k][j + l] == 0:
                                                # initialize the box counter to 1
                                                if voronoi_counter.get((i+k, j+l)) == None:
                                                    voronoi_counter[(i+k, j+l)] = 1
                                                else:
                                                    voronoi_counter[(i+k, j+l)] += 1

                                                if not self.check_tags(current_tags, self.obstacle_wave[(i+k, j+l)]):
                                                    for t in current_tags:
                                                        self.obstacle_wave[(i+k, j+l)].append(t)

                    # this will attempt to deal with the even edge case
                    elif self.graph[i][j] == wave_iteration - 1:
                        # go around the box, NOT including diagonals
                        for k in [-1, 0, 1]:
                            for l in [-1, 0, 1]:
                                # this ensures we dont diagonalize
                                if k * l == 0:

                                    # if inside the graph
                                    if i + k < len(self.graph) and i + k >= 0:
                                        if j + l < len(self.graph[i]) and j + l >= 0:

                                            # if there is another box next 
                                            # to it with the same number
                                            # and it does not share any tags,
                                            # add it
                                            if self.graph[i + k][j + l] == \
                                                    wave_iteration - 1 and \
                                                    wave_iteration > 2:

                                                if not self.check_tags(current_tags, self.obstacle_wave[(i+k, j+l)]):
                                                    for t in current_tags:
                                                        self.obstacle_wave[(i+k, j+l)].append(t)

                                                    voronoi_counter[(i+k, j+l)] = 2

            # once we have gone through the graph
            # set the new value of all the voronoi_counter points
            # and include any that had more than 1 to the voronoi_paths        
            for p in list(voronoi_counter.keys()):
                x = p[0]
                y = p[1]
                if voronoi_counter[p] > 1 and len(self.obstacle_wave[(x, y)]) > 1:
                    self.voronoi_paths[p] = []

                self.graph[x][y] = wave_iteration + 1
                modified = True

                voronoi_counter[p] = 0


        # create the voronoi_paths variables, which essentially creates
        # an adjacency list
        self.create_voronoi_paths()

    # checks if two lists contain any similar elements
    def check_tags(self, t1, t2):
        for t in t1:
            for tt in t2:
                if t == tt:
                    return True

    # call this once we have the voronoi_paths objects,
    # and need to find edges
    def create_voronoi_paths(self):

        # for each point, check all it's surrounding points and 
        # add those to its list (this includes diagonal points)
        for p in list(self.voronoi_paths.keys()):
            i = p[0]
            j = p[1]
            for k in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    # dont count yourself
                    if k == 0 and l == 0:
                        continue

                    if self.voronoi_paths.get((i + k, j + l)) != None:
                        self.voronoi_paths[p].append((i + k, j + l))


    # this pretty prints the graph
    # to the "output_graph.txt" file
    def pretty_print_graph(self):
        f = open('output_graph.txt', "w")
        
        for row in self.graph:
            line = ''
            for c in row:
                line += str(c) + ' '
            line = line[:-1]
            f.write(line + '\n')

        f.close()

    # this pretty prints the voronoi boundary
    # to the "output_voronoi.txt" file
    def pretty_print_voronoi(self):
        f = open('output_voronoi.txt', "w")
        
        for i in range(len(self.graph)):
            line = ''
            for j in range(len(self.graph[i])):
                value = self.graph[i][j]
                if value == 1:
                    line += '1 '
                
                elif self.voronoi_paths.get((i, j)) != None:
                    line += '. '

                else:
                    line += '  '

            line = line[:-1]
            f.write(line + '\n')

        f.close()

    # this pretty prints the obstacle_wave
    # to the "output_obstacle_wave.txt" file
    def pretty_print_obstacle_wave(self):
        f = open('output_obstacle_wave.txt', "w")
        
        for i in range(len(self.graph)):
            line = ''
            for j in range(len(self.graph[i])):
                value = self.obstacle_wave[(i, j)]
                if value == []:
                    line += '   '
            
                else:
                    line += str(value[0]) + ' '

            line = line[:-1]
            f.write(line + '\n')

        f.close()










