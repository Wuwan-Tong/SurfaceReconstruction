import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import trimesh
import torch

pcd1 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bones_conv/66900_sca_R_tfm_lay_rot_withNormal.ply')
# pcd2=trimesh.load('U:/Documents/IGR-master/bones_conv/66900_sca_R_tfm_lay_rot_withNormal.ply')
#pcd2 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bone1.ply')
#pcd3 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bone2.ply')
#pcd4 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bone3.ply')
#pcd5 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bone4.ply')
#pcd6 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bone5.ply')
#pcd7 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bone6.ply')
#pcd8 = o3d.io.read_point_cloud('U:/Documents/IGR-master/bone7.ply')

#o3d.visualization.draw_geometries([pcd5,pcd2,pcd3,pcd4,pcd5,pcd6,pcd7,pcd8])
#o3d.visualization.draw_geometries([pcd6])
#o3d.visualization.draw_geometries([pcd7])
#o3d.visualization.draw_geometries([pcd8])

#np_points = np.asarray(pcd1.points)
#min_x=np_points[:,0].min()
#print(min_x)
#temp_pts0=np_points[np_points[:,0]==min_x]
#temp_pts1=np_points[np_points[:,0]==min_x+1]
#temp_pts2=np_points[np_points[:,0]==min_x+2]


#fig1 = plt.figure()
#ax = fig1.add_subplot(projection='3d')
#ax.scatter(np_points[:,0], np_points[:,1], np_points[:,2], c=[0, 1, 0])
# ax.scatter(temp_pts0[:,0], temp_pts0[:,1], temp_pts0[:,2], c=[0, 1, 0])
#ax.scatter(temp_pts1[:,0], temp_pts1[:,1], temp_pts1[:,2], c=[1, 0, 0])
#ax.scatter(temp_pts2[:,0], temp_pts2[:,1], temp_pts2[:,2], c=[0, 0, 1])
#plt.show()

#save normal
#o3d.geometry.PointCloud.estimate_normals(pcd1)
np_points = np.asarray(pcd1.points)
np_normals=np.asarray(pcd1.normals)
np_data=np.append(np_points,np_normals,axis=1)
data=torch.tensor(np_data)
pass
# o3d.io.write_point_cloud('U:/Documents/IGR-master/bones_conv/66900_sca_R_tfm_lay_rot_withNormal.ply', pcd1)
