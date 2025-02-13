import os
import shutil

def Move_input_to_yolo_folder(Original_dir,yolo_dir,Experiment_name):

    Target_dir=os.path.join(yolo_dir,"Temporary_input")

    if os.path.isdir(Target_dir)==False:
        os.mkdir(Target_dir)

    if os.path.isdir(os.path.join(Target_dir,Experiment_name))==False:
        shutil.move(Original_dir,Target_dir)
    else:
        shutil.rmtree(os.path.join(Target_dir,Experiment_name))
        shutil.move(Original_dir,Target_dir)

    return Target_dir
