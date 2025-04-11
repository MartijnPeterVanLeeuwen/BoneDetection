import os
import sys
import nibabel as nib

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)
from CODE_Unet.General_Functions_Preprocessing.Loading_and_saving_data import Data_processing
import pandas as pd
from Packages_file import *
import random
from matplotlib import image
from Load_RibFrac_nii import Load_RibFrac_nii
Functions=Data_processing()
from Localise_fracture_seg import Localise_rib_seg
from tqdm import tqdm
def Create_rib_fracture_overview(Path_to_rib_segmentation,Path_to_ribfrac_segmentation,Path_to_json_file,Save_dir):

    All_ribsegmentations=sorted(os.listdir(Path_to_rib_segmentation))
    All_fracture_segmentations=sorted(os.listdir(Path_to_ribfrac_segmentation))
    All_fracture_segmentations=[i for i in All_fracture_segmentations if 'nii' in i]
    Fracture_dataframe=pd.DataFrame({"Scan":[],"Fracture_label_value":[],"Centroid":[],"Location":[]})
    Total_no_fractures=0
    for i in tqdm(range(len(All_fracture_segmentations))):
    
        filename_fracseg=All_fracture_segmentations[i]
        filename_ribseg=filename_fracseg.split('-')[0]+'-rib-seg.nii.gz'
        Rib_seg,Frac_seg=Load_RibFrac_nii(Path_to_rib_segmentation,Path_to_ribfrac_segmentation,filename_ribseg,filename_fracseg)
        regions=regionprops(label(Frac_seg>0))
        Total_no_fractures+=len(regions)
        #Fracture_dataframe=Localise_rib_seg(Rib_seg,Frac_seg,filename_fracseg,Path_to_json_file,Fracture_dataframe)
    print(Total_no_fractures)

    #Fracture_dataframe.to_excel(os.path.join(Save_dir,"Ribfracture_locations.xlsx"),index=False)

    return None

Path_to_rib_segmentation="/home/llong/Rib-Frac/train-labels"
Path_to_ribfrac_segmentation="/home/mleeuwen/DATA/Rib-Frac/train-segmentations/Segmentations"
Path_to_json_file="/home/mleeuwen/DATA/Rib-Frac/train-segmentations/RibFrac_dict.json"
Save_dir="/home/mleeuwen/DATA/Rib-Frac/train-segmentations"

Create_rib_fracture_overview(Path_to_rib_segmentation,Path_to_ribfrac_segmentation,Path_to_json_file,Save_dir)
