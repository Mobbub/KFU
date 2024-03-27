import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import pyvista as pv

your_mesh = mesh.Mesh.from_file("tri.stp")

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
pyplot.show()

mesh = pv.UnstructuredGrid(your_mesh.points, your_mesh.simplices)

adapted_mesh = mesh.delaunay_3d(alpha=2.0)

adapted_mesh.plot()

adapted_mesh.save("adapted_objectz.stp")