import voronoiPlanner as vp 

g = [
    [1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 1], 
    [1, 0, 0, 0, 1], 
    [1, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1]]

v = vp.VoronoiPlanner(g)

v.do_wavefront()

print(v.graph)
print("\n")
print(v.voronoi_paths)