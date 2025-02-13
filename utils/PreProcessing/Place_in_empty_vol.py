import os
import os
import sys
Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)
from utils.PreProcessing.Loading_and_saving_data import Data_processing
from Packages_file import *

Functions = Data_processing()

def Place_in_empty_vol(image_data,max_size_xy,max_size_z,Cross_section="Axial"):

    if Cross_section=="Axial":
        pos_1=max_size_xy
        pos_2=max_size_xy
        pos_3=max_size_z
    if Cross_section=="Coronal":
        pos_1=max_size_z
        pos_2=max_size_z
        pos_3=max_size_xy
    if Cross_section=="Sagital":
        pos_1=max_size_z
        pos_2=max_size_z
        pos_3=max_size_xy

    empty_scan=np.zeros((pos_1,pos_2,pos_3))
    image_data_shape=image_data.shape

    diff_x=int(0.5*(pos_1-image_data_shape[0]))
    diff_y=int(0.5*(pos_2-image_data_shape[1]))
    diff_z=int(0.5*(pos_3-image_data_shape[2]))

    empty_scan[diff_x:diff_x+image_data_shape[0],diff_y:diff_y+image_data_shape[1],diff_z:diff_z+image_data_shape[2]]=image_data


    return empty_scan
