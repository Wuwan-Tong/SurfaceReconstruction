# written by Wuwan Tong 2023/11
import trimesh
import os
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

# path of raw and centralized file path
home_dir=os.path.abspath(os.pardir)
path_dir=os.path.join(home_dir,'compare')

# read pcd
pcd = o3d.io.read_point_cloud(os.path.join(path_dir,'3_R_R_00_2_00001_GT.ply'))
np_points = np.asarray(pcd.points)
# read mesh
mesh700=trimesh.load_mesh(os.path.join(path_dir,'mesh_test_700.stl'))

fig1=plt.figure()
ax=fig1.add_subplot(projection='3d')
ax.plot_trisurf(mesh700.vertices[:, 0], mesh700.vertices[:,1], mesh700.vertices[:,2], triangles=mesh700.faces)
ax.scatter(np_points[:, 0],np_points[:, 1],np_points[:, 2], c= [0,1,0])
plt.show()
