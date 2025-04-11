import os
import sys
import nibabel as nib

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from CODE_Unet.General_Functions_Preprocessing.Loading_and_saving_data import Data_processing
from Packages_file import *
Functions=Data_processing()

Path_to_dummy_lesions="/home/mleeuwen/DATA/TSv3_Selection/New_dummy_lesions_test_30mm"
Path_to_CT="/home/mleeuwen/DATA/TSv3_Selection/Images"
Path_to_new_CT="/home/mleeuwen/DATA/TSv3_Selection/Osteolytic_test_30mm"
if os.path.isdir(Path_to_new_CT)==False:
    os.mkdir(Path_to_new_CT)

Test_patients=os.listdir(Path_to_dummy_lesions)

Mean_lesion_HU=44.87
std_lesion_HU=23.89

#Mean_lesion_HU=100
#std_lesion_HU=10

for i in range(len(Test_patients)):
    Image,Header=Functions.Loading_Nifti_data(Path_to_CT,Test_patients[i])
    Label,Header=Functions.Loading_Nifti_data(Path_to_dummy_lesions,Test_patients[i])

    lesions_regions=regionprops(label(Label[0]>0))
    for ii in lesions_regions:
        sampled_lesion=np.random.normal(Mean_lesion_HU,std_lesion_HU,1)[0]
        coordinates=ii.coords
        Image[0][coordinates[:,0],coordinates[:,1],coordinates[:,2]]=sampled_lesion

        print(sampled_lesion)

    Functions.Save_image_data_as_nifti(Path_to_new_CT,Test_patients[i],Image[0],Header=Header[0] )

    print(Image[0].shape)




