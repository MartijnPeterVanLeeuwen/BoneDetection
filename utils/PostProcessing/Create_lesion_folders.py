import os
import sys
import numpy as np

def Create_lesion_folders(Path_to_main_folder):

    Path_to_yolo_detection_folder=os.path.join(Path_to_main_folder,"Prediction_yolo")
    Destination_folder=os.path.join(Path_to_main_folder,"Lesions")

    if os.path.isdir(Destination_folder)==False:
        os.mkdir(Destination_folder)

    Axial_folder=os.path.join(Path_to_yolo_detection_folder,'Axial')
    Axial_prediction_folder=os.path.join(Axial_folder,"labels")
    All_axial_files=os.listdir(Axial_prediction_folder)
    All_axial_files=[i for i in All_axial_files if "txt" in i]
    Individual_lesions=np.unique(["_".join(i.split("_")[:2]) for i in All_axial_files])

    No_lesions=len(Individual_lesions)

    for i in Individual_lesions:
        Path_to_lesion_folder=os.path.join(Destination_folder,"Lesion_%s"%(i))
        if os.path.isdir(Path_to_lesion_folder)==False:
            os.mkdir(Path_to_lesion_folder)

    return None
