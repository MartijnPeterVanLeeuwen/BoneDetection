
import sys
import os
cwd="\\".join(os.getcwd().split('\\')[:-1])
sys.path.append(cwd)
import numpy as np
from code_paper.preprocess_TotalSegmentator_scans.generate_synthetic_lesion.Create_synthetic_lesions import *
from code_paper.preprocess_TotalSegmentator_scans.generate_synthetic_lesion.Fill_synthetic_lesions import *
from utils.PostProcessing.Return_label_functions import *


def Create_sphere(class_attribute,list_of_coordinates_code,list_of_coordinates_gui,CT_data,
            Path_to_desired_labels,Path_to_transformation_dict,Normalize=True,change_table=True):

        with open(Path_to_transformation_dict, 'r') as file:
            Label_transformation_dict = json.load(file)
        file.close()

        Mean_lesion_HU=44.87
        std_lesion_HU=23.89
        L=400
        W=1800
        Annotation_file_gui=np.zeros(class_attribute.ct_data.shape)
        Annotation_file_script=np.zeros(class_attribute.ct_data.shape)
        dictionary_labels=Return_label_dict(Path_to_desired_labels)
        dictionary_labels = {v: k for k, v in dictionary_labels.items()}

        for i in range(len(list_of_coordinates_code)):
             coordinate=list_of_coordinates_code[i]
             raw_coordiante_list=list_of_coordinates_gui[i]
             Empty_annotation=np.zeros(class_attribute.ct_data.shape)
             Empty_annotation=Create_sphere_coords(Empty_annotation,raw_coordiante_list[0],raw_coordiante_list[2],raw_coordiante_list[1], np.ceil(5/1.5).astype(int), resolution=100)
             coords_sphere=np.where(Empty_annotation>0)
             Bone_label=np.unique(class_attribute.overlay_mask[coords_sphere[0],coords_sphere[1],coords_sphere[2]])
             Bone_label=[i for i in Bone_label if i!=0]

             if len(Bone_label)==0:
                Bone_label_text='Not in Bone'
                Bone_label.append(100)
             else:
                Bone_label=sorted(Bone_label,reverse=True)
                Text=[]
                for k in range(len(Bone_label)):
                    Bone_label_text=dictionary_labels[Bone_label[k]]
                    Bone_label_text=Label_transformation_dict[Bone_label_text]
                    Text.append(Bone_label_text)
                if len(Text)>1:
                    Bone_label_text='/'.join(Text)

             Bone_label_text=Bone_label_text.replace('_',' ')
             Empty_annotation=Empty_annotation*Bone_label[0]
             Annotation_file_script=Annotation_file_script+Empty_annotation

             if change_table:
                 #update table
                 index = i  # 0-based index for Annotation #2
                 item_id = class_attribute.annotation_ids[index]
                 old_values = class_attribute.tree.item(item_id, "values")

                 # Create new tuple with updated ground truth (column 1)
                 new_values = (old_values[0], Bone_label_text, old_values[2])
                 class_attribute.tree.item(item_id, values=new_values)

        lesions_regions=regionprops(label(Annotation_file_script>0))
        for ii in lesions_regions:
            sampled_lesion=np.random.normal(Mean_lesion_HU,std_lesion_HU,1)[0]

            min_value=L-(0.5*W)
            max_value=L+(0.5*W)
            if Normalize:
                normalized_sampled_lesion=(sampled_lesion - min_value)/(max_value-min_value)
            else:
                normalized_sampled_lesion=sampled_lesion
            coordinates=ii.coords
            CT_data[coordinates[:,0],coordinates[:,1],coordinates[:,2]]=normalized_sampled_lesion
            class_attribute.overlay_mask[coordinates[:,0],coordinates[:,1],coordinates[:,2]]=0


        return Annotation_file_script,CT_data
