import os
import sys
from Return_label_functions import  Return_desired_labels

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)
from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.Packages_file import *

Functions = Data_processing()


Path_to_included_labels="/home/mleeuwen/DATA/Totalsegmentator_dataset_v201/Desired_labels.txt"   #Directory to the file which includes the label files that you want to include in the label mask.
directory_of_CT_folders= "/home/mleeuwen/DATA/Totalsegmentator_dataset_v201"   			 #Directory to the folders containing the label files of each of the TotalSegmentator scans.

def Combine_label_files(Path_to_included_labels,directory_of_CT_folders):
			

	Labels=sorted(Return_desired_labels("/home/mleeuwen/DATA/Totalsegmentator_dataset_v201/Desired_labels.txt"))
	New_labels=range(1,len(Labels)+1)
	int_labels=range(1,len(New_labels)+1)
	Label_dict=dict()

	for i in range(len(Labels)):
	    Label_dict[Labels[i]]=i+1

	Patient_folders = sorted(os.listdir(Directory_of_scans))
	Patient_folders=[i for i in Patient_folders if "." not in i]

	it=1
	
	for folder in tqdm(Patient_folders):
	    it = 1
	    New_label = []
	    Path_into_folder = os.path.join(Directory_of_scans, folder)

	    if os.path.isfile(os.path.join(Path_into_folder,"ct.nii.gz")) and os.path.isfile(os.path.join(Path_into_folder,"NEW_ct.nii"))==True:

	        for file in Labels:

	            Loaded_Label,Header=Functions.Loading_Nifti_data("%s/segmentations"%Path_into_folder,file,Mute=True)
        	    regions=regionprops(label(Loaded_Label[0]))
            	    Label_value=Label_dict[file]

            	if len(regions)>0:

                	if len(New_label)==0:
                    		New_label=Loaded_Label[0]
                    		New_label=(New_label>0).astype(int)*Label_value
                   		Save_header=Header[0]

                	else:
                    	       Known_mask=(New_label>0).astype(int)*-1
                    	       New_mask=(Loaded_Label[0]>0).astype(int)
                    	       Difference=New_mask+Known_mask
                    	       Difference=(Difference>0).astype(int)
                    	       Loaded_Label[0]=Difference*Label_value
                   	       New_label+=Loaded_Label[0]
                    	       Save_header=Header[0]
            	it+=1	

           Functions.Save_image_data_as_nifti(Path_into_folder,"Combined_label.nii",Data=New_label,Header=Save_header)

	return None






