import os
import sys
import nibabel as nib
import pandas as pd
import numpy as np
import json
from utils.PostProcessing.Return_label_functions import Return_label_dict

def Obtain_single_label(Path_to_desired_labels,Path_to_patient,Path_to_neighbour_dict,TH=False):

    with open(Path_to_neighbour_dict, 'r') as file:
        Neighbouring_dict = json.load(file)

    dictionary=Return_label_dict(Path_to_desired_labels)
    reversed_dict = {v: k for k, v in dictionary.items()}

    Path_to_lesions=os.path.join(Path_to_patient,"Lesions")
    All_lesions=sorted(os.listdir(Path_to_lesions))
    Lesion_count=0
    Correct=0

    Missed=0
    Summary_dict={}
    Detected_labels=[]
    Neighbouring_bones=[]

    for i in range(len(All_lesions)):
        Lesion_dict={}

        Path_into_folder=os.path.join(Path_to_lesions,All_lesions[i])
        Folders=sorted(os.listdir(Path_into_folder))
        Predictions=[]


        All_files=Folders

        Folders=All_files

        for ii in range(len(Folders)):

            df=pd.read_excel(os.path.join(Path_into_folder,Folders[ii]))
            columns=np.array(df.columns)
            No_rows=df.shape[0]

            for z in range(0,No_rows):
                if TH:
                    ID=np.where(df.iloc[z,1:]>=TH)
                else:
                    ID=np.where(df.iloc[z,1:]!=0)

                ID=np.array([i+1 for i in ID])
                Labels=columns[ID][0]
                Labels=[("_").join(i.split("_")[1:]) for i in Labels]
                Labels=[dictionary[i] for i in Labels]
                Predictions=Predictions+Labels

        Unique_labels=np.unique(Predictions)
        Unique_labels=[i for i in Unique_labels if i!=0]
        Occurences=[Predictions.count(i) for i in Unique_labels]

        if len(Occurences)==0:
            print('No bone detected')
            Lesion_dict["Detected"]=False
            Lesion_dict["Max_label"]=None
            Lesion_dict["All_Labels"]=[]
            Lesion_dict["All_no_occurences"]=[]
            Lesion_dict['Neighbours_max_pred']=[]


        else:
            Max_pred=np.argmax(Occurences)
            Output=Unique_labels[Max_pred]
            Lesion_dict["Detected"]=True
            Lesion_dict["Max_label"]=reversed_dict[Output.astype(float)]
            Lesion_dict["All_Labels"]=[reversed_dict[i.astype(float)] for i in Unique_labels]
            Lesion_dict["All_no_occurences"]=Occurences

            Neighbour_bone_keys=Neighbouring_dict[str(Output)]
            if "Acceptable" in list(Neighbour_bone_keys.keys()):
                Lesion_dict['Neighbours_max_pred']=Neighbouring_dict[str(Output)]['Acceptable']
                Neighbouring_bones=Neighbouring_bones+Neighbouring_dict[str(Output)]['Acceptable']

            Detected_labels.append(Output)

        Summary_dict[All_lesions[i]]=Lesion_dict

    return Detected_labels,Neighbouring_bones,Summary_dict
