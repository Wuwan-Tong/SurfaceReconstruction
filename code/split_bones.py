# writen by Wuwan Tong 2023/11
import SimpleITK as sitk
import numpy as np
import math
import open3d as o3d

# load image with all 8 bones
pathImage='U:/Documents/IGR-master/dSampOut_femur/Seg_Left_F.nii.gz'
img_file=sitk.ReadImage(pathImage)
img = sitk.GetArrayFromImage(img_file) # include elements0,1,2,3,4,5,6,7,8
spacing_img=img_file.GetSpacing() # in form [y,z,x]

# set voxel number threshold for processing x_min and x_max surface of the bone
vox_num_th=30

# split bones
bones=np.zeros((8,np.size(img,0),np.size(img,1),np.size(img,2)))
temp_bone=np.zeros((np.size(img,0),np.size(img,1),np.size(img,2)))
for idx_bone in np.arange(0,8,1):
    temp_bone[:,:,:]=img[:,:,:]
    # print(np.any(temp_bone == idx_bone+1))
    temp_bone[temp_bone != idx_bone+1] = 0
    temp_bone[temp_bone != 0]=1
    bones[idx_bone,:,:,:]=temp_bone

# for each bone slice alone z axis, get it's contour
bones_contour=[]
for idx_bone in np.arange(0,8,1):
    # single bone centralization
    temp_bone[:,:,:]=bones[idx_bone,:,:,:]
    #print(np.any(temp_bone ==1))

    # find contour voxel if itself ==1 and has at least one neighbor ==0, and fulfill the x_min cover and x_max cover if it's space > vox_num_th
    temp_contour=np.zeros((np.size(temp_bone,0),np.size(temp_bone,1),np.size(temp_bone,2)))
    # set a flag to check if the current frame has arrived x_max or x_min
    flag_max=False
    flag_min=False
    for i_x in np.arange(1,np.size(temp_contour,0)-1,1):
        if not flag_min:
            if not np.any(temp_bone[i_x, :, :]): continue # not reach x_min, skip when the frame is empty
            # reach bone
            flag_min=True # arrive x_min
            # m_min=i_x, process x_min
            if(np.sum(temp_bone[i_x, :, :])) > vox_num_th:
                # create a half x_min surface at i_x-1
                nz_min = np.nonzero(temp_bone[i_x, :, :])
                cent_min = [math.floor((nz_min[0].max() + nz_min[0].min()) / 2),
                            math.floor((nz_min[1].max() + nz_min[1].min()) / 2)]
                temp_contour[i_x-1,cent_min[0],cent_min[1]]=1
                for i in np.arange(np.size(nz_min,axis=1)):
                    temp_contour[i_x - 1,math.floor((nz_min[0][i]+cent_min[0])/2),math.floor((nz_min[1][i]+cent_min[1])/2)]=1
        else: # x_min arrived, x_max not yet
            if not np.any(temp_bone[i_x, :, :]): # arrive x_max
                if not flag_max:
                    flag_max=True
                    if (np.sum(temp_bone[i_x-1, :, :])) > vox_num_th: # x_max=i_x-1, process x_max
                        # create a half x_max surface at i_x
                        nz_max = np.nonzero(temp_bone[i_x-1, :, :])
                        cent_max = [math.floor((nz_max[0].max() + nz_max[0].min()) / 2),
                                    math.floor((nz_max[1].max() + nz_max[1].min()) / 2)]
                        temp_contour[i_x, cent_max[0], cent_max[1]] = 1
                        for i in np.arange(np.size(nz_max,axis=1)):
                            temp_contour[i_x, math.floor((nz_max[0][i] + cent_max[0]) / 2), math.floor((nz_max[1][i] + cent_max[1]) / 2)] = 1
                else: continue # x_max has been processed, skip when the frame is empty
        for i_y in np.arange(1, np.size(temp_contour, 1)-1, 1):
            if not np.any(temp_bone[i_x, i_y, :]): continue # skip if the row is all zero
            for i_z in np.arange(1, np.size(temp_contour, 2)-1, 1):
                if temp_bone[i_x,i_y,i_z]==1 and np.any(temp_bone[i_x,i_y-1:i_y+2,i_z-1:i_z+2]==0):
                    temp_contour[i_x,i_y,i_z]=1

    #nz1 = temp_contour.nonzero()
    #fig1 = plt.figure()
    #ax = fig1.add_subplot(projection='3d')
    #ax.scatter(nz1[0], nz1[1], nz1[2], c=[0, 1, 0])
    #plt.show()
    bones_contour.append(temp_contour)

# output as ply file
for idx_bone in np.arange(0,8,1):
    nz = bones_contour[idx_bone].nonzero()
    pts = np.zeros((np.size(nz, 1), 3))
    pts[:, 0] = nz[0]*spacing_img[2]
    pts[:, 1] = nz[1]*spacing_img[0]
    pts[:, 2] = nz[2]*spacing_img[1]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)
    path='./bone%d.ply'%idx_bone
    o3d.io.write_point_cloud(path, pcd)

