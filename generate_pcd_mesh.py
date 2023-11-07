# written by Wuwan Tong 2023/11
import copy
import numpy as np
import open3d as o3d
import math

# read mesh
mesh=o3d.io.read_triangle_mesh('U:/Documents/IGR-master/uncent_bones/66900_sca_R_tfm.stl')

mesh.compute_vertex_normals()

# copy mesh
mesh_r=copy.deepcopy(mesh)

# rotate 30 grad alone y and then 30 grad alone z
R_y=[[np.sqrt(3)/2, 0, 1/2],[0, 1, 0], [-1/2, 0, np.sqrt(3)/2]]
R_z=[[np.sqrt(3)/2, -1/2, 0], [1/2, np.sqrt(3)/2, 0], [0, 0, 1]]
R=np.dot(R_z,R_y)

# rotate mesh
mesh_r.rotate(R,center=(0,0,0))
o3d.io.write_triangle_mesh('U:/Documents/IGR-master/compare/66900_sca_R_tfm_rot.stl',mesh_r)

# sample pcd
pcd_ori = mesh.sample_points_uniformly(number_of_points=80000)
pcd_ori1=copy.deepcopy(pcd_ori)
#o3d.visualization.draw_geometries([pcd_ori])
np_points_ori = np.asarray(pcd_ori.points)

temp2=np.transpose(np_points_ori)
np_points_ori=np.transpose(np.dot(R,temp2))
pcd_ori.points = o3d.utility.Vector3dVector(np_points_ori)

# show result of rotation
o3d.visualization.draw_geometries([pcd_ori1,mesh])
o3d.visualization.draw_geometries([pcd_ori,mesh_r])

# get the max and min of point position alone x axis to get the thickness of each layer
x_max=np_points_ori[:,0].max()
x_min=np_points_ori[:,0].min()
num_layer=25
layer_dist=(x_max-x_min)/num_layer

#take only 10% of the points that closest to the layers, move them to the layer and delete the rest points
np_points_ori_temp1=np_points_ori[np.abs((np_points_ori[:,0]-x_min)%layer_dist)<0.05*layer_dist]
np_points_ori_temp2=np_points_ori[np_points_ori[:,0]-x_min<0.1*layer_dist]
np_points_ori_temp2=np_points_ori_temp2[np_points_ori_temp2[:,0]-x_min>0.05*layer_dist]
np_points_ori_temp3=np_points_ori[x_max-np_points_ori[:,0]<0.1*layer_dist]
np_points_ori_temp3=np_points_ori_temp3[x_max-np_points_ori_temp3[:,0]>0.05*layer_dist]
np_points_ori=np.append(np_points_ori_temp1,np_points_ori_temp2,axis=0)
np_points_ori=np.append(np_points_ori,np_points_ori_temp3,axis=0)
np_points_ori[x_max-np_points_ori[:,0]<0.1*layer_dist]+=layer_dist*0.5

pt_num=np.size(np_points_ori,0)
# print(pt_num)
np_points_layer=np.zeros((pt_num,3))
np_points_layer[:,:]=np_points_ori[:,:]
for i_pt in np.arange(pt_num):
    np_points_layer[i_pt,0]=math.floor((np_points_layer[i_pt,0]-x_min+0.05*layer_dist)/(layer_dist))*(layer_dist)+x_min
#transfer back to ply file
pcd_ori.points = o3d.utility.Vector3dVector(np_points_layer)
o3d.visualization.draw_geometries([pcd_ori])
o3d.io.write_point_cloud('U:/Documents/IGR-master/bones_conv/66900_sca_R_tfm_lay_rot.ply', pcd_ori)