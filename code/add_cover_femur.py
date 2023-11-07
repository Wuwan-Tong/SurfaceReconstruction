import os
import numpy as np
import open3d as o3d
from scipy.spatial import ckdtree

# path of raw and centralized file path
home_dir = os.path.abspath(os.pardir)
path_dir = os.path.join(home_dir, 'uncent_bones')
path_out = os.path.join(home_dir, 'center')

z_max=100

for file_name in os.listdir(path_dir):
    # read pcd
    pcd = o3d.io.read_point_cloud(os.path.join(path_dir, file_name))

    # get xyz values of pcd in np array
    np_points = np.asarray(pcd.points)

    # cut bone
    np_points = np_points[np_points[:, 2] < z_max]

    ## add cover at the cut plane

    # find the [x,y] value range of the cut plane
    points_near_cut_plane=np_points[np_points[:, 2] > 96]
    x_max = points_near_cut_plane[:,0].max()
    x_min = points_near_cut_plane[:,0].min()
    y_max = points_near_cut_plane[:,1].max()
    y_min = points_near_cut_plane[:,1].min()

    # projection of contour on xy plane
    bone_countor = []
    bone_countor.append([[x, y] for x, y, z in points_near_cut_plane])

    # create a rectangular point group with [(x_min,y_min),(x_max,y_max)]
    x_range=np.linspace(x_min,x_max,5)
    y_range = np.linspace(y_min, y_max, 5)
    point_group=[]
    point_group.append([[x,y] for x in x_range for y in y_range])

    map=np.zeros((int(x_max()),int(y_max)))
    for x,y in bone_countor:
        map[x, y] = 1

    nz=np.nonzero(map)
    # add xy values to 3D points group with z=100
    for i in np.arange(0,np.size(nz, 1),1):
        np.append(np_points,[[nz[0][i],nz[1][i],z_max]],axis=0)

    # transfer back to ply file
    pcd.points = o3d.utility.Vector3dVector(np_points)
    o3d.io.write_point_cloud(os.path.join(path_out, file_name), pcd)


