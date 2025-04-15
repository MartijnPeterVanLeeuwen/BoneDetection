import json
import os
import sys
import numpy as np
import json

path='/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Axial_BSv2_v5'

path_to_val=os.path.join(path,'val/images')
path_to_train=os.path.join(path,'train/images')

validation_images=os.listdir(path_to_val)
train_images=os.listdir(path_to_train)

validation_images=list(np.unique(["Scan_%s"%i.split('_')[1] for i in validation_images]))
train_images=list(np.unique(["Scan_%s"%i.split('_')[1] for i in train_images]))

train_images=[str(i) for i in train_images]
validation_images=[str(i) for i in validation_images]

print(train_images)

Path_to_json_dest='/home/mleeuwen/DATA/nnUnet_data/Dataset001_Bonesegmentation/splits_final.json'

Split_final=dict()

split_dict=dict()

split_dict["train"]=train_images
split_dict["val"]=validation_images
Split_final=[split_dict]
# Split_final[0]=split_dict
#
# print(Split_final)
#
# print(len(Split_final))
# print(Split_final[0].keys())
# print(len(Split_final[0]['train']))

import json
with open(Path_to_json_dest, 'w') as f:
    json.dump(Split_final, f)
