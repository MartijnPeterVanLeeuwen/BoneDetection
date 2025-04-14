import os
import sys
import nibabel as nib

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-3])  # Linux
sys.path.append(Main_folder)

from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.Packages_file import *
Functions=Data_processing()

Path_to_synthetic_lesion_labels="/home/mleeuwen/DATA/Total_segmentator_data/Synthetic_lesion_labels"        #Path to the generated synthetic lesion label files.
Path_to_CT="/home/mleeuwen/DATA/Total_segmentator_data/CT"                                                  #Path to the TotalSegmentator CT scans.
Path_to_CT_with_synthetic_lesions="/home/mleeuwen/DATA/Total_segmentator_data/CT_with_synthetic_lesions"    #Path to the directory where the new CT-scans with the synthetic lesions should be stored.

def Fill_synthetic_lesions(Path_to_CT,Path_to_synthetic_lesion_labels,Path_to_CT_with_synthetic_lesions,
                            Mean_lesion_HU=44.87,std_lesion_HU=23.89):

    if os.path.isdir(Path_to_CT_with_synthetic_lesions)==False:
        os.mkdir(Path_to_CT_with_synthetic_lesions)

    Test_patients=os.listdir(Path_to_synthetic_lesion_labels)

    for i in range(len(Test_patients)):
        Image,Header=Functions.Loading_Nifti_data(Path_to_CT,Test_patients[i])
        Label,Header=Functions.Loading_Nifti_data(Path_to_synthetic_lesion_labels,Test_patients[i])

        lesions_regions=regionprops(label(Label[0]>0))
        for ii in lesions_regions:
            sampled_lesion=np.random.normal(Mean_lesion_HU,std_lesion_HU,1)[0]
            coordinates=ii.coords
            Image[0][coordinates[:,0],coordinates[:,1],coordinates[:,2]]=sampled_lesion

        Functions.Save_image_data_as_nifti(Path_to_CT_with_synthetic_lesions,Test_patients[i],Image[0],Header=Header[0] )


    return None

