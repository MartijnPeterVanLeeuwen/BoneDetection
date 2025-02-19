import os
import numpy as np
import json
import pandas as pd

def Create_summary_results(Summary_dict,Storage_dir,Path_to_centroids):

    Overall_summary_dict={"Lesion":[],"Centroid_x":[],"Centroid_y":[],"Centroid_z":[],"1st Prediction":[], "fraction":[], "2nd Prediction":[],"fraction":[]}

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

        Overall_summary_dict={"Centroid_x":[],"Centroid_y":[],"Centroid_z":[],"1st Prediction":[], "fraction_1":[], "2nd Prediction":[],"fraction_2":[]}
        instance=Summary_dict[Keys[i]]

        All_labels=instance["All_Labels"]
        All_occurences=instance["All_no_occurences"]

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

        Overall_summary_dict["Centroid_x"]=  np.round(Xs[Keys_index])
        Overall_summary_dict["Centroid_y"]=  np.round(Ys[Keys_index])
        Overall_summary_dict["Centroid_z"]=  np.round(Zs[Keys_index])
        Overall_summary_dict["1st Prediction"]=  sorted_labels[0]
        Overall_summary_dict["fraction_1"]=   np.round(sorted_occurences[0]/Total_nr_predictions,2)
        Overall_summary_dict["2nd Prediction"]=  sorted_labels[1]
        Overall_summary_dict["fraction_2"]= np.round(sorted_occurences[1]/Total_nr_predictions,2)

        Complete_summary_dict[Keys[i]]=Overall_summary_dict

    df = pd.DataFrame.from_dict(data=Complete_summary_dict,orient='index')
    df.to_excel(os.path.join(Storage_dir,"Summary.xlsx"))


    return df
