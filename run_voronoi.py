import voronoiPlanner as vp 
import graphGenerator as gg 

gg.GraphGenerator(30, 30, 0.1, 'random_graph1_30_30.txt')

v = vp.VoronoiPlanner('random_graph1_30_30.txt')

v.do_wavefront()

v.pretty_print_graph()
v.pretty_print_voronoi()
v.pretty_print_obstacle_wave()