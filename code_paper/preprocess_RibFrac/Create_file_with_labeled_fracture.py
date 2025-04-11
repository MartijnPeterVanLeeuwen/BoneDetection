import os
import sys
import nibabel as nib

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from CODE_Unet.General_Functions_Preprocessing.Loading_and_saving_data import Data_processing
from Packages_file import *
Functions=Data_processing()
Data_exploration_path =os.path.join(Main_folder,"CODE_Totalsegmenter")
sys.path.append(Data_exploration_path)
from Data_exploration.Return_label_functions import Return_label_dict
Main_folder=os.path.join(Main_folder,'CODE_Totalsegmenter/Execute_Bone_Identification')
print(Main_folder)
sys.path.append(Main_folder)
from Supportive_functions.Rescale_scan import Rescale_scan

Path_to_desired_labels="/home/mleeuwen/DATA/Totalsegmentator_dataset_v201/Desired_labels.txt"
label_dictionary=Return_label_dict(Path_to_desired_labels)
Path_to_fracture_segmenations='/home/mleeuwen/DATA/Rib-Frac/train-segmentations/Segmentations'

Path_to_overview_fracture_locations='/home/mleeuwen/DATA/Rib-Frac/train-segmentations/Ribfracture_locations.xlsx'

Path_to_new_location='/home/mleeuwen/DATA/Rib-Frac/train-segmentations/Segmentations_with_bone_label_1.5'

df=pd.read_excel(Path_to_overview_fracture_locations)
Scans_indeces=df["Scan"]
Centroids=df["Centroid"]
Locations=df["Location"]

Done=os.listdir(Path_to_new_location)
Done=[]
All_segmentations=os.listdir(Path_to_fracture_segmenations)
All_segmentations=[i for i in All_segmentations if '.nii' in i]
Total_no_lesions=0
Included_lesions=0

for ii in tqdm(range(len(All_segmentations))):

    if All_segmentations[ii] not in Done:

        print(All_segmentations[ii])
        Image,Header=Functions.Loading_Nifti_data(Path_to_fracture_segmenations,All_segmentations[ii])
        Selected_indeces=[i for i in range(len(Scans_indeces)) if Scans_indeces[i] ==All_segmentations[ii]]
        Overall_dict={}

        for iii in range(len(Selected_indeces)):
            Dictionary={}
            lesion=df.iloc[Selected_indeces[iii],:]

            if lesion["Location"]!='Notfound':
                Transferred_label=label_dictionary[lesion["Location"]]
                centroid=lesion["Centroid"].split(',')
                Dictionary["Centroid"]=centroid
                Dictionary["Label"]=Transferred_label
                Overall_dict["_".join(centroid)]=Dictionary

        regions=regionprops(label(Image[0]>0))
        Keys_dict=list(Overall_dict.keys())
        Empty_seg=np.zeros(Image[0].shape)

        for reg in regions:

            Intensities=Image[0][reg.coords[:,0],reg.coords[:,1],reg.coords[:,2]]
            label_values=np.unique(Intensities)
            label_values=np.unique([i for i in label_values if i!=0])
            Centroid=np.array(reg.centroid).astype(int)
            Centroid=[str(i) for i in Centroid]
            current_key="_".join(Centroid)

            if current_key in Keys_dict:
                print('found')
                new_value=int(Overall_dict[current_key]["Label"])
                Empty_seg[reg.coords[:,0],reg.coords[:,1],reg.coords[:,2]]=new_value
                print(new_value)
                Included_lesions+=1
            else:
                print('absent')

            Total_no_lesions+=1

        print(np.unique(Empty_seg))
        Second_regions=len(regionprops(label(Empty_seg>0)))
        Rescaled_scan=np.round(Rescale_scan(Empty_seg,Header[0]["pixdim"],rescale_to=1.5,Mute=False,order=0))
        Third_regions=len(regionprops(label(Rescaled_scan>0)))

        print(Second_regions,Third_regions)
        if Second_regions!=Third_regions:
            asdlkfjasldkfjlaksdjflk
        Header[0]["pixdim"][1:4]=1.5

        #Functions.Save_image_data_as_nifti(Path_to_new_location,All_segmentations[ii],np.round(Rescaled_scan),Header=Header[0])




print(Total_no_lesions,Included_lesions)

