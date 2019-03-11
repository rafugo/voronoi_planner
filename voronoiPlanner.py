# this class will take a graph and generate a labelling of the graph with
# the voronoi paths

class VoronoiPlanner:

    def __init__(self, graph):
        # this is the graph given as a two-dimensional array
        # there will be 1's for the obstacles/walls, 0 otherwise
        self.graph = graph

        # this is the adjacency list of the points that are considered
        # as the Voronoi edges
        self.voronoi_paths = {}

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
                                            if self.graph[i + k][j + l] == 0:
                                                # initialize the box counter to 0
                                                if voronoi_counter.get((i+k, j+l)) == None:
                                                    voronoi_counter[(i+k, j+l)] = 1
                                                else:
                                                    voronoi_counter[(i+k, j+l)] += 1

            # once we have gone through the graph
            # set the new value of all the voronoi_counter points
            # and include any that had more than 1 to the voronoi_paths        
            for p in list(voronoi_counter.keys()):
                x = p[0]
                y = p[1]
                if voronoi_counter[p] > 1:
                    self.voronoi_paths[p] = []

                self.graph[x][y] = wave_iteration + 1
                modified = True

        # create the voronoi_paths variables, which essentially creates
        # an adjacency list
        self.create_voronoi_paths()

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







