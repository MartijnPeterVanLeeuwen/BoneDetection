import os
import sys
import nibabel as nib
import numpy as np



Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from CODE_Totalsegmenter.Data_exploration.Return_desired_scans import Return_desired_patients
from CODE_Unet.General_Functions_Preprocessing.Loading_and_saving_data import Data_processing
from CODE_Totalsegmenter.Pre_processing_yolo.Apply_windowing import Apply_windowing
from Create_nnUnet_dir import Set_up_nnUNET_dir

Functions = Data_processing()

Path_to_CT="/home/mleeuwen/DATA/TSv3_Selection/Images"
Path_to_label="/home/mleeuwen/DATA/TSv3_Selection/Labels"

Path_to_yolo_data="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Axial_BSv2_v5"
Path_to_train=os.path.join(Path_to_yolo_data,'train/labels')
Path_to_val=os.path.join(Path_to_yolo_data,'val/labels')
Path_to_test=os.path.join(Path_to_yolo_data,'test/labels')

training_images=os.listdir(Path_to_train)
Unique_train_scans=np.unique([i.split('_')[1] for i in training_images])
Training_CT_scans=["Scan_%s.nii"%i for i in Unique_train_scans]
validation_images=os.listdir(Path_to_val)
Unique_val_scans=np.unique([i.split('_')[1] for i in validation_images])
Validation_CT_scans=["Scan_%s.nii"%i for i in Unique_val_scans]
test_images=os.listdir(Path_to_test)
Unique_test_scans=np.unique([i.split('_')[1] for i in test_images])
Test_CT_scans=["Scan_%s.nii"%i for i in Unique_test_scans]

Path_to_results="/home/mleeuwen/DATA/nnUnet_data"
Directories=Set_up_nnUNET_dir(Path_to_results,'Bonesegmentation_20mm')

L=400
W=1800
for i in range(len(Unique_train_scans)):

    Im_name="Scan_%s.nii"%Unique_train_scans[i]
    Image,Header=Functions.Loading_Nifti_data(Path_to_CT,Im_name)
    Label,Header=Functions.Loading_Nifti_data(Path_to_label,Im_name)

    Image=Apply_windowing(Image[0],L,W,Mute=False)

    Save_name="Scan_001_%s.nii"%Unique_train_scans[i]

    Functions.Save_image_data_as_nifti(Directories[0],Save_name,Image,Header=Header[0])
    Functions.Save_image_data_as_nifti(Directories[1],Save_name,Label[0],Header=Header[0])



for i in range(len(Unique_test_scans)):

    Im_name="Scan_%s.nii"%Unique_test_scans[i]
    print(Im_name)
    Image,Header=Functions.Loading_Nifti_data(Path_to_CT,Im_name)
    Label,Header=Functions.Loading_Nifti_data(Path_to_label,Im_name)

    Image=Apply_windowing(Image[0],L,W,Mute=False)

    Save_name="Scan_001_%s.nii"%Unique_test_scans[i]
    Functions.Save_image_data_as_nifti(Directories[0],Save_name,Image,Header=Header[0])


