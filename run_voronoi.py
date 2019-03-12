import voronoiPlanner as vp 
import graphGenerator as gg 

# gg.GraphGenerator(30, 30, 0.4, 7, 'random_graph1_30_30.txt')

v = vp.VoronoiPlanner('random_graph1_30_30.txt')

v.pretty_print_graph()
v.pretty_print_voronoi()
v.pretty_print_obstacle_wave()

v.pretty_print_path((2, 20), (26, 4))