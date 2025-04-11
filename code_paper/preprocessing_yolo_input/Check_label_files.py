import os
import sys
from SETUPDIR import Set_up_dir
import nibabel as nib

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from CODE_Unet.General_Functions_Preprocessing.Loading_and_saving_data import Data_processing
from Packages_file import *


Path_to_datasets="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Total_Bone_detector_Total_dataset"

for dataset in ["train","val","test"]:
    print(dataset)
    Path_to_dataset=os.path.join(Path_to_datasets,"%s/labels"%dataset)
    Path_to_new_labels=os.path.join(Path_to_datasets,"%s/new_labels"%dataset)

    if os.path.isdir(Path_to_new_labels)==False:
        os.mkdir(Path_to_new_labels)

    label_files=os.listdir(Path_to_dataset)
    Yolo_image_size=640
    min_pixels=5
    empty_files=[]

    for ii in tqdm(range(len(label_files))):
        i=label_files[ii]
        Path_to_label_file=os.path.join(Path_to_dataset,i)

        with(open(Path_to_label_file,"r")) as f:
            data=f.readlines()
        f.close()
        new_list=[]

        for line in data:
            list_of_elements=line.split(" ")
            width=float(list_of_elements[3])
            height=float(list_of_elements[4][:-1])
            if (width*Yolo_image_size)>=min_pixels or (height*Yolo_image_size)>=min_pixels:
                new_list.append(line)
            #else:
            #    print(width*Yolo_image_size,height*Yolo_image_size)

        if len(new_list)==0:
            empty_files.append(i)
            print("found empty file")

        with(open(os.path.join(Path_to_new_labels,i),'w')) as f:
            f.writelines(new_list)
        f.close()

