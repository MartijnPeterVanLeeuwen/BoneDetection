import os
import sys
import shutil

def Cleanup_folder(patient_folder):

    All_folders=os.listdir(patient_folder)

    Path_to_label_folders=[i for i in All_folders if "Labels_" in i ]

    for i in range(len(Path_to_label_folders)):
        to_be_removed=os.path.join(patient_folder,Path_to_label_folders[i])
        shutil.rmtree(to_be_removed)


    return None
