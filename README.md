# SurfaceReconstruction
## citation
@incollection{icml2020_2086,
 author = {Gropp, Amos and Yariv, Lior and Haim, Niv and Atzmon, Matan and Lipman, Yaron},
 booktitle = {Proceedings of Machine Learning and Systems 2020},
 pages = {3569--3579},
 title = {Implicit Geometric Regularization for Learning Shapes},
 year = {2020}
}
## AI code from https://github.com/amosgropp/IGR
# a short guide for surface reconstruction
you can change the parameters in reconstruction/setup.conf
train{
input_path: the path of the input img
d_in:=3 for 3D images and =2 for 2D
checkpoint_frequency=50 : every 50 epochs save a checkpoint which you can use later for further training, and every 50 epochs plot a trained result, including a ply surface, a html with both surface and pcd, a stl surface
learning_rate_schedule: decide the training rate
}
plot{
resolution: resolution of plot surface, including all output ply, html and stl file. Attention: if the resolution is larger than 128, It would be very! very! very! slow to plot
}
network{
    inputs{
        dims = [ 512, 512, 512, 512, 512, 512, 512, 512 ] : size of CNN layers, according to the paper it can also be changed to 256
        skip_in = [4]: decide which layer is the skip in layer
        radius_init: radius of the init potato
        beta: a param for soft decision
        }
     loss{
        lambda = 0.1 : weight in training loss
        normals_lambda = 1 : weight in training loss
        }

 you can alode change the number of epochs and the batch size in reconstruction/run.py, the arguments at around line 350
 # if pcd without normal
 please read the comments in function load_point_cloud_by_file_extension(file_name), you have to change the code
        
        
        
