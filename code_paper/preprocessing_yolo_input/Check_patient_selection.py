import os
import numpy as np

Path_to_model_1="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Total_Bone_detector_Total_dataset"
Path_to_model_2="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Total_Bone_detector_Coronal"
Path_to_model_3="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Total_Bone_detector_Sagital"
dataset="test"
Train_images=os.listdir(os.path.join(Path_to_model_1,"%s/images"%dataset))
Patient_nrs_d1=list(np.unique([i.split("_")[1] for i in Train_images]))
Train_images=os.listdir(os.path.join(Path_to_model_2,"%s/images"%dataset))
Patient_nrs_d2=list(np.unique([i.split("_")[1] for i in Train_images]))
Train_images=os.listdir(os.path.join(Path_to_model_3,"%s/images"%dataset))
Patient_nrs_d3=list(np.unique([i.split("_")[1] for i in Train_images]))

if Patient_nrs_d1==Patient_nrs_d2:
    print("yes")
if Patient_nrs_d1==Patient_nrs_d3:
    print("yes")
print(Patient_nrs_d1)
print(Patient_nrs_d2)
print(Patient_nrs_d3)
