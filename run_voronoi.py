import voronoiPlanner as vp 
import graphGenerator as gg 

# gg.GraphGenerator(100, 100, 0.2, 30, 'random_graph1_100_100.txt')

v = vp.VoronoiPlanner('random_graph1_100_100.txt')

v.pretty_print_graph()
v.pretty_print_voronoi()
v.pretty_print_obstacle_wave()

v.pretty_print_path((6, 30), (45, 30))