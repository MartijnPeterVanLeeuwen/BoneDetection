import os
import numpy as np
import json

def Create_summary_results(Summary_dict,Storage_dir):

    Keys=list(Summary_dict.keys())

    Overview_prediction_dict={}

    for i in range(len(Keys)):

        instance=Summary_dict[Keys[i]]

        All_labels=instance["All_Labels"]
        All_occurences=instance["All_no_occurences"]

        sorted_labels = [val for _, val in sorted(zip(All_occurences, All_labels),reverse=True)]
        sorted_occurences=sorted(All_occurences,reverse=True)
        Total_nr_predictions=sum(sorted_occurences)
        Label_dict={}

        for ii in range(len(sorted_occurences)):

            percentage=sorted_occurences[ii]/Total_nr_predictions

            if ii == 0:
                Label_dict[sorted_labels[ii]+' (final label)']=np.round(percentage,2)
            else:
                Label_dict[sorted_labels[ii]]=np.round(percentage,2)

        Overview_prediction_dict[Keys[i]]=Label_dict

    with open(os.path.join(Storage_dir,'Predicted_labels.json'), 'w') as f:
        json.dump(Overview_prediction_dict, f, indent=4)

    return None
