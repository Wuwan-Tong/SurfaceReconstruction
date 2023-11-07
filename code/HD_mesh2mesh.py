# written by Wuwan Tong 2023/11
import pymeshlab

mesh_set=pymeshlab.MeshSet()
mesh_set.load_new_mesh('U:/Documents/IGR-master/compare/66900_sca_R_tfm.stl')
mesh_set.load_new_mesh('U:/Documents/IGR-master/compare/mesh_800.stl')
ant=mesh_set.apply_filter('hausdorff_distance', targetmesh=1, sampledmesh=0, savesample = True)
max_HD=ant['max']
mean_HD=ant['mean']
print(max_HD)
print(mean_HD)