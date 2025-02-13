import os
import shutil

def Move_yolo_prediction(Original_dir,yolo_dir,Experiment):

    Target_dir=os.path.join(yolo_dir,f"runs/detect/{Experiment}")

    if os.path.isdir(Target_dir)==False:
        os.mkdir(Target_dir)

    Experiment_folder=Original_dir
    if os.path.isdir(Experiment_folder)==False:
        os.mkdir(Experiment_folder)

    Yolo_prediction_folder=os.path.join(Experiment_folder,"Prediction_yolo")
    Bone_detection_folder=os.path.join(Yolo_prediction_folder,"Bone_detection")
    if os.path.isdir(Bone_detection_folder)==False:
        os.mkdir(Yolo_prediction_folder)
        os.mkdir(Bone_detection_folder)
    shutil.move(Target_dir,Yolo_prediction_folder)

    os.rename(os.path.join(Yolo_prediction_folder,Experiment),Bone_detection_folder)

    return None
