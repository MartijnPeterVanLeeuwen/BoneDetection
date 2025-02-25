import os
import numpy as np
import json
import pandas as pd
from utils.PostProcessing.Return_label_functions import Return_label_dict

def Create_summary_results(Summary_dict,Storage_dir,Path_to_centroids,path_to_bone_switch_label,path_to_bone_types,Switch_orientation=True,Reduce_label=False):

    Bone_to_int_dictionary=Return_label_dict(path_to_bone_types)

    with open(path_to_bone_switch_label, 'r') as file:
        Switch_dictionary = json.load(file)
    file.close()

    Lesions=pd.read_excel(Path_to_centroids)

    Lesion_IDs=list(Lesions['Lesion_ID'])
    Labels=list(Lesions['Label'])

    Xs=list(Lesions['Centroid_x'])
    Ys=list(Lesions['Centroid_y'])
    Zs=list(Lesions['Centroid_z'])

    Combinations=["Lesion_%s_%s"%(Lesion_IDs[i],Labels[i]) for i in range(len(Lesion_IDs))]

    Keys=list(Summary_dict.keys())

    Complete_summary_dict={}

    for i in range(len(Keys)):
        Keys_index=Combinations.index(Keys[i])

        Overall_summary_dict={"Lesion_ID":[],"Centroid_x":[],"Centroid_y":[],"Centroid_z":[],"1st Prediction":[],"1st Prediction (range)":[],
                                    "1st Prediction (int)":[],"Fraction_of_predictions_1":[] ,"2nd Prediction":[],"Fraction_of_predictions_2":[]}

        instance=Summary_dict[Keys[i]]

        All_labels=instance["All_Labels"]
        All_occurences=instance["All_no_occurences"]
        Max_neighbours=instance["Neighbours_max_pred"]
        Output_int=instance["Output"]

        if Switch_orientation==True:
            Output_int=Switch_dictionary[Output_int]

        Output_int=Bone_to_int_dictionary[Output_int]

        sorted_labels = [val for _, val in sorted(zip(All_occurences, All_labels),reverse=True)]
        sorted_occurences=sorted(All_occurences,reverse=True)
        Total_nr_predictions=sum(sorted_occurences)
        Label_dict={}

        for ii in range(len(sorted_occurences)):

            if ii <2:
                percentage=sorted_occurences[ii]/Total_nr_predictions

                if ii == 0:
                    Label_dict[sorted_labels[ii]+' (final label)']=np.round(percentage,2)
                else:
                    Label_dict[sorted_labels[ii]]=np.round(percentage,2)

        while len(sorted_labels)<2:

            sorted_labels.append('-')
            sorted_occurences.append(0)

        Index_max_label=All_labels.index(sorted_labels[0])
        Neighbours=Max_neighbours
        Neighbours=[str(i) for i in Neighbours]
        Neighbours="-".join(Neighbours)

        if len(Neighbours)>0:
            Neighbours='%s'%Neighbours

        if Reduce_label==True:
            if 'rib' in str(sorted_labels[0]):
                sorted_labels[0]='Rib'
                Output_int=100
            if 'vertebra' in str(sorted_labels[0]):
                sorted_labels[0]='Vertebra'
                Output_int=101
            if 'rib' in str(sorted_labels[1]):
                sorted_labels[1]='Rib'
            if 'vertebra' in str(sorted_labels[1]):
                sorted_labels[1]='Vertebra'
            Neighbours='-'

        Overall_summary_dict["Lesion_ID"]=  Keys[i]
        Overall_summary_dict["Centroid_x"]=  np.round(Xs[Keys_index])
        Overall_summary_dict["Centroid_y"]=  np.round(Ys[Keys_index])
        Overall_summary_dict["Centroid_z"]=  np.round(Zs[Keys_index])
        Overall_summary_dict["1st Prediction"]=  str(sorted_labels[0])
        Overall_summary_dict["1st Prediction (range)"]= Neighbours
        Overall_summary_dict["1st Prediction (int)"]=   Output_int
        Overall_summary_dict["Fraction_of_predictions_1"]=   np.round(sorted_occurences[0]/Total_nr_predictions,2)
        Overall_summary_dict["2nd Prediction"]=  str(sorted_labels[1])
        Overall_summary_dict["Fraction_of_predictions_2"]= np.round(sorted_occurences[1]/Total_nr_predictions,2)

        Complete_summary_dict[Keys[i]]=Overall_summary_dict

    df = pd.DataFrame.from_dict(data=Complete_summary_dict,orient='index')

    file_path = os.path.join(Storage_dir,"Summary.xlsx")

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            worksheet.column_dimensions[col_letter].width = max_length + 2  # Extra padding

    return df
