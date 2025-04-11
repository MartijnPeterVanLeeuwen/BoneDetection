import os
import numpy as np

def Determine_data_splittage(Path_to_reference_data_splittage):

    datasets=["train","val","test"]
    Dataset=[]

    for data in datasets:
        Path_to_training_images=os.path.join(Path_to_reference_data_splittage,"%s/images"%data)
        Image_files=os.listdir(Path_to_training_images)
        Scan_nrs=np.unique([i.split("_")[1] for i in Image_files])
        Dataset.append(Scan_nrs)
    return Dataset[0],Dataset[1],Dataset[2]





