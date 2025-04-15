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
from Supportive_functions.Multimodel_yolo.Return_label_functions import *

from Supportive_functions.Packages_file import *
from Supportive_functions.Swap_axis import Swap_axis
from Supportive_functions.Rescale_scan import Rescale_scan
from Supportive_functions.Loading_and_saving_data import Data_processing
from Supportive_functions.Apply_windowing import Apply_windowing
from Supportive_functions.Check_size_yolo_im import Check_size_yolo_im
from Supportive_functions.Place_in_empty_vol import *
from matplotlib import image

Path_to_desired_labels='/home/mleeuwen/DATA/Totalsegmentator_dataset_v201/Desired_labels.txt'

dict=Return_label_dict(Path_to_desired_labels)

print(dict)

# conda create -n nnUnet python=3.11
