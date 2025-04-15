import os
import sys
import nibabel as nib
import matplotlib.pyplot as plt
import shutil
from scipy import ndimage
Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
Main_folder=os.path.join(Main_folder,'CODE_Totalsegmenter/Execute_Bone_Identification')
print(Main_folder)
sys.path.append(Main_folder)

from Supportive_functions.Packages_file import *
from Supportive_functions.Swap_axis import Swap_axis
from Supportive_functions.Rescale_scan import Rescale_scan
from Supportive_functions.Loading_and_saving_data import Data_processing
from Supportive_functions.Apply_windowing import Apply_windowing
from Supportive_functions.Check_size_yolo_im import Check_size_yolo_im
from Supportive_functions.Place_in_empty_vol import *
from matplotlib import image

Functions=Data_processing()

Path_to_nnUnet_train_data='/home/mleeuwen/DATA/nnUnet_data/Dataset001_Bonesegmentation/imagesTr'
Path_to_nnUnet_train_data_labels='/home/mleeuwen/DATA/nnUnet_data/Dataset001_Bonesegmentation/labelsTr'

Original_data='/home/mleeuwen/DATA/TSv3_Selection/Images'
Original_labels='/home/mleeuwen/DATA/TSv3_Selection/Labels'
path='/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Axial_BSv2_v5'

path_to_val=os.path.join(path,'val/images')
path_to_train=os.path.join(path,'train/images')

validation_images=os.listdir(path_to_val)
train_images=os.listdir(path_to_train)
validation_images=list(np.unique(["Scan_%s.nii"%i.split('_')[1] for i in validation_images]))
train_images=list(np.unique(["Scan_%s.nii"%i.split('_')[1] for i in train_images]))

files=validation_images+train_images

L=400
W=1800
nr=1
im=False
lab=True
for i in range(len(files)):

    Save_file_name="Scan_%s_0000.nii"%(files[i].split('.nii')[0].split("_")[-1])

    if im:
        Image,Header=Functions.Loading_Nifti_data(Original_data,files[i])
        print(np.max(Image[0]))
        Windowed_scan= Apply_windowing(Image[0],L,W)
        print(np.max(Windowed_scan),np.min(Windowed_scan))
        print(files[i].split('.nii')[0].split("_")[-1])
        Functions.Save_image_data_as_nifti(Path_to_nnUnet_train_data,Save_file_name,Windowed_scan,Header=Header[0])
    if lab:
        Label_file_name="Scan_%s.nii"%(files[i].split('.nii')[0].split("_")[-1])
        Label,Header=Functions.Loading_Nifti_data(Original_labels,files[i])
        Label=np.round(Label[0]).astype(int)
        Functions.Save_image_data_as_nifti(Path_to_nnUnet_train_data_labels,Label_file_name,np.round(Label),Header=Header[0])
