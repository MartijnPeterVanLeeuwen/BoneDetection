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

Path_to_test_data='/home/mleeuwen/DATA/nnUnet_data/Dataset001_Bonesegmentation/RibFrac'
if os.path.isdir(Path_to_test_data)==False:
    os.mkdir(Path_to_test_data)
Original_data="/home/mleeuwen/DATA/Rib-Frac/train-images"
Segmentation_data='/home/mleeuwen/DATA/Rib-Frac/train-segmentations/Segmentations'

segmentation_files=os.listdir(Segmentation_data)
test_images=[i.split('-')[0]+'-image.nii.gz' for i in segmentation_files if '.nii' in i]

L=400
W=1800
nr=1
im=True
lab=True
for i in range(len(test_images)):

    Save_file_name="Scan_%s_0000.nii"%(test_images[i].split('-')[0])

    if im:
        Image,Header=Functions.Loading_Nifti_data(Original_data,test_images[i])

        Image=Rescale_scan(Image[0],Header[0]["pixdim"],rescale_to=1.5,Mute=False,order=False)

        Header[0]["pixdim"][1:4]=1.5

        Windowed_scan= np.rot90(Apply_windowing(Image,L,W),2)

        print(np.max(Windowed_scan),np.min(Windowed_scan))
        print(test_images[i].split('.nii')[0].split("_")[-1])
        Functions.Save_image_data_as_nifti(Path_to_test_data,Save_file_name,Windowed_scan,Header=Header[0])

