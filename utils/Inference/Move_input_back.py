import os
import shutil

def Move_input_back(Original_dir,yolo_dir,Experiment):

    Target_dir=os.path.join(yolo_dir,f"Temporary_input/{Experiment}")

    if os.path.isdir(Target_dir)==False:
        os.mkdir(Target_dir)

    shutil.move(Target_dir,Original_dir)

    shutil.rmtree(os.path.join(Original_dir,"Input"))

    return None
