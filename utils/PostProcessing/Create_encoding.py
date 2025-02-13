import os
import sys
import numpy as np
import pandas as pd
Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from utils.PostProcessing.Return_label_functions import Return_label_dict

def Create_encoding(Prediction_dict,Label,Path_to_desired_labels,Model,Old_dictionary=None,Thresholded=False):

    if Old_dictionary!=None:
        Old_dictionary=Old_dictionary
    else:
        Old_dictionary=dict()

    Dictionary=Return_label_dict(Path_to_desired_labels)
    Reversed_dictionary= {str(v): k for k, v in Dictionary.items()}

    Keys_dictionary=list(Dictionary.keys())
    Reversed_keys=list(Reversed_dictionary.keys())
    Output_classes=Prediction_dict["Predicted_label_%s"%Model]

    if Thresholded==False:
        Confidence_scores=Prediction_dict["Prediction_Confidences_%s"%Model]
    else:
        Confidence_scores=Prediction_dict["Prediction_Confidences_%s_TH"%Model]

    Output_arrays=np.zeros((len(Dictionary)))

    Detected_classes=[Reversed_dictionary[i] for i in Output_classes]

    for i in Keys_dictionary:

        New_key="%s_%s"%(Model,i)

        if i not in Detected_classes:
            if New_key not in list(Old_dictionary.keys()):
                Old_dictionary[New_key]=[0]
            else:
                Old_dictionary[New_key]=Old_dictionary[New_key]+[0]

        if i in Detected_classes:
            index_in_list=Output_classes.index(str(Dictionary[i]))
            Confidence=Confidence_scores[index_in_list]
            if New_key not in list(Old_dictionary.keys()):
                Old_dictionary[New_key]=[Confidence]
            else:
                Old_dictionary[New_key]=Old_dictionary[New_key]+[Confidence]

    return Old_dictionary

