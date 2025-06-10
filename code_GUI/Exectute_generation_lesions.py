
import sys
import os
cwd="\\".join(os.getcwd().split('\\')[:-1])
sys.path.append(cwd)
import numpy as np
from code_paper.preprocess_TotalSegmentator_scans.generate_synthetic_lesion.Create_synthetic_lesions import *
from code_paper.preprocess_TotalSegmentator_scans.generate_synthetic_lesion.Fill_synthetic_lesions import *



def Create_sphere(class_attribute,list_of_coordinates_code,list_of_coordinates_gui,CT_data,Normalize=True):
        Mean_lesion_HU=44.87
        std_lesion_HU=23.89
        L=400
        W=1800
        Annotation_file_gui=np.zeros(class_attribute.ct_data.shape)
        Annotation_file_script=np.zeros(class_attribute.ct_data.shape)

        for i in range(len(list_of_coordinates_code)):
             coordinate=list_of_coordinates_code[i]
             raw_coordiante_list=list_of_coordinates_gui[i]
             Annotation_file_script=Create_sphere_coords(Annotation_file_script,raw_coordiante_list[0],raw_coordiante_list[2],raw_coordiante_list[1], np.ceil(5/1.5).astype(int), resolution=100)

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


        return Annotation_file_script,CT_data
