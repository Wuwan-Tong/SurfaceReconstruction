# written by Wuwan Tong 2023/11
import os
import numpy as np
import open3d as o3d

# path of raw and centralized file path
home_dir=os.path.abspath(os.pardir)
path_dir=os.path.join(home_dir,'uncent_bones')
path_out=os.path.join(home_dir,'center')

for file_name in os.listdir(path_dir):

    # read pcd
    pcd = o3d.io.read_point_cloud(os.path.join(path_dir,file_name))

    # get xyz values of pcd in np array
    np_points = np.asarray(pcd.points)

    # find center of the bone
    center_pcd, _ =np.meshgrid(np.mean(np_points,axis=0),np.ones((np_points.shape[0])))

    # move the bone center to [0 0 0]
    np_points=np_points-center_pcd

    # make it smaller
    #np_points=np_points/10

    #transfer back to ply file
    pcd.points = o3d.utility.Vector3dVector(np_points)
    o3d.io.write_point_cloud(os.path.join(path_out,file_name), pcd)


