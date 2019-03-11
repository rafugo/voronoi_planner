import voronoiPlanner as vp 
import graphGenerator as gg 

gg.GraphGenerator(30, 30, 0.1, 'random_graph1_30_30.txt')

v = vp.VoronoiPlanner('random_graph1_30_30.txt')

v.do_wavefront()

print(v.graph)
print("\n")
print(v.voronoi_paths)

v.pretty_print_graph()
v.pretty_print_voronoi()