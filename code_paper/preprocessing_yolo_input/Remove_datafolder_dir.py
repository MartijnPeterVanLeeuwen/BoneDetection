import os
import sys
import shutil

def Remove_dir(Target_path):

    print(os.path.isdir(Target_path))
    if os.path.isdir(Target_path):
        shutil.rmtree(Target_path)

    return None


Path_to_target_folder="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Total_Bone_detector_Total_dataset"
#Path_to_target_folder="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Sagital_v2"
#Path_to_target_folder="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Total_Bone_detector_Coronal"
Remove_dir(Path_to_target_folder)
