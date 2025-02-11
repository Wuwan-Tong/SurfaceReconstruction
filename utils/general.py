import os

import numpy as np
import torch
import trimesh
import open3d as o3d


def mkdir_ifnotexists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def as_mesh(scene_or_mesh):
    """
    Convert a possible scene to a mesh.

    If conversion occurs, the returned mesh has only vertex and face data.
    """
    if isinstance(scene_or_mesh, trimesh.Scene):
        if len(scene_or_mesh.geometry) == 0:
            mesh = None  # empty scene
        else:
            # we lose texture information here
            mesh = trimesh.util.concatenate(
                tuple(trimesh.Trimesh(vertices=g.vertices, faces=g.faces)
                    for g in scene_or_mesh.geometry.values()))
    else:
        assert(isinstance(scene_or_mesh, trimesh.Trimesh))
        mesh = scene_or_mesh
    return mesh


def concat_home_dir(path):
    #return os.path.join(os.environ['HOME'],'data',path)
    return path


def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def to_cuda(torch_obj):
    if torch.cuda.is_available():
        return torch_obj.cuda()
    else:
        return torch_obj


def load_point_cloud_by_file_extension(file_name):

    ext = file_name.split('.')[-1]

    if ext == "npz" or ext == "npy":
        point_set = torch.tensor(np.load(file_name)).float()
    else:
        # point_set = torch.tensor(trimesh.load(file_name, ext).vertices).float()
        # WT: read pcd with normals. if the pcd has no normal, comment these lines out and use only the line above, which is for now commentted out bcs trimesh.load() cannot read normal
        pcd=o3d.io.read_point_cloud(file_name)
        np_points = np.asarray(pcd.points)
        np_normals=np.asarray(pcd.normals)
        np_data = np.append(np_points, np_normals, axis=1)
        point_set = torch.tensor(np_data).float()

    return point_set


class LearningRateSchedule:
    def get_learning_rate(self, epoch):
        pass


class StepLearningRateSchedule(LearningRateSchedule):
    def __init__(self, initial, interval, factor):
        self.initial = initial
        self.interval = interval
        self.factor = factor

    def get_learning_rate(self, epoch):
        #return np.maximum(self.initial * (self.factor ** (epoch // self.interval)), 5.0e-6)
        # WT: increase the training rate decreasing speed by multiply epoch with coefficient 10
        return np.maximum(self.initial * (self.factor ** (epoch*10 // self.interval)), 5.0e-6)