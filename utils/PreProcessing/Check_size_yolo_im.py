import os
import sys
import nibabel as nib
import matplotlib.pyplot as plt
import shutil

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from utils.Packages_file import *
from utils.PreProcessing.Loading_and_saving_data import Data_processing
Functions=Data_processing()

def Check_size_yolo_im(Image_slice,z_index,Min_size,Max_size,Lesion_loc):

    Sliced_im=Image_slice

    Size_im_shape=Image_slice.shape

    Min_size=Min_size/1.5
    Max_size=Max_size/1.5

    Scaled_im_shape_mm=[Size_im_shape[0],
                        Size_im_shape[1]]

    Minimum_requirement=False
    Maximum_requirement=False

    if Scaled_im_shape_mm[z_index]>=Min_size:
        Minimum_requirement=True
    if Scaled_im_shape_mm[z_index]<Max_size:
        Maximum_requirement=True

    if Maximum_requirement==False:

        Half_size_im=int(Max_size/2)
        Temp_min_slice=Lesion_loc[z_index]-Half_size_im
        Temp_max_slice=Lesion_loc[z_index]+Half_size_im
        excess_max=Temp_max_slice-Size_im_shape[z_index]
        excess_min=0-Temp_min_slice


        if excess_max>0:
            Temp_min_slice=Temp_min_slice-abs(excess_max)
            Temp_max_slice=Size_im_shape[z_index]
            New_coord=Max_size-abs(excess_max)
        elif excess_min>0:
            Temp_min_slice=0
            Temp_max_slice=Temp_max_slice+abs(excess_min)
            New_coord=Lesion_loc[z_index]

        if excess_max<0 and excess_min<0 :
            Temp_min_slice=Temp_min_slice
            Temp_max_slice=Temp_max_slice
            New_coord=Half_size_im

        Side_correction=(Size_im_shape[1-z_index]-Max_size)/2

        if z_index==0:
            Image_slice=Image_slice[int(Temp_min_slice):int(Temp_max_slice),int(Side_correction):int(Size_im_shape[1-z_index]-Side_correction)]
        elif z_index==1:
            Image_slice=Image_slice[int(Side_correction):int(Size_im_shape[1-z_index]-Side_correction),int(Temp_min_slice):int(Temp_max_slice)]

        Lesion_loc[z_index]=New_coord
        Lesion_loc[1-z_index]=Lesion_loc[1-z_index]-int(Side_correction)


    return Image_slice,Lesion_loc

